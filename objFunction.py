from variableDirectory import variableDirectory

#Function class
class objFunction():
	def __init__(self, quadId, name, data_type, params=None):
		self.quadId = quadId
		self.name = name
		self.data_type = data_type
		if params is not None:
			self.params = params
			self.countParams = len(params)
		self.localVars = variableDirectory()
		self.countVars = 0
		
	def printFunction(self):
		try:
			stringParameters = ""
			for _par in self.params:
				stringParameters += (_par.data_type + " " + _par.name + ", ")
			print("\nFUNCTION", self.quadId, self.data_type, self.name, "\nParameters:", stringParameters, "Local variables counter:", self.countVars)
		except:
			print("\nFUNCTION", self.quadId, self.data_type, self.name, "\nLocal Variables counter:", self.countVars)
	
	def printVariable(self):
		try:
			for var in self.localVars:
				print("VARIABLE", var.id, var.data_type, var.name, var.dim)
		except:
			print("Error while printing information of variable")

	#Return the variable directory from the current function 
	def getVariableDirectory(self):
		return self.localVars
