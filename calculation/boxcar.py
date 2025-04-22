import numpy as np

def boxcar_calc(data, gate_start=0, baseline_start=55, gate_width=45):
    sig = np.sum(data[gate_start:gate_start+gate_width])/gate_width
    bg = np.sum(data[baseline_start:baseline_start+gate_width])/gate_width
    return sig - bg