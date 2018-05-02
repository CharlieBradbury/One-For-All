'''
import sys
import os
from antlr4 import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parser.one_for_allLexer import one_for_allLexer
from parser.one_for_allParser import one_for_allParser
from parser.one_for_allListener import one_for_allListener
from ruleManager import ruleManager
'''

import sys
import os
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from ruleManager import ruleManager
from virtualMachine import virtualMachine

def main(argv):
	input = argv[1]
	fileName = str(input)

	# Create and run virtual machine
	vMachine = virtualMachine(fileName)
	vMachine.run()

if __name__ == '__main__':
	main(sys.argv)
