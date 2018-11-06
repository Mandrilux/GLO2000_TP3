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
    WriteErrorLog("Error ! Can not load external libs")

def WriteErrorLog(msg, display=1):
    log = open("Error.log", "a")
    log.write(str(datetime.now()) + " " + msg + "\n")
    log.close()
    if display:
        print(msg, file=sys.stderr)
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
        a = entierAleatoire(m)
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                print ("Envoi du modulo " + str(m))
                print ("Envoi de la base " + str(n))
                send_msg(connection, str(m))
                send_msg(connection, str(n))
                print("Generation de la cle privee " + str(a))
                A = exponentiationModulaire(n, a, m)
                send_msg(connection, str(A))
                print("Envoi de la cle publique " + str(A))
                B = recv_msg(connection)
                print("Reception de la cle publique client " + B)
                k = exponentiationModulaire(int(B), a, m)
                print("Obtention de la cle partagee " + str(k))
                data = connection.recv(1024)
                print (data)
                if not data:
                    break
        finally:
            connection.close()

def runClient(port, dest):
    print("Trying " + str(dest) + ":" + str(port) + " ...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (dest, port)

    try:
        sock.connect(server_address)
    except socket.error as e:
        WriteErrorLog(str(e))
    try:
        modulo = recv_msg(sock)
        print ("Reception du modulo " + modulo)
        base = recv_msg(sock)
        print("Reception de la base " + base)
        b = entierAleatoire(int(modulo))
        print("Generation de la cle privee " + str(b))
        B = exponentiationModulaire(int(base), b, int(modulo))
        A = recv_msg(sock)
        print("Reception de la cle publique serveur " + A)
        send_msg(sock, str(B))
        print("Envoi de la cle publique " + str(B))
        k = exponentiationModulaire(int(A), b, int(modulo))
        print("Obtention de la cle partagee " + str(k))
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
    try:
        args = parser.parse_args()
    except:
        WriteErrorLog("Invalid Parameters", 0)
    port = args.port

    if args.serveur:
        server = 1
        client = 0
    if args.destination:
        dest = 1

    if server and dest:
        WriteErrorLog("Error ! Do not use --destination with server mode")
    if client and dest == 0:
        WriteErrorLog("Error ! Need destination with client mode")
    if server:
        runServer(port)
    else:
        runClient(port, args.destination)

    sys.exit(0)
