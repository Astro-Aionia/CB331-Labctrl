import time
import numpy as np
import zhinst.utils

# Log sequence recorded on 2025/04/22 10:31:44
import time
import zhinst.core

daq = zhinst.core.ziDAQServer('127.0.0.1', 8004, 6)
# Starting module scopeModule on 2025/04/22 10:31:44
scope = daq.scopeModule()
scope.set('lastreplace', 1)
scope.subscribe('/dev20014/scopes/0/wave')
scope.set('historylength', 100)
scope.set('averager/weight', 1)
scope.set('averager/restart', 0)
scope.set('averager/weight', 1)
scope.set('averager/restart', 0)
scope.set('fft/power', 0)
scope.unsubscribe('*')
scope.set('mode', 1)
scope.set('fft/spectraldensity', 0)
scope.set('fft/window', 1)
scope.set('save/directory', 'C:\\Users\\zhenggroup\\Documents\\Zurich Instruments\\LabOne\\WebServer')
daq.setInt('/dev20014/inputpwas/0/enable', 1)

