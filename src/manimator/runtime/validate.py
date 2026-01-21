import ast

ALLOWED_IMPORTS = {"manim"}

def validate_scene_code(code: str):
    """
    Raises exception if code is invalid
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in scene code: {e}")

    # enforce allowed imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name not in ALLOWED_IMPORTS:
                    raise ValueError(f"Disallowed import: {alias.name}")
        elif isinstance(node, ast.ImportFrom):
            if node.module not in ALLOWED_IMPORTS:
                raise ValueError(f"Disallowed import: {node.module}")
