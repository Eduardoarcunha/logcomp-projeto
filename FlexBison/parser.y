%{
#include "parser.tab.h"
#include <stdio.h>
extern int yylval;
void yyerror(const char *s) {
    extern int yylineno;  // Line number from Flex
    fprintf(stderr, "Error at line %d: %s\n", yylineno, s);
}
%}

%debug

%token NEWLINE LBRACE RBRACE LPAREN RPAREN SEMICOLON EQUALS OR AND EQUALITY GREATER LESS PLUS MINUS MULT DIV NOT PRINT IF ELSE COMBAT WHILE PROGRESS ACTION CHARACTER MONSTER INT INPUT IDENTIFIER NUMBER STRING

%start PROGRAM

%%

PROGRAM: 
    | PROGRAM STATEMENT
    ;

STATEMENT: 
    ASSIGNMENT SEMICOLON
    | PRINT_STATEMENT SEMICOLON
    | IF_STATEMENT NEWLINE
    | COMBAT_LOOP NEWLINE
    | VAR SEMICOLON
    | ACTION_STATEMENT NEWLINE
    | NEWLINE
    ;

ASSIGNMENT:
    IDENTIFIER EQUALS BOOLEXPRESSION
    ;

PRINT_STATEMENT:
    PRINT LPAREN BOOLEXPRESSION RPAREN
    ;

IF_STATEMENT:
    IF BOOLEXPRESSION BLOCK
    | IF BOOLEXPRESSION BLOCK ELSE BLOCK
    ;


COMBAT_LOOP:
    COMBAT SEMICOLON ASSIGNMENT SEMICOLON WHILE BOOLEXPRESSION PROGRESS ASSIGNMENT BLOCK
    ;

ACTION_STATEMENT:
    ACTION IDENTIFIER LBRACE STATEMENT_LIST "act" RBRACE
    ;


VAR:
    TYPE IDENTIFIER EQUALS BOOLEXPRESSION
    ;

TYPE:
    CHARACTER
    | MONSTER
    | INT
    ;

BOOLEXPRESSION:
    BOOLTERM
    | BOOLEXPRESSION OR BOOLTERM
    ;

BOOLTERM:
    RELEXPRESSION
    | BOOLTERM AND RELEXPRESSION
    ;

RELEXPRESSION:
    EXPRESSION
    | EXPRESSION EQUALITY EXPRESSION
    | EXPRESSION GREATER EXPRESSION
    | EXPRESSION LESS EXPRESSION
    ;

EXPRESSION:
    TERM
    | EXPRESSION PLUS TERM
    | EXPRESSION MINUS TERM
    ;

TERM:
    FACTOR
    | TERM MULT FACTOR
    | TERM DIV FACTOR
    ;

FACTOR:
    LPAREN BOOLEXPRESSION RPAREN
    | PLUS FACTOR
    | MINUS FACTOR
    | NOT FACTOR
    | IDENTIFIER
    | NUMBER
    | STRING
    | INPUT LPAREN RPAREN
    ;

BLOCK:
    LBRACE STATEMENT_LIST RBRACE
    ;


STATEMENT_LIST:
    | STATEMENT_LIST STATEMENT
    ;
    
%%

int main(void) {
    yydebug = 0;  // Activate Bison debugging
    return yyparse();
}