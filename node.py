from abc import ABC, abstractmethod

from graphviz import Digraph
from SymbolTable import SymbolTable


class Node(ABC):
    unique_id = 0

    def __init__(self, value, children):
        self.value = value
        self.children = children

        self.id = Node.unique_id
        Node.unique_id += 1

    @abstractmethod
    def evaluate(self, symbol_table):
        """Evaluate the node"""

    def to_graphviz(self, graph=None):
        if graph is None:
            graph = Digraph(comment="AST")

        # Add the current node
        # label_value = self.value if self.value is not None else self.__class__.__name__
        label_value = self.__class__.__name__
        graph.node(str(self.id), label=str(label_value))

        for child in self.children:
            # Add an edge from the current node to each child

            graph.edge(str(self.id), str(child.id))

            # Recur to add each child's subtree
            child.to_graphviz(graph)

        return graph


class BinOp(Node):
    def evaluate(self, symbol_table):
        child1 = self.children[0].evaluate(symbol_table)
        child2 = self.children[1].evaluate(symbol_table)

        if self.value == "+":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": child1["value"] + child2["value"], "type": "int"}
            raise Exception

        if self.value == "-":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": child1["value"] - child2["value"], "type": "int"}
            raise Exception

        if self.value == "*":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": child1["value"] * child2["value"], "type": "int"}
            raise Exception

        if self.value == "/":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": child1["value"] // child2["value"], "type": "int"}
            raise Exception

        if self.value == "||":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": int(child1["value"] or child2["value"]), "type": "int"}
            raise Exception

        if self.value == "&&":
            if child1["type"] == "int" and child2["type"] == "int":
                return {
                    "value": int(child1["value"] and child2["value"]),
                    "type": "int",
                }
            raise Exception

        if self.value == "==":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": int(child1["value"] == child2["value"]), "type": "int"}

            if child1["type"] == "string" and child2["type"] == "string":
                return {"value": int(child1["value"] == child2["value"]), "type": "int"}

            raise Exception

        if self.value == ">":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": int(child1["value"] > child2["value"]), "type": "int"}

            if child1["type"] == "string" and child2["type"] == "string":
                return {"value": int(child1["value"] > child2["value"]), "type": "int"}

            raise Exception

        if self.value == "<":
            if child1["type"] == "int" and child2["type"] == "int":
                return {"value": int(child1["value"] < child2["value"]), "type": "int"}

            if child1["type"] == "string" and child2["type"] == "string":
                return {"value": int(child1["value"] < child2["value"]), "type": "int"}

            raise Exception

        if self.value == ".":
            return {
                "value": str(child1["value"]) + str(child2["value"]),
                "type": "string",
            }


class UnOp(Node):
    def evaluate(self, symbol_table):
        child = self.children[0].evaluate(symbol_table)
        if self.value == "+" and child["type"] == "int":
            return {"value": child["value"], "type": "int"}

        if self.value == "-" and child["type"] == "int":
            return {"value": -child["value"], "type": "int"}

        if self.value == "!" and child["type"] == "int":
            return {"value": int(not child["value"]), "type": "int"}


class IntVal(Node):
    def evaluate(self, symbol_table):
        return {"value": self.value, "type": "int"}


class StrVal(Node):
    def evaluate(self, symbol_table):
        return {"value": self.value, "type": "string"}


class NoOp(Node):
    def evaluate(self, symbol_table):
        pass


class Block(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            if child.__class__.__name__ == "Return":
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)


class Program(Node):
    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)


class Iden(Node):
    def evaluate(self, symbol_table):
        return symbol_table.get(self.value)


class Println(Node):
    def evaluate(self, symbol_table):
        child = self.children[0].evaluate(symbol_table)
        print(child["value"])


class Assignment(Node):
    def evaluate(self, symbol_table):
        right_child = self.children[1].evaluate(symbol_table)
        symbol_table.set(
            self.children[0].value, right_child["value"], right_child["type"]
        )


class If(Node):
    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table):
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)


class For(Node):
    def evaluate(self, symbol_table):
        i = self.children[0].evaluate(symbol_table)
        while self.children[1].evaluate(symbol_table)["value"]:
            self.children[3].evaluate(symbol_table)
            self.children[2].evaluate(symbol_table)
            # Teoricamente uma mensagem aqui?



class Scan(Node):
    def evaluate(self, symbol_table):
        var = input()
        if var.isdigit():
            return {"value": int(var), "type": "int"}
        return {"value": var, "type": "string"}

        # return {"value": int(input()), "type": "int"}


class VarDec(Node):
    def evaluate(self, symbol_table):
        if len(self.children) < 2:
            symbol_table.create(self.children[0].value, self.value)
        else:
            var = self.children[1].evaluate(symbol_table)
            symbol_table.create(
                self.children[0].value, self.value, var["value"], var["type"]
            )


class FuncDec(Node):
    def evaluate(self, symbol_table):
        symbol_table.create_func(
            self.children[0].children[0].value, self, self.children[0].value
        )


class FuncCall(Node):
    def evaluate(self, symbol_table):
        if self.value == "main":
            main_func = symbol_table.get_func("main")
            main_ret = main_func["node"].children[-1].evaluate(symbol_table)
            if main_ret:
                if main_func["type"] != main_ret["type"]:
                    raise Exception
            return

        func_info = symbol_table.get_func(self.value)
        node = func_info["node"]
        local_symbol_table = SymbolTable()
        for i in range(len(self.children)):
            node.children[i + 1].evaluate(local_symbol_table)
            child = self.children[i].evaluate(symbol_table)
            local_symbol_table.set(
                node.children[i + 1].children[0].value, child["value"], child["type"]
            )

        func_return = node.children[-1].evaluate(local_symbol_table)
        if func_return["type"] != func_info["type"]:
            raise Exception
        return func_return


class Return(Node):
    def evaluate(self, symbol_table):
        return self.children[0].evaluate(symbol_table)
