^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Changelog for package remo_description
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2.1.0 (unreleased)
------------------
* IMU: imu_link for the BNO055 board on chassis_link, with a Gazebo IMU sensor that publishes
  /diffbot/imu/gazebo at 50 Hz. Its position (xacro arguments imu_xyz and imu_rpy) is provisional
  until the board's mounting on the robot is confirmed

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
