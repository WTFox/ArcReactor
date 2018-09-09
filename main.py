import random
import time

import board
import neopixel


# Colors
LIGHT_BLUE = [0, 150, 255]
LIGHT_PINK = [200, 0, 150]

# Real starting values
# BRIGHTNESS_VARIANCE = 0.045
# MIN_BRIGHTNESS = 0.1
# MAX_BRIGHTNESS = 0.4

# Dev starting values (to save my eyes)
BRIGHTNESS_VARIANCE = 0.0125
MIN_BRIGHTNESS = 0.03
MAX_BRIGHTNESS = 0.1

STARTING_BRIGHTNESS = (MIN_BRIGHTNESS + MAX_BRIGHTNESS) / 2

# Set up the lights
NUM_PIXELS = 24 
PIXEL_PIN = board.D2


def main():
    alpha_up = True
    brightness = STARTING_BRIGHTNESS
    strip = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)
    strip.fill(LIGHT_BLUE)

    while True:
        if random_bool():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)

        strip.brightness = brightness
        strip.write()


def adjust_brightness(alpha_up, current_brightness):
    if alpha_up:
        current_brightness += BRIGHTNESS_VARIANCE
    else:
        current_brightness -= BRIGHTNESS_VARIANCE

    if current_brightness <= MIN_BRIGHTNESS:
        alpha_up = True
    elif current_brightness >= MAX_BRIGHTNESS:
        alpha_up = False

    return alpha_up, clamp_value(current_brightness)


# Utility Functions
def random_bool():
    return random.randint(1, 5) == 5  


def clamp_value(val, min_val=MIN_BRIGHTNESS, max_val=MAX_BRIGHTNESS):
    return max(min(max_val, val), min_val)


main()
