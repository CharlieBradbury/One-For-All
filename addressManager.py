from errorHandler import errorHandler

class addressManager():
	def __init__(self):

		self.errorHandler = errorHandler()

		#------------------------------------------------------
		# 	STATIC ADDRESSES
		#------------------------------------------------------
		self.MEMORY_BEGIN = 1000
		self.MEMORY_END = 32999

		self.BEGIN_GLOBALS = 1000
		self.GLOBALS_INT = 1000
		self.GLOBALS_FLOAT = 3000
		self.GLOBALS_BOOLEAN = 5000
		self.GLOBALS_STRING = 7000
		self.GLOBALS_OBJECT = 9000
		self.END_GLOBALS = 10999

		self.BEGIN_LOCALS = 11000
		self.LOCALS_INT = 11000
		self.LOCALS_FLOAT = 13000
		self.LOCALS_BOOLEAN = 15000
		self.LOCALS_STRING = 17000
		self.LOCALS_OBJECT = 19000
		self.END_LOCALS = 20999

		self.BEGIN_TEMPORALS = 21000
		self.TEMPORALS_INT = 23000
		self.TEMPORALS_FLOAT = 25000
		self.TEMPORALS_BOOLEAN = 27000
		self.TEMPORALS_STRING = 29000
		self.TEMPORALS_OBJECT = 31000
		self.END_TEMPORALS = 32999

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

	# Method that given an address direction, return to which segment belongs
	def getMemorySegment(self, stringAddress):
		# Parse address to int
		address = int(stringAddress)

		# Context and varType variables
		context = "NoContext"
		varType = "NoType"

		if self.BEGIN_GLOBALS <= address <= self.END_GLOBALS:
			context = "global"
			if self.GLOBALS_INT <= address < self.GLOBALS_FLOAT:
				varType = "int"
			elif self.GLOBALS_FLOAT <= address < self.GLOBALS_BOOLEAN:
				varType = "float"
			elif self.GLOBALS_BOOLEAN <= address < self.GLOBALS_STRING:
				varType = "boolean"
			elif self.GLOBALS_STRING <= address < self.GLOBALS_OBJECT:
				varType = "string"
			elif self.GLOBALS_OBJECT <= address <= self.END_GLOBALS:
				varType = "obj"
		elif self.BEGIN_LOCALS <= address <= self.END_LOCALS:
			context = "local"
			if self.LOCALS_INT <= address < self.LOCALS_FLOAT:
				varType = "int"
			elif self.LOCALS_FLOAT <= address < self.LOCALS_BOOLEAN:
				varType = "float"
			elif self.LOCALS_BOOLEAN <= address < self.LOCALS_STRING:
				varType = "boolean"
			elif self.LOCALS_STRING <= address < self.LOCALS_OBJECT:
				varType = "string"
			elif self.LOCALS_OBJECT <= address <= self.END_LOCALS:
				varType = "obj"
		elif self.BEGIN_TEMPORALS <= address <= self.END_TEMPORALS:
			context = "temporal"
			if self.TEMPORALS_INT <= address < self.TEMPORALS_FLOAT:
				varType = "int"
			elif self.TEMPORALS_FLOAT <= address < self.TEMPORALS_BOOLEAN:
				varType = "float"
			elif self.TEMPORALS_BOOLEAN <= address < self.TEMPORALS_STRING:
				varType = "boolean"
			elif self.TEMPORALS_STRING <= address < self.TEMPORALS_OBJECT:
				varType = "string"
			elif self.TEMPORALS_OBJECT <= address <= self.END_TEMPORALS:
				varType = "obj"
		else:
			self.error.definition(self.error.INVALID_MEMORY_ACCESS, stringAddress, None)

		memorySegment = [context, varType]
		return memorySegment
			
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
		elif scope == "local":
			if data_Type == "int":
				return self.COUNTER_LOCALS_INT
			elif data_Type == "float":
				return self.COUNTER_LOCALS_FLOAT
			elif data_Type == "bool":
				return self.COUNTER_LOCALS_BOOLEAN
			elif data_Type == "string":
				return self.COUNTER_LOCALS_STRING
		elif scope == "global":
			if data_Type == "int":
				return self.COUNTER_GLOBALS_INT
			elif data_Type == "float":
				return self.COUNTER_GLOBALS_FLOAT
			elif data_Type == "bool":
				return self.COUNTER_GLOBALS_BOOLEAN
			elif data_Type == "string":
				return self.COUNTER_GLOBALS_STRING
	
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
		elif scope == "local":
			if data_Type == "int":
				self.COUNTER_LOCALS_INT += 1
			elif data_Type == "float":
				self.COUNTER_LOCALS_FLOAT += 1
			elif data_Type == "bool":
				self.COUNTER_LOCALS_BOOLEAN += 1
			elif data_Type == "string":
				self.COUNTER_LOCALS_STRING += 1
		elif scope == "global":
			if data_Type == "int":
				self.COUNTER_GLOBALS_INT += 1
			elif data_Type == "float":
				self.COUNTER_GLOBALS_FLOAT += 1
			elif data_Type == "bool":
				self.COUNTER_GLOBALS_BOOLEAN += 1
			elif data_Type == "string":
				self.COUNTER_GLOBALS_STRING += 1

	# Method that returns type of operator
	def typeOfOperator(self, operator):
		typeOperator = "NoType"

		assignmentOperators = ["="]
		arithmeticOperators = ["+", "-", "*", "/"]
		relationalOperators = [">", ">=", "<", "<=", "==", "!="]
		logicalOperators = ["&&", "||"]

		if operator in assignmentOperators:
			typeOperator = "assignment"
		elif operator in arithmeticOperators:
			typeOperator = "arithmetic"
		elif operator in relationalOperators:
			typeOperator = "relational"
		elif operator in logicalOperators:
			typeOperator = "logical"

		return typeOperator