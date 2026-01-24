
from manim import *

class Scene_03(Scene):
    def construct(self):
        title = Text("Recursive Step: Reduce the problem size", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Arrow diagram: n -> n-1
        n_text = MathTex("n", font_size=72)
        n_text.move_to(LEFT * 3)
        arrow1 = Arrow(n_text.get_right(), n_text.get_right() + RIGHT * 2, buff=0.1)
        n_minus_1_text = MathTex("n-1", font_size=72)
        n_minus_1_text.next_to(arrow1, RIGHT)

        self.play(Write(n_text))
        self.play(GrowArrow(arrow1), Write(n_minus_1_text))
        self.wait(1)

        # Code snippet
        code_str = "return n + factorial(n-1)"
        code = Code(code=code_str, language="python", font="Monospace", background="rectangle", background_stroke_color=WHITE, background_stroke_width=1, background_fill_color=BLACK, background_fill_opacity=0.8, insert_line_no=False, style="monokai")
        code.scale(0.8)
        code.next_to(n_minus_1_text, DOWN, buff=1)

        self.play(Write(code))
        self.wait(2)

        # Highlight the recursive call part
        # Since Code object doesn't support direct sub-selection easily, we'll overlay a highlight box
        # We approximate the position of "factorial(n-1)" within the code
        # The code is a single line, so we can highlight the whole line or just the relevant part
        # Let's highlight the whole line to emphasize the return statement
        highlight_box = SurroundingRectangle(code, color=YELLOW, buff=0.1)
        self.play(Create(highlight_box))
        self.wait(1)

        # Animate the reduction
        # Create a copy of n-1 and move it to the position of n for the next step
        n_minus_1_copy = n_minus_1_text.copy()
        n_minus_1_copy.move_to(n_text.get_center())
        
        self.play(
            Transform(n_minus_1_text, n_minus_1_copy),
            FadeOut(arrow1),
            FadeOut(n_text),
            FadeOut(highlight_box),
            FadeOut(code)
        )
        self.wait(1)

        # Show the base case implication
        base_case_text = Text("... until base case", font_size=36)
        base_case_text.next_to(n_minus_1_text, DOWN, buff=1)
        self.play(Write(base_case_text))
        self.wait(2)
