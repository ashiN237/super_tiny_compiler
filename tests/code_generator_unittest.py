import unittest

import src.my_parser as ps
import src.tokenizer as tk
import src.transformer as ts
import src.traverser as tv
import src.code_generator as cg


class CodeGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.node = ts.TransformedProgram()
        call_expression = ts.CallExpressionWithCallee("add")
        self.node.body = [ts.ExpressionStatement(call_expression)]
        self.node.body[0].expression.arguments = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]

    def test_generate_code(self):
        code_generator = cg.CodeGenerator(self.node)
        output = code_generator.generate_code()
        self.assertEqual(output, "add(2, 4);")