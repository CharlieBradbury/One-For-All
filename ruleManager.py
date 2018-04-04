import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from directoryManager import directoryManager
from objClass import objClass
from objFunction import objFunction
from objVariable import objVariable
from collections import OrderedDict

class ruleManager(one_for_allListener):
	def __init__(self):
		self.directory = directoryManager()

		# Class Directory
		self.classes = []   

		# Current class (Type: objClass)
		self.currentClass = None

		# Booleans to check is reading public/private and variable/function
		self.isPublic = False
		self.isClassMethod = False

	def enterClasses(self, ctx):
		print("CREATING DIRECTORY OF CLASSES")

	def enterInheritance(self, ctx):
		try:
			# The parent class is assigned to the last saved class
			self.classes[-1].parent = ctx.TOK_ID().getText()
		except:
			pass

	def enterClass_public(self, ctx):
		try:
			# Setting values of public and class booleans
			self.isPublic = True
			# If there are no functions, then we are reading variables and this boolean should be false
			self.isClassMethod = (ctx.funcs(0) is not None)
		except:
			print("Error while reading public token, not possible to know if reading variable or method")
	  
	def enterClass_private(self, ctx):
		try:
			# Setting values of private and class booleans
			self.isPublic = False
			# If there are no functions, then we are reading variables and this boolean should be false
			self.isClassMethod = (ctx.funcs(0) is not None)
		except:
			print("Error while reading private token, not possible to know if reading variable or method")

	def enterVariables(self, ctx):
		try:
			pass
		except:
			print("Error while entering variables")

	def exitVariables(self, ctx):
		try:
			pass
		except:
			print("Error while exiting variables")

	def enterFuncs (self, ctx):
		try:
			pass
		except:
			print("Error while entering functions")
	
	def exitFuncs(self, ctx):
		try:
			pass
		except:
			print("Error while exiting functions")

	def exitClass_public(self, ctx):
		pass

	def exitClass_private(self, ctx):
		pass
	
	def exitClasses(self, ctx):
		# Resetting context variables
		self.isPublic = False
		self.isClassMethod = False

		self.printClassDictionary()

	def printClassDictionary(self):
		self.classes.append(objClass(1, "Clase Prueba", "Padre Prueba"))

		for _class in self.classes:
			#Print information of each class
			_class.printClass()