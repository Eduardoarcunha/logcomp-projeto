%{
#include "parser.tab.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylval;
void yyerror(const char *s);
%}

%option yylineno

%%

[ \t]+               { /* ignore whitespace */ }
\n                   { printf("Token: NEWLINE\n"); return NEWLINE; }
"{"                  { printf("Token: LBRACE\n"); return LBRACE; }
"}"                  { printf("Token: RBRACE\n"); return RBRACE; }
"("                  { printf("Token: LPAREN\n"); return LPAREN; }
")"                  { printf("Token: RPAREN\n"); return RPAREN; }
";"                  { printf("Token: SEMICOLON\n"); return SEMICOLON; }
"="                  { printf("Token: EQUALS\n"); return EQUALS; }
"||"                 { printf("Token: OR\n"); return OR; }
"&&"                 { printf("Token: AND\n"); return AND; }
"=="                 { printf("Token: EQUALITY\n"); return EQUALITY; }
">"                  { printf("Token: GREATER\n"); return GREATER; }
"<"                  { printf("Token: LESS\n"); return LESS; }
"+"                  { printf("Token: PLUS\n"); return PLUS; }
"-"                  { printf("Token: MINUS\n"); return MINUS; }
"*"                  { printf("Token: MULT\n"); return MULT; }
"/"                  { printf("Token: DIV\n"); return DIV; }
"!"                  { printf("Token: NOT\n"); return NOT; }
"Println"            { printf("Token: PRINTLN\n"); return PRINTLN; }
"if"                 { printf("Token: IF\n"); return IF; }
"else"               { printf("Token: ELSE\n"); return ELSE; }
"combat"             { printf("Token: COMBAT\n"); return COMBAT; }
"while"              { printf("Token: WHILE\n"); return WHILE; }
"progress"           { printf("Token: PROGRESS\n"); return PROGRESS; }
"action"             { printf("Token: ACTION\n"); return ACTION; }
"character"          { printf("Token: CHARACTER\n"); return CHARACTER; }
"monster"            { printf("Token: MONSTER\n"); return MONSTER; }
"int"                { printf("Token: INT\n"); return INT; }
"Scanln"             { printf("Token: SCANLN\n"); return SCANLN; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("Token: IDENTIFIER (%s)\n", yytext); yylval = strdup(yytext); return IDENTIFIER; }
[0-9]+               { printf("Token: NUMBER (%s)\n", yytext); yylval = atoi(yytext); return NUMBER; }
\"[^"]*\"            { printf("Token: STRING (%s)\n", yytext); yylval = strdup(yytext); return STRING; }
.                    { printf("Token: UNKNOWN (%c)\n", *yytext); /* handle unrecognized characters */ }
%%

int yywrap(void) {
    return 1;
}
