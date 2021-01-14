import subprocess
from os import system


def update():
    proc = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    output = str(out.strip())[2:-1]
    print("\t\t\t\t" + output)
    print("\t\t\t\tStarting server...")
    system("server.py")

