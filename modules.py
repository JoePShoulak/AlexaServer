from roku import Roku
from helper import *


def roku_module(actions, socket):
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

    if actions[0] == "remote":
        buttons = actions[1:]
        print("\t\t\tExecuting the following combo...")

        for button in buttons:
            print("\t\t\t\t" + button)
            remote[button]()

    elif actions[0] == "resume":
        channel = official_names[" ".join(actions[1:])]
        print("\t\t\tResuming " + channel + "...")

        navigate_to_channel(roku, channel)

        try:
            button_combo(roku, combos["resume " + channel])
        except KeyError:
            print("\t\t\tError: No combo for %s yet. Does the channel exist?", channel)


mod_funcs = {
    "Roku": roku_module,
}


def execute_data(data, socket):
    commands = data.split(" and ")

    for command in commands:
        words = command.split(" ")
        module = words[0]
        actions = list(map(lambda word: word.lower(), words[1:]))

        try:
            mod_funcs[module.capitalize()](actions, socket)
        except KeyError:
            print("\nError: Module %s does not exist:", module)
    print("\n\tAll tasks complete!\n")
