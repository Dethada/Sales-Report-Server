#!/usr/bin/python3
import socket, time, sys

''' 
check for connection drops
Could not create socket
Cannot connect to Server
The connection has been dropped'''
BUFSIZE = 1024
TIMEOUT = 10
ACK = 'k'

def printBye():
    print(time.ctime()[0:19])
    print('See you again.')

if len(sys.argv) != 2:
    print('Usage: {} <city name>'.format(sys.argv[0]))
    sys.exit(-1)
else:
    print(time.ctime()[0:19])
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', 8091))
    clientsocket.settimeout(TIMEOUT)
    clientsocket.sendall('c'.encode())
    try:
        reply = clientsocket.recv(BUFSIZE).decode()
    except socket.timeout:
        print('Timed out')
        sys.exit()
    if reply == ACK:
        clientsocket.sendall(sys.argv[1].encode())
    else:
        print("Error Encountered")
        printBye()
        sys.exit()
    print(clientsocket.recv(BUFSIZE).decode())
    clientsocket.close()
    printBye()