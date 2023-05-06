import re
from enum import Enum
from typing import List


class TokenType(Enum):
    NUMBER = "number"
    NAME = "name"
    PAREN = "paren"


class Token:
    def __init__(self, token_type: 'TokenType', token_value: str) -> None:
        self.token_type = token_type
        self.token_value = token_value

    def __eq__(self, other) -> bool:
        return self.token_type == other.token_type and self.token_value == other.token_value


class Tokenizer:
    def __init__(self, input: str) -> None:
        self.input = input
        self.current_idx = 0
        self.tokens = []

    def tokenize(self) -> List['Token']:
        while self.current_idx < len(self.input):
            WHITESPACE = "\s"
            NUMBERS = "[0-9]"
            LETTERS = "[a-zA-Z_-]"
            token_value = ""

            if re.match(WHITESPACE, self.get_char()):
                while self.current_idx < len(self.input) and re.match(WHITESPACE, self.get_char()):
                    self.current_idx += 1
                continue

            if self.get_char() in ["(", ")"]:
                self.tokens.append(Token(TokenType.PAREN, self.get_char()))
                self.current_idx += 1
                continue

            if self.get_char() == "-":
                token_value += self.get_char()
                self.current_idx += 1
                if re.match(NUMBERS, self.get_char()):
                    while self.current_idx < len(self.input) and re.match(NUMBERS, self.get_char()):
                        token_value += self.get_char()
                        self.current_idx += 1
                    self.tokens.append(Token(TokenType.NUMBER, token_value))
                else:
                    raise ValueError(
                        f"The input contains an unexpected character: {self.get_char()}"
                    )
                continue

            if re.match(NUMBERS, self.get_char()):
                while self.current_idx < len(self.input) and re.match(NUMBERS, self.get_char()):
                    token_value += self.get_char()
                    self.current_idx += 1
                self.tokens.append(Token(TokenType.NUMBER, token_value))
                continue
            
            if re.match(LETTERS, self.get_char()):
                while self.current_idx < len(self.input) and re.match(LETTERS, self.get_char()):
                    token_value += self.get_char()
                    self.current_idx += 1
                self.tokens.append(Token(TokenType.NAME, token_value))
                continue
            
            raise ValueError(
                f"The input contains an unexpected character: {self.get_char()}"
            )

        return self.tokens

    def get_char(self) -> str:
        if len(self.input) <= self.current_idx:
            raise ValueError(f"The current index '{self.current_idx}' is out of range")

        return self.input[self.current_idx]
