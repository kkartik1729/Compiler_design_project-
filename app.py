"""Flask API and page for the syntax analyzer."""
from flask import Flask, jsonify, render_template, request
from lexer import tokenize, LexError
from parser import Parser, ParseError
from code_generator import generate

app = Flask(__name__)


@app.get("/")
def index(): return render_template("index.html")


@app.post("/api/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}
    source = payload.get("source", "")
    if not isinstance(source, str):
        return jsonify({"ok": False, "error": {"message": "Input must be text.", "line": 1, "column": 1}}), 400
    try:
        tokens = tokenize(source)
        visible_tokens = [t.as_dict() for t in tokens if t.type != "EOF"]
        tree = Parser(tokens).parse()
        return jsonify({"ok": True, "tokens": visible_tokens,
                        "ast": tree.as_dict(), "tree_text": tree.pretty(), "three_address_code": generate(tree)})
    except LexError as error:
        return jsonify({"ok": False, "stage": "lexical", "error": error.as_dict()}), 400
    except ParseError as error:
        return jsonify({"ok": False, "stage": "syntax", "tokens": locals().get("visible_tokens", []), "error": error.as_dict()}), 400


if __name__ == "__main__": app.run(debug=False)
