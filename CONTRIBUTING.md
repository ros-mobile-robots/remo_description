# Contributing to remo_description

This is the ROS 1 Noetic description package of Remo: its URDF (xacro), the sizes, masses and positions of its parts in `config/remo/`, and its Gazebo settings. Remo's launch files, controller configuration and simulation test are in the [diffbot repository](https://github.com/ros-mobile-robots/diffbot), which supports both DiffBot and Remo. The documentation is at [ros-mobile-robots.com](https://ros-mobile-robots.com).

The STL meshes aren't in this repository (see the README); the model works without them, with empty placeholders.

Ask questions and get help with your build in the diffbot repository's [Discussions](https://github.com/ros-mobile-robots/diffbot/discussions/categories/q-a), which cover both robots. Corrections and improvements to the model are welcome, as [issues](https://github.com/ros-mobile-robots/remo_description/issues) or pull requests here; a bug in Remo's ROS packages, launch files or simulation test goes to the [diffbot repository's issues](https://github.com/ros-mobile-robots/diffbot/issues). For a larger change, open an issue first.

## Set up and test

Use the [diffbot repository's dev container](https://github.com/ros-mobile-robots/diffbot/tree/noetic-devel/.devcontainer/noetic). For a new workspace, its setup clones `remo_description` to `~/catkin_ws/src/remo_description` at the version selected in [`diffbot_dev.repos`](https://github.com/ros-mobile-robots/diffbot/blob/noetic-devel/diffbot_dev.repos), not your branch. Check out your branch there and confirm the commit before building and testing:

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

The [simulation test](https://ros-mobile-robots.com/development/simulation-test/) drives Remo in Gazebo and checks where it went. Run it for every change to the model, and report its result in your pull request.

The diffbot repository selects Remo's model version in `diffbot_dev.repos` and `remo_robot.repos`. Merging a model change here doesn't update those pins. After tagging a release, a maintainer opens a pull request in diffbot to update both pins.

If your model change also requires changes in diffbot, such as updating Remo's navigation footprint when a base frame moves, open the matching pull request alongside your model pull request and link the two. Pin your model commit during review, then use the release tag after the model change is merged and tagged.

## Pull requests

- **One change per pull request**, on a branch named `feat/…`, `fix/…`, `docs/…` or `chore/…`.
- **Pull requests are squash-merged.** Maintainers use the PR title as the commit's subject and the description as its message, so write the title as `Area: what changed`, 65 characters or fewer, and start the description with what changes and why.
- **Versions:** if your pull request changes the model, raise the package version yourself, in two files: `<version>` in `package.xml`, and a new section in [`CHANGELOG.rst`](CHANGELOG.rst) with a line per change. Raise the first number when something built on the model has to change too, such as a moved frame or a renamed link, joint or xacro argument; the second number for any other change to the model, such as a new part or a changed mass; the third for a fix that leaves the model as it is, such as the install rules. If it only changes the guides or the README, leave the version as it is. If you're unsure which number to raise, say so in the pull request, and a maintainer sets it before the merge. After the merge, a maintainer tags the merge commit with the version, for example `1.1.0`. Tags can't be moved or deleted.
- Say how you tested it: the xacro check, the simulation test and, for a measured value, how it was measured. Link the issue with `Closes #N`.
- Measured values carry a comment with the measurement, for example the wheel diameters behind `radius`. Code comments explain why, not what changed.
- If the controller needs the same value, for example the wheel radius and separation in `diffbot_control/config/remo/geometry.yaml` in the diffbot repository, open the matching pull request there and link the two.
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
