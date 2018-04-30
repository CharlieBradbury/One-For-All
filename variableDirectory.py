from objVariable import objVariable
from objClass import objVariable_Class
from errorHandler import errorHandler
import sys

# Directory of variables, works for both normal variables and class variables
class variableDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    # Returns a boolean indicating if a variable with such ID exists in the dictionary
    def checkVariableById(self, variable_id):
        return (self.directory.get(variable_id, None) is not None)

    # Returns a boolean indicating in a variable with such Name exists in the dictionary
    def checkVariableByName(self, variable_name):
        for key, variable in self.directory.items():
            if variable.name == variable_name:
                return True
        return False

    # Returns a variable with the ID given as parameter
    # If it wasn't found, it returns an error
    def getVariableById(self, variable_id):
        try:
            return self.directory.get(variable_id, None)
        except:
            self.error.definition(self.error.VARIABLE_NOT_DEFINED, variable_id, None)

    # Returns a variable with the name given as parameter
    # If it wasn't found, it returns an error
    def getVariableByName(self, variable_name):
        for key, variable in self.directory.items():
            if variable.name == variable_name:
                return variable
        self.error.definition(self.error.VARIABLE_NOT_DEFINED, variable_name, None)

    # Return size of current directory
    def getSize(self):
        return len(self.directory)

    # Receives a variable as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addVariable(self, variable):
        if self.directory.get(variable.id, None) is None:
            self.directory[variable.id] = variable
        else:
            self.error.definition(self.error.DUPLICATED_VARIABLE, variable.id, None)

    #Receives a variable id and tries to delete it from the dictionary
    def deleteVariable(self, variable_id):
        try:
            del self.directory[variable_id]
        except:
            self.error.definition(self.error.VARIABLE_NOT_DELETED, variable_id, None)