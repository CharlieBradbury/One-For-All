import sys
from antlr4 import *
from variableDirectory import variableDirectory
from functionDirectory import functionDirectory

class scope():
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.vars = variableDirectory()
        self.function = functionDirectory()
        self.classes = dict()
        self.objects = dict()
