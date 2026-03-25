import time

class Session:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.duration = 0

    def end_session(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        return {
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": self.duration
        }