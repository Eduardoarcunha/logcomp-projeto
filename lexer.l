%{
#include "parser.tab.h"
#include <stdio.h> // Include standard I/O for printf
extern int yylval;
%}

%%

[ \t]+           { /* ignore whitespace */ }
\n               { printf("Matched NEWLINE\n"); return NEWLINE; }
"{"              { printf("Matched LBRACE\n"); return LBRACE; }
"}"              { printf("Matched RBRACE\n"); return RBRACE; }
"("              { printf("Matched LPAREN\n"); return LPAREN; }
")"              { printf("Matched RPAREN\n"); return RPAREN; }
";"              { printf("Matched SEMICOLON\n"); return SEMICOLON; }
"="              { printf("Matched EQUALS\n"); return EQUALS; }
"||"             { printf("Matched OR\n"); return OR; }
"&&"             { printf("Matched AND\n"); return AND; }
"=="             { printf("Matched EQUALITY\n"); return EQUALITY; }
">"              { printf("Matched GREATER\n"); return GREATER; }
"<"              { printf("Matched LESS\n"); return LESS; }
"+"              { printf("Matched PLUS\n"); return PLUS; }
"-"              { printf("Matched MINUS\n"); return MINUS; }
"*"              { printf("Matched MULT\n"); return MULT; }
"/"              { printf("Matched DIV\n"); return DIV; }
"!"              { printf("Matched NOT\n"); return NOT; }
"Println"        { printf("Matched PRINTLN\n"); return PRINTLN; }
"if"             { printf("Matched IF\n"); return IF; }
"else"           { printf("Matched ELSE\n"); return ELSE; }
"combat"         { printf("Matched COMBAT\n"); return COMBAT; }
"while"          { printf("Matched WHILE\n"); return WHILE; }
"progress"       { printf("Matched PROGRESS\n"); return PROGRESS; }
"action"         { printf("Matched ACTION\n"); return ACTION; }
"character"      { printf("Matched CHARACTER\n"); return CHARACTER; }
"monster"        { printf("Matched MONSTER\n"); return MONSTER; }
"int"            { printf("Matched INT\n"); return INT; }
"Scanln"         { printf("Matched SCANLN\n"); return SCANLN; }
[a-zA-Z_][a-zA-Z0-9_]*  { printf("Matched IDENTIFIER\n"); yylval = strdup(yytext); return IDENTIFIER; }
[0-9]+           { printf("Matched NUMBER\n"); yylval = atoi(yytext); return NUMBER; }
\"[^\"]*\"       { printf("Matched STRING\n"); yylval = strdup(yytext); return STRING; }

%%

int yywrap(void) {
    return 1;
}
