from src import my_parser, transformer, traverser


class InvalidTraversedNodeTypeFoundExeception(Exception):
    pass


class CodeGenerator:
    def __init__(self, node: transformer.TransformedProgram) -> None:
        self.node = node

    def generate_code(self) -> str:
        return self.generate_code_recursively(self.node)

    def generate_code_recursively(self, node: traverser.TraversedNode) -> str:
        if node.type == my_parser.NodeType.PROGRAM:
            return "\n".join(map(self.generate_code_recursively, node.body))

        elif node.type == my_parser.NodeType.EXPRESSION_STATEMENT:
            return self.generate_code_recursively(node.expression) + ";"

        elif node.type == my_parser.NodeType.CALL_EXPRESSION:
            return self.generate_code_recursively(node.callee) + "(" + ", ".join(map(self.generate_code_recursively, node.arguments)) + ")"

        elif node.type == my_parser.NodeType.IDENTIFIER:
            return node.name

        elif node.type == my_parser.NodeType.NUMBER_LITERAL:
            return node.value

        elif node.type == my_parser.NodeType.STRING_LITERAL:
            return '"' + node.value + '"'

        else:
            raise InvalidTraversedNodeTypeFoundExeception(
                f"The traversed ast contains an unexpected node type: {node.type}"
            )