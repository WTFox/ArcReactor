import random

import neopixel
from digitalio import DigitalInOut, Direction, Pull

import config
from utils import COLORS, one_in_five_chance, adjust_brightness, color_chase


strip = neopixel.NeoPixel(config.PIXEL_PIN, config.NUM_PIXELS)  
led = DigitalInOut(config.BUTTON_LED_PIN)
led.direction = Direction.OUTPUT


def main():
    button = DigitalInOut(config.BUTTON_PIN)
    button.direction = Direction.INPUT
    button.pull = Pull.UP

    color = COLORS["nuclear_blue"]
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS

    color_chase(color, strip)
    while True:
        if one_in_five_chance():
            alpha_up = not alpha_up

        if not button.value:
            button_animation()

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()


def button_animation():
    strip.fill(COLORS["light_pink"])
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS
    for i in range(180):
        led.value = True
        if one_in_five_chance():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()

    strip.fill(COLORS["nuclear_blue"])
    led.value = False


main()
