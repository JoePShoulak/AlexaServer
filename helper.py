from time import sleep
from tuyapy import *
import json
import requests


def press_virtual_button(num):
    body = json.dumps({
        "virtualButton": num,
        "accessCode": "amzn1.ask.account.AH2LLA5PJ7RSZ6T7OIZLU6IZMQ7AVXO2HDSRKGYBRFWWB276VHF2F4GJ6MLNXE42EGXTEKNVB76Z44KBSV6BAZV3CNHAIQFATWYJEWXG2AMZP3CTALQBE6YZZ3SXKKJC62KLWHWEYRSZU22BF334FB4DOQMU3QN4DO3T6RIQRSXPDXSHNUI6TEX77VF3CZEHLWO7LYO3TDQ2RDY"
    })
    requests.post(url="https://api.virtualbuttons.com/v1", data=body)


def turn_off_device(api, name):
    get_all_devices_and_ids(api)[name].turn_off()


def connect_to_smart_devices():
    USERNAME = 'joepshoulak@me.com'  # username (email) from the android app
    PASSWORD = 'Fibonacci1123!'  # password you set in your android app - choose a random one :)
    COUNTRY_CODE = 'US'  # make sure you choose your country when registering in the app
    api = TuyaApi()
    api.init(USERNAME, PASSWORD, COUNTRY_CODE)

    return api


def get_all_devices_and_ids(api):
    devices = {}
    for device in api.get_all_devices():
        devices[device.name()] = device
        print("Name: " + device.name() + ", ID: " + device.obj_id)

    return devices


combos = {
    "resume Hulu":          ["down", "select", 3, "select"],
    # "resume Netflix":   ["select", "back", 3,  # Choose our account and load, or click and out of whatever is there
    #                         "down", "down", "down", "down", "down", "down", "down", "select", "select"],
    "resume Prime Video":   ["select", 5, "right", "right", "right", "right", "right",
                             "select", 1, "down", "select", 1, "select"],
    "resume Apple TV":      [],
    "resume Disney Plus":   [],
    "resume Peacock TV":    ["down", "down", "left", "select"]
}


official_names = {
    'hulu':     'Hulu',
    'prime':    'Prime Video',
    'apple':    'Apple TV',  # there is no "continue watching," the items stay where they are and say "continue"
    'disney':   'Disney Plus',  # seems to be like apple
    'netflix':  'Netflix',  # changes what rows things are in. Leaving the code in in case it can be saved
    'peacock':  'Peacock TV',
    'spotify':  'Spotify Music',  # not really something you resume
    'xfinity':  'Xfinity Stream Beta',  # beta is closed to devices in same home as receiver
    'pandora':  'Pandora',  # same as spotify
    'fandango': 'FandangoNOW Movies & TV',  # I don't know what this is
}


def navigate_to_channel(roku, channel):
    if len(channel.split(" ")) == 1:
        channel = channel.capitalize()
    if roku.active_app.name != channel:
        if channel in official_names.values():
            roku[channel].launch()
            sleep(20)


def button_combo(roku, combo):
    remote = {
        "select": roku.select,
        "back": roku.back,
        "home": roku.home,

        "up": roku.up,
        "down": roku.down,
        "left": roku.left,
        "right": roku.right
    }

    for action in combo:
        if not isinstance(action, str):
            sleep(action)
        else:
            try:
                remote[action]()
            except KeyError:
                print("Error: %s is not set up as a button. Does it exist?", action.capitalize())
            sleep(0.5)



