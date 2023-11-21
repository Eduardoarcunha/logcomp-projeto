import sys, re
from node import *
from SymbolTable import SymbolTable
from Tokenizer  import Tokenizer

class PrePo():
    @staticmethod
    def filter(str):
        str = str.replace('\t', '    ')
        comment_pattern = r'//.*?(\n|$)'
        result = re.sub(comment_pattern, '\n', str)
        return result
                
                
class Parser:
    tokenizer: Tokenizer

    @staticmethod
    def parse_factor():
        if Parser.tokenizer.next.type == "INT":
            node = IntVal(int(Parser.tokenizer.next.value), [])
            Parser.tokenizer.select_next()
            return node
        
        if Parser.tokenizer.next.type == "STRING":
            node = StrVal(str(Parser.tokenizer.next.value), [])
            Parser.tokenizer.select_next()
            return node      
        
        if Parser.tokenizer.next.type == "ID":
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type == "LEFT_PAR":
                node = FuncCall(identifier, [])
                node.value = identifier
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type == "RIGHT_PAR":
                    Parser.tokenizer.select_next()
                else:
                    node.children.append(Parser.parse_bool_expression())
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                        node.children.append(Parser.parse_bool_expression())
                    if Parser.tokenizer.next.type == "RIGHT_PAR":
                        Parser.tokenizer.select_next()
                    else:
                        raise Exception
                return node

            node = Iden(identifier, [])
            return node

        if Parser.tokenizer.next.type == "PLUS":
            node = UnOp("+", [])
            Parser.tokenizer.select_next()
            node.children.append(Parser.parse_factor())
            return node

        if Parser.tokenizer.next.type == "MINUS":
            node = UnOp("-", [])
            Parser.tokenizer.select_next()
            node.children.append(Parser.parse_factor())
            return node
        
        if Parser.tokenizer.next.type == "NOT":
            node = UnOp("!", [])
            Parser.tokenizer.select_next()
            node.children.append(Parser.parse_factor())
            return node

        if Parser.tokenizer.next.type == "LEFT_PAR":
            Parser.tokenizer.select_next()
            node = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type == "RIGHT_PAR":
                Parser.tokenizer.select_next()
                return node
        
        if Parser.tokenizer.next.type == "INPUT":
            node = Scan(None, [])
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "LEFT_PAR":
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "RIGHT_PAR":
                    Parser.tokenizer.select_next()
            return node

        raise Exception

    @staticmethod
    def parse_term():
        node = Parser.parse_factor()
        while Parser.tokenizer.next.type in ["TIMES", "DIVIDED"]:
            operator = Parser.tokenizer.next.value
            temp = BinOp(operator, [])
            temp.children.append(node)
            Parser.tokenizer.select_next()
            temp.children.append(Parser.parse_factor())
            node = temp
    
        return node
    
    @staticmethod
    def parse_expression():
        node = Parser.parse_term()
        while Parser.tokenizer.next.type in ["PLUS", "MINUS", "CONCAT"]:
            operator = Parser.tokenizer.next.value
            temp = BinOp(operator, [])
            temp.children.append(node)
            Parser.tokenizer.select_next()
            temp.children.append(Parser.parse_term())                
            node = temp
        
        return node
    
    @staticmethod
    def parse_relative_expression():
        node = Parser.parse_expression()
        while Parser.tokenizer.next.type in ["EQUALS", "GREATER_THAN", "LESS_THAN"]:
            operator = Parser.tokenizer.next.value
            temp = BinOp(operator, [])
            temp.children.append(node)
            Parser.tokenizer.select_next()
            temp.children.append(Parser.parse_expression())
            node = temp
        return node

    @staticmethod
    def parse_bool_term():
        node = Parser.parse_relative_expression()
        while Parser.tokenizer.next.type == 'AND':
            operator = Parser.tokenizer.next.value
            temp = BinOp(operator, [])
            temp.children.append(node)
            Parser.tokenizer.select_next()
            temp.children.append(Parser.parse_relative_expression())
            node = temp
        return node
    
    @staticmethod
    def parse_bool_expression():
        node = Parser.parse_bool_term()
        while Parser.tokenizer.next.type == 'OR':
            operator = Parser.tokenizer.next.value
            temp = BinOp(operator, [])
            temp.children.append(node)
            Parser.tokenizer.select_next()
            temp.children.append(Parser.parse_bool_term())
            node = temp
        return node

    
    @staticmethod
    def parse_assignment():
        if Parser.tokenizer.next.type == "ID":
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type == "EQUAL":
                id_node = Iden(identifier, [])
                node = Assignment(None, [])
                node.children.append(id_node)
                Parser.tokenizer.select_next()
                node.children.append(Parser.parse_bool_expression())

                return node
            
            elif Parser.tokenizer.next.type == "LEFT_PAR":
                node = FuncCall(None, [])
                node.value = identifier
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type == "RIGHT_PAR":
                    Parser.tokenizer.select_next()
                else:
                    node.children.append(Parser.parse_bool_expression())
                    while Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.select_next()
                        node.children.append(Parser.parse_bool_expression())
                    if Parser.tokenizer.next.type == "RIGHT_PAR":
                        Parser.tokenizer.select_next()
                    else:
                        raise Exception
                return node
            else:
                print(Parser.tokenizer.next.type, Parser.tokenizer.next.value)
                raise Exception
        
        return None

    
    @staticmethod
    def parse_block():
        node = Block(None, [])
        if Parser.tokenizer.next.type == "LEFT_KEY":
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == "ENDL":
                Parser.tokenizer.select_next()
                while Parser.tokenizer.next.type != "RIGHT_KEY":
                    node.children.append(Parser.parse_statement())
                Parser.tokenizer.select_next()
            else:
                raise Exception
        else:
            raise Exception

        return node
    
    @staticmethod
    def parse_statement():
        node = Parser.parse_assignment()
        if node:
            if Parser.tokenizer.next.type != "SEMI_COLON":
                raise Exception
            Parser.tokenizer.select_next()

        if node is None:
            if Parser.tokenizer.next.type == "PRINT":
                node = Println(None, [])
                Parser.tokenizer.select_next()
                if Parser.tokenizer.next.type == "LEFT_PAR":
                    Parser.tokenizer.select_next()
                    node.children.append(Parser.parse_bool_expression())
                    if Parser.tokenizer.next.type == "RIGHT_PAR":
                        Parser.tokenizer.select_next()
                        if Parser.tokenizer.next.type == "SEMI_COLON":
                            Parser.tokenizer.select_next()
                        else:
                            raise Exception
                    else:
                        raise Exception
                else:
                    raise Exception
            
            elif Parser.tokenizer.next.type == "IF":
                node = If(None, [])
                Parser.tokenizer.select_next()

                condition = Parser.parse_bool_expression()
                node.children.append(condition)

                true_block = Parser.parse_block()
                node.children.append(true_block)

                if Parser.tokenizer.next.type == "ELSE":
                    Parser.tokenizer.select_next()
                    false_block = Parser.parse_block()
                    node.children.append(false_block)

            elif Parser.tokenizer.next.type == "COMBAT":
                node = For(None, [])
                Parser.tokenizer.select_next()
                
                if Parser.tokenizer.next.type != "SEMI_COLON":
                    raise Exception
                Parser.tokenizer.select_next()

                init = Parser.parse_assignment()
                node.children.append(init)

                if Parser.tokenizer.next.type != "SEMI_COLON":
                    raise Exception
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type != "WHILE":
                    raise Exception
                Parser.tokenizer.select_next()

                condition = Parser.parse_bool_expression()
                node.children.append(condition)

                if Parser.tokenizer.next.type != "PROGRESS":
                    raise Exception
                Parser.tokenizer.select_next()

                inc = Parser.parse_assignment()
                node.children.append(inc)
                block = Parser.parse_block()
                node.children.append(block)
                
            elif Parser.tokenizer.next.type == "TYPE":
                node = VarDec(None, [])
                node.value = Parser.tokenizer.next.value
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type == "ID":
                    identifier = Parser.tokenizer.next.value
                    iden_symbol = Iden(identifier, [])
                    node.children.append(iden_symbol)
                    Parser.tokenizer.select_next()

                    if Parser.tokenizer.next.type == "EQUAL":
                        Parser.tokenizer.select_next()
                        iden_val = Parser.parse_bool_expression()
                        node.children.append(iden_val)

                        if Parser.tokenizer.next.type == "SEMI_COLON":
                            Parser.tokenizer.select_next()
                        else:
                            raise Exception 

                    else:
                        raise Exception
                
                else:
                    raise Exception
            
            elif Parser.tokenizer.next.type == "ACT":
                node = Return(None, [])
                Parser.tokenizer.select_next()
                node.children.append(Parser.parse_bool_expression())
                if Parser.tokenizer.next.type == "SEMI_COLON":
                    Parser.tokenizer.select_next()
                else:
                    raise Exception

        if Parser.tokenizer.next.type == "ENDL":
            Parser.tokenizer.select_next()
            return node if node else NoOp(None, [])
        
        raise Exception
    
    @staticmethod
    def parse_declaration():
        func_dec_node = FuncDec(None, [])
        if Parser.tokenizer.next.type != "ACTION":
            raise Exception
        Parser.tokenizer.select_next()

        if Parser.tokenizer.next.type != "ID":
            raise Exception
        var_dec1_node = VarDec(None, [])
        var_dec1_iden_node = Iden(Parser.tokenizer.next.value, [])
        var_dec1_node.children.append(var_dec1_iden_node)
        func_dec_node.children.append(var_dec1_node)    # Add the first var dec child (the function name)
        Parser.tokenizer.select_next()

        if Parser.tokenizer.next.type != "LEFT_PAR":
            raise Exception
        Parser.tokenizer.select_next()
        
        if Parser.tokenizer.next.type == "RIGHT_PAR":
            Parser.tokenizer.select_next()

        elif Parser.tokenizer.next.type == "ID":
            arg_var_dec_node = VarDec(None, []) # New arg
            arg_var_dec_iden_node = Iden(Parser.tokenizer.next.value, []) # Arg identifier
            arg_var_dec_node.children.append(arg_var_dec_iden_node) # Add the iden to the var dec
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type != "TYPE":
                raise Exception
            arg_var_dec_node.value = Parser.tokenizer.next.value # Arg type
            func_dec_node.children.append(arg_var_dec_node) # Add the arg var dec to the func dec
            Parser.tokenizer.select_next()

            while Parser.tokenizer.next.type != "RIGHT_PAR":
                if Parser.tokenizer.next.type != "COMMA":
                    raise Exception
                Parser.tokenizer.select_next()
                    
                if Parser.tokenizer.next.type != "ID":
                    raise Exception
                arg_var_dec_node = VarDec(None, []) # New arg
                arg_var_dec_iden_node = Iden(Parser.tokenizer.next.value, []) # Arg identifier
                arg_var_dec_node.children.append(arg_var_dec_iden_node) # Add the iden to the var dec
                Parser.tokenizer.select_next()

                if Parser.tokenizer.next.type != "TYPE":
                    raise Exception
                arg_var_dec_node.value = Parser.tokenizer.next.value # Arg type
                func_dec_node.children.append(arg_var_dec_node) # Add the arg var dec to the func dec
                Parser.tokenizer.select_next()

            Parser.tokenizer.select_next()

        else:
            raise Exception
        
        # print(Parser.tokenizer.next.type)
        
        if Parser.tokenizer.next.type != "TYPE":
            raise Exception
        var_dec1_node.value = Parser.tokenizer.next.value
        Parser.tokenizer.select_next()
        
        block_node = Parser.parse_block()
        func_dec_node.children.append(block_node)

        if Parser.tokenizer.next.type != "ENDL":
            raise Exception
        Parser.tokenizer.select_next()

        return func_dec_node

    
    @staticmethod
    def parse_program():
        node = Program(None, [])

        while Parser.tokenizer.next.type != "EOF":
            if Parser.tokenizer.next.type == "ENDL":
                Parser.tokenizer.select_next()
            elif Parser.tokenizer.next.type == "ACTION":  # Function declaration
                child = Parser.parse_declaration()
                node.children.append(child)
            else:
                # Handling top-level statements
                statement = Parser.parse_top_level_statement()
                node.children.append(statement)
            
        return node

    @staticmethod
    def parse_top_level_statement():
        node = Parser.parse_statement()
        if node.__class__.__name__ == "Return":
            raise Exception("Return statements are not allowed outside of function definitions.")

        return node
        
    @staticmethod
    def run(code):
        Parser.tokenizer = Tokenizer(code)

        root = Parser.parse_program()
        if Parser.tokenizer.next.type != "EOF":
            raise Exception
        return root

cnc_code = ""
try:
    with open(sys.argv[1], 'r') as file:
        cnc_code = file.read() + "\n"
except FileNotFoundError:
    print(f"The file '{sys.argv[1]}' was not found.")

root = Parser.run(PrePo.filter(cnc_code))
symbol_table = SymbolTable()
# graph = root.to_graphviz()
# graph.render('ast_graph', view=True)  # Saves to 'ast_graph.pdf' and opens it
# print(symbol_table.func_table)
root.evaluate(symbol_table)