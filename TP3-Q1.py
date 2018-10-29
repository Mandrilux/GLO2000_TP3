#!/usr/bin/env python3
# -*- coding: latin-1 -*-


import sys

try:
    import argparse
    import socket
    from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire
    from socketUtil import *
except ImportError:
    print("Error ! can not loaded external libs", file=sys.stderr)
    sys.exit(84)


def runServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("0.0.0.0", port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    sock.listen(1)
    while True:
        print('waiting for a connection')
        m = trouverNombrePremier()
        n = entierAleatoire(m)
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                send_msg(connection, "Envoi du modulo " + str(m) + "\n")
                send_msg(connection, "Envoi de la base " + str(n) + "\n")
                data = connection.recv(1024).decode("utf-8").replace("\r\n", "")
                print (data)
                if not data:
                    break
            """connection.sendall(str.encode("Bien recu"), 0)"""
        finally:
            connection.close()

def runClient():
    print("on run le client")

if __name__ == "__main__":

    server = 0
    client = 1
    dest = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", action="store", dest="port", type=int, required=True)
    parser.add_argument("--serveur", "-s", help="start a server (client mode by default)", action="store_true")
    parser.add_argument("--destination", "-d", help="setup Ip destination ( with client mode only)")
    args = parser.parse_args()
    port = args.port

    if args.serveur:
        server = 1
        client = 0
    if args.destination:
        dest = 1

    if server and dest:
        print("Error ! Not --destination with server mode", file=sys.stderr)
        sys.exit(84)

    if server:
        runServer(port)
    else:
        runClient()

    sys.exit(0)
