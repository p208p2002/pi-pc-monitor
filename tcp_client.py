import socket
import sys
import argparse
import time
from core import getBasicMsg


host = 'localhost'

def echo_client(port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    sock.send(str("123").encode('utf-8'))
    time.sleep(3)
    sock.send(str("123").encode('utf-8'))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=8080)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)