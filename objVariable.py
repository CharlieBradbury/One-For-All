#Regular variable
class objVariable():
	def __init__(self, id=999, name="NoName", data_type="NoType"):
		self.id = id
		self.name = name
		self.data_type = data_type

	def printVariable(self):
		try:
			print("VARIABLE", self.id, self.data_type, self.name)
		except:
			print("Error while printing information of variable")
