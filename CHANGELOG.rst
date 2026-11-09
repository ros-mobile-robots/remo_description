^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package remo_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.9.0 (2026-11-10)
------------------
* Lidar: the xacro argument lidar_type chooses the laser scanner and its printed platform:
  'a2' (the default) for the Slamtec RPLIDAR A2 on platfom_rplidar_a2.stl, 'a1' for the
  RPLIDAR A1 on platform_rplidar_a1.stl. The A1's mesh is rplidar_a1 of the package
  robot_component_models. With 'a2', the model is the same as in 2.8.0
* With 'a1', rplidar_laser_link lies 3.2 mm further to the front, 0.6 mm further to the left
  and 1 mm higher than with 'a2' (0.0052 0.0006 0.071 on lidar_platform_link), and its x axis
  points to the robot's rear as with 'a2'. The A1 sits on its platform with its motor towards
  the rear. The simulated A1 measures from 0.15 m to 12 m, and its mass is 170 g (Slamtec's
  A1M8 datasheet, rev. 3.0). lidar_platform_link is the same for both types. The USB adapter
  and its holder (slamtec_holder_link, slamtec_usb_to_serial_link) lie 2 mm higher, because
  the A1 platform's slots for the holder lie 2 mm higher than the A2 platform's
* A config file gives a part's values per type under the key types (laser in sensors.yaml,
  lidar_platform in base.yaml). A config without types, as written for 2.8.0, still expands
  as the A2
* A part's config can give mesh_xyz and mesh_rpy for a mesh whose frame differs from its
  link's. The A1 platform's mesh uses them: its origin lies 47 mm above its feet, and its x
  axis points to the rear

2.8.0 (2026-11-09)
------------------
* The Raspberry Pi 4 B, the Jetson Nano, the breadboard, the Teensy 4.0, the RPLIDAR A2, the
  Raspberry Pi camera and the drive wheels show the meshes of the package robot_component_models
  (https://github.com/ros-mobile-robots/robot_component_models): COLLADA files in metres with
  their own colours, for example a yellow rim in a black tyre. These parts show without any
  other files. remo_description depends on the package, so a workspace needs it next to
  remo_description. Without it, RViz shows the robot without these parts, and Gazebo doesn't
  load the robot. remo_robot.repos lists the package, and the README shows how to add it. No
  frame, link, joint or xacro argument changes
* A part's mesh in a config file is a file name or a full package:// URI. A COLLADA mesh shows
  its own colours. rgba colours the other meshes and the simple shapes
* The camera's scale is one value per camera type (camera: scale), because the Raspberry Pi
  camera's mesh is in metres and the OAK cameras' meshes are in millimetres. A config with one
  scale for all camera types (camera: meshes: scale), as written for 2.5.0, still expands
* The placeholders of the replaced meshes are removed: jetson_nano_dev_kit_b01.stl,
  raspberry_pi_4B.stl, breadboard_400_point.stl, teensy_4-0.stl and wheel.stl in
  meshes/components, rplidar-a2.stl and raspi_cam_v2_IMX219.stl in meshes/sensors

2.5.0 (2026-11-06)
------------------
* IMU: the xacro argument imu_plugin names the simulated IMU's Gazebo plugin library. The default
  stays gazebo_plugins' libgazebo_ros_imu_sensor.so. The diffbot repository's simulation passes its
  copy of that plugin, which doesn't run ROS callbacks in Gazebo's physics thread. gazebo_plugins'
  plugin does, which can stop the simulation while the controllers load
  (ros-mobile-robots/diffbot#185)

2.4.0 (2026-11-06)
------------------
* IMU: the BNO055 board's weighed mass, 3 g with its header pins, instead of 5 g

2.3.0 (2026-11-06)
------------------
* Colours like the real parts, the same in RViz and Gazebo. Each part's config file gives its
  colour as rgba, which replaces the Gazebo material names (color) and the shared RViz
  materials. The printed parts are black filament, shown dark grey, the wheels are black like
  their rubber tyres, the DG01D-E gearboxes are light blue, and the boards have their opaque
  PCB colours: green Raspberry Pi, Teensy and camera, blue BNO055, black motor driver and
  Jetson Nano. The lidar, its USB adapter, the battery pack and the power bank are black, the
  caster ball is metal grey. Gazebo no longer warns about inconsistent materials
* Configs and macro calls written for 2.2.0 still expand. A part whose config has no rgba, and
  a camera_sensor call without rgba, get a neutral grey (default_rgba). The color key of such a
  config isn't read any more, so its part is grey until it gets an rgba

2.2.1 (2026-11-06)
------------------
* Wheels: the visual has the wheel's mesh once. The macro gave a wheel without a scale a second
  mesh with an empty scale. The model is the same (#8)

2.2.0 (2026-11-05)
------------------
* IMU and Teensy on the breadboard as on Remo, with their pins in the breadboard's holes: the
  IMU's center at the breadboard's front-to-back midpoint, its left edge about flush with the
  breadboard's left edge (imu_xyz -0.0401 0.0234 0.013). The Teensy half a hole step behind the
  center channel's line and 2.5 mm above the breadboard, like the IMU (-0.0414 -0.0206 0.012)

2.1.0 (2026-11-05)
------------------
* IMU: imu_link for the BNO055 board on chassis_link, with a Gazebo IMU sensor that publishes
  /diffbot/imu/gazebo at 50 Hz. Its orientation (xacro argument imu_rpy) was measured on Remo: the
  board's x axis points to the right, y forward and z up, so imu_link is turned by -90 degrees
  about z. Its position (imu_xyz) was measured by hand: the chip's center is 7 cm behind the
  wheel axle, 2.5 cm left of the center line and 8 cm above the floor

2.0.0 (2026-10-26)
------------------
* Frames: base_link and base_footprint at the drive axle's midpoint, where diff_drive_controller's
  odometry puts the robot, 36 mm in front of the base plate's center. The plate and the parts on it
  hang from a new chassis_link at the plate's center, so the parts don't move. Positions given in
  base_link or base_footprint, such as a navigation footprint, are now measured from the axle (#5)

1.0.0 (2026-10-25)
------------------
* The first numbered version, for pinning Remo's model in dependent workspaces.
* Contributor guides: CONTRIBUTING, pull request template, AGENTS.md (#4)
* Gazebo: sphere collision and damped contacts for the drive wheels (#2)
* Measured wheel radius and separation (#3)
* Install the model files, so the package works from an install space (#1)
* The first public version: empty placeholder STL meshes, and a script that downloads the real ones
