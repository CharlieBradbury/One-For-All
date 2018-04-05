import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from directoryManager import directoryManager
from objClass import *
from objFunction import objFunction
from objVariable import objVariable
from collections import OrderedDict

class ruleManager(one_for_allListener):
	def __init__(self):
		self.directory = directoryManager()
		self.classes = []             
		
		self.currentClass = ""
		self.isClassMethod = False
		self.isPublic = True

	def enterClasses(self, ctx):
		print("hola")
		self.currentClass = ctx.TOK_ID(0).getText()
		print(self.currentClass)
		for val in ctx.TOK_ID():
			lst = [val, None,None]
			self.classes.append(lst)

	def enterInheritance(self, ctx):
		try:
			self.classes[-1][1]= ctx.TOK_ID().getText()
		except:
			pass

	def enterClass_public(self, ctx):
		counter = 0
		#For variables
		
		
		#For methods
		counterMethods = 0
		if ctx.funcs(counterMethods) is not None:
			self.isClassMethod = True
			self.isPublic = True
	  
	def enterClass_private(self, ctx):
		#For variables
		counter = 0
		
		#For methods
		counterMethods = 0
		if ctx.funcs(counterMethods) is not None:
			self.isClassMethod = True
			self.isPublic = False

	def enterVariables (self, ctx):
		try:
			type = ctx.variables(counter).data_type(0).getText()
			names = ctx.variables(counter).TOK_ID()
			try:
				lst = [type, names.getText()]
				self.privateVariable.append(lst)
			except:
				for name in names:
					lst = [type, name.getText()]
					self.privateVariable.append(lst)   
		 
			try:
				counter_ids = 0
				others = ctx.variables(counter).other_var(counter_ids)
				for id in others.TOK_ID():   
					lst_other = [type, id.getText()]
					self.privateVariable.append(lst_other)
				counter_ids = counter_ids + 1
			except:
				pass
			counter = counter + 1
		except:
			pass


	def createFunction(self, type, name, params, isClassMethod, isPublic):
		if isClassMethod:
			method = objMethods("Class " + self.currentClass, name, params, type, isPublic)
			print(method.id, method.data_type, method.name, method.params)
		else:
			func = objFunction("id", name, params, type)
			print(func.data_type, func.name, func.params)


	def enterFuncs (self, ctx):
		type = ctx.data_type(0).getText()
		name = ctx.TOK_ID(0).getText()

		type_first_parameter=  ctx.parameters(0).data_type().getText()
		first_parameter = ctx.parameters(0).TOK_ID().getText()

		lst = [type_first_parameter, first_parameter]
		lst_parameters = []
		lst_parameters.append(lst)

		counter_func = 0
		counter_params = 0
		print(self.currentClass)
		try:
			while ctx.parameters(counter_func).parameters_recursive() is not None:
				param_type = ctx.parameters(counter_func).parameters_recursive().data_type(counter_params).getText()
				param_id = ctx.parameters(counter_func).parameters_recursive().TOK_ID(counter_params).getText()
				lst = [param_type,param_id]
				lst_parameters.append(lst)
				counter_params = counter_params + 1

		except:
			pass
		self.createFunction(type, name, lst_parameters, self.isClassMethod, self.isPublic)
	
	def exitClasses(self, ctx):
		self.currentClass = ""
		self.isClassMethod = False
		#Create class objects
		for obj in self.classes:
			_obj = objClass("id",obj[0],obj[1])
			self.directory.addClassToDirectory(_obj)


	
	
	