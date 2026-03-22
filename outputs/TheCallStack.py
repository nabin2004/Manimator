
from manim import *

class Thecallstack(Scene):
    def construct(self):
        title = Text("Execution Stack & Recursion", font_size=40).to_edge(UP)
        self.play(Write(title))

        code = Code(
            code="def fact(n):\n    if n == 1:\n        return 1\n    return n * fact(n-1)",
            language="python",
            font_size=24,
            line_spacing=0.8
        ).to_edge(LEFT, buff=1)
        self.play(Create(code))

        stack_label = Text("Memory Stack", font_size=30).shift(RIGHT * 3 + UP * 3)
        stack_base = Line(RIGHT * 1, RIGHT * 5).shift(DOWN * 3)
        self.play(Write(stack_label), Create(stack_base))

        frames = []
        calculations = [
            "fact(4)",
            "4 * fact(3)",
            "3 * fact(2)",
            "2 * fact(1)",
            "1"
        ]

        # Pushing frames
        for i in range(4):
            frame = VGroup(
                Rectangle(width=3.5, height=0.8, fill_opacity=0.2, color=BLUE),
                Text(calculations[i], font_size=24)
            )
            frame.move_to(RIGHT * 3 + DOWN * 2.5 + UP * (i * 0.9))
            
            pending_text = Text("PENDING", font_size=14, color=YELLOW).next_to(frame, RIGHT, buff=0.1)
            
            self.play(
                FadeIn(frame, shift=DOWN * 0.5),
                Write(pending_text),
                run_time=0.8
            )
            frames.append(VGroup(frame, pending_text))
            self.wait(0.3)

        # Base case highlight
        base_case_rect = SurroundingRectangle(code.code[1], color=GREEN)
        self.play(Create(base_case_rect))
        
        base_frame = VGroup(
            Rectangle(width=3.5, height=0.8, fill_opacity=0.5, color=GREEN),
            Text("return 1", font_size=24)
        ).move_to(RIGHT * 3 + DOWN * 2.5 + UP * (4 * 0.9))
        
        self.play(FadeIn(base_frame, shift=DOWN * 0.5))
        self.wait(1)
        self.play(Uncreate(base_case_rect))

        # Popping frames (Resolving)
        results = ["1", "2 * 1", "3 * 2", "4 * 6"]
        final_vals = ["1", "2", "6", "24"]

        self.play(FadeOut(base_frame, shift=UP * 0.5))

        for i in reversed(range(4)):
            resolved_text = Text(f"Result: {final_vals[i]}", font_size=24, color=GREEN)
            resolved_text.move_to(frames[i][0].get_center())
            
            self.play(
                Transform(frames[i][0][1], resolved_text),
                FadeOut(frames[i][1]),
                frames[i][0][0].animate.set_color(GREEN)
            )
            self.wait(0.5)
            self.play(FadeOut(frames[i], shift=UP * 0.5))

        final_msg = Text("Stack Cleared", color=WHITE, font_size=36).move_to(RIGHT * 3)
        self.play(Write(final_msg))
        self.wait(2)
