'''
import sys
from antlr4 import *
from collections import OrderedDict
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parser.one_for_allLexer import one_for_allLexer
from parser.one_for_allParser import one_for_allParser
from parser.one_for_allListener import one_for_allListener

from objFunction import objFunction
from objVariable import objVariable
from objClass import *
from variableDirectory import variableDirectory
from functionDirectory import functionDirectory
from classDirectory import classDirectory


from quadruples import quadruples
from semanticCube import semanticCube
from scopeManager import scopeManager
from addressManager import addressManager
from virtualMachine import virtualMachine
from errorHandler import errorHandler
'''

import sys
from antlr4 import *
from collections import OrderedDict
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener

from objFunction import objFunction
from objVariable import objVariable
from classVariable import classVariable
from objectO import objectO
from classMethod import *
from objClass import objClass
from variableDirectory import variableDirectory
from functionDirectory import functionDirectory
from classDirectory import classDirectory
from objectDirectory import objectDirectory


from quadruples import quadruples
from semanticCube import semanticCube
from scopeManager import scopeManager
from addressManager import addressManager
from virtualMachine import virtualMachine
from errorHandler import errorHandler

class ruleManager(one_for_allListener):

	#------------------------------------------------------
	# 	RULE MANAGER INITIALIZATION
	#------------------------------------------------------
	def __init__(self):

		#------------------------------------------------------
		# 	INITIALIZATION - MEMORY DIRECTIONS
		#------------------------------------------------------

		# Starting IDCounter at 0
		self.IDCounter = 0

		# Counter for quadruples
		self.counter = 1

		#Object that handles all memory directions
		self.addressManager = addressManager()
		#------------------------------------------------------
		# 	INITIALIZATION - CLASS, FUNCTIONS AND VARIABLES
		#------------------------------------------------------

		# Class Directory
		self.classDirectory = classDirectory()

		# Function directory
		self.funcDirectory = functionDirectory()

		# Variable Directory
		self.varDirectory = variableDirectory()

		# Object Directory 
		self.objects = objectDirectory()

		# Current class (Type: objClass)
		self.currentClass = None

		#Scope for assigning addresses
		self.currentScope = ("global", None)

		# Boolean to check if reading a class, if reading a method
		# and if the current var/method is public
		self.isPartOfClass = False
		self.isPublic = False

		#Object that manages errors
		self.error = errorHandler()

		#------------------------------------------------------
		# 	INITIALIZATION - QUADRUPLES
		#------------------------------------------------------
		self.cube = semanticCube()
		self.quadruplesList = []

		# Operands stack
		self.opdStack = []

		# Operators stack
		self.optStack = []

		# Jumps stack
		self.jumpStack = []

		#Variable stack for declaring and assigning values
		self.variableStack = []

		#Stack for managing func types for returns
		self.funcStack = []
		self.returnType = None
		self.parameterStack = []
		self.FunctionId = None

		#Stack for storing parameters for the initialization of objects
		self.initStack = []
		self.initEvalStack = []
	
		#Global variable to identify objects
		self.isObject = False

		self.nameOfFile = "program.ofa"

	#------------------------------------------------------
	# 	CLASS, FUNCTIONS AND VARIABLES
	#-----------------------------------------------------

	def enterNeuro_jump_main(self, ctx):
		#------------------------------------------------------
		#	CREATE FIRST QUADRUPLE
		#   Goto to the main method
		#-----------------------------------------------------
		self.generatesQuadruple('Goto', None, None, None)
		self.jumpStack.append(('Main', self.counter - 1))

	def enterMain(self, ctx):
		self.currentScope = ("local", "main")
		#Re-start virtual addresses for the local and temporal scope
		self.addressManager.restartVirtualAddress()
		#Create first Goto
		main = self.jumpStack.pop()[1]
		self.fillQuadruple(main,self.counter)

		#Register main function
		self.createAddRoutine("main", "int", None)

	def enterClasses(self, ctx):
		self.isPartOfClass = True

	def enterClass_definition(self, ctx):
		# Create new class just with the ID and name of the class
		# This will set current class to the recently created class
		className = ctx.TOK_ID().getText()
		self.currentScope = ("local",className)
		self.createEmptyClass(className)

	def enterClass_public(self, ctx):
		try:
			# Setting values of public and class booleans
			self.isPublic = True
			# If there are no functions in the current context, then we are reading variables and this boolean should be false
		except:
			print("Error while reading public token, not possible to know if reading variable or method")
			sys.exit()

	def enterClass_private(self, ctx):
		try:
			# Setting values of private and class booleans
			self.isPublic = False
			# If there are no functions in the current context, then we are reading variables and this boolean should be false
		except:
			print("Error while reading private token, not possible to know if reading variable or method")
			sys.exit()

	def exitVariable_definition(self, ctx):
		try:
			size = 1
			# Obtain type and names of the single or multiple variables associated to that type
			# E.g: public var int a1, a2;
			currentType = ctx.data_type().getText()

			if self.verifyType(currentType) is False:
				#Throw error 
				print("Invalid data type")
				sys.exit()

			currentVariables = ctx.TOK_ID()

			if ctx.TOK_RBRACKET():
				dim = 1
				size = self.opdStack[-1][0]

				if int(size) > 1:
					addressToSave = self.addressManager.getVirtualAddress(currentType, self.currentScope[0])
					self.generatesQuadruple('ARRAY_DECLARE', size, None, '&'+str(addressToSave))
			else:
				dim = 0

			try:
				if not self.isObject:
					#If it's not registered in class directory then is a normal variable
					for var in currentVariables:
						#Create variable object
						newVariable = self.createAddVariable(var.getText(), currentType, dim, size)
				else:
					for var in currentVariables:
						newVariable = self.createAddVariable(var.getText(), currentType, dim, size)
			except:
				self.error.definition(self.error.VARIABLE_CREATION, '', '')

		except:
			pass

	def enterVariable_assign(self, ctx):
		try:
			# Obtain type and names of the single or multiple variables associated to that type
			# E.g: public var int a1, a2;
			currentType = ctx.data_type().getText()
			currentVariables = ctx.TOK_ID()

			if ctx.TOK_RBRACKET():
				dim = 1
				size = self.opdStack[-1]
			else:
				dim = 0

			try:
				# For each name, create an object variable with such information
				for var in currentVariables:
					#Create object
					newVariable = self.createAddVariable(var.getText(), currentType, dim)
					self.variableStack.append(var.getText())
			except:
				self.error.definition(self.error.VARIABLE_CREATION, '', '')

		except:
			pass

	def enterRoutine_definition(self, ctx):
		# Obtain type and name of routine to be created
		routineName = ctx.TOK_ID().getText()
		routineType = ctx.data_type().getText()

		# Change context to local
		self.currentScope = ("local", routineName)

		#Re-start virtual addresses for the local and temporal scope
		self.addressManager.restartVirtualAddress()

		# List of parameters
		routineParameters = []

		try:
			# Obtain parameters, this case is for the first parameter, in case there is one
			paramName = ctx.parameters().TOK_ID().getText()
			paramType =  ctx.parameters().data_type().getText()

			#Create object variable for each parameter, always assume is a non array variable
			tempParam = objVariable(self.addressManager.getVirtualAddress(paramType,self.currentScope[0]), paramName, paramType, 1, 0)
			self.addressManager.updateVirtualAddress(paramType,self.currentScope[0])
			routineParameters.append(tempParam)

		except:
			pass

		try:
			countParameters = 0

			# Read parameters that go after the comma of the first one
			while ctx.parameters().parameters_recursive() is not None:
				# Counter for recursive parameters, this is used for accesing parameters that go after the first one
				paramType = ctx.parameters().parameters_recursive().data_type(countParameters).getText()
				paramName = ctx.parameters().parameters_recursive().TOK_ID(countParameters).getText()
 				#Always assume is a non array variable
				tempParam = objVariable(self.addressManager.getVirtualAddress(paramType,self.currentScope[0]), paramName, paramType, 1, 0)
				self.addressManager.updateVirtualAddress(paramType,self.currentScope[0])
				routineParameters.append(tempParam)
				countParameters += 1
		except:
			pass

		try:
			# Create routine
			self.createAddRoutine(routineName, routineType, routineParameters)
		except:
			print("Error while creating new routine")
			sys.exit()

	def exitRoutines(self, ctx):
		# Change context to global
		self.currentScope = ("global",None)

	def enterNeuro_array(self, ctx):
		pass

	def exitClass_definition(self, ctx):
		# Call method to add finished class to the class directory
		self.addFinishedClass(self.currentClass)

		# Resetting context variables
		self.isPublic = False
		self.currentClass = None

	def exitClasses(self, ctx):
		# Reset part of class boolean
		self.isPartOfClass = False
		self.currentScope = ("global",None)
		self.generatesQuadruple("ENDCLASS", None, None, None)

	def exitRestOfProgram(self, ctx):
		self.generatesQuadruple('END',None, None, None)
		#self.printQuadruples()
		'''
		print("------GLOBAL VARIABLES-----")
		for key, var in self.varDirectory.directory.items():
			var.printVariable()
		print("--------FUNCTIONS--------")
		for key, func in self.funcDirectory.directory.items():
			func.printFunction()
			func.localVars.printDirectory()
		'''

		self.printClassDictionary()
		self.objects.printDirectory()

		# Create text file with quadruples
		file = open(self.nameOfFile, "w")
		for quadruple in self.quadruplesList:
			quadString = (str(quadruple.id), str(quadruple.opt), str(quadruple.opd1), str(quadruple.opd2), str(quadruple.result))
			separator = " "
			stringComplete = separator.join(quadString)
			file.write(stringComplete + '\n')
		file.close() 

	#------------------------------------------------------
	# QUADRUPLES
	#------------------------------------------------------

	def exitAssignment(self,ctx):
		#Consult name of the variable that its going to be assigned
		name = ctx.id_().getText()
		isArray = False


		# Check if is an array
		if "[" in name:
			beginArrayPos = name.find("[")
			arrayName = name[:beginArrayPos]
			name = arrayName
			isArray = True

		#IF IT DOES NOT FIND THE VARIABLE IN LOCAL TRY IN GLOBAL
		#Verify that the name exists in the variable table
		variable = ''
		#Verify that the name exists in the variable table
		try:
			if self.currentScope[0] == "local":
				variables = self.funcDirectory.getAddressFunction(self.currentScope[1])
				variable = variables.getVariableDirectory().getVariableByName(name)

			if variable is None or self.currentScope[0] == "global" :
				variable = self.varDirectory.getVariableByName(name)

			elif variable is None:
				self.error.definition(self.error.VARIABLE_NOT_DEFINED, name, None)

			val = self.opdStack.pop()
			#Create quadruple

			self.generatesQuadruple('=',val, variable, None)
		except:
			sys.exit()

	def exitEvaluate_array(self, ctx):
		result = self.opdStack.pop()
		self.generatesQuadruple('ARRAY_POS', result, result, None)

	def exitVariable_assign(self, ctx):
		#Can declare and assign values to multiple variables
		while self.variableStack:
			#Get the name of the variable
			name = self.variableStack.pop()
			variable = ''

			#Verify that the name exists in the variable table
			try:
				if self.currentScope[0] == "local":
					variables = self.funcDirectory.getAddressFunction(self.currentScope[1])
					variable = variables.getVariableDirectory().getVariableByName(name)

				if variable is None or self.currentScope[0] == "global" :
					variable = self.varDirectory.getVariableByName(name)

				elif variable is None:
					self.error.definition(self.error.VARIABLE_NOT_DEFINED, name, None)
				val = self.opdStack.pop()
				#Create quadruple
				self.generatesQuadruple('=',val, variable, None)
			except:
				pass

	def exitRoutine_definition(self, ctx):
		#Check if the val matches type of the function
		function = self.funcStack.pop()

	def exitReturn_expr(self, ctx):
		#Get the value of the expression
		val = self.opdStack.pop()

		#Generate quadruple
		self.generatesQuadruple('RETURN', None, None, val)

	def enterToken_and(self, ctx):
		self.optStack.append(ctx.getText())
		
	def enterToken_or(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_same(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_different(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_greater(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_greater_eq(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_less(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_less_eq(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_plus(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_minus(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_multiplication(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_division(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_lparen(self, ctx):
		self.optStack.append(ctx.getText())

	def enterToken_rparen(self, ctx):
		if self.optStack[-1] == "(":
			self.optStack.pop()
		else:
			print("Error when reading ), ( was no on optStack")
			sys.exit()

	def enterNeuro_expression(self, ctx):
		if self.validateStacks():
			if self.checkOperatorsOnStack(["&&", "||"]):
				self.generateQuadruple()

	def enterNeuro_relational(self, ctx):
		if self.validateStacks():
			if self.checkOperatorsOnStack(["<", "<=", ">", ">=", "==", "!="]):
				self.generateQuadruple()

	def enterNeuro_sumMinus(self, ctx):
		if self.validateStacks():
			if self.checkOperatorsOnStack(["+", "-"]):
				self.generateQuadruple()

	def enterNeuro_multiDiv(self, ctx):
		if self.validateStacks():
			if self.checkOperatorsOnStack(["*", "/"]):
				self.generateQuadruple()

	def validateStacks(self):
		return (len(self.optStack) > 0 and len(self.opdStack) > 0)

	def checkOperatorsOnStack(self, listOperators):
		for currentOperator in listOperators:
			if self.optStack[-1] == currentOperator:
				return True

		return False

	#Method that generates quadruples for expressions
	def generateQuadruple(self):
				operator = self.optStack.pop()
				right_tuple = self.opdStack.pop()
				left_tuple = self.opdStack.pop()
				left_name = left_tuple[0]
				left_type = left_tuple[1]
				right_name = right_tuple[0]
				right_type = right_tuple[1]

				# Obtains codes from operators and operands
				operator_code = self.cube.operatorToCode(operator)
				left_code = self.cube.typeToCode(left_type)
				right_code = self.cube.typeToCode(right_type)

				resultType = self.cube.semanticValidation(operator_code, left_code, right_code)

				# Display result
				if resultType != -1:
					for key, value in self.cube.dicTypes.items():
						if resultType == value:
							resultName = key

					temp = self.addressManager.getVirtualAddress(resultName,"temporal")
					self.opdStack.append(('&'+str(temp), resultName))
					resultQuadruple = quadruples(self.counter,operator, left_name, right_name, '&'+str(temp))
					self.addressManager.updateVirtualAddress(resultName, "temporal")

					self.counter += 1
					self.quadruplesList.append(resultQuadruple)

				else:
					self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)

	#Method that generates quadruples for conditionals, loops, assignments, classes and functions
	def generatesQuadruple(self, operator, left, right, result):
		if operator == 'END':
			resultQuadruple = quadruples(self.counter, 'END', None, None, None)
			self.quadruplesList.append(resultQuadruple)
		elif operator == 'GotoF' or operator == 'Goto':
			#TO DO: Modular el siguiente fragmento de codigo
			temp = self.addressManager.getVirtualAddress('bool','temporal')
			self.opdStack.append(('&'+str(temp), 'bool'))
			resultQuadruple = quadruples(self.counter,operator, left, right, '&'+str(temp))
			self.addressManager.updateVirtualAddress(type, 'temporal')
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)
		elif operator ==  '=':
			left_type = left[1]
			right_type = right.data_type

			# Obtains codes from operators and operands
			operator_code = self.cube.operatorToCode(operator)
			left_code = self.cube.typeToCode(left_type)
			right_code = self.cube.typeToCode(right_type)
			resultType = self.cube.semanticValidation(operator_code, left_code, right_code)

			if resultType != -1:
				resultQuadruple = quadruples(self.counter,operator, left[0], None, '&'+str(right.id))
				self.counter += 1
				self.quadruplesList.append(resultQuadruple)
			else:
				print(operator, left_type, right_type)
				self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)
		elif operator == "PARAM":
			resultQuadruple = quadruples(self.counter, operator,left[0], None,'&'+ str(result))
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)
		elif operator == "ERA":
			resultQuadruple = quadruples(self.counter, operator, None, None,result)
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)

			# Search for that function in directory and push it to stack
			retrievedFunction = self.funcDirectory.getAddressFunction(result)
			formattedFunction = [retrievedFunction.name, retrievedFunction.data_type]

			self.funcStack.append(formattedFunction)

		elif operator == "GOSUB" or operator == "RETURN_ASSIGN" or operator == "WRITE":
			resultQuadruple = quadruples(self.counter, operator, None, None,result)
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)
		elif operator == "ENDCLASS"  or operator == "END_WRITE":
			resultCuadruple = quadruples(self.counter, operator, None, None,None)
			self.counter += 1
			self.quadruplesList.append(resultCuadruple)
		elif operator == 'RETURN':
			resultQuadruple = quadruples(self.counter, operator, None, None,result[0])
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)
		elif operator == 'ARRAY_DECLARE':
			resultQuadruple = quadruples(self.counter, operator, left, None, result)
			self.counter += 1
			self.quadruplesList.append(resultQuadruple)
		elif operator == 'READ':
			left_type = left[1]
			right_type = right.data_type
			if left_type == "string" and right_type == "string":
				resultCuadruple = quadruples(self.counter,operator, left[0], None, '&'+str(right.id))
				self.counter += 1
				self.quadruplesList.append(resultCuadruple)
			else:
				print(operator, left_type, right_type)
				self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)
		else:
			left_type = left[1]
			right_type = right[1]
			if left_type == right_type:
				resultQuadruple = quadruples(self.counter,operator, None, None, left[0])
				self.counter += 1
				self.quadruplesList.append(resultQuadruple)
			else:
				self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)

	#----------------------------------------------------------------------------------------
	#		QUADRUPLES FOR CLASSES
	#----------------------------------------------------------------------------------------
	def generateClassQuadruples(self, operator, left, right, result):
		if operator == "ERA":
			resultCuadruple = quadruples(self.counter, operator, None, right,result)
			self.counter += 1
			self.quadruplesList.append(resultCuadruple)

	#Method that retrieves an specific quadruple and modifies its value
	def fillQuadruple(self, id, cont):
		quad = list(filter(lambda x: x.id == id, self.quadruplesList))
		quad[0].result = cont

	# VUELVE AQUI
	def enterConstant(self, ctx):
		try:
			name = ctx.id_().getText()

			# Check if is an array
			if "[" in name:
				beginArrayPos = name.find("[")
				arrayName = name[:beginArrayPos]
				name = arrayName

			variable = ''
			#Verify that the name exists in the variable table
			if self.currentScope[0] == "local":
				variables = self.funcDirectory.getAddressFunction(self.currentScope[1])
				variable = variables.getVariableDirectory().getVariableByName(name)

			if variable is None or self.currentScope[0] == "global" :
				variable = self.varDirectory.getVariableByName(name)

			elif variable is None:
				self.error.definition(self.error.VARIABLE_NOT_DEFINED, name, None)

			lst = ('&'+str(variable.id), variable.data_type)
			self.opdStack.append(lst)
		except:
			pass

		try:
			value = ctx.FLOAT().getText()

			if value is not None:
				lst = (value, "float")
				self.opdStack.append(lst)
		except:
			pass

		try:
			value = ctx.INT().getText()

			if value is not None:
				lst = (value, "int")
				self.opdStack.append(lst)
		except:
			pass

		try:
			value = ctx.STRING().getText()

			if value is not None:
				lst = (value, "string")
				self.opdStack.append(lst)
		except:
			pass

		try:
			value = ctx.BOOLEAN().getText()

			if value is not None:
				lst = (value, "bool")
				self.opdStack.append(lst)
		except:
			pass

	# IF STATEMENT
	def enterNeuro_if(self, ctx):
		try:
			result = self.opdStack.pop()
			exp_type = result[1]
			value = result[0]
			if exp_type is not 'bool':
				self.error.definition(self.error.TYPE_MISMATCH, 'IF', exp_type)
			else:
				self.generatesQuadruple('GotoF', value, None, None)
				self.jumpStack.append(('IF',self.counter - 1))
		except:
			pass

	def enterNeuro_endif(self, ctx):
		try:
			endif = self.jumpStack.pop()[1]
			self.fillQuadruple(endif,self.counter)
		except:
			pass

	def enterNeuro_else(self, ctx):
		try:
			self.generatesQuadruple('Goto', None, None, None)
			false = self.jumpStack.pop()[1]
			self.jumpStack.append(('ELSE', self.counter - 1))
			self.fillQuadruple(false, self.counter)
		except:
			pass

	# WHILE STATEMENT
	def enterNeuro_while_begin(self, ctx):
		try:
			self.jumpStack.append(('WHILE', self.counter))
		except:
			pass

	def enterNeuro_while_expression(self, ctx):
		try:
			result = self.opdStack.pop()
			exp_type = result[1]
			value = result[0]
			if exp_type is not 'bool':
				print("Error: type mismatch if")
				sys.exit()
			else:
				self.generatesQuadruple('GotoF', value, None, None)
				self.jumpStack.append(('WHILE',self.counter - 1))
		except:
			pass

	def enterNeuro_while_end(self, ctx):
		try:
			endJump = self.jumpStack.pop()[1]
			returnJump = self.jumpStack.pop()[1]

			self.generatesQuadruple('Goto', None, None, None)
			self.fillQuadruple(self.counter - 1, returnJump)

			self.fillQuadruple(endJump, self.counter)
		except:
			pass

	# CODE ACTIONS FOR MODULE CALL
	def enterEvaluate_function(self, ctx):
		name = ctx.TOK_ID().getText()
		#print(name)
		number = ctx.expressions()
		#Check if the function exists in the function directory
		if self.funcDirectory.checkFunction(name):
			#Check that parameters match
			function = self.funcDirectory.getAddressFunction(name)

			copyParamStack = []
			for param in function.params:
				copyParamStack.append(param)

			self.parameterStack = copyParamStack

			if len(self.parameterStack) == len(number):
				self.FunctionId = function.quadId
				self.returnType = function.data_type
				self.generatesQuadruple("ERA", None, None, name)

				# Search for that function in directory and push it to stack
				formattedFunction = [function.name, function.data_type]
				self.funcStack.append(formattedFunction)
			else:

				print("The number of parameters does not match the function")
				sys.exit()

	def enterNeuro_params(self, ctx):
		#Send every parameter
		while self.parameterStack:
			param = self.parameterStack.pop()
			arg = self.opdStack.pop()
			new_memory = param.id
			self.verifyParams(arg,param)

			# Param is the action to send the parameters of a function during
			# a module call. The second element is the address of the current value,
			# The last element is where the current value is going to be stored.
			self.generatesQuadruple("PARAM", arg, None, new_memory)

	def exitNeuro_params(self, ctx):
		#Depending on the return data type, we'll assign a temporal address
		memory_address = self.addressManager.getVirtualAddress(self.returnType, "temporal")
		self.addressManager.updateVirtualAddress(self.returnType, "temporal")
		self.opdStack.append(["&"+ str(memory_address), self.returnType])
		self.generatesQuadruple("RETURN_ASSIGN", None, None, "&" + str(memory_address))
		self.generatesQuadruple("GOSUB", None, None, self.FunctionId)

	# CONSTRUCTOR
	def enterConstructor(self, ctx):
		self.currentScope = ("local", "constructor")
		self.addressManager.restartVirtualAddress()
		lst_param_const = []
		try:
			# Obtain parameters, this case is for the first parameter, in case there is one
			paramName = ctx.parameters().TOK_ID().getText()
			paramType =  ctx.parameters().data_type().getText()
	
			newVariable = objVariable(self.addressManager.getVirtualAddress(paramType, self.currentScope[0]), paramName, paramType)
			self.addressManager.updateVirtualAddress(paramType, self.currentScope[0])
			
			lst_param_const.append(newVariable)
		except:
			pass
		try:
			countParameters = 0
			# Read parameters that go after the comma of the first one
			while ctx.parameters().parameters_recursive() is not None:
				# Counter for recursive parameters, this is used for accesing parameters that go after the first one
				paramType = ctx.parameters().parameters_recursive().data_type(countParameters).getText()
				paramName = ctx.parameters().parameters_recursive().TOK_ID(countParameters).getText()

				newVariable = objVariable(self.addressManager.getVirtualAddress(paramType, self.currentScope[0]), paramName, paramType)

				self.addressManager.updateVirtualAddress(paramType, self.currentScope[0])
				lst_param_const.append(newVariable)
				countParameters += 1

		except:
			pass
		self.createConstructor(lst_param_const)
	

	def enterInit_class(self, ctx):
		#Get name of the variable that its instantiated
		name = ctx.TOK_ID().getText()
		#Identify the current scope 
		if self.currentScope[0] == "local":
			variables = self.funcDirectory.getAddressFunction(self.currentScope[1])
			#Look for the variable in the directory
			variable = variables.getVariableDirectory().getVariableByName(name)

		if variable is None or self.currentScope[0] == "global" :
			variable = self.varDirectory.getVariableByName(name)

		elif variable is None:
			self.error.definition(self.error.VARIABLE_NOT_DEFINED, name, None)
		#Get address of the object
		id = variable.id
		#Check object class
		object_class = variable.data_type
		#Create new instance in the object directory
		self.createAddObject(id, name, object_class)
		#Create quaruples for ERA CONSTRUCTOR
		self.generateClassQuadruples("ERA", None, object_class, "init")

		#Create quadruples for sending the parameters
		#Look for the method in the 

		print(variable)
	
	def enterNeuro_initEval(self, ctx):
		self.initEvalStack.append(self.opdStack.pop())

	def enterNeuro_createConstructor(self, ctx):
		#Create quadruples for sending the params
		#They are already ordered correctly
		obj_attr = self.initEvalStack.pop(0)
		#self.generateClassQuadruples("INIT_ATTR",)
	
	#---------------------------------------------
	#	INHERITANCE
	#---------------------------------------------
	def enterInheritance(self, ctx):
		className = ctx.TOK_ID().getText()
		self.currentClass.parent = className

	#----------------------------------------------
	#	OUTPUT
	#----------------------------------------------
		
	def enterNeuro_finishOutput(self, ctx):
		self.generatesQuadruple("END_WRITE", None, None,1)

	def enterNeuro_getOutput(self, ctx):
		val = self.opdStack.pop()
		
		self.generatesQuadruple("WRITE",None, None, val[0])

	#----------------------------------------------
	#	INPUT
	#----------------------------------------------
	def exitInput_(self, ctx):
		val = ctx.expressions().getText()
		input_val = (val, "string")
		name = ctx.TOK_ID().getText()
		#Check if variable exists in current context
		variable = ''
		#Verify that the name exists in the variable table
		try: 
			if self.currentScope[0] == "local":
				variables = self.funcDirectory.getAddressFunction(self.currentScope[1])
				variable = variables.getVariableDirectory().getVariableByName(name)

			if variable is None or self.currentScope[0] == "global" :
				variable = self.varDirectory.getVariableByName(name)


			elif variable is None:
				self.error.definition(self.error.VARIABLE_NOT_DEFINED, name, None)
			#Create quadruple
			self.generatesQuadruple('READ',input_val,variable, None)
		except:
			pass

	
	#------------------------------------------------------
	#	AUXILIARY METHODS
	#------------------------------------------------------
	def printClassDictionary(self):
		for key, _class in self.classDirectory.directory.items():
			#Print information of each class
			_class.printClass()

	def printFunctions(self):
		for key, function in self.funcDirectory.items():
			#Print information of each function
			function.printFunction()

	def printQuadruples(self):
		for quadruple in self.quadruplesList:
			print(quadruple.id, quadruple.opt, quadruple.opd1, quadruple.opd2, quadruple.result)

	def createAddVariable(self, name, data_type, dimensions, size=1):
		if self.isPartOfClass:
			# Set current privacy of the group of variables
			currentPrivacy = "public" if self.isPublic else "private"

			# If this is part of a class, then create an classVariable object 
			newClassVariable = classVariable(self.addressManager.getVirtualAddress(data_type, self.currentScope[0]), name, data_type, currentPrivacy)
			#Create a dict entry
			var = {self.addressManager.getVirtualAddress(data_type, self.currentScope[0]) : newClassVariable}
			#Update the address 
			self.addressManager.updateVirtualAddress(data_type, self.currentScope[0])
			#Save the variable in the current class directory
			self.currentClass.variableClassDirectory.update(var)

		else:
			# Else, this variable is not associated with a class and we need to create a objVariable object
			# and add it directly to the global variables directory
			if not self.isObject:
				newVariable = objVariable(self.addressManager.getVirtualAddress(data_type, self.currentScope[0]), name, data_type, dimensions, size)
				self.addressManager.updateVirtualAddress(data_type, self.currentScope[0], newVariable.size)
				if self.currentScope[0] == "global":
					self.varDirectory.addVariable(newVariable)
				else:
					#In case of declaring a variable inside a function
					func = self.funcDirectory.getAddressFunction(self.currentScope[1])
					func.localVars.addVariable(newVariable)
					func.countVars += 1
			elif self.isObject:
				newVariable = objVariable(self.addressManager.getVirtualAddress("obj", self.currentScope[0]), name, data_type, dimensions, size)
				self.addressManager.updateVirtualAddress("obj", self.currentScope[0])

				self.isObject = False
				if self.currentScope[0] == "global":
					self.varDirectory.addVariable(newVariable)
				else:
					#In case of declaring a variable inside a function
					func = self.funcDirectory.getAddressFunction(self.currentScope[1])
					func.localVars.addVariable(newVariable)
					func.countVars += 1
			counter = 0

	def createAddRoutine(self, name, data_type, params):
		if self.isPartOfClass:
			# Set current privacy of the group of variables
			currentPrivacy = "public" if self.isPublic else "private"
			# If this is part of a class, then create an classMethod object
			newMethod = classMethod(self.counter, name, data_type, currentPrivacy, params)
			method = {self.counter : newMethod}
			print(self.currentClass.name)
			#Add new function to the method directory of the class
			self.currentClass.methodsClassDirectory.update(method)
			#For return purposes
			self.funcStack.append([name, data_type])


		else:
			# Else, this variable is not associated with a class and we need to create a objFunction object
			# and add it directly to the function directory

			newFunction = objFunction(self.counter, name, data_type, params)
			#Add parameters to the local variable table
			if params is not None:
				param_number = len(params)
				newFunction.countVars = param_number
				newFunction.localVars.addMultipleVariables(params)
			#Add new function to the function directory
			self.funcDirectory.addFunction(newFunction)
			#For return purposes
			self.funcStack.append([name, data_type])
		# Add 1 to counter
		self.IDCounter += 1
	
	def createAddObject(self, id, name, data_type):
		#Look for the class of the object in the classes directory
		if self.classDirectory.checkClassByName(data_type):
			#If it exists then create a new object in the object directory
			newObject = objectO(id, name, data_type)
			
			#Pass the attributes and methods of the class to the object
			for key, class_value in self.classDirectory.directory.items():
				if class_value.name == name:
					#Generates copy of the class attributes into the object attrs
					newObject.objAttr.copy(class_value.variableClassDirectory)  
					#Generates copy of the class methods into the object methods
					newObject.objMethods.copy(class_value.methodsClassDirectory) 

			print("Object created", name)
			#Add object to the object directory
			self.objects.addObject(newObject)
		else:
			print("Class is not declared")
			sys.exit()
	
	def createConstructor(self, params):
		newMethod = classMethod(self.counter, "constructor", None, "public", None)
		#Add parameters to the local variable table
		if params is not None:
			param_number = len(params)
			newMethod.countVars = param_number
			newMethod.localVars.addMultipleVariables(params)
		method = {self.counter : newMethod}
		newMethod.localVars.printDirectory()
		self.currentClass.methodsClassDirectory.update(method)

	
	def verifyParams(self, argument, parameter):
		if argument[0] == parameter.name and argument[1] == parameter.data_type:
			return True
		else:
			#Throw error
			return False
	
	def verifyType(self, type):
		#First check for primitives
		if type == "string" or type == "bool" or type == "float" or type == "int":
			return True
		else:
			#Check if is a class
			if self.classDirectory.checkClassByName(type):
				self.isObject = True
				return True
			else:
				self.isObject = False
				return False

	def verifyParams(self, argument, parameter):
		if argument[0] == parameter.name and argument[1] == parameter.data_type:
			return True
		else:
			#Throw error
			return False

	def createEmptyClass(self, name):
		# Create new class and assign it to currentClass
		self.currentClass = objClass(self.IDCounter, name)

		# Add 1 to counter
		self.IDCounter += 1

	def addFinishedClass(self, objClass):
		self.classDirectory.addClass(objClass)