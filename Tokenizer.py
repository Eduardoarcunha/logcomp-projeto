from typing import Union


class Token:
    def __init__(self, type: str, value: Union[int, str]):
        self.type = type
        self.value = value


class Tokenizer:
    protected_words = {
        "print": "PRINT",
        "if": "IF",
        "else": "ELSE",
        "input": "INPUT",
        "character": "TYPE",
        "int": "TYPE",
        "monster": "TYPE",
        "act": "ACTION",
        "while": "WHILE",
        "combat": "COMBAT",
        "progress": "PROGRESS",
    }

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next: Token

        self.select_next()

    def parse_numeric(self):
        type = "INT"
        value = ""

        while (
            self.position < len(self.source) and self.source[self.position].isnumeric()
        ):
            value += self.source[self.position]
            self.position += 1

        self.next = Token(type, int(value))

    def parse_operator(self, type, value):
        self.position += 1
        self.next = Token(type, value)

    def parse_alpha(self):
        value = ""
        character = self.source[self.position]
        while self.position < len(self.source) and (
            character.isalnum() or character == "_"
        ):
            value += self.source[self.position]
            self.position += 1
            character = self.source[self.position]

        if value in Tokenizer.protected_words:
            self.next = Token(Tokenizer.protected_words[value], value)
        else:
            self.next = Token("ID", value)

    def parse_double_char_operator(self, expected_char, type, value):
        self.position += 1
        if self.source[self.position] == expected_char:
            self.parse_operator(type, value)
        else:
            raise Exception

    def parse_string(self):
        value = ""
        self.position += 1
        character = self.source[self.position]
        while self.position < len(self.source) and (character != '"'):
            value += self.source[self.position]
            self.position += 1
            character = self.source[self.position]
        self.next = Token("STRING", value)
        self.position += 1

    def select_next(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", 0)
            return

        character = self.source[self.position]

        if character.isnumeric():
            self.parse_numeric()
        elif character == "+":
            self.parse_operator("PLUS", "+")
        elif character == "-":
            self.parse_operator("MINUS", "-")
        elif character == "*":
            self.parse_operator("TIMES", "*")
        elif character == "/":
            self.parse_operator("DIVIDED", "/")
        elif character == "(":
            self.parse_operator("LEFT_PAR", "(")
        elif character == ")":
            self.parse_operator("RIGHT_PAR", ")")
        elif character == "\n":
            self.parse_operator("ENDL", 0)
        elif character == "\t":
            self.parse_operator("TAB", 0)
        elif character == "=":
            self.position += 1
            if self.source[self.position] == "=":
                self.parse_operator("EQUALS", "==")
            else:
                self.parse_operator("EQUAL", "=")
        elif character == '"':
            self.parse_string()
        elif character.isalpha():
            self.parse_alpha()
        elif character == "!":
            self.parse_operator("NOT", "!")
        elif character == ";":
            self.parse_operator("SEMI_COLON", ";")
        elif character == "{":
            self.parse_operator("LEFT_KEY", "{")
        elif character == "}":
            self.parse_operator("RIGHT_KEY", "}")
        elif character == "<":
            self.parse_operator("LESS_THAN", "<")
        elif character == ">":
            self.parse_operator("GREATER_THAN", ">")
        elif character == ",":
            self.parse_operator("COMMA", ",")
        elif character == "|":
            self.parse_double_char_operator("|", "OR", "||")
        elif character == "&":
            self.parse_double_char_operator("&", "AND", "&&")
        elif character == ".":
            self.parse_operator("CONCAT", ".")
        elif character == " ":
            self.position += 1
            self.select_next()
        else:
            raise Exception
