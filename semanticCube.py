import sys

class semanticCube():
	def __init__(self):

		# Declare dicTypes, dicOperators and cube
		self.dicTypes = dict()
		self.dicOperators = dict()
		self.cube = dict()

		# Initialize dicTypes
		self.dicTypes['error'] = -1
		self.dicTypes['int'] = 0
		self.dicTypes['float'] = 1
		self.dicTypes['bool'] = 2
		self.dicTypes['string'] = 3
		self.dicTypes['obj'] = 4

		# Initialize dicOperators
		self.dicOperators['='] = 0
		self.dicOperators['+'] = 1
		self.dicOperators['-'] = 2
		self.dicOperators['*'] = 3
		self.dicOperators['/'] = 4
		self.dicOperators['>'] = 5
		self.dicOperators['>='] = 6
		self.dicOperators['<'] = 7
		self.dicOperators['<='] = 8
		self.dicOperators['=='] = 9
		self.dicOperators['!='] = 10
		self.dicOperators['&&'] = 11
		self.dicOperators['||'] = 12



		# Initialize cube
		self.cube = self.createCube(-1, *(5, 5, 13))
		self.cubeDeclaration()

	# Receives the name of a type and return its code
	def typeToCode(self, typeName):
		return self.dicTypes[typeName]

	# Receives the name of an operators and returns its code
	def operatorToCode(self, operatorName):
		return self.dicOperators[operatorName]

	''' *semanticValidation*
		Description:
			Function that receives tokens of the two operands as well as the operators and
			returns the corresponding type of the semantic cube.
		
		Params:
			operator -> Operator
			operand1 -> First operand
			operand2 -> Second operand
	'''
	def semanticValidation(self, operator, operand1, operand2):
		#print("Cube coordinates (x, y, z): ", operand1, operand2, operator)
		return self.cube[operand1][operand2][operator]

	def createCube(self, value, *dimensions):
		newCube = [[[value for _ in range(dimensions[2])] for _ in range(dimensions[1])] for _ in range(dimensions[0])]
		return newCube

	def cubeDeclaration(self):
		# Defining the intiial value of all the cube

		''' Assignment of valid combinations '''
		
		''' ------------ INT[0] ------------ '''

		''' INT[0] - INT[0] '''
		# Assignment Operator (0)
		self.cube[0][0][0] = 0

		#Arithmetic Operators (1 - 4)
		self.cube[0][0][1] = 0
		self.cube[0][0][2] = 0
		self.cube[0][0][3] = 0
		self.cube[0][0][4] = 0

		# Relational Operators (5 - 8)
		self.cube[0][0][5] = 2
		self.cube[0][0][6] = 2
		self.cube[0][0][7] = 2
		self.cube[0][0][8] = 2

		# Equality Operators (9 - 10)
		self.cube[0][0][9] = 2
		self.cube[0][0][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' INT[0] - FLOAT[1] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		self.cube[0][1][1] = 1
		self.cube[0][1][2] = 1
		self.cube[0][1][3] = 1
		self.cube[0][1][4] = 1

		# Relational Operators (5 - 8)
		self.cube[0][1][5] = 2
		self.cube[0][1][6] = 2
		self.cube[0][1][7] = 2
		self.cube[0][1][8] = 2

		# Equality Operators (9 - 10)
		self.cube[0][1][9] = 2
		self.cube[0][1][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' INT[0] - BOOL[2] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' INT[0] - STRING[3] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' INT[0] - OBJ[4] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' ------------ FLOAT[1] ------------ '''

		''' FLOAT[1] - INT[0] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		self.cube[1][0][1] = 1
		self.cube[1][0][2] = 1
		self.cube[1][0][3] = 1
		self.cube[1][0][4] = 1

		# Relational Operators (5 - 8)
		self.cube[1][0][5] = 2
		self.cube[1][0][6] = 2
		self.cube[1][0][7] = 2
		self.cube[1][0][8] = 2
		
		# Equality Operators (9 - 10)
		self.cube[1][0][9] = 2
		self.cube[1][0][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' FLOAT[1] - FLOAT[1] '''
		# Assignment Operator (0)
		self.cube[1][1][0] = 1

		#Arithmetic Operators (1 - 4)
		self.cube[1][1][1] = 1
		self.cube[1][1][2] = 1
		self.cube[1][1][3] = 1
		self.cube[1][1][4] = 1

		# Relational Operators (5 - 8)
		self.cube[1][1][5] = 2
		self.cube[1][1][6] = 2
		self.cube[1][1][7] = 2
		self.cube[1][1][8] = 2

		# Equality Operators (9 - 10)
		self.cube[1][1][9] = 2
		self.cube[1][1][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' FLOAT[1] - BOOL[2] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' FLOAT[1] - STRING[3] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' FLOAT[1] - OBJ[4] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' ------------ BOOL[2] ------------ '''

		''' BOOL[2] - INT[0] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' BOOL[2] - FLOAT[1] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' BOOL[2] - BOOL[2] '''
		# Assignment Operator (0)
		self.cube[2][2][0] = 2

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		self.cube[2][2][5] = 2
		self.cube[2][2][6] = 2
		self.cube[2][2][7] = 2
		self.cube[2][2][8] = 2

		# Equality Operators (9 - 10)
		self.cube[2][2][9] = 2
		self.cube[2][2][10] = 2

		# Logical Operators (11 - 12)
		self.cube[2][2][11] = 2
		self.cube[2][2][12] = 2

		''' BOOL[2] - STRING[3] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' BOOL[2] - OBJ[4] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR



		''' ------------ STRING[3] ------------ '''

		''' STRING[3] - INT[0] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' STRING[3] - FLOAT[1] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' STRING[3] - BOOL[2] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' STRING[3] - STRING[3] '''
		# Assignment Operator (0)
		self.cube[3][3][0] = 3

		#Arithmetic Operators (1 - 4)
		self.cube[3][3][1] = 3

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		self.cube[3][3][9] = 2
		self.cube[3][3][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' STRING[3] - OBJ[4] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' ------------ OBJ[4] ------------ '''

		''' OBJ[4] - INT[0] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' OBJ[4] - FLOAT[1] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' OBJ[4] - BOOL[2] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' OBJ[4] - STRING[3] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		# ALL ERROR

		# Logical Operators (11 - 12)
		# ALL ERROR

		''' OBJ[4] - OBJ[4] '''
		# Assignment Operator (0)
		# ALL ERROR

		#Arithmetic Operators (1 - 4)
		# ALL ERROR

		# Relational Operators (5 - 8)
		# ALL ERROR

		# Equality Operators (9 - 10)
		self.cube[4][4][9] = 2
		self.cube[4][4][10] = 2

		# Logical Operators (11 - 12)
		# ALL ERROR