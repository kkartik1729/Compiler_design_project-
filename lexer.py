"""Position-aware lexer for the project's arithmetic expression language."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    type: str
    lexeme: str
    line: int
    column: int
    offset: int

    def as_dict(self):
        return {"type": self.type, "lexeme": self.lexeme, "line": self.line,
                "column": self.column, "offset": self.offset}


class LexError(ValueError):
    def __init__(self, message, line, column, character=None):
        super().__init__(message)
        self.message, self.line, self.column, self.character = message, line, column, character

    def as_dict(self):
        return {"message": self.message, "line": self.line, "column": self.column,
                "character": self.character}


SINGLE = {"+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE",
          "(": "LEFT_PAREN", ")": "RIGHT_PAREN", "=": "ASSIGNMENT"}


def tokenize(source):
    """Return tokens including EOF; reject every unsupported character."""
    tokens, i, line, col = [], 0, 1, 1
    while i < len(source):
        ch = source[i]
        if ch.isspace():
            if ch == "\n": line, col = line + 1, 1
            else: col += 1
            i += 1
            continue
        start, start_line, start_col = i, line, col
        if ch.isdigit() or (ch == "." and i + 1 < len(source) and source[i + 1].isdigit()):
            seen_dot = ch == "."
            i += 1; col += 1
            while i < len(source) and (source[i].isdigit() or (source[i] == "." and not seen_dot)):
                if source[i] == ".": seen_dot = True
                i += 1; col += 1
            lexeme = source[start:i]
            if lexeme.endswith("."):
                raise LexError("A number cannot end with a decimal point.", start_line, start_col, lexeme)
            tokens.append(Token("NUMBER", lexeme, start_line, start_col, start))
        elif ch.isalpha() or ch == "_":
            i += 1; col += 1
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1; col += 1
            tokens.append(Token("IDENTIFIER", source[start:i], start_line, start_col, start))
        elif ch in SINGLE:
            tokens.append(Token(SINGLE[ch], ch, line, col, i)); i += 1; col += 1
        else:
            raise LexError(f"Invalid character {ch!r}.", line, col, ch)
    tokens.append(Token("EOF", "", line, col, len(source)))
    return tokens
