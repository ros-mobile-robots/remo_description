#!/usr/bin/env python3
"""Make Remo's wheel mesh wheel_colours.dae from DiffBot's public wheel.stl.

The wheel is the model "Wheel D65x25" by KlimukVI on GrabCAD:
https://grabcad.com/library/wheel-d65x25-1. GrabCAD's terms apply to the mesh, not this
repository's BSD 3-Clause License. See meshes/components/wheel_colours.LICENSE.md.

The input is diffbot_description/meshes/components/wheel.stl in the diffbot repository at the
commit DIFFBOT_COMMIT, a binary STL with the SHA-256 checksum STL_SHA256. The script downloads
the STL from GitHub, or reads a local copy given with --stl. It stops if the checksum differs.
A clone of the diffbot repository gives a local copy:

    git show 787ad3a:diffbot_description/meshes/components/wheel.stl > wheel.stl

The output is one COLLADA 1.4.1 mesh with two materials, a yellow rim and a black tyre. It has
each STL triangle once, with its vertex order and its stored normal, in metres with the axle
along z, like the STL. The same input gives the same file, byte for byte.

Usage:
    python3 scripts/make_wheel_dae.py                  write meshes/components/wheel_colours.dae
    python3 scripts/make_wheel_dae.py --check          check that the file is what this makes
    python3 scripts/make_wheel_dae.py --stl wheel.stl  read a local copy of the STL
"""

import argparse
import hashlib
import math
from pathlib import Path
import struct
import sys
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Sequence
from typing import Tuple
import urllib.request

DIFFBOT_COMMIT = '787ad3a5df9b7da3eed111cd0b11599e3325e693'
STL_PATH = 'diffbot_description/meshes/components/wheel.stl'
STL_URL = ('https://raw.githubusercontent.com/ros-mobile-robots/diffbot/'
           f'{DIFFBOT_COMMIT}/{STL_PATH}')
STL_SHA256 = '5dff27077acd9cf43b9fbdfd9fc616d0037d583d3d9c5ae8a67cbbe778a7d6cc'
MODEL_URL = 'https://grabcad.com/library/wheel-d65x25-1'
DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / 'meshes/components/wheel_colours.dae'

# wheel.stl has four surfaces. Two reach 25.7 mm from the axle, the rim. Two reach 32.8 mm and
# 34.46 mm, the tyre's inner wall and its tread. A surface that reaches farther than this
# belongs to the tyre.
TYRE_MIN_RADIUS = 0.028  # m
# Ambient and diffuse colour, red green blue alpha. The yellow is close to the rim in a photo
# of Remo. The black is the wheel's rgba in config/remo/front_wheel.yaml.
COLOURS = {'rim': '0.95 0.72 0.05 1', 'tyre': '0.10 0.10 0.10 1'}
# The COLLADA 1.4.1 schema requires an asset's created and modified dates. A fixed date keeps
# the file the same each time it is made.
DATE = '2026-11-07T00:00:00Z'
# 9 significant digits give back each float32 value of the STL exactly.
DIGITS = 9
LINE_WIDTH = 99

HEADER_COMMENT = f"""<!-- The wheel "Wheel D65x25" by KlimukVI, {MODEL_URL}
     GrabCAD's terms apply to this file, not the BSD 3-Clause License of remo_description.
     See wheel_colours.LICENSE.md next to this file.
     Made by scripts/make_wheel_dae.py from DiffBot's wheel.stl, without changing its
     triangles: one mesh with two materials, a yellow rim and a black tyre. -->
"""

Vector = Tuple[float, float, float]
Edge = Tuple[Vector, Vector]


class Triangle(NamedTuple):
    """One STL triangle: its stored normal and its three corners in their order."""

    normal: Vector
    corners: Tuple[Vector, Vector, Vector]


class Part(NamedTuple):
    """The triangles of one material, as indices into the mesh's positions and normals."""

    material: str
    position_indices: List[Tuple[int, int, int]]
    normal_indices: List[int]


class MeshIndex(NamedTuple):
    """The index of each distinct corner position and each distinct normal."""

    positions: Dict[Vector, int]
    normals: Dict[Vector, int]


def read_stl_bytes(stl: str) -> bytes:
    """Return the STL file's bytes, from a local path or, if stl is empty, from GitHub."""
    if stl:
        return Path(stl).read_bytes()
    print(f'Downloading {STL_URL}')
    with urllib.request.urlopen(STL_URL) as response:
        data: bytes = response.read()
    return data


def check_checksum(data: bytes) -> None:
    """Stop unless the STL is the pinned version of DiffBot's wheel.stl."""
    checksum = hashlib.sha256(data).hexdigest()
    if checksum != STL_SHA256:
        sys.exit(f'The STL has the SHA-256 checksum {checksum}, expected {STL_SHA256}.')


