import platform
from os import system


def update():
    print()
    system("git pull")
    print()

    print("\t\t\t\tStarting server...")
    if platform.node() == "Infinium":
        system("server.py")
    else:
        system("python3.8 server.py")

