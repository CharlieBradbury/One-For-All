#Create object to store elements of a class
class objClass():
	def __init__(self, id, name, parent):
		self.id = id
		self.name = name
		self.parent = parent

		# Variables
		self.publicVariables = {}
		self.publicMethods = {}

		# Methods
		self.privateVariables = {}
		self.privateMethods = {}
	
	# Add public variable
	def addPublicVariable(self, objVar):
		self.publicVariables[objVar.name] = objVar

	# Add public method
	def addPublicMethod(self, objFunc):
		self.publicMethods[objFunc.name] = objFunc
	
	# Add public variable
	def addPrivateVariable(self, objVar):
		self.privateVariables[objVar.name] = objVar

	# Add public method
	def addPrivateMethod(self, objFunc):
		self.privateMethods[objFunc.name] = objFunc

	def printClass(self):
		try:
			print("CLASS INFORMATION")
			print("Name of class: ", self.name)
			print("Inherits from: ", self.parent)
			print("Public variables: ", self.publicVariables)
			print("Public methods: ", self.publicMethods)
			print("Private variables: ", self.privateVariables)
			print("Private methods: ", self.privateMethods)
		except:
			print("Error while printing information of class")

#Variable associated to a class
class objVariable_Class():
	def __init__(self, id, name, data_type, pri):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.isPublic = isPublic