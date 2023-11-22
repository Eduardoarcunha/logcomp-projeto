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
"%"                  { printf("Token: MODULO\n"); return MODULO;}
"!"                  { printf("Token: NOT\n"); return NOT; }
"."                  { printf("Token: CONCAT\n"); return CONCAT; }
","                  { printf("Token: COMMA\n"); return COMMA; }
"print"              { printf("Token: PRINT\n"); return PRINT; }
"if"                 { printf("Token: IF\n"); return IF; }
"else"               { printf("Token: ELSE\n"); return ELSE; }
"combat"             { printf("Token: COMBAT\n"); return COMBAT; }
"while"              { printf("Token: WHILE\n"); return WHILE; }
"progress"           { printf("Token: PROGRESS\n"); return PROGRESS; }
"action"             { printf("Token: ACTION\n"); return ACTION; }
"act"                { printf("Token: ACT\n"); return ACT; }
"string"             { printf("Token: TYPE\n"); return TYPE; }
"int"                { printf("Token: TYPE\n"); return TYPE; }
"input"              { printf("Token: INPUT\n"); return INPUT; }
"roll"               { printf("Token: ROLL\n"); return ROLL; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("Token: IDENTIFIER (%s)\n", yytext); yylval = strdup(yytext); return IDENTIFIER; }
[0-9]+               { printf("Token: NUMBER (%s)\n", yytext); yylval = atoi(yytext); return NUMBER; }
\"[^"]*\"            { printf("Token: STRING (%s)\n", yytext); yylval = strdup(yytext); return STRING; }
.                    { printf("Token: UNKNOWN (%c)\n", *yytext); /* handle unrecognized characters */ }
%%

int yywrap(void) {
    return 1;
}
