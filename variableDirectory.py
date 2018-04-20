from objVariable import objVariable 
import sys

class variableDirectory:
    def __init__(self):
        self.directory = dict()
    
    def addVariable (self, variable):
        if self.directory.get(variable.name, None) is None:
            self.directory[variable.name] = variable
        else:
            print("The variable" + variable.name + "is already defined")
            sys.exit()
    
    def checkVariable(self, var_name):
        if self.directory.get(var_name, None) is None:
            print("The variable " + var_name + " does not exist")
            sys.exit()
        else:
            return True

    def getAddressVariable(self, var_name):
        if self.directory.get(var_name, None) is not None:
            return self.directory.get(var_name, None)

            

