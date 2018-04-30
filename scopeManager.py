import sys
from antlr4 import *

from addressManager import addressManager

from objVariable import objVariable

from variableDirectory import variableDirectory
from routineDirectory import routineDirectory
from classDirectory import classDirectory

# Element of the memory, which is the parent and the directories
class scopeManager():
	def __init__(self, scopeName):
		
		# Priority of the memory
		self.scopeName = scopeName

		# Variables, rotuines and class directories
		self.variableDirectory = variableDirectory()
		self.routineDirectory = routineDirectory()
		self.classDirectory = classDirectory()

		#Temporal memory
		self.temporalMemory = variableDirectory()

		# Instance of addressManager for this particular memory
		self.adManager = addressManager()

	# Searchs temporal variable and returns its value
	def searchTemporalAddress(self, address):
		if(self.temporalMemory.checkVariableById(address)):
			return self.temporalMemory.getVariableById(address).value;
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultTemporal(self, resultValue, address):
		typeString = str(type(resultValue))
		tempVariable = objVariable(address, "tempVariable", typeString, 0, resultValue)
		self.temporalMemory.addVariable(tempVariable)