import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser

def main(argv):
	input = FileStream(argv[1])
	lexer = one_for_allLexer(input)
	stream = CommonTokenStream(lexer)
	parser = one_for_allParser(stream)
	tree = parser.programa()

if __name__ == '__main__':
	main(sys.argv)
