from addressManager import addressManager
from scopeManager import scopeManager
from quadruples import quadruples
import copy

class virtualMachine():
	def __init__(self, nameOfFile):

		#------------------------------------------------------
		# 	QUADRUPLES
		#------------------------------------------------------
		# List of quadruples and current quad to execute
		self.quadruples = []
		self.exeQuadruple = None

		# Counter of quads and total quads
		self.counterQuad = 1
		self.counterTotalQuads = None

		#------------------------------------------------------
		# 	SCOPES
		#------------------------------------------------------
		# Current memory (changes depending on the context) an address manager
		self.currentScope = scopeManager("global")
		self.adManager = addressManager()
		
		# For managing multipe contexts
		self.contextStack = []

		#------------------------------------------------------
		# 	JUMPS AND RETURNS
		#------------------------------------------------------
		# For managing jumps caused by goto, gotof, gosub and return
		self.jumpReturnStack = []
		# For managing parameters to be returned in routines
		self.returnStack = []
		
		#------------------------------------------------------
		# 	ARRAYS
		#------------------------------------------------------
		# Array stack
		self.offSetStack = []

		#------------------------------------------------------
		# 	CLASSES
		#------------------------------------------------------
		# List of classes, which saves scopes for classes
		self.registeredClasses = dict()

		#------------------------------------------------------
		# 	NAME OF FILE TO READ
		#------------------------------------------------------
		# Name of file to read
		self.nameOfFile = nameOfFile
	
	# Method that runs .obj file
	def run(self):
		lines = [line.rstrip('\n') for line in open(self.nameOfFile)]

		for stringQuad in lines:
			listQuad = stringQuad.split(" ")
			newQuad = quadruples(listQuad[0], listQuad[1], listQuad[2], listQuad[3], listQuad[4])
			self.quadruples.append(newQuad)

		# Prints quads and executes instructions
		#self.printQuadruples()
		self.executeInstructions()

		# Print list of classes for validation
		#for nameOfClass, classContext in self.registeredClasses.items():
		#	print ("ESTO ES UNA CLASE REGISTRADA", nameOfClass)

	# Prints quadruples
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
				if self.currentScope.isArrayGlobal(address)  or self.currentScope.isArrayLocal(address):
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
			
			memorySegment = self.currentScope.adManager.getMemorySegment(address)

			context = memorySegment[0]
			name_type = memorySegment[1]

			if context == "global":
				if self.currentScope.isArrayGlobal(address):
					# Retrieve array number
					offSet = self.offSetStack.pop()
				# Save the result in global memory
				self.currentScope.saveResultGlobal(result, address, name_type, offSet)
			elif context == "local":
				if self.currentScope.isArrayLocal(address):
					# Retrieve array number
					offSet = self.offSetStack.pop()
				# Save the result in global memory
				self.currentScope.saveResultLocal(result, address, name_type, offSet)
			elif context == "temporal":
				# Save the result in temporal memory
				self.currentScope.saveResultTemporal(result, address, name_type)


	def executeInstructions(self):

		self.counterTotalQuads = len(self.quadruples)

		lastAddress = None

		while self.counterQuad <= self.counterTotalQuads:

			# Obtain quadruple to execute and the operator
			exeQuadruple = self.quadruples[self.counterQuad - 1]
			leftOpd = exeQuadruple.opd1
			rightOpd = exeQuadruple.opd2
			operator = exeQuadruple.opt
			resultAddress = exeQuadruple.result

			print(self.counterQuad, operator, leftOpd, rightOpd, resultAddress)

			#------------------------------------------------------
			# 	ASSIGNMENT
			#------------------------------------------------------
			if operator == '=':
				# Retrieve only left value of quadruple, and save it in result
				leftValue = self.getValueAt(leftOpd, resultAddress, operator)
				self.saveResultAt(leftValue, resultAddress)
			#------------------------------------------------------
			# 	ARITHMETHIC OPERATORS
			#------------------------------------------------------
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
			#------------------------------------------------------
			# 	RELATIONAL OPERATORS
			#------------------------------------------------------
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
			#------------------------------------------------------
			# 	LOGICAL OPERATORS
			#------------------------------------------------------
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
			#------------------------------------------------------
			# 	CONDTIONAL OPERATORS
			#------------------------------------------------------
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
			#------------------------------------------------------
			# 	MODULE OPERATORS
			#------------------------------------------------------
			elif operator == 'ERA':
				# Save current context
				self.contextStack.append(self.currentScope)

				# Create new context
				nameOfFunction = str(resultAddress)
				self.currentScope = scopeManager(nameOfFunction, self.currentScope.globalMemory)
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
				previousScope.globalMemory = self.currentScope.globalMemory

				self.currentScope = previousScope

				# After changing context, we assign the result
				self.saveResultAt(resultOfFunction, whereToSaveResult)

				# Then, we can move the pointer back to where we were
				previousPointer = self.jumpReturnStack.pop()
				self.counterQuad = previousPointer
			elif operator == "MAIN":
				mainContext = scopeManager("main", self.currentScope.globalMemory)
				self.contextStack.append(mainContext)

			#------------------------------------------------------
			# 	ARRAY OPERATORS
			#------------------------------------------------------
			elif operator == 'ARRAY_POS':
				offSetValue = self.getValueAt(resultAddress, None, operator)
				self.offSetStack.append(offSetValue)
			# ARRAY OPERATORS
			elif operator == 'ARRAY_DECLARE':
				# Create array
				self.saveResultAt(None, resultAddress, int(leftOpd))
			#------------------------------------------------------
			# 	READ/WRITE OPERATORS
			#------------------------------------------------------	
			elif operator == 'WRITE':
				result = self.getValueAt(resultAddress)
				print(result)
			elif operator == 'END_WRITE':
				pass
			elif operator == 'READ':
				leftValue = self.getValueAt(leftOpd)
				self.saveResultAt(leftValue, resultAddress)
			#------------------------------------------------------
			# 	CLASS OPERATORS
			#------------------------------------------------------
			elif operator == "BEGIN_CLASS":
				# Create new context for this class and save it in dictionary
				nameOfClass = str(resultAddress)
				newClassContext = scopeManager(nameOfClass, self.currentScope.globalMemory)
				
				# Insert current class in contextStack
				self.contextStack.append(self.currentScope)

				# Replace current class
				self.currentScope = newClassContext
			elif operator == "END_CLASS":
				# Pop class from contextStack
				updatedContext = self.contextStack.pop()
				updatedContext.globalMemory = self.currentScope.globalMemory

				# Replace current scope
				self.currentScope = updatedContext
			elif operator == "CREATE_OBJ":
				# Create new context for such object

				nameOfObject = rightOpd
				newObjectContext = scopeManager(nameOfObject, self.currentScope.globalMemory)

				# Save a value in object memory representing such object
				self.saveResultAt(nameOfObject, resultAddress)

				# Insert current object in current class context
				self.registeredClasses[nameOfObject] = newObjectContext
				self.contextStack.append(self.currentScope)

				# Replace current class
				self.currentScope = newObjectContext

			elif operator == "END_OBJ":
				# Pop class from contextStack
				updatedContext = self.contextStack.pop()
				updatedContext.globalMemory = self.currentScope.globalMemory

				# Update on registeredClasses
				nameOfClass = self.currentScope.scopeName
				self.registeredClasses[nameOfClass] = copy.copy(self.currentScope)

				# Replace current scope
				self.currentScope = updatedContext


			elif operator == "ATTR":

				# Save the value of the object in the current context which is of the
				# class currently being intiliazed
				leftValue = self.getValueAt(leftOpd, resultAddress)
				self.saveResultAt(leftValue, resultAddress)
				
			elif operator == "ACCESS_OBJ":

				# First, retrieve name of the object being referred
				nameOfObject = self.getValueAt(leftOpd)
				# Then, retrive such context from registeredClasses and change contexts
				classContext = self.registeredClasses[nameOfObject]
				classContext.globalMemory = self.currentScope.globalMemory
				self.contextStack.append(self.currentScope)
				self.currentScope = classContext

				# Once context has been changed, retrive value
				valueOfAttribute = self.getValueAt(rightOpd)

				# Go back to previous context again
				updatedContext = self.contextStack.pop()
				updatedContext.globalMemory = self.currentScope.globalMemory
				nameOfObject = self.currentScope.scopeName
				self.registeredClasses[nameOfObject] = copy.copy(self.currentScope)

				# Replace current scope
				self.currentScope = updatedContext
				# Save value retrieved from class context
				self.saveResultAt(valueOfAttribute, resultAddress)

			#------------------------------------------------------
			# 	INCREASE POINTER TO NEXT QUADRUPLES
			#------------------------------------------------------
			# Increase counter by 1
			self.counterQuad += 1

	def printMemory(self):
		print("=====SCOPE=====", self.currentScope.scopeName)
		print("GLOBAL MEMORY")
		self.currentScope.globalMemory.printDirectory()
		print("LOCAL MEMORY")
		self.currentScope.localMemory.printDirectory()
		print("TEMPORAL MEMORY")
		self.currentScope.temporalMemory.printDirectory()