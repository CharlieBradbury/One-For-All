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
			return self.temporalMemory.getVariableById(address)
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultTemporal(self, resultValue, address):
		typeString = str(type(resultValue))
		tempVariable = objVariable(address, "tempVariable", typeString, 0, 1, resultValue)
		self.temporalMemory.addVariable(tempVariable)

	# Searchs temporal variable and returns its value
	def searchLocalAddress(self, address):
		if(self.localMemory.checkVariableById(address)):
			return self.localMemory.getVariableById(address)
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultLocal(self, resultValue, address, offSet=-1):
		typeString = str(type(resultValue))
		varFound = self.searchLocalAddress(address)

		if offSet > -1:
			if varFound is None:
				# Then the variable does not exist and we create it
				resultArray = [None] * (offSet + 1) 
			else:
				# Modify specific element
				resultArray = varFound.value
				resultArray[offSet] = resultValue

			resultArray[offSet] = resultValue
			tempVariable = objVariable(address, "localVariable", typeString, 0, 1, resultArray)
			self.localMemory.addVariable(tempVariable)
		else:
			# Variabe is simple
			tempVariable = objVariable(address, "localVariable", typeString, 0, 1, resultValue)
			self.localMemory.addVariable(tempVariable)

	# Searchs temporal variable and returns its value
	def searchGlobalAddress(self, address):
		if(self.globalMemory.checkVariableById(address)):
			return self.globalMemory.getVariableById(address)
		else:
			return None
		
	# Saves the result of a temporal variable in an adress
	def saveResultGlobal(self, resultValue, address, offSet=-1):
		typeString = str(type(resultValue))
		varFound = self.searchGlobalAddress(address)

		if offSet > -1:
			if varFound is None:
				# Then the variable does not exist and we create it
				resultArray = [None] * (offSet + 1) 
			else:
				# Modify specific element
				resultArray = varFound.value
				resultArray[offSet] = resultValue

			resultArray[offSet] = resultValue
			tempVariable = objVariable(address, "globalVariable", typeString, 0, 1, resultArray)
			self.globalMemory.addVariable(tempVariable)
		else:
			# Variabe is simple
			tempVariable = objVariable(address, "globalVariable", typeString, 0, 1, resultValue)
			self.globalMemory.addVariable(tempVariable)

	def isArrayGlobal(self, address):
		# Get array with such address
		foundVariable = self.searchGlobalAddress(address)

		if foundVariable is None:
			return False
		else:
			return isinstance(foundVariable.value, list)

	def isArrayLocal(self, address):
		# Get array with such address
		foundVariable = self.searchLocalAddress(address)

		if foundVariable is None:
			return False
		else:
			return isinstance(foundVariable.value, list)