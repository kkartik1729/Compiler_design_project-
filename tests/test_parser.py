import unittest
from parser import parse, ParseError
from lexer import LexError
from code_generator import generate

class ParserTests(unittest.TestCase):
    def test_precedence(self):
        tree = parse("a + b * c")
        self.assertEqual(tree.value, "+")
        self.assertEqual(tree.children[1].value, "*")
        self.assertEqual(generate(tree), ["t1 = b * c", "t2 = a + t1"])
    def test_parentheses(self):
        tree = parse("(a + b) * c")
        self.assertEqual(tree.value, "*"); self.assertEqual(tree.children[0].value, "+")
    def test_unary_and_assignment(self):
        self.assertEqual(parse("-a + 5").children[0].kind, "UnaryExpression")
        self.assertEqual(parse("x = 10 + 20").kind, "Assignment")
    def test_valid_division(self): self.assertEqual(parse("10 / 2").value, "/")
    def test_malformed(self):
        for source in ("a + * b", "(a + b", "10 /", "a b", "()", "x =", "a = b = 1"):
            with self.subTest(source=source), self.assertRaises(ParseError): parse(source)
    def test_empty_and_lexical_error(self):
        with self.assertRaises(ParseError): parse("")
        with self.assertRaises(LexError): parse("@a + 2")

if __name__ == "__main__": unittest.main()
