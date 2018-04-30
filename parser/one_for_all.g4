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
	TOK_PROGRAM TOK_ID TOK_SEMICOLON (classes)? (variables)? (routines)? restOfProgram;

restOfProgram:
    main;

classes:
    (class_definition)+;

class_definition:
	TOK_CLASS TOK_ID inheritance TOK_LBRACE (class_public)? (class_private)? TOK_RBRACE;

inheritance:
    (TOK_COLON TOK_ID)?;

class_public:
    (TOK_PUBLIC variables | TOK_PUBLIC routines)+;

class_private:
     (TOK_PRIVATE variables | TOK_PRIVATE routines)+;

routines:
    (routine_definition)+;

routine_definition:
    TOK_FUNCTION data_type TOK_ID TOK_LPAREN (parameters)? TOK_RPAREN block;

parameters:
    TOK_VAR data_type TOK_ID (TOK_LBRACKET expressions neuro_array TOK_RBRACKET)? parameters_recursive;

parameters_recursive:
    (TOK_COMMA  TOK_VAR data_type TOK_ID (TOK_LBRACKET expressions neuro_array TOK_RBRACKET)?)*;

neuro_array:
;

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
    (assignment | condition | loop | output | input_ | variables |return_expr)*;

assignment:
	 id_ TOK_EQUAL expressions TOK_SEMICOLON;

condition:
    TOK_IF TOK_LPAREN expressions TOK_RPAREN neuro_if block condition_else neuro_endif;

neuro_if:
;

neuro_endif:
;

loop:
    TOK_WHILE TOK_LPAREN expressions TOK_RPAREN block;

input_:
    TOK_READ TOK_LPAREN STRING TOK_COMMA TOK_ID TOK_RPAREN TOK_SEMICOLON;

output:
	TOK_WRITE TOK_LPAREN (expressions) (TOK_COMMA)?)+ TOK_RPAREN TOK_SEMICOLON;

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
	(id_definition_)+;

id_definition_:
    TOK_ID | evaluate_class | evaluate_function | evaluate_array;

evaluate_class:
	TOK_ID TOK_DOT TOK_ID(TOK_LPAREN expressions TOK_RPAREN)?;

evaluate_function:
	TOK_ID TOK_LPAREN (expressions (TOK_COMMA)?)* neuro_params TOK_RPAREN;

neuro_params:
;

evaluate_array:
	TOK_ID TOK_LBRACKET expressions TOK_RBRACKET;
