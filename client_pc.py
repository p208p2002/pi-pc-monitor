import socket
import sys
import argparse
import time
from core import getBasicMsg,getUsageMsg


defaulthost = '192.168.43.50'
defaultPort = 8080

def echo_client(host,port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    sock.send(getBasicMsg().encode('utf-8'))
    while True:
        sock.send(getUsageMsg().encode('utf-8'))
        time.sleep(0.25)


    sock.close()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, default=defaultPort)
    parser.add_argument('--host', action="store", dest="host", type=int, default=defaulthost)
    given_args = parser.parse_args()
    port = given_args.port
    host = given_args.host
    echo_client(host,port)