# FocusTime

"Time-keeping for people who need to focus"

## Getting Set Up

1. Python 3 is required, and using a python virtual environment (`venv`) is *strongly* recommended:

   ```bash
   py -m venv venv
   ```

2. Execute the relevant `activate` script for your platform. This may be `activate`, `activate.bat` or `Activate.ps1`.

3. Make sure `pip` is up to date in the virtual environment:

   ```bash
   py -m pip install --upgrade pip
   ```

4. Use `pip` to install `pytest`, and `toga` (with pre-release features)

   ```bash
   pip install pytest
   pip install --pre toga
   ```

## Building / Testing / Deploying from the Command-line

TBD

---

5. The recommended IDE is [VSCode](https://code.visualstudio.com/). Configure this in accordance with the [RTK Reference Manual](https://fortescue-autonomy.gitlab.io/rtk/reference-manual/tools/visual_studio_code/) and the [RTK Python Style Guide](https://gitlab.com/groups/fortescue-autonomy/-/wikis/RTK/Python-Style-Guide). For this project, there are a few extra things to configure for better integration into VSCode:

   a. Use the `.vscode/settings.json` file to tell VSCode to use the local virtual environment automatically for things like linting and debugging, by adding the following line:

   ```json
   "python.pythonPath": "${workspaceFolder}/venv/Scripts/python.exe"
   ```

   b. Tell VSCode's testing support functionality to use `pytest`, and to find tests in the `./test` folder by adding the following lines to the `.vscode/settings.json` file:

   ```json
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true,
   ```

   c. Set up a debugging / running launch configuration by adding the following lines to the `.vscode/launch.json` file:

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Launch from Main",
               "type": "python",
               "request": "launch",
               "module": "dashboard.dashboard"
           }
       ]
   }
   ```

   You can then use VSCode's built-in support for debugging, breakpoints, testing frameworks and so on.

## Attribution List

* dashboard by Atif Arshad from the Noun Project
