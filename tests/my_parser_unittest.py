import unittest

import src.my_parser as ps
import src.tokenizer as tk


class ParserTest(unittest.TestCase):
    def test_parser_number(self):
        parser = ps.Parser([tk.Token(tk.TokenType.NUMBER, "10")])
        output = parser.parse()
        expected = ps.Program()
        expected.body = [ps.NumberLiteral("10")]
        self.assertEqual(output, expected)

    def test_parser_paren(self):
        parser = ps.Parser([
            tk.Token(tk.TokenType.PAREN, "("),
            tk.Token(tk.TokenType.NAME, "add"),
            tk.Token(tk.TokenType.PAREN, ")")
        ])
        output = parser.parse()
        expected = ps.Program()
        expected.body = [ps.CallExpression("add")]
        self.assertEqual(output, expected)

    def test_parser_paren_params(self):
        parser = ps.Parser([
            tk.Token(tk.TokenType.PAREN, "("),
            tk.Token(tk.TokenType.NAME, "add"),
            tk.Token(tk.TokenType.NUMBER, "2"),
            tk.Token(tk.TokenType.NUMBER, "4"),
            tk.Token(tk.TokenType.PAREN, ")")
        ])
        output = parser.parse()
        expected = ps.Program()
        call_expression = ps.CallExpression("add")
        call_expression.params = [ps.NumberLiteral("2"), ps.NumberLiteral("4")]
        expected.body = [call_expression]
        self.assertEqual(output, expected)
    
    def test_parser_invalid_token_error(self):
        parser = ps.Parser([tk.Token(tk.TokenType.PAREN, ")")])
        with self.assertRaises(ValueError):
            parser.parse()