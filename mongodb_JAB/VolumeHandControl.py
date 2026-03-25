from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np


class VolumeController:
    def __init__(self):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

        volRange = self.volume.GetVolumeRange()
        self.minVol = volRange[0]
        self.maxVol = volRange[1]
        self.current_vol = self.get_current_volume()

    def get_current_volume(self):
        return self.volume.GetMasterVolumeLevel()

    def set_volume(self, length):
        vol = np.interp(length, [50, 300], [self.minVol, self.maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        self.volume.SetMasterVolumeLevel(vol, None)
        self.current_vol = vol
        return volBar, volPer