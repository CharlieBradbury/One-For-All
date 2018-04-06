import sys

''' * typesDeclaration *
	Description: 
		Function that creates the dictionary of types to codes
		Returns a dictionary that binds a string (data type) to an integer (code)

	Parameters: 
		None
'''
def typesDeclaration():
	# Dictionary of types to its code
	dicTypes = {'error' : -1}
	dicTypes['int'] = 0
	dicTypes['float'] = 1
	dicTypes['bool'] = 2
	dicTypes['string'] = 3
	dicTypes['obj'] = 4
	
	return dicTypes

''' * operatorsDeclaration *
	Description: 
		Function that creates the dictionary of data names to codes
		Returns a dictionary that binds a string (data type) to an integer (code)

	Parameters: 
		None
'''
def operatorsDeclaration():
	# Dictionary of operators to its code
	dicOperators = {'=' : 0}
	dicOperators['+'] = 1
	dicOperators['-'] = 2
	dicOperators['*'] = 3
	dicOperators['/'] = 4
	dicOperators['>'] = 5
	dicOperators['>='] = 6
	dicOperators['<'] = 7
	dicOperators['<='] = 8
	dicOperators['=='] = 9
	dicOperators['!='] = 10
	dicOperators['&&'] = 11
	dicOperators['||'] = 12

	return dicOperators

''' * typeToCode *
	Description: 
		Function that obtains the code of a type by searching on the dictionary
		Returns the code of the type given as parameter

	Parameters:
		Dictionary of types
		String representing the type to search
'''
def typeToCode(dicTypes, typeName):
	return dicTypes[typeName]

''' * operatorToCode *
	Description: 
		Function that obtains the code of an operator by searching on the dictionary
		Returns the code of the operator given as parameter

	Parameters:
		Dictionary of operators
		String representing the operator to search
'''
def operatorToCode(dicOperators, operatorName):
	return dicOperators[operatorName]

''' *cubeDeclaration*
	Description:
		Function for declarating the dimensions as well as the contents of the semantic cube
		Returns a list of lists of lists with the values to the datatype that is returned
		from involving two operands and one operator.
	
	Params:
		dimensions -> List of 3 elements, being the x, y and z length of the cube, respectively
		value -> Default value of all elements in the cube
'''
def cubeDeclaration(value, *dimensions):
	# Defining the intiial value of all the cube
	cube = [[[value for _ in range(dimensions[2])] for _ in range(dimensions[1])] for _ in range(dimensions[0])]

	''' Assignment of valid combinations '''
	
	''' ------------ INT[0] ------------ '''

	''' INT[0] - INT[0] '''
	# Assignment Operator (0)
	cube[0][0][0] = 0

	#Arithmetic Operators (1 - 4)
	cube[0][0][1] = 0
	cube[0][0][2] = 0
	cube[0][0][3] = 0
	cube[0][0][4] = 0

	# Relational Operators (5 - 8)
	cube[0][0][5] = 2
	cube[0][0][6] = 2
	cube[0][0][7] = 2
	cube[0][0][8] = 2

	# Equality Operators (9 - 10)
	cube[0][0][9] = 2
	cube[0][0][10] = 2

	# Logical Operators (11 - 12)
	# ALL ERROR

	''' INT[0] - FLOAT[1] '''
	# Assignment Operator (0)
	# ALL ERROR

	#Arithmetic Operators (1 - 4)
	cube[0][1][1] = 1
	cube[0][1][2] = 1
	cube[0][1][3] = 1
	cube[0][1][4] = 1

	# Relational Operators (5 - 8)
	cube[0][1][5] = 2
	cube[0][1][6] = 2
	cube[0][1][7] = 2
	cube[0][1][8] = 2

	# Equality Operators (9 - 10)
	cube[0][1][9] = 2
	cube[0][1][10] = 2

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
	cube[1][0][1] = 1
	cube[1][0][2] = 1
	cube[1][0][3] = 1
	cube[1][0][4] = 1

	# Relational Operators (5 - 8)
	cube[1][0][5] = 2
	cube[1][0][6] = 2
	cube[1][0][7] = 2
	cube[1][0][8] = 2
	
	# Equality Operators (9 - 10)
	cube[1][0][9] = 2
	cube[1][0][10] = 2

	# Logical Operators (11 - 12)
	# ALL ERROR

	''' FLOAT[1] - FLOAT[1] '''
	# Assignment Operator (0)
	cube[1][1][0] = 1

	#Arithmetic Operators (1 - 4)
	cube[1][1][1] = 1
	cube[1][1][2] = 1
	cube[1][1][3] = 1
	cube[1][1][4] = 1

	# Relational Operators (5 - 8)
	cube[1][1][5] = 2
	cube[1][1][6] = 2
	cube[1][1][7] = 2
	cube[1][1][8] = 2

	# Equality Operators (9 - 10)
	cube[1][1][9] = 2
	cube[1][1][10] = 2

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
	cube[2][2][0] = 2

	#Arithmetic Operators (1 - 4)
	# ALL ERROR

	# Relational Operators (5 - 8)
	cube[2][2][5] = 2
	cube[2][2][6] = 2
	cube[2][2][7] = 2
	cube[2][2][8] = 2

	# Equality Operators (9 - 10)
	cube[2][2][9] = 2
	cube[2][2][10] = 2

	# Logical Operators (11 - 12)
	cube[2][2][11] = 2
	cube[2][2][12] = 2

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
	cube[3][3][0] = 3

	#Arithmetic Operators (1 - 4)
	cube[3][3][1] = 3

	# Relational Operators (5 - 8)
	# ALL ERROR

	# Equality Operators (9 - 10)
	cube[3][3][9] = 2
	cube[3][3][10] = 2

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
	cube[4][4][9] = 2
	cube[4][4][10] = 2

	# Logical Operators (11 - 12)
	# ALL ERROR

	return cube

''' *semanticValidation*
	Description:
		Function that receives tokens of the two operands as well as the operators and
		returns the corresponding type of the semantic cube.
	
	Params:
		cube -> Semantic cube
		operator -> Operator
		operand1 -> First operand
		operand2 -> Second operand
'''
def semanticValidation(cube, operator, operand1, operand2):
	print("Cube coordinates (x, y, z): ", operand1, operand2, operator)
	return cube[operand1][operand2][operator]

''' Program to test semantic cube is working by reading user input (E.g.: int + int) and showing
the corresponding type depending if its a valid expression'''
if __name__ == "__main__":

	''' By default, all the elements of the cube are marked as error since
	most of the combinations are not valid. Valid combinations are set manually '''
	cube = cubeDeclaration(-1, *(5, 5, 13))

	# Call functions to obtain dictionary of types and operators
	dicTypes = typesDeclaration()
	dicOperators = operatorsDeclaration()

	while True:
	# Read user input
		expression = input("Provide expression (E.g.: int + int): ")

		# Obtain tokens
		tokens = expression.split(' ')

		# Convert tokens to codes
		operand1 = typeToCode(dicTypes, tokens[0])
		operator = operatorToCode(dicOperators, tokens[1])
		operand2 = typeToCode(dicTypes, tokens[2])

		# Do semantic validation
		resultType = semanticValidation(cube, operator, operand1, operand2)

		# Display result
		if resultType == -1:
			print("Error: Invalid operation")
		else:
			
			for key, value in dicTypes.items():
				if resultType == value:
					resultName = key

			print("Valid operation, it returns type", resultName)
			print(" ")