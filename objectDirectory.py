from objectO import objectO
from errorHandler import errorHandler
import sys

# Directory of classes
class objectDirectory:
    def __init__(self):
        self.directory = {}
        self.error = errorHandler()
    
    # Returns a boolean indicating if a object with such ID exists in the dictionary
    def checkObjectById(self, obj_id):
        return (self.directory.get(obj_id, None) is not None)

    # Returns a boolean indicating in a class with such Name exists in the dictionary
    def checkObjectByName(self, obj_name):
        for key, tClass in self.directory.items():
            if tClass.name == obj_name:
                return True
        return False

    # Returns a class with the ID given as parameter
    # If it wasn't found, it returns an error
    def getObjectById(self, obj_id):
        try:
            return self.directory.get(obj_id, None)
        except:
            self.error.definition(self.error.CLASS_NOT_DEFINED, obj_id, None)

    # Returns a class with the name given as parameter
    # If it wasn't found, it returns an error
    def getObjectByName(self, object_name):
        for key, tClass in self.directory.items():
            if tClass.name == object_name:
                return tClass
        self.error.definition(self.error.CLASS_NOT_DEFINED, object_name, None)

    def getObjectByClassName(self, class_name):
        for key, tClass in self.directory.items():
            if tClass.type == class_name:
                return tClass
        self.error.definition(self.error.CLASS_NOT_DEFINED, class_name, None)

    # Return size of current directory
    def getSize(self):
        return len(self.directory)

    # Receives a class as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addObject(self, obj):
        if self.directory.get(obj.id, None) is None:
            self.directory[obj.id] = obj
        else:
            self.error.definition(self.error.DUPLICATED_CLASS, obj.id, None)

    #Receives a class id and tries to delete it from the dictionary
    def deleteClass(self, obj_id):
        try:
            del self.directory[obj_id]
        except:
            self.error.definition(self.error.CLASS_NOT_DELETED, obj_id, None)

    def printDirectory(self):
        for key,obj in self.directory.items():
            obj.printObject()
   
