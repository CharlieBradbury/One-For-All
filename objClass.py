#Create object to store elements of a class
class objClass():
	def __init__(self, id, name, parent="NoParent"):
		self.id = id
		self.name = name
		self.parent = parent

		# Variables
		self.publicVariables = dict()
		self.publicMethods = dict()

		# Methods
		self.privateVariables = dict()
		self.privateMethods = dict()
	
	# Add public variable
	def addPublicVariable(self, objVar):
		self.publicVariables[objVar.name] = objVar

	# Add public method
	def addPublicMethod(self, objMethod):
		self.publicMethods[objMethod.name] = objMethod
	
	# Add private variable
	def addPrivateVariable(self, objVar):
		self.privateVariables[objVar.name] = objVar

	# Add private method
	def addPrivateMethod(self, objMethod):
		self.privateMethods[objMethod.name] = objMethod

	def printClass(self):
		try:
			print("")
			print("CLASS INFORMATION")
			print("Name of class:", self.name)
			print("Inherits from:", self.parent)

			print("Public variables: ")
			for key, pubVar in self.publicVariables.items():
				pubVar.printClassVariable()

			print("Public methods: ")
			for key, pubMethod in self.publicMethods.items():
				pubMethod.printMethod()

			print("Private variables: ")
			for key, priVar in self.privateVariables.items():
				priVar.printClassVariable()

			print("Private methods: ")
			for key, priMethod in self.privateMethods.items():
				priMethod.printMethod()

			print("")
		except:
			print("Error while printing information of class")

#Variable associated to a class
class objVariable_Class():
	def __init__(self, id, name, data_type, privacy):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.privacy = privacy

	def printClassVariable(self):
		try:
			print("CLASS VARIABLE", self.id, self.privacy, self.data_type, self.name)
		except:
			print("Error while printing information of class variable")

#Mehods for a class    
#params is a list of variables object 
class objMethod():
	def __init__(self, id, name, data_type, params, privacy):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.params = params
		self.privacy = privacy
		self.tempVars = []

	def printMethod(self):
		try:
			stringParameters = ""

			for _par in self.params:
				stringParameters += (_par.data_type + " " + _par.name + ", ")

			print("METHOD", self.id, self.privacy, self.data_type, self.name, "Parameters:", stringParameters)
		except:
			print("Error while printing information of method")
