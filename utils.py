import random
import time


def one_in_five_chance():
    return random.randint(1, 5) == 5


def clamp_value(val, min_val, max_val):
    return max(min(max_val, val), min_val)


class Timer(object):
    def __init__(self, interval):
        self.interval = interval
        self.start_timer()

    def start_timer(self):
        self.prevtime = time.monotonic()

    @property
    def timer_done(self):
        t = time.monotonic()
        if (t - self.prevtime) >= self.interval:
            self.prevtime = t
            return True
        return False
