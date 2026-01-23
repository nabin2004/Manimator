
from manim import *

class FactorialRecursion(Scene):
    def construct(self):
        title = Text("Factorial Calculation", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        math_def = MathTex(r"n! = n \times (n-1)!")
        math_def.next_to(title, DOWN, buff=0.5)
        self.play(Write(math_def))
        self.wait(1)

        code_str = [
            "def factorial(n):",
            "    if n <= 1:",
            "        return 1",
            "    return n * factorial(n - 1)"
        ]
        code = Code(
            code=code_str,
            font="Monospace",
            background="rectangle",
            background_stroke_color=WHITE,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai",
            font_size=24
        )
        code.shift(LEFT * 3.5)
        self.play(Create(code))
        self.wait(1)

        stack_group = VGroup()
        stack_labels = ["5!", "4!", "3!", "2!", "1!"]
        stack_values = ["5 * 4!", "4 * 3!", "3 * 2!", "2 * 1!", "1"]
        
        start_y = 2.5
        for i in range(5):
            rect = RoundedRectangle(
                width=3, height=0.8, 
                corner_radius=0.1, 
                fill_color=BLUE_B, 
                fill_opacity=0.5, 
                stroke_color=WHITE
            )
            rect.shift(RIGHT * 3.5 + UP * (start_y - i * 1.0))
            
            label = Text(stack_labels[i], font_size=24)
            label.move_to(rect.get_center() + LEFT * 0.8)
            
            value = MathTex(stack_values[i], font_size=24)
            value.move_to(rect.get_center() + RIGHT * 0.8)
            
            frame = VGroup(rect, label, value)
            stack_group.add(frame)
            self.play(FadeIn(frame, shift=UP*0.5))
            self.wait(0.3)

        self.wait(2)

        arrow = Arrow(
            start=code.get_right() + RIGHT * 0.5,
            end=stack_group[0].get_left() + LEFT * 0.5,
            buff=0.2,
            stroke_width=3
        )
        self.play(GrowArrow(arrow))
        self.wait(1)

        highlight_rect = SurroundingRectangle(stack_group[0], color=YELLOW, buff=0.1)
        self.play(Create(highlight_rect))
        self.wait(0.5)

        calc_text = MathTex(r"5 \times 24 = 120", color=YELLOW)
        calc_text.next_to(stack_group[0], DOWN, buff=0.5)
        self.play(Write(calc_text))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(math_def),
            FadeOut(code),
            FadeOut(stack_group),
            FadeOut(arrow),
            FadeOut(highlight_rect),
            FadeOut(calc_text)
        )
