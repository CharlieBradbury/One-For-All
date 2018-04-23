import sys
from antlr4 import *

class scope():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.varsDirectory = dict()
        self.routinesDirectory = dict()
        self.classesDirectory = dict()