import unittest

import src.tokenizer as tk


class TokenizerTest(unittest.TestCase):
    def test_tokenize_space(self):
        tokenizer = tk.Tokenizer(" ")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 0)

    def test_tokenize_number(self):
        tokenizer = tk.Tokenizer("10")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], tk.Token(tk.TokenType.NUMBER, "10"))

    def test_tokenize_letter(self):
        tokenizer = tk.Tokenizer("add")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0], tk.Token(tk.TokenType.NAME, "add"))

    def test_tokenize_paren(self):
        tokenizer = tk.Tokenizer("()")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 2)
        self.assertEqual(output[0], tk.Token(tk.TokenType.PAREN, "("))
        self.assertEqual(output[1], tk.Token(tk.TokenType.PAREN, ")"))

    def test_tokenize_add_2_4(self):
        tokenizer = tk.Tokenizer("(add 2 4)")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 5)
        self.assertEqual(output[0], tk.Token(tk.TokenType.PAREN, "("))
        self.assertEqual(output[1], tk.Token(tk.TokenType.NAME, "add"))
        self.assertEqual(output[2], tk.Token(tk.TokenType.NUMBER, "2"))
        self.assertEqual(output[3], tk.Token(tk.TokenType.NUMBER, "4"))
        self.assertEqual(output[4], tk.Token(tk.TokenType.PAREN, ")"))

    def test_tokenize_add_10_sub_4_2(self):
        tokenizer = tk.Tokenizer("(add 10 (subtract 4 2))")
        output = tokenizer.tokenize()
        self.assertEqual(len(output), 9)
        self.assertEqual(output[0], tk.Token(tk.TokenType.PAREN, "("))
        self.assertEqual(output[1], tk.Token(tk.TokenType.NAME, "add"))
        self.assertEqual(output[2], tk.Token(tk.TokenType.NUMBER, "10"))
        self.assertEqual(output[3], tk.Token(tk.TokenType.PAREN, "("))
        self.assertEqual(output[4], tk.Token(tk.TokenType.NAME, "subtract"))
        self.assertEqual(output[5], tk.Token(tk.TokenType.NUMBER, "4"))
        self.assertEqual(output[6], tk.Token(tk.TokenType.NUMBER, "2"))
        self.assertEqual(output[7], tk.Token(tk.TokenType.PAREN, ")"))
        self.assertEqual(output[8], tk.Token(tk.TokenType.PAREN, ")"))
