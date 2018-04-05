#Create object to store elements of a class
class objClass():
    def __init__(self, id, name, parent):
        self.id = id
        self.name = name
        self.parent = parent
        self.varTable = {}
        self.methodTable = {}
    
    #To add variables to class object
    def createVariables(self, objVar):
        self.varTable.update({objVar.name : objVar})
    
    #To add methods to our class object 
    def createMethods(self, objMethod):
        self.methodTable.update({objMethod.name : objMethod})

#Variable associated to a class
class objVariable_Class():
    def __init__(self, id, name, data_type, isPublic):
        self.id = id
        self.name = name
        self.data_type = data_type
        self.isPublic = isPublic

#Mehods for a class    
#params is a list of variables object 
class objMethods():
    def __init__(self, id, name, params, data_type, isPublic):
        self.id = id
        self.name = name
        self.params = params
        self.data_type = data_type
        self.isPublic = isPublic
        self.tempVars = []
