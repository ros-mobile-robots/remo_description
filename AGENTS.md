# Agent instructions for remo_description

Read [CONTRIBUTING.md](CONTRIBUTING.md) first; this file adds what an agent needs to work here without guessing. The same rules apply to people and agents.

## Before you push

Find your change in this list. Each line says what to run or check, and links the section with the details.

- **A xacro or config file:** the model expands without errors, and Remo's simulation test passes with your commit checked out in the workspace. Report the tested commit and the measured motions from the test's result file, not only pass/fail ([Commands](#commands)). Raise the package version ([Commits and pull requests](#commits-and-pull-requests)).
- **A new xacro argument, or a new choice of an argument:** expand the model with every choice you added or changed, and find the link, joint or property that the choice has to produce ([A new argument or choice](#a-new-argument-or-choice)).
- **A collision, contact or inertia setting:** such a setting can change how Remo turns in Gazebo. Compare the odometry with the true pose in the test's output, before and after ([Things that are easy to get wrong](#things-that-are-easy-to-get-wrong)).
- **A value that the diffbot repository also has:** the wheel radius, the wheel separation, or a frame that Remo's navigation footprint uses. Open the matching pull request in the diffbot repository and link the two ([Things that are easy to get wrong](#things-that-are-easy-to-get-wrong)).
- **A new feature of the model, or a change that the documentation describes:** the documentation pull request is planned with the model change ([Commits and pull requests](#commits-and-pull-requests)).
- **Only the guides or the README:** nothing to run, and the version stays.
- **The commits and the pull request:** one topic, signed commits, and no attribution lines for AI tools ([Commits and pull requests](#commits-and-pull-requests)).

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

Work in the diffbot repository's dev container. For a new workspace, its setup clones this repository to `~/catkin_ws/src/remo_description` at the version selected in `diffbot_dev.repos`, not your branch. Check out the branch you're testing there first (CONTRIBUTING.md shows how), or the test runs the unchanged model. In the dev container, in `~/catkin_ws`:

```bash
git -C src/remo_description log -1 --oneline                        # the commit you test: yours?
xacro src/remo_description/urdf/remo.urdf.xacro > /tmp/remo.urdf   # prints nothing: the model expands
catkin build && source devel/setup.bash                             # Summary: All … packages succeeded!
rostest diffbot_gazebo sim_drive_remo.test                          # RESULT: SUCCESS, after about a minute
```

- **No workflow runs in this repository.** The diffbot repository's CI tests the version of this model that `diffbot_dev.repos` pins, not your branch. The results in your pull request are the only test of your commit, so name the commit with them.
- **The measured motions:** the simulation test loads the model into Gazebo, drives Remo and logs the motion by the odometry and by the true pose. [Read the results](https://ros-mobile-robots.com/development/simulation-test/#read-the-results) on the Simulation Test page says where the result file is.

### A new argument or choice

The simulation test drives the default model. A new xacro argument, or a new choice of `camera_type` or `sbc_type`, can be broken while the default passes. Expand the model with every choice you added or changed, and find the link, joint or property that the choice has to produce. For example, the choice `jetson` of `sbc_type`:

```bash
xacro src/remo_description/urdf/remo.urdf.xacro sbc_type:="'jetson'" > /tmp/remo_jetson.urdf
grep -o '<link name="jetson[^"]*"' /tmp/remo_jetson.urdf
```

The second command prints `<link name="jetson_deck_link"` and `<link name="jetson_nano_link"`, the two links that take the place of `rpi_deck_link` and `rpi_link`. The inner quotes belong to the value: the model compares the argument with a quoted string. Put the commands and what they printed into the pull request.

## Xacro and config files

- **Macros:** a macro does one thing, and its comment block says what it builds and lists each parameter with its name, type, meaning and unit. The list has the names of the macro's `params` attribute, no more and no fewer: compare the two whenever you add, rename or remove a parameter. The example below shows the layout. Some older blocks in `urdf/include/common_macros.urdf.xacro` differ from their macro, such as the `mesh` entry of `wheel`. Correct a block when you change its macro.
- **Names:** a name says what the value is, such as `wheel_props` or `camera_rgba`. A number that an expression needs, and whose meaning the reader can't see, becomes a named property.
- **Expressions:** a long `${…}` expression is split into named properties, so that each line can be read by itself.
- **One place decides:** a rule lives in one macro or property that the others use, as the colour of a part without `rgba` lives in `default_rgba`. Not in a test that several macros repeat.
- **Defaults:** a default has one source. A value that a config file gives is not typed again as a fallback in a macro, unless the fallback keeps an older config layout working, and then its comment says which layout.
- **Config values:** a physical quantity that you add or change in `config/remo/*.yaml` has its unit in its comment. The comment also says where the value comes from, in one of four ways:
    - **Measured:** how it was measured, as the two wheel diameters behind `radius` in `front_wheel.yaml`.
    - **Specified:** the datasheet or the drawing, with its figure or page.
    - **Derived:** the formula and its inputs, as for `y_offset` in `front_wheel.yaml`.
    - **Chosen:** the reason for the choice.
- **Values without a unit:** a mesh path, a switch, a scale or a colour gets a comment that says what the value means and which values it can take, where its name doesn't say so. `mesh` and `rgba` in `front_wheel.yaml` show the form.
- **No invented sources:** don't write a datasheet figure, a measurement or a date that you can't show. An estimate is called an estimate.
- **Comments:** they say why, and what the reader can't see in the file: which frame, which axis, who uses the value. Not how the model was before. That belongs in `CHANGELOG.rst` and the pull request.

A comment block with the layout of the first rule. The block describes the macro `wheel` of `urdf/include/common_macros.urdf.xacro`, whose parameters are `prefix`, `reflect`, `wheel_props` and `base_props`:

```xml
<!-- Wheel: a wheel's link, its joint on chassis_link and the joint's transmission.

  params:
  - prefix [string]: start of the link's and the joint's name, such as front_left
  - reflect [1 or -1]: the robot's side, 1 for the left wheel (+y) and -1 for the right one
  - wheel_props [dictionary]: the wheel's values from config/remo/front_wheel.yaml, lengths in m
    and the mass in kg
  - base_props [dictionary]: the base's values from config/remo/base.yaml, lengths in m and
    masses in kg
-->
<xacro:macro name="wheel" params="prefix reflect wheel_props base_props">
```

The next example is not a line of the model. In it, `wheel_y` is the y coordinate (m) of the left wheel's outer face in `chassis_link`, whose y axis points to the robot's left. The first origin leaves the reader to find out what 0.0125 is. The second one names the number and says where it comes from:

```xml
<origin xyz="0 ${wheel_y - 0.0125} 0" rpy="0 0 0" />
```

```xml
<!-- The joint lies in the wheel's middle plane, half the wheel's width inside its outer face -->
<xacro:property name="half_wheel_width" value="${wheel_props['length'] / 2}" />
<origin xyz="0 ${wheel_y - half_wheel_width} 0" rpy="0 0 0" />
```

With the example inputs `wheel_y` = 0.100 m and a wheel width `wheel_props['length']` of 0.025 m, both origins expand to a y value of 0.0875 m. xacro prints the value as `0.08750000000000001`, with the rounding of a floating-point number. Check a changed frame the same way in the real model: expand the model and read the origin of the joint you changed. For the left wheel, that is `front_left_wheel_joint`:

```bash
grep -A 4 '<joint name="front_left_wheel_joint" type' /tmp/remo.urdf
```

The last line of the output is the origin, `xyz="0.036000000000000004 0.072 -0.0336"`. Its y value of 0.072 m is half of the wheel separation of 0.144 m that `front_wheel.yaml` names. Then run the simulation test and compare the odometry with Gazebo's true pose in the result file ([Read the results](https://ros-mobile-robots.com/development/simulation-test/#read-the-results)).

## Things that are easy to get wrong

- **The wheel radius and separation are also in the diffbot repository**, in `diffbot_control/config/remo/geometry.yaml`. Change both, in two linked pull requests.
- **Masses set the wheels' inertia**, and Remo's Gazebo wheel gains in the diffbot repository (`diffbot_control/config/remo/pid.yaml`) are chosen for it: the P gain must stay below 2J/h. A changed wheel mass needs the gains checked.
- **Contact settings work together:** the sphere collision, `minDepth` 0 and the compliant contact stiffness. Change one at a time and measure.
- **The diffbot repository pins this model's version** in `diffbot_dev.repos` and `remo_robot.repos`. Merging a model change here doesn't update those pins. After tagging, a maintainer opens a pull request in diffbot to update both pins. If your model change also requires changes in diffbot (for example Remo's navigation footprint when a base frame moves), open the matching pull request alongside yours and link the two. Pin your model commit during review, then use the release tag after the model change is merged and tagged.
- **Never add real mesh files** to this repository, and don't replace the placeholders.

## Commits and pull requests

- **One topic:** one change per pull request and per commit.
- **Branch:** `feat/…`, `fix/…`, `docs/…`, `chore/…`, `refactor/…` or `test/…`, followed by a short topic in kebab-case, such as `fix/wheel-radius`.
- **Title and description:** squash-merged by a maintainer, who uses the title as the commit subject and the description as its message. Title `Area: what changed`, 65 characters or fewer. The description starts with what and why, then how it was tested. Use the pull request template.
- **Issues:** end the description with `Closes #N` when the pull request resolves issue N. For an issue that stays open, name the issue without a closing keyword, as in `Part of #N`.
- **Signed commits:** sign every commit with GPG, `git commit -S`. `git log --show-signature -1` shows the signature of the last commit. A coding agent that can't sign stops and reports that, and doesn't commit unsigned.
- **Version:** if you change the model, raise the package version yourself, in `package.xml` and in a new `CHANGELOG.rst` section. CONTRIBUTING.md says which number to raise. Don't create tags: a maintainer tags the merge commit.
- **Comments:** see [Xacro and config files](#xacro-and-config-files). Measured values say how they were measured.
- **Documentation:** a new feature of the model comes with documentation on ros-mobile-robots.com, and so does every change to something that the site describes: a new xacro argument or choice, a new part, a moved frame, a changed mass or contact setting, and a change to the commands above. Open a pull request in [ros-mobile-robots.github.io](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io), planned with the model change, and link the pull request under `## Related`. Its pages follow that repository's [writing rules](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io/blob/main/AGENTS.md#writing-rules), and a new check gets its [walk through the tests](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io/blob/main/AGENTS.md#a-features-tests). If you can't open that pull request, say under `## Related` what the pages need. A maintainer then takes the page over before the model change is merged: with a documentation pull request, or with an issue in that repository that names the page and has an assignee.
- **AI tools:** no attribution lines for AI tools in commits or pull requests (`Co-Authored-By:` for a tool, "Generated with …"). No disclosure of AI use is needed.
