#!/usr/bin/env python3
# -*- coding: latin-1 -*-


import sys

try:
    import argparse
    import socket
    from cryptoModule import entierAleatoire, trouverNombrePremier, exponentiationModulaire
    from socketUtil import *
    from datetime import datetime
except ImportError:
    errormsg = "Error ! Can not load external libs"
    log = open("Error.log", "a")
    log.write(str(datetime.now()) + " " + errormsg + "\n")
    log.close()
    print(errormsg, file=sys.stderr)
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
                print ("Envoi du modulo " + str(m))
                print ("Envoi de la base " + str(n))
                send_msg(connection, str(m))
                send_msg(connection, str(n))
                data = connection.recv(1024)
                print (data)
                if not data:
                    break
           #    data = connection.recv(1024).decode("utf-8").replace("\r\n", "")
           #    print (data)
           #    if not data:
           #        break
            """connection.sendall(str.encode("Bien recu"), 0)"""
        finally:
            connection.close()

def runClient(port, dest):
    print("Trying " + str(dest) + ":" + str(port) + " ...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (dest, port)
    sock.connect(server_address)

    try:
        message = recv_msg(sock)
        print (message)
    finally:
        sock.close()

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
        errormsg = "Error ! Do not use --destination with server mode"
        log = open("Error.log", "a")
        log.write(str(datetime.now()) + " " + errormsg + "\n")
        log.close()
        print(errormsg, file=sys.stderr)
        sys.exit(84)
    if client and dest == 0:
        errormsg = "Error ! Need destination with client mode"
        log = open("Error.log", "a")
        log.write(str(datetime.now()) + " " + errormsg + "\n")
        log.close()
        print(errormsg, file=sys.stderr)
        sys.exit(84)
    if server:
        runServer(port)
    else:
        runClient(port, args.destination)

    sys.exit(0)
