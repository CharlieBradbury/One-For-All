#Create object to store elements of a class
from classVariable import classVariable
from classMethod import classMethod

class objClass():
	def __init__(self, id, name, parent="NoParent"):
		self.id = id
		self.name = name
		self.parent = parent

		# Variables and methods
		self.variableClassDirectory = {}
		self.methodsClassDirectory = {}

	def printClass(self):
		try:
			print("")
			print("CLASS INFORMATION")
			print("Class Id", self.id)
			print("Name of class:", self.name)
			print("Inherits from:", self.parent)


			print("Variables: ")
			for key, var in self.variableClassDirectory.items():
				var.printClassVariable()

			print("Methods: ")
			for key, method in self.methodsClassDirectory.items():
				method.printMethod()

			print("----------------------")
		except:
			print("Error while printing information of class")