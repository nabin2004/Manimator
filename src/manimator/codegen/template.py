MANIM_SCENE_TEMPLATE = """
{scene_body}
"""

def indent_code(code: str, level: int = 0) -> str: # Let's keep 0 for now, this might be useful later
    return "\n".join((" " * 4 * level) + line for line in code.splitlines())
