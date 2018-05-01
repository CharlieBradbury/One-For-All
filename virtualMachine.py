from addressManager import addressManager

class virtualMachine():
	def __init__(self):
		# Total of quadruples
		self.totalQuad = None
		# Counter of the current quads to execute and actual quad to execute
		self.counterQuad = 1
		self.exeQuadruple = None

		# Current memory (changes depending on the context), receives and object of type scopeManager
		self.currentScope = None

		self.adManager = addressManager()

		# For managing jumps caused by goto, gotof, gosub and return
		self.jumpStack = []

	def parseVariable(self, variable):
		variableType = variable.data_type;
		variableUnparsedValue = variable.value;
		parsedValue = None

		if variableType == "int" :
			parsedValue = int(variableUnparsedValue)
		elif variableType == "float" :
			parsedValue = float(variableUnparsedValue)
		elif variableType == "bool" :
			parsedValue = bool(variableUnparsedValue)
		elif variableType == "string" :
			parsedValue = variableUnparsedValue

		return parsedValue

	# Parse a constant (in string form from quadruple) into an actual value
	# of type. Result address and operator are used as extra info in trying to determine
	# the value of constantString, specially in the case of relational comparitions
	def parseConstant(self, constantString, resultAddress, operator):
		parsedValue = None

		if constantString[0] == "\"":
			# Then is a string
			parseValue = constantString
		else:
			# Get type of operator and of the result (based on its address number)
			operatorType = self.adManager.typeOfOperator(operator)
			resultType = self.adManager.getMemorySegment(resultAddress.replace("&", ""))[1]

			if resultType == "int":
				parsedValue = int(constantString)
			elif resultType == "float":
				parsedValue = float(constantString)
			elif resultType == "boolean":
				# If the result is boolean, then check if the operand is equal to the internal
				# representation of true and false inside the compiler. If it matches the
				# representation, then the matched value is equal to the value compared to True
				if constantString in ["True", "False"]:
					parsedValue = (constantString == "True")
				else:
					# At this point the constant is nor a string or boolean, then it means is 
					# int/float used in a relational operation, so we can parse it as float
					parsedValue = float(constantString)

		return parsedValue

	# Value that receives as parameter an address (identified with an &) or a
	# constant (without &) and returns its value. If receives a constant, it just returns
	# such value. If it receives an address, it searchs for the value of that address
	# in the memory of the current context.
	def getValueAt(self, constantOrAddress, resultAddress=None, operator=None):

		constantOrAddress = str(constantOrAddress)
		if(constantOrAddress[0] == "&"):
			# Then its an address, we need to search for it in the proper variable table
			address = constantOrAddress.replace("&", "")
			context = self.currentScope.adManager.getMemorySegment(address)[0]
			foundVariable = None

			if context == "global":
				# Search for that id in globalMemory
				foundVariable = self.currentScope.searchGlobalAddress(address)
			elif context == "local":
				# Search for that id in localMemory
				foundVariable = self.currentScope.searchLocalAddress(address)
			elif context == "temporal":
				# Search for that id in temporalMemory
				foundVariable = self.currentScope.searchTemporalAddress(address)
			return foundVariable
		else:
			# If not, then is a constant and we can return such value
			cleanResult = self.parseConstant(constantOrAddress, resultAddress, operator)
			return cleanResult
		
	# Receives a value and an address to save that result at
	def saveResultAt(self, result, address):	

			# Then its an address, we need to search for it in the proper variable table
			address = address.replace("&", "")
			context = self.currentScope.adManager.getMemorySegment(address)[0]

			if context == "global":
				# Save the result in global memory
				self.currentScope.saveResultGlobal(result, address)
			elif context == "local":
				# Save the result in local memory
				self.currentScope.saveResultLocal(result, address)
			elif context == "temporal":
				# Save the result in temporal memory
				self.currentScope.saveResultTemporal(result, address)

	def executeInstructions(self, quadruples):
		self.totalQuad = len(quadruples)

		lastAddress = None

		while self.counterQuad <= self.totalQuad:
			# Obtain quadruple to execute and the operator
			exeQuadruple = quadruples[self.counterQuad - 1]
			leftOpd = exeQuadruple.opd1
			rightOpd = exeQuadruple.opd2
			operator = exeQuadruple.opt
			resultAddress = exeQuadruple.result

			# ASSIGNMENT OPERATOR
			if operator == '=':
				# Retrieve only left value of quadruple, and save it in result
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				self.saveResultAt(leftValue, resultAddress)
			# ARITHMETIC OPERATORS
			elif operator == '+':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue + rightValue, resultAddress)				
			elif operator == '-':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue - rightValue, resultAddress)	
			elif operator == '*':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue * rightValue, resultAddress)
			elif operator == '/':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue / rightValue, resultAddress)
			# RELATIONAL OPERATORS
			elif operator == '>':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue > rightValue, resultAddress)
			elif operator == '>=':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue >= rightValue, resultAddress)
			elif operator == '<':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue < rightValue, resultAddress)
			elif operator == '<=':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)	
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue <= rightValue, resultAddress)
			elif operator == '==':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue == rightValue, resultAddress)
			elif operator == '!=':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue != rightValue, resultAddress)
			# LOGICAL OPERATORS	
			elif operator == '&&':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue and rightValue, resultAddress)
			elif operator == '||':
				# Retrive values of both operands, and save result and resultAddress
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				rightValue = self.getValueAt(rightOpd, resultAddress, operator)
				self.saveResultAt(leftValue or rightValue, resultAddress)
			# CONDITIONAL OPERATORS
			elif operator == 'Goto':
				# Save the quad that we need to comeback later (which is the current + 1)
				self.jumpStack.append(self.counterQuad);
				# Change the current counterQuad to the resultAddress - 1, which in this case is
				# just a number of quadruple. (E.g. 64). Compensate because of increment at the end.
				self.counterQuad = resultAddress - 1
			elif operator == 'GotoF':
				# Retrieve value at leftoperator and check if its true
				leftValue = self.getValueAt(leftOpd)
				# Change the current counterQuad to the resultAddress only is is false
				if not leftValue:
					self.counterQuad = resultAddress - 1
			elif operator == 'END':
				pass

			# Increase counter by 1
			self.counterQuad += 1

		# Print result at last quadruple
		print("solo funciona para test01.txt porque abajo hardcodeo el acceso a la temporal")
		finalResult = self.getValueAt('&11000', '&11000')
		print("FINAL RESULT:", lastAddress, finalResult)
