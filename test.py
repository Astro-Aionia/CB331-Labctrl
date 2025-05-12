from labctrl.components.TOPAS.remote import ProxiedTOPAS
from labctrl.labconfig import LabConfig, lcfg

topas = ProxiedTOPAS(config=lcfg.config["TOPAS"]["T23233P"])

for wv in range(3500, 3550, 1):
    response = topas.set_wavelength(interaction="DF1-SIG", wavelength=wv)
    print(response)