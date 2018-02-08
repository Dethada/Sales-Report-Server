#!/usr/bin/python3
import socket, time, sys

''' Add in timeouts '''
BUFSIZE = 1024
TIMEOUT = 10
ACK = 'k'

if len(sys.argv) != 2:
    print('Usage: {} <city name>'.format(sys.argv[0]))
    sys.exit(-1)
else:
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('127.0.0.1', 8091))
    time.sleep(20)
    # clientsocket.settimeout(TIMEOUT)
    # clientsocket.sendall('c'.encode())
    # reply = clientsocket.recv(BUFSIZE).decode()
    # if reply == ACK:
    #     print(time.ctime()[0:19])
    #     clientsocket.sendall(sys.argv[1].encode())
    # print(clientsocket.recv(BUFSIZE).decode())
    # clientsocket.close()
    # print(time.ctime()[0:19])
    # print('See you again.')