from classVariable import classVariable
from classMethod import classMethod
from classDirectory import classDirectory
from copy import copy

class objectO():
	def __init__(self,id=1, name="NoNameObject", type="NoTypeObject"):
		#Address of the object 
		self.id = id 
		#Name of the object
		self.name = name 
		#Class of the object
		self.type = type

		#Methods of the object
		self.objMethods = {}
		#Attributes of the objects
		self.objAttr = {}
	
	#This function will be use to initialize the values of the object in the constructor
	def initObject(self):
		pass

	def printObject(self):
		try:
			print("")
			print("Object INFORMATION")
			print("Class", self.type)
			print("Name of object:", self.name)
			print("Address of object", self.id)
				
			print("Variables: ")
			for key, var in self.objAttr.items():
				var.printClassVariable()

			print("Methods: ")
			for key, method in self.objMethods.items():
				method.printMethod()

			print("----------------------")
		except:
			print("Error while printing information of object")