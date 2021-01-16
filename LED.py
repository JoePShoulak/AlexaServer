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

def fade_out(device):
    with canvas(device) as draw:
        draw.line((0, 0, 7, 7), fill="white")
        draw.line((7, 7, 0, 0), fill="white")
            
def low_pulse(device):
    fade_circle(device, 0, 0, 7)
    fade_circle(device, 1, 8, 15)
    fade_circle(device, 1, 8, 15, backward=True)
    fade_circle(device, 0, 0, 7, backward=True)

def high_pulse(device):
    delay = 0.01
    fade_circle(device, 0, 0, 3, delay)
    fade_circle(device, 1, 4, 7, delay)
    fade_circle(device, 2, 8, 11, delay)
    fade_circle(device, 3, 12, 15, delay)
    fade_circle(device, 3, 12, 15, delay, backward=True)
    fade_circle(device, 2, 8, 11, delay, backward=True)
    fade_circle(device, 1, 4, 7, delay, backward=True)
    fade_circle(device, 0, 0, 3, delay, backward=True)

def slower_high_pulse(device):
    delay = 0.1
    fade_circle(device, 0, 0, 3, delay)
    fade_circle(device, 1, 4, 7, delay)
    fade_circle(device, 2, 8, 11, delay)
    fade_circle(device, 3, 12, 15, delay)
    fade_circle(device, 3, 12, 15, delay, backward=True)
    fade_circle(device, 2, 8, 11, delay, backward=True)
    fade_circle(device, 1, 4, 7, delay, backward=True)
    fade_circle(device, 0, 0, 3, delay, backward=True)
    
        
   

def demo(n, block_orientation, rotate, inreverse):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
    print("Created device")

    # start demo
    msg = "MAX7219 LED Matrix Demo"
    print(msg)
    for j in range(10):
        for i in range(3):
            slower_high_pulse(device)

        for i in range(3):
            high_pulse(device)
            high_pulse(device)
            sleep(1)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
