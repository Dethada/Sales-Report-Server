#!/usr/bin/python3
import socket, sys, os
from heapq import nlargest, nsmallest

''' 
Use classes 
block multiple upload connections
update upload handler
multithreading'''

BUFSIZE = 1024
ACK = 'k'
DIR = 'uploads/'
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8091))
serversocket.listen(1)
print("Listening on port 8091...")

''' determines which handler should be used for the connection '''
def main(connection):
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

def cityReportHandler(connection):
    try:
        city = connection.recv(BUFSIZE).decode()
    except socket.timeout:
        return
    try:
        fp = open("{}{}.txt".format(DIR, city), 'r')
    except FileNotFoundError:
        connection.sendall("\nCity not found\n".encode())
        return
    connection.sendall(getSummary(fp).encode())
    fp.close()

class InvalidFormat(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(self.code)

''' takes in a single split line returns the sales value of the line
returns none if no valid float value is found or line format is wrong'''
def lineValidation(splitline):
    if len(splitline) != 6: # skip line if it has invalid format
        raise InvalidFormat(1)
    try:
        return float(splitline[4])
    except ValueError: # skip line if it has invalid data
        raise InvalidFormat(2)

'''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php
takes in a dictonary and n as parameter where n is number of top values
returns top n keys with values from dict'''
def getTop(dictionary, n):
    top = nlargest(n, dictionary, key=dictionary.get) # get n keys with highest values
    for i in range(n):
        top[i] = '{:<23}{:23.2f}'.format(top[i], dictionary[top[i]])
    return top

''' takes in a dictonary and n as parameter where n is number of lowest values
returns bottom n keys with values from dict '''
def getBottom(dictionary, n):
    btm = nsmallest(n, dictionary, key=dictionary.get) # get n keys with lowest values
    btm.reverse()
    for i in range(n):
        btm[i] = '{:<23}{:23.2f}'.format(btm[i], dictionary[btm[i]])
    return btm

''' takes in citySales, category sales and total sales amt as parameters
prints out the sales summary for all cities and categories '''
def returnSummary(city, catSales, totalSale):
    output = ''
    noCats = len(catSales)
    if noCats == 0:
        return "Invalid data file. Operation aborted."
    avgCatSale = totalSale / noCats
    divider = '=' * 46
    output += "Total Sales from {} is {:.2f}\n".format(city, totalSale)
    output += "The Average Sales From {} Item Categories:\n{:46.2f}\n\n".format(noCats, avgCatSale)
    if noCats > 3:
        output += "Top Three Item Categories\n{}\n".format(divider)
        for cat in getTop(catSales, 3):
            output += '{}\n'.format(cat)
        output += "{0}\n\nBottom Three Item Categories\n{0}\n".format(divider)
        for cat in getBottom(catSales, 3):
            output += '{}\n'.format(cat)
    else: # different format for 3 or less categories
        output += "Sales Figures by Item Categories\n{}\n".format(divider)
        for cat in getTop(catSales, noCats):
            output += '{}\n'.format(cat)
    output += '{}\n'.format(divider)
    return output

''' takes in a filepointer as parameter
prints summary of the purchases records'''
def getSummary(fp):
    catSales = {}
    totalSale = 0
    city = None
    for line in fp:
        splitline = line.split("\t")
        try:
            salesAmt = lineValidation(splitline)
        except InvalidFormat:
            continue
        totalSale += salesAmt # calculate total sales amount
        city, cat = splitline[2], splitline[3]
        try:
            catSales[cat] += salesAmt # calculate category sales amount
        except KeyError:
            catSales[cat] = salesAmt # add category to dictionary
    return returnSummary(city, catSales, totalSale)

def uploadHandler(connection):
    line = None
    city = set()
    output = ''
    if not os.path.exists(DIR):
        os.makedirs(DIR) # create uploads directory
    while True:
        try:
            line = connection.recv(BUFSIZE).decode()
        except socket.timeout:
            return
        if line != 'N' and line != None:
            splitline = line.split('\t')
            try:
                lineValidation(splitline)
            except InvalidFormat:
                connection.sendall("Operation aborted due to invalid data.".encode())
                return
            city.add(splitline[2])
            if len(city) != 1:
                connection.sendall("Operation aborted due to invalid data.".encode())
                return
            output += '{}\n'.format(line)
            connection.sendall(ACK.encode())
        else:
            break
    with open('{}{}.txt'.format(DIR, list(city)[0]), 'w') as f:
        f.write(output)


# listen for connections
while True:
    try:
        connection, address = serversocket.accept()
        connection.settimeout(10)
        main(connection)
    except KeyboardInterrupt:
        print('\nClosing Server...')
        serversocket.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)