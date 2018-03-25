import sys
from antlr4 import *
from one_for_allLexer import one_for_allLexer
from one_for_allParser import one_for_allParser
from one_for_allListener import one_for_allListener
from directoryManager import directoryManager
from objClass import objClass
from objFunction import objFunction
from objVariable import objVariable
from collections import OrderedDict

class ruleManager(one_for_allListener):
    def __init__(self):
        self.rows = []
        self.header = []
        self.current = []

        self.directory = directoryManager()
        self.classes = []
        self.privateMethod = []
        self.publicMethod = []
        self.privateVariable = []
        self.publicVariable = []

    def enterClasses(self, ctx):
        # By default, all classes have None as parent
        for val in ctx.TOK_ID():
            lst = [val, None]
            self.classes.append(lst)

    def enterInheritance(self, ctx):
        try:
            self.classes[-1][1]= ctx.TOK_ID().getText()
        except:
            print("No inheritance")

    def printDictionary(self):
        for x in self.classes:
            print(x[0],':',x[1])

    def exitClasses(self, ctx):
        #Create class objects
        for obj in self.classes:
            _obj = objClass("id",obj[0],obj[1])
            self.directory.addClassToDirectory(_obj)
        self.printDictionary()

    def enterVariables(self, ctx):
        print(ctx.parentCtx.getText())
