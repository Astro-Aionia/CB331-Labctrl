from labctrl.labstat import LabStat
from labctrl.labconfig import LabConfig

from .bundle_PyQt6 import BundlePyQt6TOPAS

class FactoryTOPAS:
    def __init__(self, lcfg: LabConfig, lstat: LabStat) -> None:
        self.lcfg = lcfg
        self.lstat = lstat
        self.generated = dict()

    def generate_bundle(self, bundle_config: dict):
        """
        actually generates the bundle
            bundle_config:  dict that contains all information needed to generate
                             the bundle
                            required fields:
                                "Config" : config dict of target device

        for now only bokeh bundle is used, so direct generation,
        if more are required, then the fork goes here
        """
        name = bundle_config["Config"]["Name"]
        if name in self.generated:
            print("[SANITY] FactoryTOPAS: BundleTOPAS with name {} already generated before!".format(name))
        foo = BundlePyQt6TOPAS(bundle_config, self.lcfg, self.lstat)
        self.generated[name] = foo
        return foo