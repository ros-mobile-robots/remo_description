^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package remo_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.6.0 (2026-11-07)
------------------
* Wheels: a yellow rim and a black tyre like the real wheels, in RViz and Gazebo. The wheel's
  mesh is the COLLADA file wheel_colours.dae, one mesh with a material for the rim and one for
  the tyre. With the new key mesh_colours in front_wheel.yaml, the wheel shows the mesh's own
  colours and gets no URDF or Gazebo material from rgba. rgba colours the cylinder (mesh '').
  A front_wheel.yaml without mesh_colours, as in older versions, colours the wheel with rgba
* wheel_colours.dae is the real wheel, the model "Wheel D65x25" by KlimukVI from GrabCAD, and the
  one real mesh in this repository. GrabCAD's terms apply to it, not the BSD license
  (meshes/components/wheel_colours.LICENSE.md). scripts/make_wheel_dae.py makes it from DiffBot's
  public wheel.stl in the diffbot repository

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
