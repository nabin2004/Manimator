
from manim import *

class Scene_01(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Function box
        func_box = Rectangle(width=3, height=1.5, color=BLUE)
        func_text = Text("solve()", font_size=24).move_to(func_box)
        func_group = VGroup(func_box, func_text)
        
        self.play(Create(func_box), Write(func_text))
        self.wait(0.5)

        # Arrow pointing to itself
        arrow = CurvedArc(radius=1.5, angle=PI/2, color=WHITE)
        arrow.shift(RIGHT * 1.5)
        arrow_label = Text("calls itself", font_size=20).next_to(arrow, UP, buff=0.1)
        
        self.play(Create(arrow), Write(arrow_label))
        self.wait(0.5)

        # Question mark
        question_mark = Text("?", font_size=60, color=YELLOW)
        question_mark.next_to(func_group, DOWN, buff=1)
        
        self.play(Write(question_mark))
        self.wait(2)

        # Fade out
        self.play(FadeOut(VGroup(title, func_group, arrow, arrow_label, question_mark)))