def parse_stl(data: bytes) -> List[Triangle]:
    """Return the triangles of a binary STL file, with float32 values as Python floats."""
    count = struct.unpack_from('<I', data, 80)[0]
    if len(data) != 84 + 50 * count:
        sys.exit('The input is not a binary STL file.')
    triangles = []
    for offset in range(84, len(data), 50):
        values = struct.unpack_from('<12f', data, offset)
        corners = (vector(values, 3), vector(values, 6), vector(values, 9))
        triangles.append(Triangle(normal=vector(values, 0), corners=corners))
    return triangles


def vector(values: Sequence[float], start: int) -> Vector:
    """Return the three values from start on as a vector."""
    return (values[start], values[start + 1], values[start + 2])


def edges_of(triangle: Triangle) -> List[Edge]:
    """Return the triangle's three edges, each with its two corners in sorted order."""
    first, second, third = triangle.corners
    pairs = ((first, second), (second, third), (third, first))
    return [(min(pair), max(pair)) for pair in pairs]


def find_root(parents: List[int], index: int) -> int:
    """Return the surface that the triangle belongs to, as the index of its root triangle."""
    while parents[index] != index:
        parents[index] = parents[parents[index]]
        index = parents[index]
    return index


def surfaces(triangles: Sequence[Triangle]) -> List[int]:
    """Return a surface number for each triangle.

    Two triangles belong to the same surface when they share an edge that no other triangle
    uses. Corners are the same when their coordinates are equal. The rim and the tyre touch
    each other along edges that more than two triangles use, so they stay apart.
    """
    triangles_of_edge: Dict[Edge, List[int]] = {}
    for index, triangle in enumerate(triangles):
        for edge in edges_of(triangle):
            triangles_of_edge.setdefault(edge, []).append(index)
    parents = list(range(len(triangles)))
    for sharing in triangles_of_edge.values():
        if len(sharing) == 2:
            parents[find_root(parents, sharing[1])] = find_root(parents, sharing[0])
    return [find_root(parents, index) for index in range(len(triangles))]


def radius(point: Vector) -> float:
    """Return the point's distance from the axle, the z axis."""
    return math.hypot(point[0], point[1])


def tyre_flags(triangles: Sequence[Triangle]) -> List[bool]:
    """Return True for each triangle of the tyre, False for each triangle of the rim."""
    surface_of = surfaces(triangles)
    reach: Dict[int, float] = {}
    for surface, triangle in zip(surface_of, triangles):
        farthest = max(radius(corner) for corner in triangle.corners)
        reach[surface] = max(reach.get(surface, 0.0), farthest)
    return [reach[surface] > TYRE_MIN_RADIUS for surface in surface_of]


def index_of(values: Sequence[Vector]) -> Dict[Vector, int]:
    """Return each distinct value's index in the sorted list of distinct values."""
    return {value: index for index, value in enumerate(sorted(set(values)))}


def wrap(tokens: Sequence[str], indent: str = '      ') -> str:
    """Join the tokens with spaces, in lines of at most LINE_WIDTH characters."""
    lines = []
    line = indent
    for token in tokens:
        if len(line) + 1 + len(token) > LINE_WIDTH and line.strip():
            lines.append(line)
            line = indent
        line += token if line == indent else ' ' + token
    lines.append(line)
    return '\n'.join(lines)


def format_vectors(vectors: Sequence[Vector]) -> str:
    """Return the vectors' numbers, with DIGITS significant digits, in wrapped lines."""
    return wrap([f'{value:.{DIGITS}g}' for vector in vectors for value in vector])


def effect_xml(material: str) -> str:
    """Return a matte effect in the material's colour, without a specular highlight."""
    colour = COLOURS[material]
    return f"""  <effect id="{material}-effect">
   <profile_COMMON><technique sid="common"><phong>
    <ambient><color>{colour}</color></ambient>
    <diffuse><color>{colour}</color></diffuse>
    <specular><color>0 0 0 1</color></specular>
   </phong></technique></profile_COMMON>
  </effect>
"""


def source_xml(name: str, vectors: Sequence[Vector]) -> str:
    """Return a COLLADA source of 3D vectors, the positions or the normals."""
    return f"""    <source id="wheel-{name}">
     <float_array id="wheel-{name}-array" count="{len(vectors) * 3}">
{format_vectors(vectors)}
     </float_array>
     <technique_common>
      <accessor source="#wheel-{name}-array" count="{len(vectors)}" stride="3">
       <param name="X" type="float"/><param name="Y" type="float"/><param name="Z" type="float"/>
      </accessor>
     </technique_common>
    </source>
"""


def triangles_xml(part: Part) -> str:
    """Return the part's triangles: a position index and a normal index for each corner."""
    indices = [str(index)
               for corners, normal in zip(part.position_indices, part.normal_indices)
               for corner in corners for index in (corner, normal)]
    return f"""    <triangles material="{part.material}" count="{len(part.normal_indices)}">
     <input semantic="VERTEX" source="#wheel-vertices" offset="0"/>
     <input semantic="NORMAL" source="#wheel-normals" offset="1"/>
     <p>
{wrap(indices)}
     </p>
    </triangles>
"""


