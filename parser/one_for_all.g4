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
TOK_ID : [a-zA-Z0-9]+;
TOK_RETURN : 'return';
ESPACIOS : [ \n\t\r] -> skip;


programa: 
	TOK_PROGRAM TOK_ID TOK_SEMICOLON classes (variables)? (routines)? restOfProgram;

restOfProgram:
    main;

classes:
    (classDefinition)+;

classDefinition:
	TOK_CLASS TOK_ID inheritance TOK_LBRACE (class_public)? (class_private)? TOK_RBRACE;

inheritance:
    (TOK_COLON TOK_ID)?;

class_public:
    (TOK_PUBLIC variables| TOK_PUBLIC routines)+;

class_private:
     (TOK_PRIVATE variables| TOK_PRIVATE routines)+;

routines:
    (routineDefinition)+;

routineDefinition:
    TOK_FUNCTION data_type TOK_ID TOK_LPAREN (parameters)? TOK_RPAREN block;

parameters:
    TOK_VAR data_type TOK_ID parameters_recursive;

parameters_recursive:
    (TOK_COMMA  TOK_VAR data_type TOK_ID)*;

variables:
    (variableDefinition)+;

variableDefinition:
	TOK_VAR data_type TOK_ID (TOK_COMMA TOK_ID)* TOK_SEMICOLON;

data_type:
    (TOK_INT | TOK_FLOAT | TOK_STRING | TOK_BOOLEAN | TOK_ID);

main:
    TOK_MAIN block;

block:
    TOK_LBRACE statute TOK_RBRACE;

statute:
    (assignment | condition | loop | output | input_ | variables)*;

assignment:
    id_ TOK_EQUAL expr TOK_SEMICOLON statute;

condition:
    TOK_IF TOK_LPAREN expr TOK_RPAREN  block (conditionelse)?;

loop:
    TOK_WHILE  TOK_LPAREN expr TOK_RPAREN block;


input_:
    TOK_READ TOK_LPAREN STRING TOK_COMMA TOK_ID TOK_RPAREN TOK_SEMICOLON statute;

output:
    TOK_WRITE TOK_LPAREN output_aux TOK_RPAREN TOK_SEMICOLON statute;

output_aux:
    (expr | STRING | escrituraaux);

escrituraaux: 
	(TOK_COMMA output_aux)*; 

conditionelse:
    TOK_ELSE block;

expr: 
    (relational_expr expr_aux)+;

expr_aux:
    (ruleand | ruleor)*;

ruleand:
    TOK_AND;

ruleor:
    TOK_OR;

relational_expr:
    sumMinus_expr (TOK_SAME | TOK_GREATER | TOK_GREATER_EQ | TOK_LESS | TOK_LESS_EQ | TOK_DIFFERENT)*;

sumMinus_expr:
    (multiDiv_expr regla4 expr_aux2)+;

expr_aux2:
    (rulesum | ruleminus)*;

rulesum:
    TOK_PLUS;

ruleminus:
    TOK_MINUS;

multiDiv_expr:
    (factor expr_aux3)+;

expr_aux3:
    (rulemultiply | ruledivide)*;

rulemultiply:
    TOK_MULTIPLICATION;

ruledivide:
    TOK_DIVISION;

factor:
    ((TOK_LPAREN expr TOK_RPAREN) | constant);

constant: (id_ | FLOAT | INT | STRING | BOOLEAN);

id_:
   TOK_ID getId (TOK_DOT TOK_ID (TOK_LPAREN expr TOK_RPAREN)? | TOK_LPAREN expr TOK_RPAREN | TOK_LBRACKET expr TOK_RBRACKET )*;

getId:
;

regla4:
;