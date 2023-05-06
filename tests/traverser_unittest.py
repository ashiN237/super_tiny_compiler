import unittest

import src.my_parser as ps
import src.transformer as tf
import src.traverser as tv


class TraverserTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.ast = ps.Program()
        call_expression = ps.CallExpression("add")
        call_expression.params = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        self.ast.body = [call_expression]

    def test_traverser(self):
        expected = ps.Program()
        call_expression = ps.CallExpression("add")
        call_expression.params = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        call_expression.context = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        expected.body = [call_expression]
        expression = tf.CallExpressionWithCallee("add")
        expression_statement = tf.ExpressionStatement(expression)
        expression_statement.expression.arguments = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        expected.context = [expression_statement]

        traveser = tv.Traverser(self.ast)
        traveser.traverse()
        self.assertEqual(self.ast, expected)