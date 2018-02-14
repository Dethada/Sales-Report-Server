#!/usr/bin/python3
import socket, sys, os
from heapq import nlargest, nsmallest

BUFSIZE = 1024
ACK = 'k'
DIR = 'uploads/'
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8091))
serversocket.listen(1)
print("Listening on port 8091...")

def main(connection):
    buf = connection.recv(BUFSIZE)
    rec = buf.decode()
    while True:
        pass

# listen for connections
while True:
    try:
        connection, address = serversocket.accept()
        main(connection)
    except KeyboardInterrupt:
        print('\nClosing Server...')
        serversocket.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)