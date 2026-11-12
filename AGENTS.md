# Agent instructions for remo_description

Read [CONTRIBUTING.md](CONTRIBUTING.md) first; this file adds what an agent needs to work here without guessing. The same rules apply to people and agents.

## What this is

Remo's ROS 1 Noetic description package. Remo's launch files, controller configuration and simulation test are in the [diffbot repository](https://github.com/ros-mobile-robots/diffbot), which supports both DiffBot and Remo (`model:=remo`). The documentation is at [ros-mobile-robots.com](https://ros-mobile-robots.com).

| Path | What's in it |
|---|---|
| `urdf/remo.urdf.xacro` | The robot; xacro args `camera_type` and `sbc_type` |
| `urdf/include/common_macros.urdf.xacro` | Macros for wheels, motors and inertias (the drive wheels collide as spheres) |
| `urdf/include/robot.gazebo.xacro` | Gazebo plugin and the wheels' contact settings (friction, kp, kd, minDepth) |
| `config/remo/*.yaml` | Part sizes, masses and positions; `front_wheel.yaml` has the measured radius and offsets |
| `meshes/` | Empty placeholder STL files; the real meshes aren't in this repository |

## Commands

Work in the diffbot repository's dev container. For a new workspace, its setup clones this repository to `~/catkin_ws/src/remo_description` at the version selected in `diffbot_dev.repos`, not your branch. Check out the branch you're testing there first (CONTRIBUTING.md shows how) and confirm the commit with `git -C src/remo_description log -1`, or the test runs the unchanged model. In `~/catkin_ws`:

```bash
xacro src/remo_description/urdf/remo.urdf.xacro > /tmp/remo.urdf   # the model expands without errors
catkin build && source devel/setup.bash
rostest diffbot_gazebo sim_drive_remo.test
```

## Before you call a change done

- The xacro expands without errors, and Remo's simulation test passes; it loads the model into Gazebo. Report the measured motions from the test's result file, not only pass/fail.
- The diffbot repository selects Remo's model version in `diffbot_dev.repos` and `remo_robot.repos`; merging a model change here doesn't update those pins. After tagging, a maintainer opens a pull request in diffbot to update both pins. If your model change also requires changes in diffbot (for example Remo's navigation footprint when a base frame moves), open the matching pull request alongside yours and link the two. Pin your model commit during review, then use the release tag after the model change is merged and tagged.
- A changed collision, contact or inertia setting can change how Remo turns in Gazebo. Compare the odometry with the true pose in the test's output, before and after.

## Xacro and config files

- **Macros:** a macro does one thing, and its comment block says what it builds and lists each parameter with its name, type, meaning and unit. The layout is the `params:` list of the comment blocks in `urdf/include/common_macros.urdf.xacro`.
- **Names:** a name says what the value is, such as `wheel_props` or `camera_rgba`. A number that an expression needs, and whose meaning the reader can't see, becomes a named property.
- **Expressions:** a long `${…}` expression is split into named properties, so that each line can be read by itself.
- **One place decides:** a rule lives in one macro or property that the others use, as the colour of a part without `rgba` lives in `default_rgba`. Not in a test that several macros repeat.
- **Defaults:** a default has one source. A value that a config file gives is not typed again as a fallback in a macro, unless the fallback keeps an older config layout working, and then its comment says which layout.
- **Config values:** every value in `config/remo/*.yaml` has its unit and its source in a comment: the datasheet with its figure, or how and when it was measured.
- **Comments:** they say why, and what the reader can't see in the file: which frame, which axis, who uses the value. Not how the model was before. That belongs in `CHANGELOG.rst` and the pull request.

An example, not a line of the model: the first origin below leaves the reader to find out what 0.0125 is. The second one names it and says where it comes from:

```xml
<origin xyz="0 ${wheel_y - 0.0125} 0" rpy="0 0 0" />
```

```xml
<!-- The joint lies in the wheel's middle plane, half the wheel's width from its inner face -->
<xacro:property name="half_wheel_width" value="${wheel_props['length'] / 2}" />
<origin xyz="0 ${wheel_y - half_wheel_width} 0" rpy="0 0 0" />
```

## Things that are easy to get wrong

- **The wheel radius and separation are also in the diffbot repository**, in `diffbot_control/config/remo/geometry.yaml`. Change both, in two linked pull requests.
- **Masses set the wheels' inertia**, and Remo's Gazebo wheel gains in the diffbot repository (`diffbot_control/config/remo/pid.yaml`) are chosen for it: the P gain must stay below 2J/h. A changed wheel mass needs the gains checked.
- **Contact settings work together:** the sphere collision, `minDepth` 0 and the compliant contact stiffness. Change one at a time and measure.
- **Never add real mesh files** to this repository, and don't replace the placeholders.

## Commits and pull requests

- One change per pull request and per commit; branch `feat/…`, `fix/…`, `docs/…` or `chore/…`.
- Squash-merged by a maintainer, who uses the title as the commit subject and the description as its message. Title `Area: what changed`, 65 characters or fewer. The description starts with what and why, then how it was tested, then `Closes #N`. Use the pull request template.
- If you change the model, raise the package version yourself, in `package.xml` and in a new `CHANGELOG.rst` section; CONTRIBUTING.md says which number to raise. Don't create tags: a maintainer tags the merge commit.
- **Comments:** see [Xacro and config files](#xacro-and-config-files). Measured values say how they were measured.
- **Documentation:** a change that a reader of ros-mobile-robots.com can see (a new xacro argument, a moved frame, a new part, a changed mass) comes with a pull request in [ros-mobile-robots.github.io](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io), planned with the model change and linked under `## Related`. If you can't open it, say in your pull request what the docs need. The writing rules are in that repository's `AGENTS.md`.
- No attribution lines for AI tools in commits or pull requests (`Co-Authored-By:` for a tool, "Generated with …"). No disclosure of AI use is needed.
