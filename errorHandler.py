import sys 

class errorHandler():
    # For variables 
    VARIABLE_NOT_DEFINED = [10, "Variable not defined"]
    VARIABLE_NOT_FOUND = [11, "Variable does not exist"]
    VARIABLE_CREATION = [12, "Error while creating variable"]
    DUPLICATED_VARIABLE = [13, "Variable already declared"]
    VARIABLE_NOT_DELETED = [14, "Could not delete variable"]

    # For routines 
    ROUTINE_NOT_DEFINED = [20, "Routine not defined"]
    ROUTINE_NOT_FOUND = [21, "Routine does not exist"]
    ROUTINE_CREATION = [22, "Error while creating Routine"]
    DUPLICATED_ROUTINE = [23, "Routine already declared"]
    ROUTINE_NOT_DELETED = [14, "Could not delete routine"]
    
    # For classes 
    CLASS_NOT_DEFINED = [30, "Class not defined"]
    CLASS_NOT_FOUND = [31, "Class does not exist"]
    CLASS_CREATION = [32, "Error while creating Class"]
    DUPLICATED_CLASS = [33, "Class already declared"]
    CLASS_NOT_DELETED = [34, "Could not delete class"]

    #For operation
    INVALID_OPERATION = [100, "Invalid operation"]
    TYPE_MISMATCH = [101, "Type mismatch"]

    # For Memory
    INVALID_MEMORY_ACCESS = [200, "Invalid access to memory, out of range"] 
    
    # Defines and prints an error code and its message
    def definition(self, error_type, arg1, arg2):
        # Adjusts print depending on the number of arguments received with some value
        if arg1 is not None:
            if arg2 is not None:
                print("Error (" + str(error_type[0]) + "): " + str(error_type[1]), arg1, arg2)
            else:
                print("Error (" + str(error_type[0]) + "): " + str(error_type[1]), arg1)
        else:
            print("Error (" + str(error_type[0]) + "): " + str(error_type[1]))
        sys.exit()