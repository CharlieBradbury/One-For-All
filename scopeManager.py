import sys
from antlr4 import *

from addressManager import addressManager

from objVariable import objVariable

from variableDirectory import variableDirectory
from functionDirectory import functionDirectory
from classDirectory import classDirectory

# Element of the memory, which is the parent and the directories
class scopeManager():
	def __init__(self, scopeName):
		
		# Priority of the memory
		self.scopeName = scopeName

		# Global memory
		self.globalMemory = variableDirectory()
		self.functionDirectory = functionDirectory()
		self.classDirectory = classDirectory()

		# Local Memory
		self.localMemory = variableDirectory()

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

	# Searchs temporal variable and returns its value
	def searchLocalAddress(self, address):
		if(self.localMemory.checkVariableById(address)):
			return self.localMemory.getVariableById(address).value;
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultLocal(self, resultValue, address):
		typeString = str(type(resultValue))
		tempVariable = objVariable(address, "localVariable", typeString, 0, resultValue)
		self.localMemory.addVariable(tempVariable)

	# Searchs temporal variable and returns its value
	def searchGlobalAddress(self, address):
		if(self.globalMemory.checkVariableById(address)):
			return self.globalMemory.getVariableById(address).value;
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultGlobal(self, resultValue, address):
		typeString = str(type(resultValue))
		tempVariable = objVariable(address, "globalVariable", typeString, 0, resultValue)
		self.globalMemory.addVariable(tempVariable)

