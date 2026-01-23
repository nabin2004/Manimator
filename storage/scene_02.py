
from manim import *

class Scene_02(Scene):
    def construct(self):
        stop_sign = RegularPolygon(n=8, radius=1.5, color=RED, fill_opacity=0.8)
        stop_sign.shift(LEFT * 4)
        stop_text = Text("STOP", font_size=36, weight=BOLD).move_to(stop_sign.get_center())
        stop_group = VGroup(stop_sign, stop_text)

        code_str = "if n == 0:\n    return 0"
        code = Code(code=code_str, language="python", font="Monospace", background="rectangle", background_stroke_color=WHITE, background_stroke_width=2, insert_line_no=False, style="monokai")
        code.scale(0.8)
        code.shift(RIGHT * 4)

        arrow = Arrow(start=code.get_left(), end=stop_sign.get_right(), buff=0.2, color=YELLOW)
        arrow_label = Text("Base Case", font_size=28, color=YELLOW).next_to(arrow, UP, buff=0.1)

        self.play(Create(stop_sign), Write(stop_text))
        self.play(Write(code))
        self.play(Create(arrow), Write(arrow_label))
        self.wait(2)
