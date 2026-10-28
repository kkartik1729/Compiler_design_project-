# Syntax Analyzer and Parse Tree Generator Using Python

An educational Flask application that tokenizes arithmetic expressions, validates them with a hand-written recursive-descent parser, constructs an abstract syntax tree (AST), and generates three-address intermediate code. The AST is the compact operator-and-operand tree produced by the parser; it is not a concrete derivation tree containing every grammar production.

Repository: https://github.com/kkartik1729/Compiler_design_project-

## Features

- Position-aware tokenization for decimal numbers, identifiers, arithmetic operators, parentheses, and assignment.
- Recursive-descent syntax analysis with precedence, left associativity, unary minus, and optional leading assignment.
- AST JSON, expandable visual tree, and text tree.
- Three-address code generated from the AST.
- Lexical and syntax diagnostics with line and column.
- Responsive browser interface, examples, and a JSON Flask endpoint.

## Requirements and setup

Python 3.10 or newer is recommended. Flask is the sole runtime dependency.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python app.py
```

Open http://127.0.0.1:5000. The API accepts JSON at `POST /api/analyze`, for example:

```json
{"source":"a + b * c"}
```

Successful responses include tokens, AST, text tree, and intermediate code. Invalid input returns HTTP 400 with the stage and diagnostic details. The application never evaluates source text with Python `eval` or `exec`.

## Architecture

`lexer.py` creates typed tokens and source positions. `parser.py` consumes those tokens through `expression`, `term`, `unary`, and `primary` methods. `ast_nodes.py` defines immutable AST nodes and a text rendering. `code_generator.py` emits three-address code by recursively walking the AST. `app.py` connects the compiler to the Flask page and endpoint. The template, stylesheet, and JavaScript provide the interface and render only data returned by the server.

## Grammar

```text
Program   → Statement EOF
Statement → IDENTIFIER '=' Expr | Expr
Expr      → Term (('+' | '-') Term)*
Term      → Unary (('*' | '/') Unary)*
Unary     → '-' Unary | Primary
Primary   → NUMBER | IDENTIFIER | '(' Expr ')'
```

Multiplication and division bind more tightly because `Expr` obtains operands from `Term`, while `Term` consumes multiplication and division before returning to `Expr`. The loops make both binary precedence levels left-associative. Parentheses parse a nested `Expr` and thereby override that grouping. Assignment is accepted only as one leading identifier followed by `=` and an expression.

## Examples

| Input | AST root / expected effect | Intermediate code |
|---|---|---|
| `a + b * c` | `+`, with `*` as the right child | `t1 = b * c`; `t2 = a + t1` |
| `(a + b) * c` | `*`, with `+` as the left child | `t1 = a + b`; `t2 = t1 * c` |
| `x = 10 + 20` | assignment to `x` | `t1 = 10 + 20`; `x = t1` |
| `a + * b` | syntax diagnostic at `*` | Not generated |

## Tests

Run the standard-library unittest suite from the project root:

```powershell
python -m unittest discover -s tests -v
```

The suite covers lexer tokens and positions, precedence and grouping, unary minus, assignment, malformed input, AST-driven code generation, and Flask routes.

## Scope and limitations

The language supports decimal numeric tokens, identifiers, parentheses, unary minus, `+`, `-`, `*`, `/`, and one leading assignment. It does not evaluate expressions or resolve identifier values. It has no exponent notation, unary plus, multiple statements, comparison/boolean operators, functions, comments, type checking, or division-by-zero analysis. The generated tree is an AST, not a full concrete parse tree. Error recovery reports the first error.

## Project report

The TEC report and its editable DOCX are in `docs/report/`. Screenshots from the running application and original diagrams are in `docs/screenshots/` and `docs/diagrams/`.
