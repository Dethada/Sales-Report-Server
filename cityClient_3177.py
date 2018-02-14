#!/usr/bin/python3
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''
import socket, time, sys

BUFSIZE = 1024
TIMEOUT = 10
ACK = 'k'
INIT = 'c'

''' prints exit time, close socket and exit '''
def exitErr(sock):
    print(time.ctime()[0:19])
    sock.close()
    sys.exit(1)

if len(sys.argv) != 2:
    print('Usage: {} <city name>'.format(sys.argv[0]))
    sys.exit(1)
else:
    print(time.ctime()[0:19]) # print start time
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientsocket.connect(('127.0.0.1', 8091))
    except ConnectionRefusedError:
        print('Cannot connect to Server')
        exitErr(clientsocket)
    clientsocket.settimeout(TIMEOUT)
    clientsocket.sendall(INIT.encode())
    try:
        reply = clientsocket.recv(BUFSIZE).decode()
    except socket.timeout:
        print('Timed out')
        exitErr(clientsocket)
    if reply == ACK: # send the cityname to the server
        clientsocket.sendall(sys.argv[1].encode())
    else:
        print("Error Encountered")
        exitErr(clientsocket)
    try: # prints the summary or the err msg
        print(clientsocket.recv(BUFSIZE).decode())
    except socket.timeout:
        print('Timed out')
        exitErr(clientsocket)
    clientsocket.close()
    print(time.ctime()[0:19])
    print('See you again.')