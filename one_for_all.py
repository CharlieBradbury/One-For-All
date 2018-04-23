import sys
import os
from antlr4 import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from parser.one_for_allLexer import one_for_allLexer
from parser.one_for_allParser import one_for_allParser
from parser.one_for_allListener import one_for_allListener
from ruleManager import ruleManager

def main(argv):
	input = FileStream(argv[1])
	lexer = one_for_allLexer(input)
	stream = CommonTokenStream(lexer)
	parser = one_for_allParser(stream)

	tree = parser.programa()
	walker = ParseTreeWalker()
	oneforAll = ruleManager()
	walker.walk(oneforAll, tree)
    

if __name__ == '__main__':
	main(sys.argv)
