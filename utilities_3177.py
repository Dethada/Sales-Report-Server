'''
Author: David Zhu (P1703177)
Class: DISM/FT/1A/21
'''
from heapq import nlargest, nsmallest

class CityReport:
    ''' initialize CityReport object '''
    def __init__(self, cityName, dir):
        self.cityName = cityName
        self.dir = dir

    '''reference: https://www.w3resource.com/python-exercises/dictionary/python-data-type-dictionary-exercise-22.php
    takes in a dictonary and n as parameter where n is number of top values
    returns top n keys with values from dict'''
    def getTop(self, dictionary, n):
        top = nlargest(n, dictionary, key=dictionary.get) # get n keys with highest values
        for i in range(n):
            top[i] = '{:<23}{:23.2f}'.format(top[i], dictionary[top[i]])
        return top

    ''' takes in a dictonary and n as parameter where n is number of lowest values
    returns bottom n keys with values from dict '''
    def getBottom(self, dictionary, n):
        btm = nsmallest(n, dictionary, key=dictionary.get) # get n keys with lowest values
        btm.reverse()
        for i in range(n):
            btm[i] = '{:<23}{:23.2f}'.format(btm[i], dictionary[btm[i]])
        return btm

    ''' returns summary of the purchases records '''
    def getSummary(self):
        try:
            fp = open("{}{}.txt".format(self.dir, self.cityName), 'r')
        except FileNotFoundError:
            return "\nInvalid City Name. Please try again.\n"
        catSales = {}
        totalSale = 0
        output = ''
        for line in fp:
            splitline = line.split("\t")
            salesAmt = float(splitline[4])
            totalSale += salesAmt # calculate total sales amount
            cat = splitline[3]
            try:
                catSales[cat] += salesAmt # calculate category sales amount
            except KeyError:
                catSales[cat] = salesAmt # add category to dictionary
        noCats = len(catSales)
        # check if number of categories is valid
        if noCats == 0:
            return "Invalid data file. Operation aborted."
        avgCatSale = totalSale / noCats
        divider = '=' * 46
        output += "Total Sales from {} is {:.2f}\n".format(self.cityName, totalSale)
        output += "The Average Sales From {} Item Categories:\n{:46.2f}\n\n".format(noCats, avgCatSale)
        if noCats > 3:
            output += "Top Three Item Categories\n{}\n".format(divider)
            for cat in self.getTop(catSales, 3):
                output += '{}\n'.format(cat)
            output += "{0}\n\nBottom Three Item Categories\n{0}\n".format(divider)
            for cat in self.getBottom(catSales, 3):
                output += '{}\n'.format(cat)
        else: # different format for 3 or less categories
            output += "Sales Figures by Item Categories\n{}\n".format(divider)
            for cat in self.getTop(catSales, noCats):
                output += '{}\n'.format(cat)
        output += '{}\n'.format(divider)
        fp.close()
        return output

''' Raise this exception when the file has a invalid format '''
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

''' close file pointer if it is opened '''
def closeFP(fp):
    if fp != None:
        fp.close()