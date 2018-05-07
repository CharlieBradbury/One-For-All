grammar one_for_all;

STRING : '"'.*?'"';
FLOAT : [0-9]+('.'[0-9]+);
INT : [0-9]+;
BOOLEAN : TRUE | FALSE;
TOK_AND : '&&' ;
TOK_OR  : '||' ;
TRUE : 'true' ;
FALSE : 'false';
TOK_IF : 'if';
TOK_ELSE : 'else';
TOK_WHILE : 'while';
TOK_VAR : 'var';
TOK_PROGRAM : 'program';
TOK_CLASS : 'class';
TOK_PRIVATE : 'private';
TOK_PUBLIC : 'public';
TOK_MAIN : 'main';
TOK_INIT : 'init';
TOK_READ : 'read';
TOK_FUNCTION : 'function';
TOK_WRITE :'write';
TOK_LPAREN : '('; 
TOK_RPAREN : ')';
TOK_LBRACE : '{';
TOK_RBRACE : '}';
TOK_LBRACKET : '[';
TOK_RBRACKET : ']';
TOK_PLUS : '+';
TOK_MINUS : '-';
TOK_MULTIPLICATION : '*';
TOK_DIVISION : '/';
TOK_EQUAL : '=';
TOK_DIFFERENT : '!=';
TOK_GREATER : '>';
TOK_LESS : '<';
TOK_GREATER_EQ : '>=';
TOK_LESS_EQ : '<=';
TOK_SAME : '==';
TOK_SEMICOLON : ';';
TOK_COLON : ':';
TOK_DOT : '.';
TOK_COMMA : ',';
TOK_INT : 'int';
TOK_FLOAT : 'float';
TOK_BOOLEAN : 'bool';
TOK_STRING : 'string';
TOK_RETURN : 'return';
TOK_ID : [a-zA-Z0-9]+;
ESPACIOS : [ \n\t\r] -> skip;

programa: 
	TOK_PROGRAM TOK_ID TOK_SEMICOLON ? (variables)? neuro_jump_main (classes)? (routines)? restOfProgram;

neuro_jump_main:
;

restOfProgram:
    main;

classes:
    (class_definition)+;

class_definition:
	TOK_CLASS TOK_ID (inheritance)? TOK_LBRACE (class_public)? (class_private)? constructor TOK_RBRACE;

inheritance:
    TOK_COLON TOK_ID;

neuro_inheritance:
;

class_public:
    (TOK_PUBLIC variables | TOK_PUBLIC routines)+;

class_private:
     (TOK_PRIVATE variables | TOK_PRIVATE routines)+;

constructor:
	TOK_INIT TOK_LPAREN (parameters)? TOK_RPAREN block;

routines:
    (routine_definition)+;

routine_definition:
    TOK_FUNCTION data_type TOK_ID TOK_LPAREN (parameters)? TOK_RPAREN block;

parameters:
    TOK_VAR data_type TOK_ID (parameters_recursive)?;

parameters_recursive:
    (TOK_COMMA TOK_VAR data_type TOK_ID)+;

variables:
    (variable_definition | variable_assign)+;

variable_definition:
	TOK_VAR data_type TOK_ID (TOK_LBRACKET expressions TOK_RBRACKET)? (TOK_COMMA TOK_ID (TOK_LBRACKET expressions TOK_RBRACKET)? )* TOK_SEMICOLON;

variable_assign:
	TOK_VAR data_type TOK_ID (TOK_LBRACKET expressions TOK_RBRACKET)? TOK_EQUAL expressions (TOK_COMMA TOK_ID (TOK_LBRACKET expressions TOK_RBRACKET)? TOK_EQUAL expressions)* TOK_SEMICOLON;

data_type:
    (TOK_INT | TOK_FLOAT | TOK_STRING | TOK_BOOLEAN | TOK_ID);

main:
    TOK_MAIN block;

block:
   TOK_LBRACE statute TOK_RBRACE;

