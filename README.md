# PyQt-Labctrl

Ultrafast experiments controlling framework with PyQt6 front end. The structure is from [Zizhi's labctrl program](https://github.com/F6/labctrl).

- author:       Aionia
- email:        A_Ionia@outlook.com
- online repo:  https://github.com/Astro-Aionia/pyqt-labctrl


## How to Use

1. Add a new instruments:

    first, implement the RESTful API for the new device in "servers", also provide an emulator if possible (the emulator helps you to debug higher layer programs without actually having to be connected to the lab equipment).

    By "RESRful" we mean the device tells the user what it can do when accessed, this makes it simpler for users to use it without complicated documentation.

    Assign a new port to your API and add it to the table in `./servers/README.md` (to avoid conflicting with existing devices.)

    Add a json config file of the new device in `./configs/`. The config file must include the API host and port for the new device， because servers are isolated part of the software and probably runs on other computers, the program have no way to know which port and host to access if not specified in the configs (unless we include UDP broadcasting in our software, but this is not as reliable as directly pin down the addresses).

2.  Add a new widget

    For every instrument, add a new GUI frond end in `./widgets/` to communicate with its server with HTTP. In this program PyQt6 is used as the frond end. One can also use other front end.

3. Add a new application

    For an actual experiment, create a new GUI in `./apps/` conbining with all widgets of needed instruments.

## Deployment

Use Ananconda to create an env, install required packages with

```cmd
pip install -f requirements.txt
```
