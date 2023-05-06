from typing import Callable, List, Optional
from enum import Enum

import src.my_parser as ps
import src.transformer as tf

class TraversedNode(Enum):
    pass

class Traverser:
    def __init__(self, ast: ps.Program) -> None:
        self.ast = ast

    def traverse(self) -> None:
        self.traverse_node(self.ast)

    def traverse_array(self, node_array: List[ps.Node], parent: ps.Node) -> None:
        for child in node_array:
            self.traverse_node(child, parent)

    def traverse_node(self, node: ps.Node, parent: ps.Node = None) -> None:
        visitor = {
            ps.NodeType.NUMBER_LITERAL: ContextHundler(ps.NodeType.NUMBER_LITERAL),
            ps.NodeType.STRING_LITERAL: ContextHundler(ps.NodeType.STRING_LITERAL),
            ps.NodeType.CALL_EXPRESSION: ContextHundler(ps.NodeType.CALL_EXPRESSION),
        }
        methods = visitor.get(node.type)

        if methods and methods.enter:
            methods.enter(node, parent)

        if node.type == ps.NodeType.PROGRAM:
            self.traverse_array(node.body, node)
        elif node.type == ps.NodeType.CALL_EXPRESSION:
            self.traverse_array(node.params, node)
        elif node.type == ps.NodeType.NUMBER_LITERAL:
            pass
        elif node.type == ps.NodeType.STRING_LITERAL:
            pass


class ContextHundler:
    def __init__(self, node_type: 'ps.NodeType') -> None:
        self.enter = self.define_enter(node_type)

    def define_enter(self, node_type: 'ps.NodeType') -> Callable[[ps.Node, Optional[ps.Node]], None]:
        if node_type == ps.NodeType.NUMBER_LITERAL:
            return self.number_literal_enter
        if node_type == ps.NodeType.STRING_LITERAL:
            return self.string_literal_enter
        if node_type == ps.NodeType.CALL_EXPRESSION:
            return self.call_expression_enter

    def number_literal_enter(self, node: ps.NumberLiteral, parent: ps.Node) -> None:
        parent.context.append(ps.NumberLiteral(node.value))

    def string_literal_enter(self, node: ps.StringLiteral, parent: ps.Node) -> None:
        parent.context.append(ps.StringLiteral(node.value))

    def call_expression_enter(self, node: ps.CallExpression, parent: ps.Node) -> None:
        expression = tf.CallExpressionWithCallee(node.value)
        node.context = expression.arguments

        if parent.type != ps.NodeType.CALL_EXPRESSION:
            expression = tf.ExpressionStatement(expression)
            node.context = expression.expression.arguments

        parent.context.append(expression)