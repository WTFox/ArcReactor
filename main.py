import neopixel
from digitalio import DigitalInOut, Direction, Pull

import config
from utils import COLORS, one_in_five_chance, adjust_brightness, color_chase


strip = neopixel.NeoPixel(config.PIXEL_PIN, config.NUM_PIXELS)  
led = DigitalInOut(config.BUTTON_LED_PIN)
led.direction = Direction.OUTPUT

button_presses = 0


def main():
    global button_presses
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
            button_animation(
                COLORS["nuclear_blue"],
                get_next_color(button_presses)
            )
            button_presses += 1

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()


def get_next_color(b_presses):
    colors = sorted(COLORS.keys())
    colors.remove('nuclear_blue')
    index = b_presses % len(colors)
    return COLORS[colors[index]]


def button_animation(current_color, new_color):
    strip.fill(new_color)
    alpha_up = True
    brightness = config.STARTING_BRIGHTNESS
    for i in range(180):
        led.value = True
        if one_in_five_chance():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)
        strip.brightness = brightness
        strip.write()

    strip.fill(current_color)
    led.value = False


main()
