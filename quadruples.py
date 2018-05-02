# MATH OPERATIONS 
# ADD_OP = 1
# SUBSTRACT_OP = 2
# MULTIPLY_OP = 3
# DIVIDE_OP = 4
#
# LOGIC OPERATIONS
# OR = 5 
# AND = 6
# EQUAL = 7
# NOT_EQUAL =  8
# LESS_EQUAL_THAN = 9
# GREATER_EQUAL_THAN = 10
# LESS_THAN = 11
# GREATER_THAN = 12
#
# JUMPS
# GOTOF = 13
# GOTO = 14
# GOSUB = 15
class quadruples():
    def __init__(self, counter, opt, opd1, opd2, result):
        self.id = counter
        self.opt = opt
        self.opd1 = opd1
        self.opd2 = opd2
        self.result = result