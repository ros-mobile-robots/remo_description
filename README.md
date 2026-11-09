# remo_description

ROS URDF description package of REMO robot (Research Education Mobile/Modular robot) a highly modifiable and extendable mobile robot based on [Nvidia's Jetbot](https://github.com/NVIDIA-AI-IOT/jetbot). This repository contains the stl files to 3D print Remo robot.

![https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/remo-rviz-spin.gif](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/remo-rviz-spin.gif)

## Mesh Files

Remo's model takes the meshes of its parts from two places.

### Purchased parts: robot_component_models

The Raspberry Pi 4 B, the Jetson Nano, the breadboard, the Teensy 4.0, the RPLIDAR A2, the Raspberry Pi camera and the drive wheels are meshes of the package [robot_component_models](https://github.com/ros-mobile-robots/robot_component_models). This package has display models of off-the-shelf robot components, made from public datasheets, drawings and photos. Remo uses its COLLADA files (`.dae`), which are in metres and have their own colours. With the package in the workspace, RViz and Gazebo show these parts without any other files.

`remo_description` needs the package in the same catkin workspace. From the workspace's root, clone the package next to `remo_description`, at the version that this model uses:

```bash
git clone --branch 1.0.0 https://github.com/ros-mobile-robots/robot_component_models.git src/robot_component_models
```

Then build the workspace, for example with `catkin build`, and source its `devel/setup.bash` again.

[`remo_robot.repos`](remo_robot.repos) lists the package at the same version. This file lists the repositories of a workspace on Remo's Raspberry Pi, for [`vcs import`](https://github.com/dirk-thomas/vcstool). One of them is the camera driver `raspicam_node`, which requires the Raspberry Pi's camera libraries. In the diffbot repository's dev container, rosdep can't resolve its dependency `libraspberrypi0`, and `rosdep install` stops with `Cannot locate rosdep definition for [libraspberrypi0]`. To add robot_component_models to a development workspace, use the clone command above.

Without the package in the workspace:

- `rosdep install` stops with `Cannot locate rosdep definition for [robot_component_models]`.
- The xacro file still expands.
- RViz shows the robot without these parts and logs `Could not load resource [package://robot_component_models/...]` for each of them.
- Gazebo doesn't load the robot. The node `spawn_model` of `gazebo_ros` stops with `Package[robot_component_models] does not have a path` and `Spawn service failed`.

### STL Mesh Files

The STL files in [`meshes/`](meshes) are empty placeholders. They stand for Remo's 3D printed parts, such as the chassis, the decks, the lidar platform and the camera mounts, and for the parts that robot_component_models doesn't have, such as the motors, the battery pack and the OAK cameras.

This repository does not include the STL mesh files due to size and licensing.

To obtain the mesh files:

1. [Purchase / Register](https://fjp.gumroad.com/l/GnMpU)
2. Download the provided `stl_download_config.yaml`
3. Run:

```bash
pip install pyyaml requests
python3 scripts/download_assets.py
```

## Camera Types

The [`remo.urdf.xacro`](urdf/remo.urdf.xacro) accepts a `camera_type`
[xacro arg](http://wiki.ros.org/xacro#Rospack_commands) which lets you choose between the following different camera types

| Raspicam v2 with IMX219 | OAK-1 | OAK-D |
|:-----------------------:|:-----:|:-----:|
| [<img src="https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/raspi-cam.png" width="700">](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/raspi-cam.png) | [<img src="https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/oak-1.png" width="700">](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/oak-1.png) | [<img src="https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/oak-d.png" width="700">](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/camera_types/oak-d.png) |

## Single Board Computer Types

Another xacro argument is the `sbc_type` wher you can select between `jetson` and `rpi`.

| Jetson Nano | Raspberry Pi 4 B |
|:-----------------------:|:-----:|
| [<img src="https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/sbc_types/jetson-nano.png" width="700">](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/sbc_types/jetson-nano.png) | [<img src="https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/sbc_types/raspi.png" width="700">](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/sbc_types/raspi.png) |


## Usage

This is a ROS package which should be cloned in a catkin workspace.
To use `remo_description` inside a Gazebo simulation or on a real 3D printed Remo robot, you can directly make use of the ROS packages in the 
[ros-mobile-robots/diffbot](https://github.com/ros-mobile-robots/diffbot) repository. 
Most of the launch files you find in the `diffbot` repository
accept a `model` argument. Just append `model:=remo` to the end of a `roslaunch` command to make use of this `remo_description` package.

### Assembly

For assembly instructions please watch the video below:

[![remo fusion animation](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/remo_fusion_animation.gif)](https://youtu.be/6aAEbtfVbAk)

### Git LFS and Bandwith Quota

The binary stl files are hosted on GitHub using [Git Large File Storage (git lfs)](https://git-lfs.github.com/) 
to avoid increasing the total size of the repository because of possible stl file changes.
For open source repositories, GitHub has a bandwith limit of 1 GB (up to 1.5 GB) per month. 
Depending on how many users clone/pull the stl files using git lfs per month, this bandwith can be exhausted after a few days. 
If you are not able to clone/pull the stl files and only get the pointer files, you have to wait until the bandwith quota resets back to zero. 
In case you need the stl files immediately, and to support this work you can get [immediate access to the stl files](https://gumroad.com/l/GnMpU?wanted=true):

<a class="gumroad-button" href="https://gumroad.com/l/GnMpU?wanted=true" data-gumroad-single-product="true">Access Remo STL files</a>

Also if you find this work useful please consider the funding options to support the development and design of this robot.
However, you will always be able to clone/pull and use the Remo stl files once the bandwith quota resets.


## Contributing

You addons to Remo are most welcome, feel free to open a discussion/issue or directly create a pull request.

## :handshake: Acknowledgment

- [Louis Morandy-Rapiné](https://louisrapine.com/) for his great work on REMO robot and designing it in [Fusion 360](https://www.autodesk.com/products/fusion-360/overview).


## License

`remo_description` is licenses under the [BSD-3 clause](./LICENSE).
See also [open-source-license-acknowledgements-and-third-party-copyrights.md](open-source-license-acknowledgements-and-third-party-copyrights.md).
