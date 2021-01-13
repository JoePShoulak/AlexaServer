import os
from threading import Thread

from roku import Roku
from helper import *
from time import sleep


def shutdown():
    os.system('shutdown -s')

    press_virtual_button(1)

    api = connect_to_smart_devices()
    turn_off_device(api, "Monitor 2")
    turn_off_device(api, "Monitor 1")


def infinium_module(actions):
    print("\t\tReceived Infinium command.")

    if actions == ["shut", "down"]:
        print("\t\t\tShutting down...")
        Thread(target=shutdown).start()


def roku_module(actions):
    print("\t\tReceived Roku command.")
    roku = Roku('192.168.0.170')

    remote = {
        "select": roku.select,
        "back": roku.back,
        "home": roku.home,

        "up": roku.up,
        "down": roku.down,
        "left": roku.left,
        "right": roku.right
    }

    if actions == "remote":
        buttons = actions[1:]
        print("\t\t\t\tExecuting the following combo...")

        for button in buttons:
            print("\t\t\t\t\t" + button)
            remote[button]()

    elif actions[0] == "resume":
        channel = official_names[" ".join(actions[1:])]
        print("\t\t\tResuming " + channel + "...")

        navigate_to_channel(roku, channel)

        try:
            button_combo(roku, combos["resume " + channel])
        except KeyError:
            print("Error: No combo for %s yet. Does the channel exist?", channel)


r = Roku('')
mod_funcs = {
    "Roku": roku_module,
    "Infinium": infinium_module
}


def execute_data(data):
    commands = data.split(" and ")

    for command in commands:
        words = command.split(" ")
        module = words[0]
        actions = list(map(lambda word: word.lower(), words[1:]))

        try:
            mod_funcs[module.capitalize()](actions)
        except KeyError:
            print("\nError: Module %s does not exist:", module)
    print("\n\tAll tasks complete!\n")
