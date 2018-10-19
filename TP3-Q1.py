#!/usr/bin/env python3
# -*- coding: latin-1 -*-


import sys

try:
    import argparse
    import socket
except ImportError:
    print("Error ! can not loaded external libs", file=sys.stderr)
    sys.exit(84)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", dest="port", type=int, default=1337)
    port = vars(parser.parse_args())["port"]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

    while True:

        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)
            while True:
                data = connection.recv(1024).decode("utf-8").replace("\r\n", "")
                print (data)
                if not data:
                    break

        finally:
            connection.close()
