from enum import Enum
from typing import List

from src.tokenizer import Token
import src.tokenizer as tk


class Node(Enum):
    pass


class Program:
    def __init__(self) -> None:
        self.type = NodeType.PROGRAM
        self.body = []
        self.context = []
    
    def __eq__(self, other) -> bool:
        return self.type == other.type and self.body == other.body


class NumberLiteral:
    def __init__(self, value: str) -> None:
        self.type = NodeType.NUMBER_LITERAL
        self.value = value

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.value == other.value


class StringLiteral:
    def __init__(self, value) -> None:
        self.type = NodeType.STRING_LITERAL
        self.value = value

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.value == other.value


class CallExpression:
    def __init__(self, value) -> None:
        self.type = NodeType.CALL_EXPRESSION
        self.value = value
        self.params = []

    def __eq__(self, other) -> bool:
        return (self.type == other.type and self.value == other.value and 
                self.params == other.params)


class NodeType(Enum):
    PROGRAM = "Program"
    CALL_EXPRESSION = "CallExpression"
    NUMBER_LITERAL = "NumberLiteral"
    STRING_LITERAL = "StringLiteral"
    EXPRESSION_STATEMENT = "ExpressionStatement"
    IDENTIFIER = "Identifier"


class Parser:
    def __init__(self, tokens: List['Token']) -> None:
        self.tokens = tokens
        self.current_idx = 0
        self.ast = Program()
    
    def parse(self) -> Program:
        while self.current_idx < len(self.tokens):
            self.ast.body.append(self.walk_tokens())

        return self.ast

    def walk_tokens(self) -> Node:
        token = self.get_token()

        if token.token_type == tk.TokenType.NUMBER:
            self.current_idx += 1
            return NumberLiteral(token.token_value)
        
        if token.token_type == tk.TokenType.NAME:
            self.current_idx += 1
            return StringLiteral(token.token_value)

        if token.token_type == tk.TokenType.PAREN and token.token_value == "(":
            self.current_idx += 1
            token = self.get_token()

            node = CallExpression(token.token_value)
            self.current_idx += 1
            token = self.get_token()

            while token.token_type != tk.TokenType.PAREN or (token.token_type == tk.TokenType.PAREN and token.token_value != ")"):
                node.params.append(self.walk_tokens())
                token = self.get_token()
            
            self.current_idx += 1
            return node
        
        raise ValueError(
            f"The self.tokens contains an unexpected token: {self.tokens[self.current_idx]}"
        )


    def get_token(self) -> 'Token':
        if len(self.tokens) <= self.current_idx:
            raise ValueError(
                f"The current index '{self.current_idx}' is out of range"
            )

        return self.tokens[self.current_idx]