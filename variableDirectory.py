from objVariable import objVariable 
from errorHandler import errorHandler
import sys

class variableDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    def checkVariable(self, var_name):
        if self.directory.get(var_name, None) is None:
            return False
        else:
            return True

    def addVariable (self, variable):
        if self.checkVariable(variable.name):
            return None
            #self.error.definition(self.error.DUPLICATED_VARIABLE, variable.name, None)
        else:
            self.directory[variable.name] = variable
    
    #Method that adds multiple variable objects list to the directory
    def addMultipleVariables (self, variables):
        try:
            for var in variables:
                if self.checkVariable(var.name) is False:
                    self.directory[var.name] = var
        except:
            pass

    def getAddressVariable(self, var_name):
        if self.checkVariable(var_name):
            return self.directory.get(var_name, None)
            
    def printDirectory(self):
        for key,var in self.directory.items():
            var.printVariable()
            

