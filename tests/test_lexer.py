import unittest
from lexer import tokenize, LexError

class LexerTests(unittest.TestCase):
    def test_tokens_and_positions(self):
        tokens = tokenize("x = 10 + a")
        self.assertEqual([t.type for t in tokens], ["IDENTIFIER", "ASSIGNMENT", "NUMBER", "PLUS", "IDENTIFIER", "EOF"])
        self.assertEqual((tokens[2].line, tokens[2].column), (1, 5))
    def test_invalid_character(self):
        with self.assertRaises(LexError) as caught: tokenize("@a + 2")
        self.assertEqual((caught.exception.line, caught.exception.column), (1, 1))
    def test_decimal(self): self.assertEqual(tokenize(".25 + 1.5")[0].lexeme, ".25")

if __name__ == "__main__": unittest.main()
