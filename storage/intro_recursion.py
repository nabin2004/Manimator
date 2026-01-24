
from manim import *

class Intro_recursion(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))

        flowchart_group = VGroup()
        
        func_box = Rectangle(width=3, height=1.5, color=WHITE, fill_opacity=0.2)
        func_text = Text("Function", font_size=24).move_to(func_box)
        func_group = VGroup(func_box, func_text)
        
        arrow = Arrow(start=func_box.get_bottom(), end=func_box.get_bottom() + DOWN * 1.5, buff=0.1)
        
        self_box = Rectangle(width=3, height=1.5, color=YELLOW, fill_opacity=0.2)
        self_text = Text("Function (Self)", font_size=24).move_to(self_box)
        self_group = VGroup(self_box, self_text)
        self_group.next_to(arrow, DOWN)

        flowchart_group.add(func_group, arrow, self_group)
        flowchart_group.move_to(ORIGIN).shift(DOWN * 0.5)

        self.play(Create(func_box), Write(func_text))
        self.play(Create(arrow))
        self.play(Create(self_box), Write(self_text))

        description = Text(
            "Solving a problem by breaking it into\nsmaller, similar problems",
            font_size=32,
            color=GREEN,
            line_spacing=1.2
        )
        description.next_to(flowchart_group, DOWN, buff=1)

        self.play(Write(description))
        self.wait(3)
