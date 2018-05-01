#Regular variable
from arrayManager import arrayManager

class objVariable():
	def __init__(self, id, name, data_type, dim=0, value=None):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.dim = dim
		self.value = value

	def printVariable(self):
		try:
			print("VARIABLE", self.id, self.data_type, self.name, self.dim)
		except:
			print("Error while printing information of variable")