def asset_xml() -> str:
    """Return the asset: the model's creator and source, the conversion, units and up axis."""
    return f""" <asset>
  <contributor>
   <author>KlimukVI</author>
   <comments>The model "Wheel D65x25" on GrabCAD</comments>
   <copyright>GrabCAD's terms apply, see wheel_colours.LICENSE.md</copyright>
   <source_data>{MODEL_URL}</source_data>
  </contributor>
  <contributor>
   <authoring_tool>remo_description scripts/make_wheel_dae.py</authoring_tool>
   <comments>From DiffBot's wheel.stl, diffbot {DIFFBOT_COMMIT}</comments>
  </contributor>
  <created>{DATE}</created>
  <modified>{DATE}</modified>
  <unit name="meter" meter="1"/>
  <up_axis>Z_UP</up_axis>
 </asset>
"""


def collada(positions: Sequence[Vector], normals: Sequence[Vector], parts: List[Part]) -> str:
    """Return the COLLADA document: one geometry with a triangle list per material."""
    names = [part.material for part in parts]
    materials = ''.join(f'  <material id="{name}-material" name="{name}">'
                        f'<instance_effect url="#{name}-effect"/></material>\n'
                        for name in names)
    bindings = ''.join(f'      <instance_material symbol="{name}" target="#{name}-material"/>\n'
                       for name in names)
    return f"""<?xml version="1.0" encoding="utf-8"?>
{HEADER_COMMENT}<COLLADA xmlns="http://www.collada.org/2005/11/COLLADASchema" version="1.4.1">
{asset_xml()} <library_effects>
{''.join(effect_xml(name) for name in names)} </library_effects>
 <library_materials>
{materials} </library_materials>
 <library_geometries>
  <geometry id="wheel" name="wheel">
   <mesh>
{source_xml('positions', positions)}{source_xml('normals', normals)}\
    <vertices id="wheel-vertices"><input semantic="POSITION" source="#wheel-positions"/></vertices>
{''.join(triangles_xml(part) for part in parts)}   </mesh>
  </geometry>
 </library_geometries>
 <library_visual_scenes>
  <visual_scene id="scene">
   <node id="wheel-node" name="wheel">
    <instance_geometry url="#wheel">
     <bind_material><technique_common>
{bindings}     </technique_common></bind_material>
    </instance_geometry>
   </node>
  </visual_scene>
 </library_visual_scenes>
 <scene><instance_visual_scene url="#scene"/></scene>
</COLLADA>
"""


def make_part(material: str, triangles: Sequence[Triangle], mesh_index: MeshIndex) -> Part:
    """Return the triangles as a part with the material, in their order."""
    position_indices = []
    for triangle in triangles:
        first, second, third = (mesh_index.positions[corner] for corner in triangle.corners)
        position_indices.append((first, second, third))
    normal_indices = [mesh_index.normals[triangle.normal] for triangle in triangles]
    return Part(material=material, position_indices=position_indices,
                normal_indices=normal_indices)


def wheel_dae(triangles: Sequence[Triangle]) -> str:
    """Return the wheel as COLLADA text, the rim's triangles first, each part in STL order."""
    mesh_index = MeshIndex(
        positions=index_of([corner for triangle in triangles for corner in triangle.corners]),
        normals=index_of([triangle.normal for triangle in triangles]))
    is_tyre = tyre_flags(triangles)
    rim = [triangle for triangle, tyre in zip(triangles, is_tyre) if not tyre]
    tyre = [triangle for triangle, tyre in zip(triangles, is_tyre) if tyre]
    parts = [make_part('rim', rim, mesh_index), make_part('tyre', tyre, mesh_index)]
    for part in parts:
        print(f'{part.material}: {len(part.normal_indices)} triangles')
    return collada(sorted(mesh_index.positions), sorted(mesh_index.normals), parts)


def parse_arguments() -> argparse.Namespace:
    """Return the command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--stl', default='',
                        help='a local copy of the STL, instead of downloading it')
    parser.add_argument('--output', default=str(DEFAULT_OUTPUT), help='the COLLADA file')
    parser.add_argument('--check', action='store_true',
                        help='compare the output file with what the script makes, write nothing')
    return parser.parse_args()


def main() -> None:
    """Make wheel_colours.dae, or check it with --check."""
    arguments = parse_arguments()
    data = read_stl_bytes(arguments.stl)
    check_checksum(data)
    text = wheel_dae(parse_stl(data))
    output = Path(arguments.output)
    if arguments.check:
        if not output.exists() or output.read_text(encoding='utf-8') != text:
            sys.exit(f'{output} differs from what scripts/make_wheel_dae.py makes.')
        print(f'{output} is what scripts/make_wheel_dae.py makes.')
        return
    output.write_text(text, encoding='utf-8')
    print(f'Wrote {output}, {len(text.encode("utf-8"))} bytes.')


if __name__ == '__main__':
    main()
