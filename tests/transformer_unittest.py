import unittest

import src.my_parser as ps
import src.transformer as tf


class TransformerTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ast = ps.Program()
        call_expression = ps.CallExpression("add")
        call_expression.params = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        self.ast.body = [call_expression]


    def test_transformer(self):
        expected = tf.TransformedProgram()
        call_expression = tf.CallExpressionWithCallee("add")
        expected.body = [tf.ExpressionStatement(call_expression)]
        expected.body[0].expression.arguments = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]

        transfomer = tf.Transformer(self.ast)
        output = transfomer.transform()
        self.assertEqual(output, expected)