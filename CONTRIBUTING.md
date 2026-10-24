# Contributing to remo_description

This is the ROS 1 Noetic description package of Remo: its URDF (xacro), the sizes, masses and positions of its parts in `config/remo/`, and its Gazebo settings. Remo's ROS packages, launch files and simulation test are in [diffbot](https://github.com/ros-mobile-robots/diffbot), and the documentation is at [ros-mobile-robots.com](https://ros-mobile-robots.com).

The STL meshes aren't in this repository (see the README); the model works without them, with empty placeholders.

Ask questions and get help with your build in diffbot's [Discussions](https://github.com/ros-mobile-robots/diffbot/discussions/categories/q-a), which cover both robots. Corrections and improvements to the model are welcome, as [issues](https://github.com/ros-mobile-robots/remo_description/issues) or pull requests here; a bug in Remo's ROS packages, launch files or simulation test goes to [diffbot](https://github.com/ros-mobile-robots/diffbot/issues). For a larger change, open an issue first.

## Set up and test

Use [diffbot's dev container](https://github.com/ros-mobile-robots/diffbot/tree/noetic-devel/.devcontainer/noetic): it clones this repository to `~/catkin_ws/src/remo_description` and builds it with the DiffBot packages. The container clones the version of this repository that diffbot pins in [`diffbot_dev.repos`](https://github.com/ros-mobile-robots/diffbot/blob/noetic-devel/diffbot_dev.repos), not your change. Check out your branch there first, and check that it's your commit:

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

The [simulation test](https://ros-mobile-robots.com/development/simulation-test/) drives Remo in Gazebo and checks where it went. Run it for every change to the model. diffbot pins a version of this repository, so a new version reaches diffbot only through a diffbot pull request that moves the pin: open it together with yours, tested with your change.

## Pull requests

- **One change per pull request**, on a branch named `feat/…`, `fix/…`, `docs/…` or `chore/…`.
- **Pull requests are squash-merged.** Maintainers use the PR title as the commit's subject and the description as its message, so write the title as `Area: what changed`, 65 characters or fewer, and start the description with what changes and why.
- **Versions:** a pull request that changes the model also sets the next version in `package.xml` and adds it to [`CHANGELOG.rst`](CHANGELOG.rst), with a line per change. Raise the first number when something built on the model has to change too, such as a moved frame or a renamed link, joint or xacro argument; the second number for any other change to the model; the third for a fix that leaves the model as it is, such as the install rules. A pull request that only changes the guides or the README needs no new version. Maintainers add the version if it's missing, and after the merge they tag the merge commit with it. Tags can't be moved or deleted.
- Say how you tested it: the xacro check, the simulation test and, for a measured value, how it was measured. Link the issue with `Closes #N`.
- Measured values carry a comment with the measurement, for example the wheel diameters behind `radius`. Code comments explain why, not what changed.
- If the controller needs the same value, for example the wheel radius and separation in diffbot's `diffbot_control/config/remo/geometry.yaml`, open the matching diffbot pull request and link them.
- If the documentation describes what you change, for example a measured value or a contact setting, open a pull request in [ros-mobile-robots.github.io](https://github.com/ros-mobile-robots/ros-mobile-robots.github.io) too, or say in your PR what the docs need.
- Maintainers mirror model changes to the Insiders repository, which has the meshes, with the same versions and tags.

## AI-assisted contributions

You're welcome to use AI tools. Whatever produced the change, you're its author and responsible for it:

- Understand every change and be able to explain it in review, in your own words.
- Test it as described above, and report what you actually ran. Don't claim tests that didn't run.
- Check that the xacro macros, parameters and Gazebo tags you use exist. Pull requests with invented ones are closed.
- Keep the PR description and your review replies short and specific.

You don't need to say whether you used AI. Please don't add attribution lines for AI tools to commits or pull requests, such as `Co-Authored-By:` for a tool or "Generated with …".

## License

By contributing, you agree that your contributions are licensed under this repository's [BSD 3-Clause License](LICENSE).
