# ##############################
# # Title: Stop Watch
# # Desc: Helper class for time management
# # Author: Arjun Singh
# ##############################

import time


class StopWatch:
    """Set deadlines and reset clock"""
    end_time = None

    def __init__(self):
        self.end_time = time.time()

    def past(self):
        """Check if current time is past deadline time"""
        return time.time() > self.end_time

    def reset(self, delta=0):
        """Set future time (now + delta in seconds)"""
        self.end_time = time.time() + delta
