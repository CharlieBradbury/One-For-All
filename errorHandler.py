import sys

class errorHandler():
    #For variables 
    VARIABLE_NOT_DEFINED =  1
    VARIABLE_NOT_FOUND =  2
    VARIABLE_CREATION =  3  
    DUPLICATED_VARIABLE =  4

    #Operation
    INVALID_OPERATION = 5
    TYPE_MISMATCH = 6

    #Classes
    CLASS_NOT_DEFINED =7
    DUPLICATED_CLASS = 8
    CLASS_NOT_DELETED = 9

    def __init__(self):
        self.directory = dict()       
    
    def definition(self, error_type, arg1, arg2):
        if error_type == 1:
            print("Error (" + str(error_type) + ") : Variable not defined ", arg1)
        elif error_type == 2:
            print("Error (" + str(error_type) + ") : Variable does not exist", arg1)
        elif error_type == 3:
            print("Error (" + str(error_type) + ") : Error while creating new variable ", arg1)
        elif error_type == 4:
            print("Error (" + str(error_type) + ") : Variable already declared ", arg1)
        elif error_type == 5:
            print("Error (" + str(error_type) + ") : Invalid operation", arg1, arg2)
        elif error_type == 6:
            print("Error (" + str(error_type) + ") : Type mismatch", arg1, arg2)
        elif error_type == 7:
            print("Error (" + str(error_type) + ") : Class not defined", arg1)
        elif error_type == 8:
            print("Error (" + str(error_type) + ") : Class already defined", arg1)
        elif error_type == 9:
            print("Error (" + str(error_type) + ") : Class not deleted", arg1)

        
        #raise Exception(error_type)
        


