import random
import time
import config

COLORS = dict(
    baja_blast=[0, 235, 100],
    blue=[0, 0, 255],
    green=[0, 255, 0],
    light_pink=[255, 51, 204],
    nuclear_blue=[0, 150, 255],
    purple=[150, 0, 255],
    red=[255, 0, 0],
)


def one_in_five_chance():
    return random.randint(1, 5) == 5


def clamp_value(val, min_val, max_val):
    return max(min(max_val, val), min_val)


def color_chase(color, strip):
    for i in range(config.NUM_PIXELS):
        strip[i] = color
        time.sleep(0.04)
        strip.show()


def adjust_brightness(alpha_up, current_brightness):
    if alpha_up:
        current_brightness += config.BRIGHTNESS_VARIANCE
    else:
        current_brightness -= config.BRIGHTNESS_VARIANCE

    if current_brightness <= config.MIN_BRIGHTNESS:
        alpha_up = True
    elif current_brightness >= config.MAX_BRIGHTNESS:
        alpha_up = False

    return (
        alpha_up,
        clamp_value(
            val=current_brightness,
            min_val=config.MIN_BRIGHTNESS,
            max_val=config.MAX_BRIGHTNESS,
        ),
    )


class Timer(object):
    def __init__(self, interval):
        self.interval = interval

    def start(self):
        self.prevtime = time.monotonic()

    @property
    def done(self):
        t = time.monotonic()
        if (t - self.prevtime) >= self.interval:
            self.prevtime = t
            return True
        return False
