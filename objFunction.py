#Function class
class objFunction():
	def __init__(self, id, name, data_type, params):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.params = params
		self.tempVars = []
		self.returnValue = 13

	def printFunction(self):
		try:

			stringParameters = ""

			for _par in self.params:
				stringParameters += (_par.data_type + " " + _par.name + ", ")

			print("FUNCTION", self.id, self.data_type, self.name, "Parameters:", stringParameters)
		except:
			print("Error while printing information of function")
