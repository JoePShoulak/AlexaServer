from tuyapy import *
from time import sleep
from random import randrange
from threading import Thread
import numpy

global stop_loop
stop_loop = False

all_lights = {
    'Den Main 1': 'ebacf1b57b5fdd4c16kjvu',
    'Den Main 2': 'eb11efb59ae065d95fuve7',
    'Den Main 3': 'eb535dc4ea64b2656cphhw',
    'Den Main 4': 'ebd68299ad91af49c4ghxr',

    'Bathroom 1': '6676520440f520f9c9f0',
    'Bathroom 2': '6676520424a1600a52e6',

    'Dining 1': '6676520440f520fd60bd',
    'Dining 2': '6676520440f520fa0f61',
    'Den Lamp': '3026412140f520efb8fd',

    'Pantry': '6676520440f520f84945',

    'Bedroom Lamp': '6676520440f520fcd995'
}

den_main_ids = ["Den Main 1",
                "Den Main 2",
                "Den Main 3",
                "Den Main 4"]


def map_spectrum(color):
    color[0] = int((numpy.arctan(color[0] / 45 - 4)/1.11/1.2 + 1) * 180)
    return color


def display_animation_options():
    print("Pick an animation!")
    i = 1
    for animation in animations.keys():
        print("\t" + str(i) + ": " + animation)
        i += 1
    print("\t0: Exit")
    print("?: ", end="")


def get_devices_from_ids(ids, api_obj):
    devices = []

    for id in ids:
        devices.append(api_obj.get_device_by_id(all_lights[id]))

    return devices


def set_light_color(light, color):
    light.set_color(color)


def turn_off_light(light):
    light.turn_off()


def turn_on_light(light):
    light.turn_on()


def set_lights_to_color(lights, color):
    threads = []

    if color == "white":
        color = [0, 0, 1000]
    else:
        color = [color, 1000, 1000]
    for light in lights:
        threads.append(Thread(target=set_light_color, args=(light, color,), daemon=True))

    for t in threads:
        t.start()


def turn_off_lights(lights):
    threads = []

    for light in lights:
        threads.append(Thread(target=turn_off_light, args=(light,), daemon=True))

    for t in threads:
        t.start()


def turn_on_lights(lights):
    threads = []

    for light in lights:
        threads.append(Thread(target=turn_on_light, args=(light,), daemon=True))

    for t in threads:
        t.start()


def reset_lights(lights):
    set_lights_to_color(lights, "white")
    turn_on_lights(lights)


def random_basic_color():
    return randrange(0, 15) * 16


def rainbow(lights):
    color = 0
    while not stop_loop:
        if color == 360:
            color = 0
        else:
            color += 1

        set_lights_to_color(lights, color)
        sleep(0.5)


def cross_faded(lights):
    half1 = [lights[0], lights[2]]
    half2 = [lights[1], lights[3]]

    old_color = random_basic_color()

    it = 0

    while not stop_loop:
        if it % 2 == 0:
            subset = half1
        else:
            subset = half2

        new_color = random_basic_color()
        if abs(new_color - old_color) < 90:
            new_color = (new_color + 90) % 360

        set_lights_to_color(subset, new_color)
        old_color = new_color
        it = 1 - it
        sleep(1)


def marquee(lights):
    half1 = [lights[0], lights[2]]
    half2 = [lights[1], lights[3]]

    it = 0

    while not stop_loop:
        if it % 2 == 0:
            subset = half1
            other = half2
        else:
            subset = half2
            other = half1

        turn_off_lights(other)
        turn_on_lights(subset)

        it = 1 - it

        sleep(1)


def nebula(lights):
    color = 0

    while not stop_loop:
        threads = []
        i = 0
        for light in lights:
            temp_color = map_spectrum([(color + (32*i)) % 256, 100, 100])
            threads.append(Thread(target=set_light_color, args=(light, temp_color,)))
            i += 1

        for t in threads:
            t.start()

        color = (color + 2) % 360
        sleep(0.5)
