import socket
from threading import Thread
from modules import *
from LED import *

def listening_animation(device):
    while True:
        if not pause:
            slower_high_pulse(device)

def executing_animation(device):
    for i in range(2):
        high_pulse(device)

def server_program():
    # get the hostname
    host = ''
    port = 5000  # initiate port no above 1024
    server_socket = socket.socket()

    
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1, block_orientation=0,
                     rotate=0, blocks_arranged_in_reverse_order=False)

    server_socket.bind((host, port))  # bind host address and port together
    print("Server is online. Awaiting commands. ")
    global pause
    pause = False
    Thread(target=listening_animation, args=(device,), daemon=True).start()

    while True:
        try:
            server_socket.listen(2)
            conn, address = server_socket.accept()  # accept new connection
            
            print("Connection from: " + str(address))
            data = conn.recv(1024).decode()

            pause = True
            executing_animation(device)
            pause = False
            
            print("\tReceived data:", data)
            conn.send("success".encode())  # Tell them we got their command

            execute_data(data, server_socket)
        except KeyboardInterrupt:
            print("Shutting down server...")
            pause = True
            sleep(3)
            exit()
            

if __name__ == '__main__':
    print()
    server_program()


