import sys
from antlr4 import *

class scopeManager():
    def __init__(self, parent):
        self.parent = parent;
        self.varsDirectory = dict()
        self.routinesDirectory = dict()
        self.classesDirectory = dict()