import time

import neopixel

import config
from utils import COLORS, Timer, clamp_value, one_in_five_chance


STRIP = neopixel.NeoPixel(config.PIXEL_PIN, config.NUM_PIXELS)
TIMER = Timer(3)


def main():
    """ Entry point for Circuit Python 
    `mode` determines the pattern. The choices are:

        0 - Arc Reactor pattern
        1 - Color Chase and Color Cycle Arc Reactor
        2 - Color Ring Cycle
        3 - Rainbow Whell
    """
    mode = 0

    # Arc Reactor
    if mode == 0:
        color_chase(COLORS['nuclear_blue'], 0.04)
        while True:
            arc_reactor(COLORS['nuclear_blue'])

    # Color Chase and Color Cycle Arc Reactor
    elif mode == 1:
        while True:
            for color in COLORS.values():
                color_chase(color, 0.02)
                time.sleep(0.3)
            for color in COLORS.values():
                arc_reactor(color)

    # Color Ring Cycle
    elif mode == 2:
        while True:
            for color in COLORS.values():
                ring_cycle(color)

    # Rainbow Cycle
    elif mode == 3:
        rainbow_cycle()


def color_chase(color, wait):
    for i in range(config.NUM_PIXELS):
        STRIP[i] = color
        time.sleep(wait)
        STRIP.show()


def arc_reactor(color):
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS
    STRIP.fill(color)

    while True:
        if one_in_five_chance():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        STRIP.brightness = brightness
        STRIP.write()

        if TIMER.timer_done:
            return


def rainbow_cycle():
    while True:
        for j in range(255):
            for i in range(config.NUM_PIXELS):
                rc_index = (i * 256 // config.NUM_PIXELS) + j
                STRIP[i] = wheel(rc_index & 255)
            STRIP.show()


def ring_cycle(color):
    offset = 0  # Position of spinner animation
    iteration = 1
    while not iteration >= 40:  # ~3 seconds
        # A little trick here: pixels are processed in groups of 8
        # (with 2 of 8 on at a time), NeoPixel rings are 24 pixels
        # (8*3) and 16 pixels (8*2), so we can issue the same data
        # to both rings and it appears correct and contiguous
        # (also, the pixel order is different between the two ring
        # types, so we get the reversed motion on #2 for free).
        for i in range(24):  # For each LED...
            if ((offset + i) & 7) < 2:  # 2 pixels out of 8...
                STRIP[i] = color  # are set to current color
            else:
                STRIP[i] = [0, 0, 0]  # other pixels are off
        STRIP.write()  # Refresh LED states
        time.sleep(0.04)  # 40 millisecond delay
        offset += 1  # Shift animation by 1 pixel on next frame
        if offset >= 8:
            offset = 0

        iteration += 1


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
            max_val=config.MAX_BRIGHTNESS
        )
    )


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0) or (pos > 255):
        return (0, 0, 0)
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


main()
