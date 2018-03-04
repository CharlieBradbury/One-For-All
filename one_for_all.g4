grammar one_for_all;

STRING : '"'.*?'"';
FLOAT : [0-9]+('.'[0-9]+);
INT : [0-9]+;
BOOLEAN : TRUE | FALSE;
TOK_AND : '&&' ;
TOK_OR  : '||' ;
TOK_NOT : '!';
TRUE : 'true' ;
FALSE : 'false';
TOK_IF : 'if';
TOK_ELSE : 'else';
TOK_WHILE : 'while';
TOK_PRINT : 'print';
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
TOK_LBRACKET : '{';
TOK_RBRACKET : '}';
TOK_SUM : '+';
TOK_SUBSTRACTION : '-';
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
TOK_COMMA : ',';
TOK_INT : 'int';
TOK_FLOAT : 'float';
TOK_BOOLEAN : 'bool';
TOK_STRING : 'string';
TOK_ID : [a-zA-Z0-9]+;
ESPACIOS : [ \n\t\r] -> skip;


programa: 
	TOK_PROGRAM TOK_ID TOK_SEMICOLON classes vars funcs main;

classes:
    TOK_CLASS TOK_ID inheritance TOK_LBRACKET class_public class_private TOK_RBRACKET classes;

inheritance:
    TOK_COLON TOK_ID
    |
    ;

class_public:
    TOK_PUBLIC TOK_COLON TOK_LBRACKET variable_declaration function_declaration TOK_RBRACKET;

class_private:
    TOK_PRIVATE TOK_COLON TOK_LBRACKET variable_declaration function_declaration TOK_RBRACKET;

variable_declaration:
    vars
    |
    ;

function_declaration:
    funcs
    |
    ;

funcs:
    TOK_FUNCTION type TOK_ID TOK_LPAREN parameters TOK_RPAREN block funcs;

parameters:
    TOK_VAR type TOK_ID TOK_COMMA parameters
    |
    ;

vars:
    TOK_VAR type TOK_ID other_var TOK_SEMICOLON vars;

other_var:
    TOK_COMMA TOK_ID other_var
    |
    ;

type:
    TOK_INT
    |
    TOK_FLOAT
    |
    TOK_STRING
    |
    TOK_BOOLEAN
    |
    TOK_ID
    ;

main:
    TOK_MAIN block;

block:
    TOK_LBRACKET statute TOK_RBRACKET
	;

statute:
    assignment
    |
    condition
    |
    loop
    |
    output
    |
    input
    |
    ;

assignment:
    TOK_ID TOK_EQUAL expr TOK_SEMICOLON statute;

condition:
    TOK_IF TOK_LPAREN expr TOK_RPAREN block conditionelse statute;

loop:
    TOK_WHILE TOK_LPAREN expr TOK_RPAREN block statute;

input:
    TOK_READ TOK_LPAREN STRING TOK_COMMA TOK_ID TOK_RPAREN TOK_SEMICOLON statute;

output:
    TOK_WRITE TOK_LPAREN output_aux  TOK_RPAREN TOK_SEMICOLON statute;

output_aux:
    expr
    |
    STRING
    |
    escrituraaux
    ;

escrituraaux: 
	TOK_COMMA output_aux escrituraaux |;