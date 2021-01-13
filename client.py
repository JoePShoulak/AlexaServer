
import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = "infinium shut down"

    client_socket.send(message.encode())  # send message
    data = client_socket.recv(8).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    print()
    try:
        client_program()
    except ConnectionRefusedError:
        print("The server doesn't appear to be online.\n")
