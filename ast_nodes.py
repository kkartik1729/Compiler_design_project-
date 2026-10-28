"""AST node model and readable tree serialization."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ASTNode:
    kind: str
    value: str
    children: tuple = ()
    line: int = 1
    column: int = 1

    def as_dict(self):
        return {"kind": self.kind, "value": self.value, "line": self.line,
                "column": self.column, "children": [child.as_dict() for child in self.children]}

    def pretty(self):
        lines = []
        def walk(node, prefix="", last=True, root=False):
            label = f"{node.kind}: {node.value}"
            lines.append(("" if root else prefix + ("└── " if last else "├── ")) + label)
            next_prefix = prefix if root else prefix + ("    " if last else "│   ")
            for idx, child in enumerate(node.children):
                walk(child, next_prefix, idx == len(node.children) - 1)
        walk(self, root=True)
        return "\n".join(lines)
