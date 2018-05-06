#Variable associated to a class
class classVariable():
	def __init__(self, id, name, data_type,privacy, dim=0, value=None):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.privacy = privacy
		self.dim = dim
		self.value = value

	def printClassVariable(self):
		try:
			print("CLASS VARIABLE", self.id, self.privacy, self.data_type, self.name)
		except:
			print("Error while printing information of class variable")
