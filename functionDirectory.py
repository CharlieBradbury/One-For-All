from objFunction import objFunction
from errorHandler import errorHandler
import sys

class functionDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    def addFunction (self, function):
        if self.checkFunction(function.name):
            self.error.definition(self.error.DUPLICATED_FUNCTION, function.name, None)
        else:
            self.directory[function.name] = function
            
    def checkFunction(self, func_name):
        if self.directory.get(func_name, None) is None:
            return False
        else:
            return True

    def getAddressFunction(self, func_name):
        if self.checkFunction(func_name):
            return self.directory.get(func_name, None)

    def printDirectory(self):
        for key, func in self.directory.items():
            func.printFunction()

            

