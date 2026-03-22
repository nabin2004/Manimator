
from manim import *

class Factorialexample(Scene):
    def construct(self):
        title = Text("Recursive Breakdown: n!", font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        steps = VGroup(
            Text("factorial(3)", font_size=36, font="Monospace"),
            Text("3 * factorial(2)", font_size=36, font="Monospace"),
            Text("2 * factorial(1)", font_size=36, font="Monospace"),
            Text("1 * factorial(0)", font_size=36, font="Monospace")
        )
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        steps.shift(LEFT * 1.5 + DOWN * 0.5)

        arrows = VGroup()
        for i in range(len(steps) - 1):
            arrow = CurvedArrow(
                steps[i].get_left() + LEFT * 0.2,
                steps[i+1].get_left() + LEFT * 0.2,
                angle=PI/2
            )
            arrows.add(arrow)

        self.play(Write(steps[0]))
        self.wait(0.5)

        for i in range(len(arrows)):
            self.play(
                Create(arrows[i]),
                FadeIn(steps[i+1], shift=DOWN * 0.3)
            )
            self.wait(0.5)

        base_case_rect = SurroundingRectangle(steps[-1], color=YELLOW)
        base_case_label = Text("Base Case", color=YELLOW, font_size=24).next_to(base_case_rect, RIGHT)
        
        self.play(Create(base_case_rect))
        self.play(Write(base_case_label))
        self.wait(2)
