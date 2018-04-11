import sys
from antlr4 import *
sys.path.append('C:\\Users\\dadel\\Desktop\\One-For-All\\parser')
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser

class scopeManager():
    def __init__(self, parent):
        self.parent = parent;
        self.varsDirectory = dict()
        self.routinesDirectory = dict()
        self.classesDirectory = dict()