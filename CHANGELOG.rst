^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package remo_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.2.0 (2026-11-05)
------------------
* IMU and Teensy on the breadboard as on Remo: the IMU's center lies on the breadboard's center
  line from front to back, with the board's left edge flush with the breadboard's left edge
  (imu_xyz -0.040 0.023 0.013). The Teensy sits with its pins in the breadboard's holes, half a
  hole step behind the center line and 2.5 mm above the breadboard (-0.0415 -0.0206 0.012)

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
