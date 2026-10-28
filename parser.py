"""Recursive-descent parser that constructs an abstract syntax tree."""
from ast_nodes import ASTNode
from lexer import tokenize, Token, LexError


class ParseError(ValueError):
    def __init__(self, message, token):
        super().__init__(message)
        self.message, self.token = message, token

    def as_dict(self):
        return {"message": self.message, "line": self.token.line,
                "column": self.token.column, "found": self.token.lexeme or "end of input"}


class Parser:
    def __init__(self, tokens): self.tokens, self.current = tokens, 0
    def peek(self): return self.tokens[self.current]
    def advance(self):
        token = self.peek()
        if token.type != "EOF": self.current += 1
        return token
    def match(self, *types):
        if self.peek().type in types: return self.advance()
        return None
    def expect(self, kind, message):
        token = self.match(kind)
        if token is None: raise ParseError(message, self.peek())
        return token

    def parse(self):
        if self.peek().type == "EOF": raise ParseError("Enter an expression to analyze.", self.peek())
        if self.peek().type == "IDENTIFIER" and self.tokens[self.current + 1].type == "ASSIGNMENT":
            name = self.advance(); self.advance()
            if self.peek().type == "EOF": raise ParseError("Expected an expression after '='.", self.peek())
            expr = self.expression()
            root = ASTNode("Assignment", "=", (ASTNode("Identifier", name.lexeme, (), name.line, name.column), expr), name.line, name.column)
        else:
            root = self.expression()
        if self.peek().type != "EOF":
            token = self.peek()
            if token.type == "ASSIGNMENT": message = "Assignment is allowed only at the start of a statement."
            elif token.type == "IDENTIFIER" or token.type == "NUMBER": message = "Unexpected token after the expression; an operator may be missing."
            else: message = f"Unexpected token {token.lexeme!r} after the expression."
            raise ParseError(message, token)
        return root

    def expression(self):
        node = self.term()
        while (op := self.match("PLUS", "MINUS")) is not None:
            rhs = self.term(); node = ASTNode("BinaryExpression", op.lexeme, (node, rhs), op.line, op.column)
        return node

    def term(self):
        node = self.unary()
        while (op := self.match("MULTIPLY", "DIVIDE")) is not None:
            rhs = self.unary(); node = ASTNode("BinaryExpression", op.lexeme, (node, rhs), op.line, op.column)
        return node

    def unary(self):
        op = self.match("MINUS")
        if op:
            if self.peek().type in ("EOF", "RIGHT_PAREN", "PLUS", "MULTIPLY", "DIVIDE"):
                raise ParseError("Expected an operand after unary '-'.", self.peek())
            return ASTNode("UnaryExpression", "-", (self.unary(),), op.line, op.column)
        return self.primary()

    def primary(self):
        token = self.match("NUMBER")
        if token: return ASTNode("Number", token.lexeme, (), token.line, token.column)
        token = self.match("IDENTIFIER")
        if token: return ASTNode("Identifier", token.lexeme, (), token.line, token.column)
        if self.match("LEFT_PAREN"):
            if self.peek().type == "RIGHT_PAREN": raise ParseError("Parentheses cannot be empty; expected an expression.", self.peek())
            node = self.expression()
            self.expect("RIGHT_PAREN", "Missing closing ')'.")
            return node
        token = self.peek()
        if token.type == "EOF": message = "Expected a number, identifier, unary '-', or '('."
        elif token.type == "RIGHT_PAREN": message = "Expected an operand before ')'."
        elif token.type == "ASSIGNMENT": message = "Expected an expression; assignment requires a leading identifier."
        else: message = f"Expected an operand, found {token.lexeme!r}."
        raise ParseError(message, token)


def parse(source):
    return Parser(tokenize(source)).parse()
