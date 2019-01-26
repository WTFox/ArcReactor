import random
import neopixel

import config
from utils import COLORS, one_in_five_chance, adjust_brightness, color_chase


strip = neopixel.NeoPixel(config.PIXEL_PIN, config.NUM_PIXELS)


def main():
    button_pressed = False
    color = COLORS["nuclear_blue"]
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS

    color_chase(color, strip)
    while True:
        if one_in_five_chance():
            alpha_up = not alpha_up

        if random.randint(1, 1000) == 1000:
            button_animation()

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()


def button_animation():
    strip.fill(COLORS["light_pink"])
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS
    for i in range(180):
        if one_in_five_chance():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()

    strip.fill(COLORS["nuclear_blue"])


main()
