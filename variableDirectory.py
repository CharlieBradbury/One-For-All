from objVariable import objVariable 
from errorHandler import errorHandler
import sys

class variableDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    def addVariable (self, variable):
        if self.directory.get(variable.name, None) is None:
            self.directory[variable.name] = variable
        else:
            self.error.definition(self.error.DUPLICATED_VARIABLE, variable.name, None)
    
    def checkVariable(self, var_name):
        if self.directory.get(var_name, None) is None:
            self.error.definition(self.error.VARIABLE_NOT_DEFINED, var_name, None)
        else:
            return True

    def getAddressVariable(self, var_name):
        if self.directory.get(var_name, None) is not None:
            return self.directory.get(var_name, None)
            

