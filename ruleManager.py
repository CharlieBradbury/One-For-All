import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from directoryManager import directoryManager
from objClass import objClass
from objClass import objVariable_Class
from objClass import objMethod
from objFunction import objFunction
from objVariable import objVariable

from collections import OrderedDict

class ruleManager(one_for_allListener):
	def __init__(self):
		self.directory = directoryManager()

		# Starting IDCounter at 0
		self.IDCounter = 0

		# Class Directory
		self.classDirectory = dict()

		# Global variables
		self.globalVarsDirectory = dict()

		# Function directory
		self.functionDirectory = dict()

		# Current class (Type: objClass)
		self.currentClass = None

		# Boolean to check if reading a class, if reading a method
		# and if the current var/method is public
		self.isPartOfClass = False
		self.isPublic = False

	def enterClasses(self, ctx):
		self.isPartOfClass = True

	def enterClassDefinition(self, ctx):
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
	  
	def enterClass_private(self, ctx):
		try:
			# Setting values of private and class booleans
			self.isPublic = False
			# If there are no functions in the current context, then we are reading variables and this boolean should be false
		except:
			print("Error while reading private token, not possible to know if reading variable or method")

	def enterVariableDefinition(self, ctx):
		try:
			# Obtain type and names of the single or multiple variables associated to that type
			# E.g: public var int a1, a2;
			currentType = ctx.data_type().getText()
			currentVariables = ctx.TOK_ID()

			try:
				# For each name, create an object variable with such information
				for var in currentVariables:
					#Create object
					newVariable = self.createAddVariable(var.getText(), currentType) 
			except:
				print("Error while creating new variable")
		except:
			print("Error while preparing information for variables creation")

	def enterRoutineDefinition(self, ctx):
		# Obtain type and name of routine to be created
		routineName = ctx.TOK_ID().getText()
		routineType = ctx.data_type().getText()

		# List of parameters
		routineParameters = []

		try:
			# Obtain parameters, this case is for the first parameter, in case there is one
			paramName = ctx.parameters().TOK_ID().getText()
			paramType =  ctx.parameters().data_type().getText()

			# Temporal parameters, 999 because not sure if these variables should have and ID or not
			tempParam = objVariable(999, paramName, paramType)
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

				# Temporal parameters, 999 because not sure if these variables should have and ID or not
				tempParam = objVariable(999, paramName, paramType)
				routineParameters.append(tempParam)

				countParameters += 1
		except:
			pass

		try:
			# Create routine
			self.createAddRoutine(routineName, routineType, routineParameters)
		except:
			print("Error while creating new routine")
	
	def exitClassDefinition(self, ctx):
		# Call method to add finished class to the class directory
		self.addFinishedClass(self.currentClass)

		# Resetting context variables
		self.isPublic = False
		self.currentClass = None
	
	def exitClasses(self, ctx):
		# Reset part of class boolean
		self.isPartOfClass = False

		# Print classes
		print("--- CLASSES ---")
		self.printClassDictionary()

	def enterRestOfProgram(self, ctx):
		print("--- GLOBAL VARIABLES ---")
		self.printGlobalVariables()

		print("--- FUNCTIONS ---")
		self.printFunctions()

	''' AUXILIARY FUNCTIONS '''
	def printClassDictionary(self):
		for key, _class in self.classDirectory.items():
			#Print information of each class
			_class.printClass()

	def printGlobalVariables(self):
		for key, globalVar in self.globalVarsDirectory.items():
			#Print information of each variable
			globalVar.printVariable()

	def printFunctions(self):
		for key, function in self.functionDirectory.items():
			#Print information of each function
			function.printFunction()

	''' CREATION METHODS '''
	def createAddVariable(self, name, data_type):
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
			newVariable = objVariable(self.IDCounter, name, data_type)
			self.globalVarsDirectory[name] = newVariable

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
			newFunction = objFunction(self.IDCounter, name, data_type, params)
			self.functionDirectory[name] = newFunction

		# Add 1 to counter
		self.IDCounter += 1

	def createEmptyClass(self, name):
		# Create new class and assign it to currentClass
		self.currentClass = objClass(self.IDCounter, name)

		# Add 1 to counter 
		self.IDCounter += 1

	def addFinishedClass(self, objClass):
		self.classDirectory[objClass.name] = objClass