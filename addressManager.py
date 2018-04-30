class addressManager():
	def __init__(self):
		#------------------------------------------------------
		# 	STATIC ADDRESSES
		#------------------------------------------------------
		self.GLOBALS_INT = 1000
		self.GLOBALS_FLOAT = 3000
		self.GLOBALS_BOOLEAN = 5000
		self.GLOBALS_STRING = 7000

		self.LOCALS_INT = 9000
		self.LOCALS_FLOAT = 11000
		self.LOCALS_BOOLEAN = 13000
		self.LOCALS_STRING = 15000

		self.TEMPORALS_INT = 17000
		self.TEMPORALS_FLOAT = 19000
		self.TEMPORALS_BOOLEAN = 21000
		self.TEMPORALS_STRING = 23000

		self.GLOBALS_OBJECT = 25000
		self.LOCALS_OBJECT = 27000
		self.TEMPORALS_OBJECT = 29000


		#--------------------------------------------------------
		#	COUNTER ADDRESSES
		#--------------------------------------------------------
		self.COUNTER_GLOBALS_INT = self.GLOBALS_INT
		self.COUNTER_GLOBALS_FLOAT = self.GLOBALS_FLOAT
		self.COUNTER_GLOBALS_BOOLEAN = self.GLOBALS_BOOLEAN
		self.COUNTER_GLOBALS_STRING = self.GLOBALS_STRING

		self.COUNTER_LOCALS_INT = self.LOCALS_INT
		self.COUNTER_LOCALS_FLOAT = self.LOCALS_FLOAT
		self.COUNTER_LOCALS_BOOLEAN = self.LOCALS_BOOLEAN
		self.COUNTER_LOCALS_STRING = self.LOCALS_STRING

		self.COUNTER_TEMPORALS_INT = self.TEMPORALS_INT
		self.COUNTER_TEMPORALS_FLOAT = self.TEMPORALS_FLOAT
		self.COUNTER_TEMPORALS_BOOLEAN = self.TEMPORALS_BOOLEAN
		self.COUNTER_TEMPORALS_STRING = self.TEMPORALS_STRING

		self.COUNTER_GLOBALS_OBJECT = self.GLOBALS_OBJECT
		self.COUNTER_LOCALS_OBJECT = self.LOCALS_OBJECT
		self.COUNTER_TEMPORALS_OBJECT = self.TEMPORALS_OBJECT

		#Method that returns the virtual address available
	def getVirtualAddress(self, data_Type, scope):
		if scope == "temporal":
			if data_Type == "int":
				return self.COUNTER_TEMPORALS_INT
			elif data_Type == "float":
				return self.COUNTER_TEMPORALS_FLOAT
			elif data_Type == "bool":
				return self.COUNTER_TEMPORALS_BOOLEAN
			elif data_Type == "string":
				return self.COUNTER_TEMPORALS_STRING
			elif data_Type == "object":
				return self.COUNTER_TEMPORALS_OBJECT
		elif scope == "local":
			if data_Type == "int":
				return self.COUNTER_LOCALS_INT
			elif data_Type == "float":
				return self.COUNTER_LOCALS_FLOAT
			elif data_Type == "bool":
				return self.COUNTER_LOCALS_BOOLEAN
			elif data_Type == "string":
				return self.COUNTER_LOCALS_STRING
			elif data_Type == "object":
				return self.COUNTER_LOCALS_OBJECT
		elif scope == "global":
			if data_Type == "int":
				return self.COUNTER_GLOBALS_INT
			elif data_Type == "float":
				return self.COUNTER_GLOBALS_FLOAT
			elif data_Type == "bool":
				return self.COUNTER_GLOBALS_BOOLEAN
			elif data_Type == "string":
				return self.COUNTER_GLOBALS_STRING
			elif data_Type == "object":
				return self.COUNTER_GLOBALS_OBJECT
	
	#Method that updates the virtual addresses
	def updateVirtualAddress(self, data_Type, scope):
		if scope == "temporal":
			if data_Type == "int":
				self.COUNTER_TEMPORALS_INT += 1
			elif data_Type == "float":
				self.COUNTER_TEMPORALS_FLOAT += 1
			elif data_Type == "bool":
				self.COUNTER_TEMPORALS_BOOLEAN += 1
			elif data_Type == "string":
				self.COUNTER_TEMPORALS_STRING += 1
			elif data_Type == "object":
				self.COUNTER_TEMPORALS_OBJECT += 1
		elif scope == "local":
			if data_Type == "int":
				self.COUNTER_LOCALS_INT += 1
			elif data_Type == "float":
				self.COUNTER_LOCALS_FLOAT += 1
			elif data_Type == "bool":
				self.COUNTER_LOCALS_BOOLEAN += 1
			elif data_Type == "string":
				self.COUNTER_LOCALS_STRING += 1
			elif data_Type == "object":
				self.COUNTER_LOCALS_OBJECT += 1
		elif scope == "global":
			if data_Type == "int":
				self.COUNTER_GLOBALS_INT += 1
			elif data_Type == "float":
				self.COUNTER_GLOBALS_FLOAT += 1
			elif data_Type == "bool":
				self.COUNTER_GLOBALS_BOOLEAN += 1
			elif data_Type == "string":
				self.COUNTER_GLOBALS_STRING += 1
			elif data_Type == "object":
				self.COUNTER_GLOBALS_OBJECT += 1
	
	#Method that restarts counter for the local and temporal addresses 
	# every time it enters to a new function 
	def restartVirtualAddress(self):
		self.COUNTER_TEMPORALS_INT = self.TEMPORALS_INT
		self.COUNTER_TEMPORALS_FLOAT = self.TEMPORALS_FLOAT
		self.COUNTER_TEMPORALS_BOOLEAN = self.TEMPORALS_BOOLEAN
		self.COUNTER_TEMPORALS_STRING = self.TEMPORALS_STRING
		self.COUNTER_TEMPORALS_OBJECT = self.TEMPORALS_OBJECT
		self.COUNTER_LOCALS_INT = self.LOCALS_INT
		self.COUNTER_LOCALS_FLOAT = self.LOCALS_FLOAT
		self.COUNTER_LOCALS_BOOLEAN = self.LOCALS_BOOLEAN
		self.COUNTER_LOCALS_STRING = self.LOCALS_STRING
		self.COUNTER_LOCALS_OBJECT = self.LOCALS_OBJECT

