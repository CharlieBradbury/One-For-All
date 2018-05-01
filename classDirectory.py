<<<<<<< HEAD
from objClass import objClass
from errorHandler import errorHandler
import sys

# Directory of classes
class classDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    # Returns a boolean indicating if a class with such ID exists in the dictionary
    def checkClassById(self, class_id):
        return (self.directory.get(class_id, None) is not None)

    # Returns a boolean indicating in a class with such Name exists in the dictionary
    def checkClassByName(self, class_name):
        for key, tClass in self.directory.items():
            if tClass.name == class_name:
                return True
        return False

    # Returns a class with the ID given as parameter
    # If it wasn't found, it returns an error
    def getClassById(self, class_id):
        try:
            return self.directory.get(class_id, None)
        except:
            self.error.definition(self.error.CLASS_NOT_DEFINED, class_id, None)

    # Returns a class with the name given as parameter
    # If it wasn't found, it returns an error
    def getClassByName(self, class_name):
        for key, tClass in self.directory.items():
            if tClass.name == class_name:
                return tClass
        self.error.definition(self.error.CLASS_NOT_DEFINED, class_name, None)

    # Return size of current directory
    def getSize(self):
        return len(self.directory)

    # Receives a class as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addClass(self, tClass):
        if self.directory.get(tClass.id, None) is None:
            self.directory[tClass.id] = tClass
        else:
            self.error.definition(self.error.DUPLICATED_CLASS, tClass.id, None)

    #Receives a class id and tries to delete it from the dictionary
    def deleteClass(self, class_id):
        try:
            del self.directory[class_id]
        except:
=======
from objClass import objClass
from errorHandler import errorHandler
import sys

# Directory of classes
class classDirectory:
    def __init__(self):
        self.directory = dict()
        self.error = errorHandler()
    
    # Returns a boolean indicating if a class with such ID exists in the dictionary
    def checkClassById(self, class_id):
        return (self.directory.get(class_id, None) is not None)

    # Returns a boolean indicating in a class with such Name exists in the dictionary
    def checkClassByName(self, class_name):
        for key, tClass in self.directory.items():
            if tClass.name == class_name:
                return True
        return False

    # Returns a class with the ID given as parameter
    # If it wasn't found, it returns an error
    def getClassById(self, class_id):
        try:
            return self.directory.get(class_id, None)
        except:
            self.error.definition(self.error.CLASS_NOT_DEFINED, class_id, None)

    # Returns a class with the name given as parameter
    # If it wasn't found, it returns an error
    def getClassByName(self, class_name):
        for key, tClass in self.directory.items():
            if tClass.name == class_name:
                return tClass
        self.error.definition(self.error.CLASS_NOT_DEFINED, class_name, None)

    # Return size of current directory
    def getSize(self):
        return len(self.directory)

    # Receives a class as parameter and tries to add it to the directory
    # If it cannot be added, it displays an error
    def addClass(self, tClass):
        if self.directory.get(tClass.id, None) is None:
            self.directory[tClass.id] = tClass
        else:
            self.error.definition(self.error.DUPLICATED_CLASS, tClass.id, None)

    #Receives a class id and tries to delete it from the dictionary
    def deleteClass(self, class_id):
        try:
            del self.directory[class_id]
        except:
>>>>>>> 5c2149a286042df86ff44edfeb16dbeadb01c713
            self.error.definition(self.error.CLASS_NOT_DELETED, class_id, None)