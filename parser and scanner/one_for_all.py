import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from ruleManager import ruleManager

def main(argv):
	input = FileStream(argv[1])
	lexer = one_for_allLexer(input)
	stream = CommonTokenStream(lexer)
	parser = one_for_allParser(stream)
	print("Start Walking...")
	tree = parser.programa()
	walker = ParseTreeWalker()
	oneforAll = ruleManager()
	walker.walk(oneforAll, tree)
    

if __name__ == '__main__':
	main(sys.argv)
	
