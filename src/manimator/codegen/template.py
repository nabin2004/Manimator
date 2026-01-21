MANIM_SCENE_TEMPLATE = """
from manim import *

class {scene_class_name}(Scene):
    def construct(self):
{scene_body}
"""

def indent_code(code: str, level: int = 2) -> str:
    return "\n".join((" " * 4 * level) + line for line in code.splitlines())
