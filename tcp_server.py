import socket
import sys
import argparse
import json

host = 'localhost'
data_payload = 1024
backlog = 10


def socket_server(port):
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # sock.settimeout(5)
    server_address = (host, port)
    print ("Starting up echo server  on %s port %s" % server_address)
    sock.bind(server_address)
    sock.listen(backlog)

    print ("Waiting to receive message from client")
    client, address = sock.accept()
    while True:
        recvData = ''
        data = client.recv(data_payload)
        if data:
            print("\n\n")
            print(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    # parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    # port = given_args.port
    port = 8080
    socket_server(port)