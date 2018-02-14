#!/usr/bin/python3
'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''
import socket, sys, os
from utilities_3177 import *

BUFSIZE = 1024
ACK = 'k'
DIR = 'uploads/'
PORT = 8091
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind(('localhost', PORT))
except OSError as e:
    if str(e) == '[Errno 98] Address already in use':
        print('Port {} already in use'.format(PORT))
    else:
        print('Unexpected error occured')
    sys.exit(1)
serversocket.listen(1)
print("Listening on port {}...".format(PORT))

''' determines which handler should be used for the connection '''
def main(connection):
    print('Handling a client connection...', end='\r')
    try:
        rec = connection.recv(BUFSIZE).decode()
    except socket.timeout:
        connection.close()
        return
    if rec == 's': # pass to uploadHandler
        connection.sendall(ACK.encode())
        uploadHandler(connection)
    elif rec == 'c': # pass to cityReportHandler
        connection.sendall(ACK.encode())
        cityReportHandler(connection)
    connection.close()
    print(' '*31, end='\r')

''' 
takes the client connection as parameter
sends city sales report to client '''
def cityReportHandler(connection):
    try:
        city = connection.recv(BUFSIZE).decode()
    except socket.timeout:
        return
    report = CityReport(city, DIR)
    connection.sendall(report.getSummary().encode())

''' 
takes the client connection as parameter
recieves city sales records from the client
validates the records and stores them '''
def uploadHandler(connection):
    line = None
    city = set()
    fp = None
    if not os.path.exists(DIR):
        os.makedirs(DIR) # create uploads directory
    while True:
        try:
            line = connection.recv(BUFSIZE).decode()
        except socket.timeout:
            closeFP(fp)
            break
        if line != 'N' and line != None:
            splitline = line.split('\t')
            try:
                lineValidation(splitline)
            except InvalidFormat: # invalid line, terminate the upload
                connection.sendall("Operation aborted due to invalid data.".encode())
                closeFP(fp)
                break
            city.add(splitline[2])
            if len(city) != 1: # multiple cities detected, terminate the upload
                connection.sendall("Operation aborted due to invalid data.".encode())
                closeFP(fp)
                break
            connection.sendall(ACK.encode())
            # write the record out to disk
            try:
                fp.write('{}\n'.format(line))
            except AttributeError:
                fp = open('{}{}.txt'.format(DIR, list(city)[0]), 'w')
                fp.write('{}\n'.format(line))
        else:
            closeFP(fp)
            break

# listen for connections
while True:
    try:
        connection, address = serversocket.accept()
        connection.settimeout(10)
        main(connection)
    except KeyboardInterrupt:
        print('\nClosing Server...')
        serversocket.close()
        sys.exit(0)