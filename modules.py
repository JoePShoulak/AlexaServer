from roku import Roku
from helper import *
from lights import *


def light_module(actions, socket):
    print("\t\tReceived Light command.")

    animations = {
        "rainbow": rainbow,
        "cross_faded": cross_faded,
        "marquee": marquee,
        "nebula": nebula
    }

    USERNAME = 'joepshoulak@me.com'  # username (email) from the android app
    PASSWORD = 'Fibonacci1123!'  # password you set in your android app - choose a random one :)
    COUNTRY_CODE = 'US'  # make sure you choose your country when registering in the app
    api = TuyaApi()

    logged_in = False

    try:
        api.init(USERNAME, PASSWORD, COUNTRY_CODE)
        logged_in = True
    except:
        print("\t\t\t! API Error. Try again in 60 seconds.")

    if logged_in or actions[0] == "stop":
        den_main = get_devices_from_ids(den_main_ids, api)

        stop_loop = True
        sleep(1)
        reset_lights(den_main)
        stop_loop = False
        sleep(1)

        if actions[0] != "stop":
            Thread(target=animations[actions[0]], args=(den_main,), daemon=True).start()


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


mod_funcs = {
    "Roku": roku_module,
    "Lights": light_module,
    "lights": light_module
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
            print("\t\t\t! Module or command does not exist.")

    print("\n\tAll tasks complete!\n")
