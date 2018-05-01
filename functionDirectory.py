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
<<<<<<< HEAD
        else:
            self.error.definition(self.error.FUNCTION_NOT_DEFINED, func_name, None)
=======
>>>>>>> 5c2149a286042df86ff44edfeb16dbeadb01c713

    def printDirectory(self):
        for key, func in self.directory.items():
            func.printFunction()

            

