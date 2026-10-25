# Agent instructions for remo_description

Read [CONTRIBUTING.md](CONTRIBUTING.md) first; this file adds what an agent needs to work here without guessing. The same rules apply to people and agents.

## What this is

Remo's ROS 1 Noetic description package. Remo's ROS packages, controllers and simulation test are in the [diffbot repository](https://github.com/ros-mobile-robots/diffbot) (`model:=remo`), named after DiffBot, the project's other robot; it holds the packages for both robots. The documentation is at [ros-mobile-robots.com](https://ros-mobile-robots.com).

| Path | What's in it |
|---|---|
| `urdf/remo.urdf.xacro` | The robot; xacro args `camera_type` and `sbc_type` |
| `urdf/include/common_macros.urdf.xacro` | Macros for wheels, motors and inertias (the drive wheels collide as spheres) |
| `urdf/include/robot.gazebo.xacro` | Gazebo plugin and the wheels' contact settings (friction, kp, kd, minDepth) |
| `config/remo/*.yaml` | Part sizes, masses and positions; `front_wheel.yaml` has the measured radius and offsets |
| `meshes/` | Empty placeholder STL files; the real meshes aren't in this repository |

## Commands

Work in the dev container of the diffbot repository, which has this repository at `~/catkin_ws/src/remo_description`. The container clones the version that the diffbot repository pins in its `diffbot_dev.repos`: check out the branch you're testing there first (CONTRIBUTING.md shows how) and confirm the commit with `git -C src/remo_description log -1`, or the test runs the unchanged model. In `~/catkin_ws`:

```bash
xacro src/remo_description/urdf/remo.urdf.xacro > /tmp/remo.urdf   # the model expands without errors
catkin build && source devel/setup.bash
rostest diffbot_gazebo sim_drive_remo.test
```

## Before you call a change done

- The xacro expands without errors, and Remo's simulation test passes; it loads the model into Gazebo. Report the measured motions from the test's result file, not only pass/fail.
- The diffbot repository uses the version of this repository that it pins in `diffbot_dev.repos`; a maintainer moves the pin after tagging. If the diffbot repository has to change together with the model (for example Remo's navigation footprint after a moved frame), open that pull request in the diffbot repository at the same time as yours and link the two: it pins your branch's commit until yours is merged.
- A changed collision, contact or inertia setting can change how Remo turns in Gazebo. Compare the odometry with the true pose in the test's output, before and after.

## Things that are easy to get wrong

- **The wheel radius and separation are also in the diffbot repository**, in `diffbot_control/config/remo/geometry.yaml`. Change both, in two linked pull requests.
- **Masses set the wheels' inertia**, and Remo's Gazebo wheel gains in the diffbot repository (`diffbot_control/config/remo/pid.yaml`) are chosen for it: the P gain must stay below 2J/h. A changed wheel mass needs the gains checked.
- **Contact settings work together:** the sphere collision, `minDepth` 0 and the compliant contact stiffness. Change one at a time and measure.
- **Never add real mesh files** to this repository, and don't replace the placeholders.

## Commits and pull requests

- One change per pull request and per commit; branch `feat/…`, `fix/…`, `docs/…` or `chore/…`.
- Squash-merged by a maintainer, who uses the title as the commit subject and the description as its message. Title `Area: what changed`, 65 characters or fewer. The description starts with what and why, then how it was tested, then `Closes #N`. Use the pull request template.
- A change to the model raises the version by hand, in `package.xml` and in a new `CHANGELOG.rst` section; CONTRIBUTING.md says which number to raise. Don't create tags: a maintainer tags the merge commit.
- Code comments explain why, not what changed; measured values say how they were measured.
- No attribution lines for AI tools in commits or pull requests (`Co-Authored-By:` for a tool, "Generated with …"). No disclosure of AI use is needed.