return_expr:
	TOK_RETURN expressions TOK_SEMICOLON;

statute:
    (assignment | condition | loop | output | input_ | variables |return_expr | init_class)*;

assignment:
	 id_ TOK_EQUAL expressions TOK_SEMICOLON;

condition:
    TOK_IF TOK_LPAREN expressions TOK_RPAREN neuro_if block condition_else neuro_endif;

neuro_if:
;

neuro_endif:
;

loop:
    TOK_WHILE neuro_while_begin TOK_LPAREN expressions TOK_RPAREN neuro_while_expression block neuro_while_end;

neuro_while_begin:
;

neuro_while_expression:
;

neuro_while_end:
;

input_:
    TOK_READ TOK_LPAREN expressions TOK_COMMA TOK_ID TOK_RPAREN TOK_SEMICOLON;

output:
	TOK_WRITE TOK_LPAREN expressions neuro_getOutput (output_recursive)? neuro_finishOutput TOK_RPAREN TOK_SEMICOLON;
	
output_recursive:
	(TOK_COMMA expressions neuro_getOutput)+;
	
neuro_getOutput:
;
	
neuro_finishOutput:
;

condition_else:
    (neuro_else TOK_ELSE block)?;

neuro_else:
;

expressions:
	(expression_definition)+;

expression_definition: 
    relational_exprs ((token_and | token_or) relational_exprs neuro_expression)?;

neuro_expression:
	;

token_and:
	TOK_AND;

token_or:
	TOK_OR;

relational_exprs:
	(relational_expr_definition)+;

relational_expr_definition:
    sumMinus_exprs ((token_same | token_different | token_greater | token_greater_eq | token_less | token_less_eq) sumMinus_exprs neuro_relational)?;

neuro_relational:
	;

token_same:
	TOK_SAME;

token_different:
	TOK_DIFFERENT;

token_greater:
	TOK_GREATER;

token_greater_eq:
	TOK_GREATER_EQ;

token_less:
	TOK_LESS;

token_less_eq:
	TOK_LESS_EQ;

sumMinus_exprs:
	(sumMinus_expr_definition)+;

sumMinus_expr_definition:
    multiDiv_exprs neuro_sumMinus (token_plus | token_minus)?;

neuro_sumMinus:
	;

token_plus:
	TOK_PLUS;

token_minus:
	TOK_MINUS;

multiDiv_exprs:
	(multiDiv_expr_definition)+;

multiDiv_expr_definition:
    factor neuro_multiDiv (token_multiplication | token_division)?;

neuro_multiDiv:
	;

token_multiplication:
	TOK_MULTIPLICATION;

token_division:
	TOK_DIVISION;

factor:
    (token_lparen expressions token_rparen) | constant;

token_lparen:
	TOK_LPAREN;

token_rparen:
	TOK_RPAREN;

constant: 
	(FLOAT | INT | STRING | BOOLEAN | id_);

id_:
	id_definition_;

id_definition_:
	evaluate_method | evaluate_function | evaluate_class | evaluate_array | TOK_ID;
	
init_class:
	TOK_ID TOK_EQUAL TOK_INIT TOK_ID TOK_LPAREN (expressions neuro_initEval (TOK_COMMA)?)* neuro_createConstructor TOK_RPAREN TOK_SEMICOLON;
	
neuro_initEval:
;

neuro_createConstructor:
;

evaluate_class:
	TOK_ID TOK_DOT TOK_ID;

evaluate_method:
	evaluate_method_aux neuro_params;

evaluate_method_aux:
	TOK_ID TOK_DOT TOK_ID TOK_LPAREN (expressions (TOK_COMMA expressions)*)? TOK_RPAREN;

evaluate_function:
	evaluate_function_aux neuro_params;

evaluate_function_aux:
	TOK_ID TOK_LPAREN (expressions (TOK_COMMA expressions)*)? TOK_RPAREN;

neuro_params:
;

evaluate_array:
	TOK_ID TOK_LBRACKET expressions TOK_RBRACKET;