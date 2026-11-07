# wheel_colours.dae: credit and terms

`wheel_colours.dae` in this folder is the wheel model [Wheel D65x25](https://grabcad.com/library/wheel-d65x25-1) by **KlimukVI**, published on GrabCAD on 2019-05-08 as "Wheel D65x25 for Arduino car project". It's the wheel of Remo and DiffBot.

## Terms

The BSD 3-Clause License of remo_description doesn't cover this file. GrabCAD's terms apply to it. GrabCAD's help article [How can models be used and shared?](https://help.grabcad.com/article/246-how-can-models-be-used-and-shared) says:

- Public use without any money changing hands, for example in a free CAD library, is covered if you credit the original creator and link to the model.
- Commercial use, such as selling the model or prints of it, needs the original designer's explicit permission.

If you share this file or a file made from it, keep this credit with it: the model's name, its creator KlimukVI and the link to the model. Ask the creator on GrabCAD before any commercial use.

## Changes

[`scripts/make_wheel_dae.py`](../../scripts/make_wheel_dae.py) makes this file from DiffBot's `diffbot_description/meshes/components/wheel.stl` in the [diffbot repository](https://github.com/ros-mobile-robots/diffbot), at commit `787ad3a5df9b7da3eed111cd0b11599e3325e693`, SHA-256 `5dff27077acd9cf43b9fbdfd9fc616d0037d583d3d9c5ae8a67cbbe778a7d6cc`. That STL is the same model, in metres with the axle along z. The script converts it to COLLADA without changing its triangles, and gives the rim and the tyre a material each, yellow and black.
