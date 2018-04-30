from addressManager import addressManager

class virtualMachine():
	def __init__(self):
		# Total of quadruples
		self.totalQuad = None
		# Counter of the current quads to execute and actual quad to execute
		self.counterQuad = 0
		self.exeQuadruple = None

		# Global memory (shared between all contexts), receives and object of type scopeManager
		self.globalMemory = None

		# Current memory (changes depending on the context), receives and object of type scopeManager
		self.currentMemory = None

		self.adManager = addressManager()

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
	def getValueAt(self, constantOrAddress, resultAddress, operator=None):

		#print("Cur", constantOrAddress, resultAddress, operator)

		if(constantOrAddress[0] == "&"):
			# Then its an address, we need to search for it in the proper variable table
			address = constantOrAddress.replace("&", "")
			context = self.currentMemory.adManager.getMemorySegment(address)[0]

			foundVariable = None

			if context == "global":
				# Search for that id in globalMemory
				foundVariable = self.globalMemory.searchGlobalAddress(address)
			elif context == "local":
				# Search for that id in localMemory
				foundVariable = self.currentMemory.searchLocalAddress(address)
			elif context == "temporal":
				# Search for that id in temporalMemory
				foundVariable = self.currentMemory.searchTemporalAddress(address)
			return foundVariable
		else:
			# If not, then is a constant and we can return such value
			cleanResult = self.parseConstant(constantOrAddress, resultAddress, operator)
			return cleanResult
		
	# Receives a value and an address to save that result at
	def saveResultAt(self, result, address):

		if(address[0] == "&"):
			# Then its an address, we need to search for it in the proper variable table
			address = address.replace("&", "")

			segmentString = self.currentMemory.adManager.getMemorySegment(address)[0]

			if segmentString == "global":
				# Save the result in global memory
				self.globalMemory.saveResultGlobal(result, address)
			elif segmentString == "local":
				# Save the result in local memory
				self.currentMemory.saveResultLocal(result, address)
			elif segmentString == "temporal":
				# Save the result in temporal memory
				self.currentMemory.saveResultTemporal(result, address)

	def executeInstructions(self, quadruples):
		self.totalQuad = len(quadruples)

		lastAddress = None

		while self.counterQuad < self.totalQuad:
			# Obtain quadruple to execute and the operator
			exeQuadruple = quadruples[self.counterQuad]
			leftOpd = exeQuadruple.opd1
			rightOpd = exeQuadruple.opd2
			operator = exeQuadruple.opt
			resultAddress = exeQuadruple.result


			# ARITHMETIC OPERATORS
			if operator == '+':
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

			# Increase counter by 1
			self.counterQuad += 1
			if self.counterQuad == self.totalQuad:
				lastAddress = resultAddress

		# Print result at last quadruple
		finalResult = self.getValueAt(lastAddress, lastAddress)
		print("FINAL RESULT:", finalResult)