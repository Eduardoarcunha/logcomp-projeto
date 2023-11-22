# Linguagem de Programação C&C (Code and Code)

## Sobre este repositório

Este repositório tem como objetivo descrever a linguagem de programaçãop Code&Code e armazenar o código fonte do compilador desta desenvolvido para a disciplina de LogComp.

## EBNF

**PROGRAM = { DECLARATION | TOP_LEVEL_STATEMENT };**

**DECLARATION = "action", IDENTIFIER, "(", ARGS, ")", "TYPE", BLOCK, "\n" ;**

**ARGS = ( λ | IDENTIFIER, TYPE, {",", IDENTIFIER, TYPE} )**

**BLOCK = "{", "\n", {STATEMENT}, "}" ;**

**TOP_LEVEL_STATEMENT = ( λ | ASSIGNMENT, ";" | PRINT, ";" | IF | COMBAT_LOOP | VAR, ";" | ACTION), "\n" ;**

**STATEMENT = ( λ | ASSIGNMENT, ";" | PRINT, ";" | IF | COMBAT_LOOP | VAR, ";" | "act", ";"), "\n" ;**

**ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;**

**PRINT = "print", "(", BOOLEXPRESSION, ")" ;**

**IF = "if", BOOLEXPRESSION, BLOCK, {"else", BLOCK}" ;**

**COMBAT_LOOP = "combat", ";", ASSIGNMENT, ";", "while", BOOLEXPRESSION, "progress", ASSIGNMENT, BLOCK ;**

**VAR = TYPE, IDENTIFIER, "=", BOOLEXPRESSION ;**

**TYPE = ("string", "int")**

**BOOLEXPRESSION = BOOLTERM, {"||", BOOLTERM} ;**

**BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION} ;**

**RELEXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION} ;**

**EXPRESSION = TERM, { ("+" | "-"), TERM } ;**

**TERM = FACTOR, { ("*" | "/", ".", "%"), FACTOR } ;**

**FACTOR = (("+" | "-" | "!"), FACTOR) | string | NUMBER | "(", BOOLEXPRESSION, ")" | IDENTIFIER | "input", "(", ")" | "roll", "(", BOOLEXPRESSION, ")" ;**

**IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;**

**NUMBER = DIGIT, { DIGIT } ;**

**LETTER = ( a | ... | z | A | ... | Z ) ;**

**DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;**