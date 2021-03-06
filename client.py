
import socket


def client_program():  # Ask on stack overflow why this works here but not on pi
    # host = socket.gethostname()  # local device
    host = '192.168.0.30'  # working computer
    # host = '192.168.0.44'  # raspberry pi
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = "lights truck"

    client_socket.send(message.encode())  # send message
    data = client_socket.recv(8).decode()  # receive response

    print('Received from server: ' + data)  # show in terminal

    client_socket.close()  # close the connection


if __name__ == '__main__':
    print()
    client_program()
    try:
        pass
    except ConnectionRefusedError:
        print("The server doesn't appear to be online.\n")
