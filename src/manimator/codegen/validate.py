import ast

def validate_python_code(code: str):
    """
    Raises SyntaxError if invalid
    Can add more checks (e.g., only allowed imports, no exec)
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise SyntaxError(f"Scene code invalid: {e}")

    # Optional: enforce allowed imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name != "manim":
                    raise ValueError(f"Disallowed import: {alias.name}")
