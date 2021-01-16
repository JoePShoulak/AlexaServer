import re
from time import sleep
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def clear_device(device):
    with canvas(device) as draw:
        draw.rectangle((0, 0, 0, 0,), outline="black", fill="black")
    device.contrast(0)


def fade_circle(device, radius, min_intensity, max_intensity, delay=0.1, backward=False):  # 0-16
    with canvas(device) as draw:
        draw.ellipse((3-radius, 3-radius, 4+radius, 4+radius), outline="white", fill="black")
    for intensity in range(max_intensity - min_intensity):
        intensity += min_intensity
        if backward:
            intensity = (max_intensity + min_intensity) - intensity
        device.contrast(intensity * 16)
        sleep(delay)
        if backward and intensity <= 1:
            clear_device(device)


def low_pulse(device):
    delay = 0.1
    fade_circle(device, 0, 0, 5, delay)
    fade_circle(device, 1, 6, 10, delay)
    fade_circle(device, 2, 11, 15, delay)
    fade_circle(device, 2, 11, 15, delay, backward=True)
    fade_circle(device, 1, 6, 10, delay, backward=True)
    fade_circle(device, 0, 0, 5, delay, backward=True)


def high_pulse(device):
    delay=0.01
    fade_circle(device, 0, 0, 3, delay)
    fade_circle(device, 1, 4, 7, delay)
    fade_circle(device, 2, 8, 11, delay)
    fade_circle(device, 3, 12, 15, delay)
    fade_circle(device, 3, 12, 15, delay, backward=True)
    fade_circle(device, 2, 8, 11, delay, backward=True)
    fade_circle(device, 1, 4, 7, delay, backward=True)
    fade_circle(device, 0, 0, 3, delay, backward=True)