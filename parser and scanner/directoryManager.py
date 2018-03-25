import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser

class directoryManager():
    def __init__(self):
        self.dictClasses = {}
        self.dictGlobalsVars = {}
        self.dictFunctions = {}

    def addClassToDirectory(self, objClass):
        print("Create class")
        self.dictClasses.update({objClass.name : objClass})
    
    def addGlobalsToDirectory(self, objVariable):
        self.dictGlobalsVars.update({objVariable.name : objVariable})

    def addFunctionToDirectory(self, objFunction):
        self.dictFunctions.update({objFunction.name : objFunction})
