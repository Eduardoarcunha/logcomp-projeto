# Linguagem de Programação C&C (Code and Code)

## Sobre este repositório

Este repositório tem como objetivo descrever a linguagem de programaçãop Code&Code e armazenar o código fonte do compilador desta desenvolvido para a disciplina de LogComp.

## EBNF

**PROGRAM = { STATEMENT };**

**BLOCK = "{", "\n", {STATEMENT}, "}" ;**

**STATEMENT = ( λ | ASSIGNMENT | PRINT | IF | COMBAT_LOOP | VAR | ACTION), "\n" ;**

**ASSIGNMENT = IDENTIFIER, "=", BOOLEXPRESSION ;**

**PRINT = "Println", "(", BOOLEXPRESSION, ")" ;**

**IF = "if", "BOOLEXPRESSION, BLOCK, {"else", BLOCK}" ;**

**COMBAT_LOOP = "combat", ";", ASSIGNMENT, ";", "while", BOOLEXPRESSION, "progress", BOOLEXPRESSION, BLOCK ;**

**ACTION = "action", IDENTIFIER, "{", "\n", {STATEMENT}, "act" "}" ;**

**VAR = TYPE, IDENTIFIER, "=", BOOLEXPRESSION;**

**TYPE = ("character", "monster", "int")**

**BOOLEXPRESSION = BOOLTERM, {"||", BOOLTERM} ;**

**BOOLTERM = RELEXPRESSION, {"&&", RELEXPRESSION} ;**

**RELEXPRESSION = EXPRESSION, {("==" | ">" | "<"), EXPRESSION} ;**

**EXPRESSION = TERM, { ("+" | "-"), TERM } ;**

**TERM = FACTOR, { ("*" | "/"), FACTOR } ;**

**FACTOR = (("+" | "-" | "!"), FACTOR) | string | NUMBER | "(", BOOLEXPRESSION, ")" | IDENTIFIER | "Scanln", "(", ")" ;**

**IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;**

**NUMBER = DIGIT, { DIGIT } ;**

**LETTER = ( a | ... | z | A | ... | Z ) ;**

**DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;**