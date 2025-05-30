# -*- coding: utf-8 -*-

"""labconfig.py:
This module provides the singleton class LabConfig to hold parameters for
instruments and experiment configurations.
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211010"

import json
# import time
import os
# from glob import glob
# import numpy as np
# from datetime import datetime
# from enum import Enum
from functools import wraps

from .singleton import Singleton
# from .labstat import lstat


# class ExperimentType(Enum):
#     IMFS = "IR Modulated Fluorescence"
#     WLS = "White Light Spectrum Test"
#     IPVP = "IR Pump Visible Probe"
#     TRPL = "Time-resolved Photoluminescence (Kerr Gating)"
#     THz = "Vis/IR Pump THz Probe"


class LabConfig(metaclass=Singleton):
    """Singleton class to hold all the information needed for our experiment.
    """

    def __init__(self) -> None:
        self.__load_default()

    def __load_default(self) -> None:
        """recursively load all json in configs dir and assemble them into a big one"""
        default_config_dir = 'configs'
        self.config = dict()

        def get_cfg(root: str):
            root = root.replace("\\", "/")
            keys = root.split('/')
            keys.pop(0)
            cfg = self.config # default case
            for k in keys:
                cfg = cfg[k]
            return cfg

        for root, dirs, files in os.walk(default_config_dir):
            cfg = get_cfg(root)
            common = None
            if '_COMMON.json' in files:  # deal with properties common to all
                filepath = root + '/_COMMON.json'
                with open(filepath, 'r') as f:
                    common = json.load(f)
                files.remove('_COMMON.json')

            for file in files:
                if file.endswith('.json'):
                    filepath = root + '/' + file
                    # print(filepath)
                    cfgname = file[:-5]
                    with open(filepath, 'r') as f:
                        cfg[cfgname] = json.load(f)
                    if common:
                        for k in common: # copy common configs
                            cfg[cfgname][k] = common[k]

            for dir in dirs:
                cfg[dir] = dict()

    def load_config(self, config: dict = None) -> None:
        """If a config is loaded, recursively overwrite default settings 
        or current settings.
        This method only cares about loading config, no sanity check
        """
        def recursive_load(df: dict, dt: dict) -> None:
            for k, v in iter(df.items()):
                if type(v) is not dict:
                    dt[k] = v
                else:
                    recursive_load(v, dt[k])

        if config:
            recursive_load(config, self.config)

    def save_config(self, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=4)

    def refresh_config(self) -> None:
        """
        When lab config is updated, do the following:
            - Save a backup config in last_config.json
            - (When debugging) Print some of the config
            - (TODO) Try to do some simple sanity check and gives warnings
        """
        self.save_config("last_config.json")
        # a convenient alias: print sums when refresh config
        # expmsg(self.print_lists())
        # expmsg(self.estimate_time())

    def update_config(self, func):
        """add this decorator so that lcfg is immediately updated after the function call"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print(args)
            # print(kwargs)
            func(*args, **kwargs)
            self.refresh_config()
        return wrapper


lcfg = LabConfig()
last_config_file = "last_config.json"

if last_config_file in os.listdir():
    with open(last_config_file, 'r') as f:
        last_config = json.load(f)
    lcfg.load_config(last_config)

lcfg.refresh_config()
