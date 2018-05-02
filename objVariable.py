#Regular variable
from arrayManager import arrayManager

class objVariable():
	def __init__(self, id, name, data_type, dim=0, size=1, value=None):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.dim = dim
		self.size = int(size)
		self.value = value

	def setSize(self):
		try:
			if self.size > 1:
				self.value = [None] * self.size
		except:
			print("Error while trying to convert variable to array")

	def printVariable(self):
		try:
			print("VARIABLE", self.id, self.data_type, self.name, self.dim, self.value)
		except:
			print("Error while printing information of variable")
