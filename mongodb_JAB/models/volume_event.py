import time

class VolumeEvent:
    @staticmethod
    def create_event(old_vol, new_vol, distance):
        return {
            "timestamp": time.time(),
            "old_volume": old_vol,
            "new_volume": new_vol,
            "finger_distance": distance
        }