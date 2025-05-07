# remo_description

ROS URDF description package of REMO robot (Research Education Mobile/Modular robot) a highly modifiable and extendable mobile robot based on [Nvidia's Jetbot](https://github.com/NVIDIA-AI-IOT/jetbot). This repository contains the stl files to 3D print Remo robot.

![https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/remo-rviz-spin.gif](https://raw.githubusercontent.com/ros-mobile-robots/ros-mobile-robots.github.io/main/docs/resources/remo/remo-rviz-spin.gif)

## STL Mesh Files

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
