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
        self.directory = directoryManager()
        self.classes = []             
        self.privateMethod = []       #return_type, name, list of parameters
        self.publicMethod = []        #return_type, name, list of parameters
        self.privateVariable = []
        self.publicVariable = []
        self.functions = []          #return_type, name, list of parameters

        self.currentClass = ""
        self.isClassMethod = False
        self.isPublic = True

    def enterClasses(self, ctx):
        # By default, all classes have None as parent

        # No public/ private variables or methods
        # lst[class_name, inheritance, public_vars, public_methods, private_vars, private_methods]
        print(self.currentClass)
        for val in ctx.TOK_ID():
            lst = [val, None,None,None,None,None]
            self.classes.append(lst)

    def enterInheritance(self, ctx):
        try:
            self.classes[-1][1]= ctx.TOK_ID().getText()
        except:
            pass

    def enterClass_public(self, ctx):
        counter = 0
        #For variables
        while ctx.variables(counter) is not None:
            type = ctx.variables(counter).data_type(0).getText()
            names = ctx.variables(counter).TOK_ID()
            try:
                lst = [type, names.getText()]
                self.publicVariable.append(lst)
            except:
                for name in names:
                    lst = [type, name.getText()]
                    self.publicVariable.append(lst)   
         
            try:
                counter_ids = 0
                others = ctx.variables(counter).other_var(counter_ids)
                for id in others.TOK_ID():   
                    lst_other = [type, id.getText()]
                    self.publicVariable.append(lst_other)
                counter_ids = counter_ids + 1
            except:
                pass
            counter = counter + 1
        
        #For methods
        counterMethods = 0
        if ctx.funcs(counterMethods) is not None:
            self.isClassMethod = True
            self.isPublic = True
      
    def enterClass_private(self, ctx):
        counter = 0
        while ctx.variables(counter) is not None:
            type = ctx.variables(counter).data_type(0).getText()
            names = ctx.variables(counter).TOK_ID()
            try:
                lst = [type, names.getText()]
                self.privateVariable.append(lst)
            except:
                for name in names:
                    lst = [type, name.getText()]
                    self.privateVariable.append(lst)   
         
            try:
                counter_ids = 0
                others = ctx.variables(counter).other_var(counter_ids)
                for id in others.TOK_ID():   
                    lst_other = [type, id.getText()]
                    self.privateVariable.append(lst_other)
                counter_ids = counter_ids + 1
            except:
                pass
            counter = counter + 1
        
        #For methods
        counterMethods = 0
        if ctx.funcs(counterMethods) is not None:
            self.isClassMethod = True
            self.isPublic = False

    def enterFuncs (self, ctx):
        try:
            type = ctx.data_type(0).getText()
            name = ctx.TOK_ID(0).getText()
            method = [type, name]
            lst_parameters = []
            first_parameter = ctx.parameters(0).TOK_ID().getText()
            type_first =  ctx.parameters(0).data_type().getText()

            lst = [type_first, first_parameter]
            #If public method from a class
            if self.isClassMethod and self.isPublic:
                lst_parameters.append(lst)
                counter_func = 0
                counter_params = 0
                try:
                    while ctx.parameters(counter_func).parameters_recursive() is not None:
                        type = ctx.parameters(counter_func).parameters_recursive().data_type(counter_params).getText()
                        id = ctx.parameters(counter_func).parameters_recursive().TOK_ID(counter_params).getText()
                        lst  = [type, id]
                        lst_parameters.append(lst)
                        counter_params = counter_params + 1
                except:
                    pass
                
                method.append(lst_parameters)
                self.publicMethod = method

            #If private method from a class   
            if self.isClassMethod and self.isPublic is False:
                lst_parameters.append(lst)
                counter_func = 0
                counter_params = 0
                try:
                    while ctx.parameters(counter_func).parameters_recursive() is not None:
                        type = ctx.parameters(counter_func).parameters_recursive().data_type(counter_params).getText()
                        id = ctx.parameters(counter_func).parameters_recursive().TOK_ID(counter_params).getText()
                        lst  = [type, id]
                        lst_parameters.append(lst)
                        counter_params = counter_params + 1
                except:
                    pass
                
                method.append(lst_parameters)
                self.privateMethod = method
            
            #If is just a function 
            if self.isClassMethod is False:
                lst_parameters.append(lst)
                counter_func = 0
                counter_params = 0
                try:
                    while ctx.parameters(counter_func).parameters_recursive() is not None:
                        type = ctx.parameters(counter_func).parameters_recursive().data_type(counter_params).getText()
                        id = ctx.parameters(counter_func).parameters_recursive().TOK_ID(counter_params).getText()
                        lst  = [type, id]
                        lst_parameters.append(lst)
                        counter_params = counter_params + 1
                except:
                    pass
                
                method.append(lst_parameters)
                self.functions = method
                print(self.functions)

        except:
            pass
    
    def exitFuncs(self, ctx):
        pass

    def exitClass_public(self, ctx):
        print("Public variables", self.publicVariable)
        print("Public Methods", self.publicMethod)

    def exitClass_private(self, ctx):
        print("Private",self.privateMethod)   

    def printDictionary(self):
        for x in self.classes:
            print(x[0],':',x[1])
    
    def exitClasses(self, ctx):
        self.isClassMethod = False
        #Create class objects
        for obj in self.classes:
            _obj = objClass("id",obj[0],obj[1])
            self.directory.addClassToDirectory(_obj)
        #self.printDictionary()


    
    
    