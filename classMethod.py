from variableDirectory import variableDirectory
#Mehods for a class    
#params is a list of variables object 
class classMethod():
	def __init__(self, id, name, data_type, privacy, params=None):
		self.id = id
		self.name = name
		self.data_type = data_type
		self.privacy = privacy
		if params is not None:
			self.params = params
			self.countParams = len(params)
		self.localVars = variableDirectory()
		self.countVars = 0

	def printMethod(self):
		print("METHOD", self.id, self.privacy, self.data_type, self.name)
		self.localVars.printDirectory()
		'''try:
			stringParameters = ""
			for _par in self.params:
				stringParameters += (_par[0] + " " + _par[1] + ", ")
			print("METHOD", self.id, self.privacy, self.data_type, self.name)
			self.localVars.printDirectory()
		except:
			print("METHOD", self.id, self.privacy, self.data_type, self.name)
			self.localVars.printDirectory()
			print("Error while printing information of method")
		'''
