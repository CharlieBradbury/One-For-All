from objFunction import objFunction
from objClass import objMethod
from errorHandler import errorHandler
import sys

# Directory of routines, works for both functions and methods
class routineDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()

    def getSize(self):
        return len(self.directory)
    
    # Returns a boolean indicating if a routine with such ID exists in the dictionary
    def checkRoutineById(self, routine_id):
        return (self.directory.get(routine_id, None) is not None)

    # Returns a boolean indicating in a routine with such Name exists in the dictionary
    def checkRoutineByName(self, routine_name):
        for key, routine in self.directory.items():
            if routine.name == routine_name:
                return True
        return False

    # Returns a routine with the ID given as parameter
    # If it wasn't found, it returns an error
    def getRoutineById(self, routine_id):
        try:
            return self.directory.get(routine_id, None)
        except:
            self.error.definition(self.error.ROUTINE_NOT_DEFINED, routine_id, None)

    # Returns a routine with the name given as parameter
    # If it wasn't found, it returns an error
    def getRoutineByName(self, routine_name):
        for key, routine in self.directory.items():
            if routine.name == routine_name:
                return routine
        self.error.definition(self.error.ROUTINE_NOT_DEFINED, routine_name, None)

    # Receives a routine as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addRoutine(self, routine):
        if self.directory.get(routine.id, None) is None:
            self.directory[routine.id] = routine
        else:
            self.error.definition(self.error.DUPLICATED_ROUTINE, routine.name, None)

    #Receives a routine id and tries to delete it from the dictionary
    def deleteRoutine(self, routine_id):
        try:
            del self.directory[routine_id]
        except:
            self.error.definition(self.error.ROUTINE_NOT_ADDED, routine_id, None)