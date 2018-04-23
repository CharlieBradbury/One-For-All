import sys
import os
from antlr4 import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parser.one_for_allLexer import one_for_allLexer
from parser.one_for_allParser import one_for_allParser
from parser.one_for_allListener import one_for_allListener
from scope import scope
from objClass import *
from objFunction import objFunction
from objVariable import objVariable
from collections import OrderedDict
from semanticCube import semanticCube
from quadruples import quadruples
from variableDirectory import variableDirectory
from functionDirectory import functionDirectory
from addressManager import addressManager
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
		self.classDirectory = dict()

		# Function directory
		self.funcDirectory = functionDirectory()

		# Variable Directory
		self.varDirectory = variableDirectory()

		# Current class (Type: objClass)
		self.currentClass = None

		#Scope Manager stack that stores the scopes
		current_scope = scope("global", None)
		self.scopeManager = []
		self.scopeManager.append(current_scope)

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
	
		#------------------------------------------------------
		#	CREATE FIRST QUADRUPLE
		#   Goto to the main method
		#-----------------------------------------------------
		self.generatesQuadruple('Goto', None, None, None)
		self.jumpStack.append(('Main',self.counter - 1))


	#------------------------------------------------------
	# 	CLASS, FUNCTIONS AND VARIABLES
	#-----------------------------------------------------

	def enterMain(self, ctx):
		main = self.jumpStack.pop()[1]
		self.fillQuadruple(main,self.counter)

	def enterClasses(self, ctx):
		self.isPartOfClass = True

	def enterClass_definition(self, ctx):
		# Create new class just with the ID and name of the class
		# This will set current class to the recently created class
		className = ctx.TOK_ID().getText()
		self.createEmptyClass(className)

	def enterInheritance(self, ctx):
		try:
			# Assign parent to the current class
			className = ctx.TOK_ID().getText()
			self.currentClass.parent = className
		except:
			pass

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

	def enterVariable_definition(self, ctx):
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

		# List of parameters
		routineParameters = []

		try:
			# Obtain parameters, this case is for the first parameter, in case there is one
			paramName = ctx.parameters().TOK_ID().getText()
			paramType =  ctx.parameters().data_type().getText()

			#Create object variable for each parameter, always assume is a non array variable
			tempParam = objVariable(self.addressManager.getVirtualAddress(paramType,"local"), paramName, paramType,0)
			self.addressManager.updateVirtualAddress(paramType,"local")
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
				tempParam = objVariable(self.addressManager.getVirtualAddress(paramType,"local"), paramName, paramType,0)
				self.addressManager.updateVirtualAddress(paramType,"local")
				routineParameters.append(tempParam)
				'''CHECK PARAMETERS NOT WORKING WITH ARRAYS'''
				countParameters += 1
		except:
			pass

		try:
			# Create routine
			self.createAddRoutine(routineName, routineType, routineParameters)
		except:
			print("Error while creating new routine")
			sys.exit()

	
	def enterNeuro_array(self, ctx):
		pass
		'''param = self.routineParameters.pop()
		value = self.opdStack.pop()
		new_paramType = param[0]
		new_param = param[1]
		size = value[0]'''

		'''self.routineParameters.append([new_paramType, new_param, size])'''

	
	def exitClass_definition(self, ctx):
		# Call method to add finished class to the class directory
		self.addFinishedClass(self.currentClass)

		# Resetting context variables
		self.isPublic = False
		self.currentClass = None
	
	def exitClasses(self, ctx):
		# Reset part of class boolean
		self.isPartOfClass = False

		'''
		#print("--- CLASSES ---")
		#self.printClassDictionary()
		'''

	def exitRestOfProgram(self, ctx):
		pass
		self.printQuadruples()

		for key, var in self.varDirectory.directory.items():
			print(var.printVariable())
		
		for key, func in self.funcDirectory.directory.items():
			func.printFunction()

	#------------------------------------------------------
	# QUADRUPLES
	#------------------------------------------------------	

	def exitAssignment(self,ctx):
		#Consult name of the variable that its going to be assigned
		name = ctx.id_().getText()
		#Verify that the name exists in the variable table
		if self.varDirectory.checkVariable(name):
			variable = self.varDirectory.getAddressVariable(name)
		val = self.opdStack.pop()
		#Create quadruple
		self.generatesQuadruple('=',val, variable, None)
	
	def exitVariable_assign(self, ctx):
		#Can declare and assign values to multiple variables
		while self.variableStack:
			#Get the name of the variable 
			name = self.variableStack.pop()
			#Verify that the name exists in the variable table
			if self.varDirectory.checkVariable(name):
				variable = self.varDirectory.getAddressVariable(name)
			#Get the corresponding value of the expression
			val = self.opdStack.pop()
			#Create quadruple
			self.generatesQuadruple('=',val, variable, None)
	
	def exitReturn_expr(self, ctx):
		#Get the value of the expression 
		val = self.opdStack.pop()
		#Check if the val matches type of the function
		function = self.funcStack.pop()
		#Generate quadruple
		self.generatesQuadruple('RETURN',val, function, None)


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
					resultCuadruple = quadruples(self.counter,operator, left_name, right_name, '&'+str(temp))
					self.addressManager.updateVirtualAddress(resultName, "temporal")

					self.counter += 1
					self.quadruplesList.append(resultCuadruple)

				else:
					self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)

	#Method that generates quadruples for conditionals, loops, assignments, classes and functions
	def generatesQuadruple(self, operator, left, right, result):
		if operator == 'GotoF' or operator == 'Goto':
			#TO DO: Modular el siguiente fragmento de codigo
			temp = self.addressManager.getVirtualAddress('bool','temporal')
			self.opdStack.append(('&'+str(temp), 'bool'))
			resultCuadruple = quadruples(self.counter,operator, left, right, '&'+str(temp))
			self.addressManager.updateVirtualAddress(type, 'temporal')
			self.counter += 1
			self.quadruplesList.append(resultCuadruple)
		elif operator ==  '=':
			left_type = left[1]
			right_type = right.data_type
			# Obtains codes from operators and operands
			operator_code = self.cube.operatorToCode(operator) 
			left_code = self.cube.typeToCode(left_type)
			right_code = self.cube.typeToCode(right_type)
			resultType = self.cube.semanticValidation(operator_code, left_code, right_code)

			if resultType != -1:
				resultCuadruple = quadruples(self.counter,operator, left[0], None, '&'+str(right.id))
				self.counter += 1
				self.quadruplesList.append(resultCuadruple)
			else:

				self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)
		else:
			left_type = left[1]
			right_type = right[1]
			if left_type == right_type:
				resultCuadruple = quadruples(self.counter,operator, None, None, left[0])
				self.counter += 1
				self.quadruplesList.append(resultCuadruple)
			else:
				self.error.definition(self.error.INVALID_OPERATION, left_type, right_type)


	#Method that retrieves an specific quadruple and modifies its value
	def fillQuadruple(self, id, cont):
		quad = list(filter(lambda x: x.id == id, self.quadruplesList))
		quad[0].result = cont
		
	# Enter a parse tree produced by one_for_allParser#id_.
	def enterConstant(self, ctx):
		try: 
			idName = ctx.id_().getText()
			print(idName)
			#Verify that the name exists in the variable table
			if self.varDirectory.checkVariable(idName):
				variable = self.varDirectory.getAddressVariable(idName)
				lst = ('&'+str(variable.id), variable.data_type)
				self.opdStack.append(lst)
			else:
				self.error.definition(self.error.VARIABLE_NOT_FOUND, idName)

		except:
			pass

		try: 
			value = ctx.FLOAT().getText()

			if value is not None:
				lst = (value, "float")
				print("EVALUATE FLOAT:", lst)
				self.opdStack.append(lst)
		except:
			pass

		try: 
			value = ctx.INT().getText()

			if value is not None:
				lst = (value, "int")
				#print("EVALUATE INT:", lst)
				self.opdStack.append(lst)
		except:
			pass

		try: 
			value = ctx.STRING().getText()

			if value is not None:
				lst = (value, "string")
				#print("EVALUATE STRING:", lst)
				self.opdStack.append(lst)
		except:
			pass

		try: 
			value = ctx.BOOLEAN().getText()

			if value is not None:
				lst = (value, "bool")
				#print("EVALUATE BOOLEAN:", lst)
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

	#------------------------------------------------------
	#	AUXILIARY METHODS
	#------------------------------------------------------
	def printClassDictionary(self):
		for key, _class in self.classDirectory.items():
			#Print information of each class
			_class.printClass()

	def printGlobalVariables(self):
		for key, globalVar in self.globalVarsDirectory.items():
			#Print information of each variable
			globalVar.printVariable()

	def printFunctions(self):
		for key, function in self.funcDirectory.items():
			#Print information of each function
			function.printFunction()

	def printQuadruples(self):
		for quadruple in self.quadruplesList:
			print(quadruple.id, quadruple.opt, quadruple.opd1, quadruple.opd2, quadruple.result)

	def createAddVariable(self, name, data_type, dimensions):
		if self.isPartOfClass:
			# Set current privacy of the group of variables
			currentPrivacy = "public" if self.isPublic else "private"

			# If this is part of a class, then create an objVariable_Class object 
			newClassVariable = objVariable_Class(self.IDCounter, name, data_type, currentPrivacy)

			# Add it calling the corresponding method depending if it is a public or global variable
			if currentPrivacy:
				self.currentClass.addPublicVariable(newClassVariable)
			else:
				self.currentClass.addPrivateVariable(newClassVariable)
		else:
			# Else, this variable is not associated with a class and we need to create a objVariable object
			# and add it directly to the global variables directory

			newVariable = objVariable(self.addressManager.getVirtualAddress(data_type, 'global'), name, data_type, dimensions)
			self.addressManager.updateVirtualAddress(data_type, 'global')
			self.varDirectory.addVariable(newVariable)
			counter = 0

		# Add 1 to counter
		self.IDCounter += 1

	def createAddRoutine(self, name, data_type, params):
		if self.isPartOfClass:
			# Set current privacy of the group of variables
			currentPrivacy = "public" if self.isPublic else "private"

			# If this is part of a class, then create an objMethod object 
			newMethod = objMethod(self.IDCounter, name, data_type, params, currentPrivacy)

			if currentPrivacy:
				self.currentClass.addPublicMethod(newMethod)
			else:
				self.currentClass.addPrivateMethod(newMethod)
		else:
			# Else, this variable is not associated with a class and we need to create a objFunction object
			# and add it directly to the function directory
			newFunction = objFunction(self.counter, name, data_type, params, params)
			self.funcDirectory.addFunction(newFunction)
			self.funcStack.append([name, data_type])
		# Add 1 to counter
		self.IDCounter += 1

	def createEmptyClass(self, name):
		# Create new class and assign it to currentClass
		self.currentClass = objClass(self.IDCounter, name)

		# Add 1 to counter 
		self.IDCounter += 1

	def addFinishedClass(self, objClass):
		self.classDirectory[objClass.name] = objClass