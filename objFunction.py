#Function class
class objFunction():
	def __init__(self, quadId, name, data_type, params, variables):
		self.quadId = quadId
		self.name = name
		self.data_type = data_type
		self.params = params
		self.countParams = len(params)
		self.tempVars = variables

	def printFunction(self):
		try:

			stringParameters = ""

			for _par in self.params:
				stringParameters += (_par.data_type + " " + _par.name + ", ")

			print("FUNCTION", self.quadId, self.data_type, self.name, "Parameters:", stringParameters)
		except:
			print("Error while printing information of function")
