import src.my_parser as ps
from src.traverser import Traverser


class TransformedProgram:
    def __init__(self) -> None:
        self.type = ps.NodeType.PROGRAM
        self.body = []

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.body == other.body


class ExpressionStatement:
    def __init__(self, expression) -> None:
        self.type = ps.NodeType.EXPRESSION_STATEMENT
        self.expression = CallExpressionWithCallee(expression.callee.name)

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.expression == other.expression


class CallExpressionWithCallee:
    def __init__(self, name) -> None:
        self.type = ps.NodeType.CALL_EXPRESSION
        self.callee = Identifier(name)
        self.arguments = []

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.callee == other.callee and self.arguments == other.arguments


class Identifier:
    def __init__(self, name) -> None:
        self.type = ps.NodeType.IDENTIFIER
        self.name = name

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.name == other.name
    

class Transformer:
    def __init__(self, ast: ps.Program) -> None:
        self.ast = ast

    def transform(self) -> TransformedProgram:
        transformed_ast = TransformedProgram()
        self.ast.context = transformed_ast.body
        Traverser(self.ast).traverse()

        return transformed_ast