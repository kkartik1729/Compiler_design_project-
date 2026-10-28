"""Three-address code generation from the AST."""
def generate(node):
    lines, counter = [], [0]
    def visit(current):
        if current.kind == "Number" or current.kind == "Identifier": return current.value
        if current.kind == "UnaryExpression":
            operand = visit(current.children[0]); counter[0] += 1; temp = f"t{counter[0]}"
            lines.append(f"{temp} = -{operand}"); return temp
        if current.kind == "BinaryExpression":
            left, right = visit(current.children[0]), visit(current.children[1])
            counter[0] += 1; temp = f"t{counter[0]}"
            lines.append(f"{temp} = {left} {current.value} {right}"); return temp
        if current.kind == "Assignment":
            name = current.children[0].value; result = visit(current.children[1])
            lines.append(f"{name} = {result}"); return name
        raise ValueError(f"Unsupported AST node: {current.kind}")
    visit(node)
    return lines
