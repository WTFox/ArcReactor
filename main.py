import random
import time

import board
import neopixel


# Colors
LIGHT_BLUE = [0, 150, 255]
LIGHT_PINK = [200, 0, 150]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]

# Real starting values
BRIGHTNESS_VARIANCE = 0.09
MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1

# Dev starting values (to save my eyes)
# BRIGHTNESS_VARIANCE = 0.0125
# MIN_BRIGHTNESS = 0.03
# MAX_BRIGHTNESS = 0.1

STARTING_BRIGHTNESS = (MIN_BRIGHTNESS + MAX_BRIGHTNESS) / 2

# Set up the lights
NUM_PIXELS = 24
PIXEL_PIN = board.D1

strip = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS)


def main():
    arc_reactor(LIGHT_BLUE)
    # ring_cycle(LIGHT_BLUE)
    # rainbow_cycle()


def arc_reactor(color):
    alpha_up = True
    brightness = STARTING_BRIGHTNESS
    strip.fill(color)

    while True:
        if one_in_five_chance():
            alpha_up = not alpha_up

        alpha_up, brightness = adjust_brightness(alpha_up, brightness)

        strip.brightness = brightness
        strip.write()


def rainbow_cycle():
    while True:
        for j in range(255):
            for i in range(len(strip)):
                idx = int((i * 256 / len(strip)) + j)
                strip[i] = wheel(idx & 255)
            strip.write()
            time.sleep(0.001)
 

def ring_cycle(color):
    numpix = 24  # Number of NeoPixels
    mode = 0  # Current animation effect
    offset = 0  # Position of spinner animation
    prevtime = time.monotonic()  # Time of last animation mode switch
    
    while True:  
        # A little trick here: pixels are processed in groups of 8
        # (with 2 of 8 on at a time), NeoPixel rings are 24 pixels
        # (8*3) and 16 pixels (8*2), so we can issue the same data
        # to both rings and it appears correct and contiguous
        # (also, the pixel order is different between the two ring
        # types, so we get the reversed motion on #2 for free).
        for i in range(numpix):  # For each LED...
            if ((offset + i) & 7) < 2:  # 2 pixels out of 8...
                strip[i] = color  # are set to current color
            else:
                strip[i] = [0, 0, 0]  # other pixels are off
        strip.write()  # Refresh LED states
        time.sleep(0.04)  # 40 millisecond delay
        offset += 1  # Shift animation by 1 pixel on next frame
        if offset >= 8:
            offset = 0
    
        t = time.monotonic()  # Current time in seconds
        if (t - prevtime) >= 8:  # Every 8 seconds...
            mode += 1  # Advance to next mode
            if mode > 1:  # End of modes?
                mode = 0  # Start over from beginning
                # Rotate color R->G->B
                color = [color[2], color[0], color[1]]
            strip.fill([0, 0, 0])  # Turn off all pixels
            prevtime = t  # Record time of last mode change


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
 

# Utility Functions
def one_in_five_chance():
    return random.randint(1, 5) == 5  


def clamp_value(val, min_val=MIN_BRIGHTNESS, max_val=MAX_BRIGHTNESS):
    return max(min(max_val, val), min_val)


main()
