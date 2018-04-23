from objFunction import objFunction
from errorHandler import errorHandler
import sys

class functionDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    def addFunction (self, function):
        if self.directory.get(function.name, None) is None:
            self.directory[function.name] = function
        else:
            self.error.definition(self.error.DUPLICATED_FUNCTION, function.name, None)
    
    def checkFunction(self, func_name):
        if self.directory.get(func_name, None) is None:
            self.error.definition(self.error.FUNCTION_NOT_DEFINED, func_name, None)
        else:
            return True

    def getAddressFunction(self, func_name):
        if self.directory.get(func_name, None) is not None:
            return self.directory.get(func_name, None)

            

