from objVariable import objVariable 
from errorHandler import errorHandler
import sys

class variableDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    # Returns a boolean indicating if a variable with such ID exists in the dictionary
    def checkVariableById(self, var_id):
        return (self.directory.get(var_id, None) is not None)

    # Returns a boolean indicating in a variable with such Name exists in the dictionary
    def checkVariableByName(self, var_name):
        for key, variable in self.directory.items():
            if variable.name == var_name:
                return True
        return False

    # Returns a variable with the ID given as parameter
    # If it wasn't found, it returns an error
    def getVariableById(self, var_id):
        try:
            return self.directory.get(var_id, None)
        except:
            self.error.definition(self.error.VARIABLE_NOT_DEFINED, var_id, None)

    # Returns a variable with the name given as parameter
    # If it wasn't found, it returns an error
    def getVariableByName(self, var_name):
        for key, variable in self.directory.items():
            if variable.name == var_name:
                return variable
        self.error.definition(self.error.VARIABLE_NOT_DEFINED, var_name, None)

    # Receives a variable as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addVariable(self, variable):
        if self.directory.get(variable.id, None) is None:
            self.directory[variable.id] = variable
        else:
            self.error.definition(self.error.DUPLICATED_VARIABLE, variable.id, None)
    
    #Method that adds multiple variable objects list to the directory
    def addMultipleVariables (self, variables):
        try:
            for var in variables:
                if self.checkVariableByName(var.name) is False:
                    self.directory[var.id] = var
        except:
            pass
            
    def printDirectory(self):
        for key,var in self.directory.items():
            var.printVariable()