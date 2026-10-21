# Contributing to remo_description

This is the ROS 1 Noetic description package of Remo: its URDF (xacro), the sizes, masses and positions of its parts in `config/remo/`, and its Gazebo settings. Remo's ROS packages, launch files and simulation test are in [diffbot](https://github.com/ros-mobile-robots/diffbot), and the documentation is at [ros-mobile-robots.com](https://ros-mobile-robots.com).

The STL meshes aren't in this repository (see the README); the model works without them, with empty placeholders.

Corrections and improvements to the model are welcome, as issues or pull requests. For a larger change, open an issue first.

## Set up and test

Use [diffbot's dev container](https://github.com/ros-mobile-robots/diffbot/tree/noetic-devel/.devcontainer/noetic): it clones this repository to `~/catkin_ws/src/remo_description` and builds it with the DiffBot packages. The container clones this repository's `main`, not your change. Check out your branch there first, and check that it's your commit:

```bash
cd ~/catkin_ws/src/remo_description
git remote add fork https://github.com/<you>/remo_description.git   # once
git fetch fork && git checkout -B <your-branch> fork/<your-branch>
git log -1 --oneline                                                 # your commit?
```

Then, in `~/catkin_ws`:

```bash
xacro src/remo_description/urdf/remo.urdf.xacro > /tmp/remo.urdf   # the model expands without errors
roslaunch remo_description view_remo.launch           # the model in RViz
catkin build && rostest diffbot_gazebo sim_drive_remo.test
```

The [simulation test](https://ros-mobile-robots.com/development/simulation-test/) drives Remo in Gazebo and checks where it went. Run it for every change to the model: diffbot's CI uses this repository's main branch, so a change here can break diffbot's CI after it's merged.

## Pull requests

- **One change per pull request**, on a branch named `feat/…`, `fix/…`, `docs/…` or `chore/…`.
- **Pull requests are squash-merged.** Maintainers use the PR title as the commit's subject and the description as its message, so write the title as `Area: what changed`, 65 characters or fewer, and start the description with what changes and why.
- Say how you tested it: the xacro check, the simulation test and, for a measured value, how it was measured. Link the issue with `Closes #N`.
- Measured values carry a comment with the measurement, for example the wheel diameters behind `radius`. Code comments explain why, not what changed.
- If the controller needs the same value, for example the wheel radius and separation in diffbot's `diffbot_control/config/remo/geometry.yaml`, open the matching diffbot pull request and link them.
- If the documentation describes what you change, for example a measured value or a contact setting, open a pull request in [ros-mobile-robots.github.io](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io) too, or say in your PR what the docs need.
- Maintainers mirror model changes to the version of this package that has the meshes.

## AI-assisted contributions

You're welcome to use AI tools. Whatever produced the change, you're its author and responsible for it:

- Understand every change and be able to explain it in review, in your own words.
- Test it as described above, and report what you actually ran. Don't claim tests that didn't run.
- Check that the xacro macros, parameters and Gazebo tags you use exist. Pull requests with invented ones are closed.
- Keep the PR description and your review replies short and specific.

You don't need to say whether you used AI. Please don't add attribution lines for AI tools to commits or pull requests, such as `Co-Authored-By:` for a tool or "Generated with …".

## License

By contributing, you agree that your contributions are licensed under this repository's [BSD 3-Clause License](LICENSE).
