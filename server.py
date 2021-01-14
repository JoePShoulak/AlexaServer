import socket
from modules import *


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server is online. Awaiting commands. ")

    # configure how many client the server can listen simultaneously
    while True:
        server_socket.listen(2)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        print("\tReceived data:", data)
        conn.send("success".encode())  # Tell them we got their command

        execute_data(data, server_socket)


if __name__ == '__main__':
    print()
    server_program()


