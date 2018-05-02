from addressManager import addressManager
from scopeManager import scopeManager
from quadruples import quadruples
import copy

class virtualMachine():
	def __init__(self, nameOfFile):
		# Total of quadruples
		self.totalQuad = None
		# Counter of the current quads to execute and actual quad to execute
		self.counterQuad = 1
		self.exeQuadruple = None

		# Current memory (changes depending on the context), receives and object of type scopeManager
		self.currentScope = currentScope = scopeManager("local")

		self.adManager = addressManager()

		# For managing jumps caused by goto, gotof, gosub and return
		self.jumpStack = []
		# For managing parameters to be returned in routines
		self.returnStack = []

		self.jumpReturnStack = []

		# For managing multipe contexts
		self.contextStack = []

		# Array stack
		self.offSetStack = []

		# Print list
		self.printList = []

		# List of quadruples
		self.quadruples = []

		# Name of file to read
		self.nameOfFile = nameOfFile
	
	def run(self):
		lines = [line.rstrip('\n') for line in open(self.nameOfFile)]

		for stringQuad in lines:
			listQuad = stringQuad.split(" ")
			newQuad = quadruples(listQuad[0], listQuad[1], listQuad[2], listQuad[3], listQuad[4])
			self.quadruples.append(newQuad)

		self.printQuadruples()
		self.executeInstructions()


	def printQuadruples(self):
		counter = 1;
		for quad in self.quadruples:
			
			leftOpd = quad.opd1
			rightOpd = quad.opd2
			operator = quad.opt
			resultAddress = quad.result
			print(counter, operator, leftOpd, rightOpd, resultAddress)
			counter += 1
			
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
	def parseConstantWithOperator(self, constantString, resultAddress, operator):
		parsedValue = None

		if constantString[0] == "\"":
			# Then is a string
			parsedValue = constantString
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

	def parseConstant(self, constantString, resultAddress=None):

		
		if constantString[0] == "\"":
			# Then is a string
			parsedValue = constantString
		else:
			# Get type of operator and of the result (based on its address number)
			resultType = self.adManager.getMemorySegment(resultAddress.replace("&", ""))[1]

			if resultType == "int":
				parsedValue = int(constantString)
			elif resultType == "float":
				parsedValue = float(constantString)
			elif resultType == "boolean":
				if constantString in ["True", "False"]:
					parsedValue = (constantString == "True")

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
				# Search for that id in globalMemory	i
				foundVariable = self.currentScope.searchGlobalAddress(address)
			elif context == "local":
				# Search for that id in localMemory
				foundVariable = self.currentScope.searchLocalAddress(address)
			elif context == "temporal":
				# Search for that id in temporalMemory
				foundVariable = self.currentScope.searchTemporalAddress(address)

			valueToReturn = None

			if foundVariable is not None:
				if self.currentScope.isArrayGlobal(address):
					offSet = self.offSetStack.pop()
					valueToReturn = foundVariable.value[offSet]
				else:
					valueToReturn = foundVariable.value

			return valueToReturn
		elif operator == 'ARRAY_POS':
			cleanResult = int(constantOrAddress)
			return cleanResult
		elif operator is not None:
			# If not, then is a constant and we can return such value
			cleanResult = self.parseConstantWithOperator(constantOrAddress, resultAddress, operator)
			return cleanResult
		else:

			cleanResult = self.parseConstant(constantOrAddress, resultAddress)
			return cleanResult
		
	# Receives a value and an address to save that result at
	def saveResultAt(self, result, address, offSet=-1):	
			# Then its an address, we need to search for it in the proper variable table
			address = address.replace("&", "")
			context = self.currentScope.adManager.getMemorySegment(address)[0]
	
			if context == "global":
				if self.currentScope.isArrayGlobal(address):
					# Retrieve array number
					offSet = self.offSetStack.pop()
				# Save the result in global memory
				self.currentScope.saveResultGlobal(result, address, offSet)
			elif context == "local":
				# Save the result in local memory
				self.currentScope.saveResultLocal(result, address)
			elif context == "temporal":
				# Save the result in temporal memory
				self.currentScope.saveResultTemporal(result, address)


	def executeInstructions(self):

		self.totalQuad = len(self.quadruples)

		lastAddress = None

		while self.counterQuad <= self.totalQuad:

			# Obtain quadruple to execute and the operator
			exeQuadruple = self.quadruples[self.counterQuad - 1]
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
				# Change the current counterQuad to the resultAddress - 1, which in this case is
				# just a number of quadruple. (E.g. 64). Compensate because of increment at the end.
				self.counterQuad = int(resultAddress) - 1
			elif operator == 'GotoF':	

				leftValue = self.getValueAt(leftOpd)
				
				# Change the current counterQuad to the resultAddress only is is false
				if leftValue is False:
					self.counterQuad = int(resultAddress) - 1
			elif operator == 'END':
				pass
			# MODULE OPERATORS
			elif operator == 'ERA':
				# Save current context
				self.contextStack.append(self.currentScope)

				# Create new context
				self.currentScope = scopeManager("local")
			elif operator == 'PARAM':

				# The adress here is the adress in which we need to save the leftValue
				# However, first we need to search the leftoperand in the previous context
				contextToComeback = copy.copy(self.currentScope)
				previousContext = copy.copy(self.contextStack[-1])

				# Search for that value in previous context
				self.currentScope = previousContext
				# We pass resultAdress just as reference
				leftValue = self.getValueAt(leftOpd, resultAddress)

				# Change context again and save it in this context
				self.currentScope = contextToComeback
				self.saveResultAt(leftValue, resultAddress)
			elif operator == 'RETURN_ASSIGN':
				# Save address in which we will save, this address corresponds
				# to the context that called the function
				self.returnStack.append(resultAddress)
			elif operator == 'GOSUB':
				# Save the quad that we need to comeback later (which is the current)
				self.jumpReturnStack.append(self.counterQuad);
				# Change quad to the jump
				self.counterQuad = int(resultAddress) - 1

			elif operator == 'RETURN':
				# First, we need to obtain where to save
				whereToSaveResult = self.returnStack.pop()	

				# We obtain the value of the current function
				resultOfFunction = self.getValueAt(resultAddress, whereToSaveResult)


				# Then we change context
				previousScope = self.contextStack.pop()
				self.currentScope = previousScope

				# After changing context, we assign the result
				self.saveResultAt(resultOfFunction, whereToSaveResult)

				# Then, we can move the pointer back to where we were
				previousPointer = self.jumpReturnStack.pop()
				self.counterQuad = previousPointer
			elif operator == 'ARRAY_POS':
				offSetValue = self.getValueAt(resultAddress, None, operator)
				self.offSetStack.append(offSetValue)
			elif operator == 'ARRAY_DECLARE':
				# Create array
				self.saveResultAt(None, resultAddress, int(leftOpd))
			elif operator == 'WRITE':
				result = self.getValueAt(resultAddress)
				print(result)
			elif operator == 'END_WRITE':
				pass
			elif operator == 'READ':
				leftValue = self.getValueAt(leftOpd)
				self.saveResultAt(leftValue, resultAddress)

			# Increase counter by 1
			self.counterQuad += 1

	def printMemory(self):
		print("GLOBAL MEMORY")
		self.currentScope.globalMemory.printDirectory()
		print("LOCAL MEMORY")
		self.currentScope.localMemory.printDirectory()
		print("TEMPORAL MEMORY")
		self.currentScope.temporalMemory.printDirectory()