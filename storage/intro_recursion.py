
from manim import *

class Intro_recursion(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # Create the function box
        func_box = Rectangle(height=2, width=3, color=BLUE, fill_opacity=0.2)
        func_text = Text("Function", font_size=24).move_to(func_box)
        func_group = VGroup(func_box, func_text)
        
        self.play(Create(func_box), Write(func_text))
        self.wait(0.5)

        # Create the self-referential arrow
        arrow = CurvedArrow(
            start_point=func_box.get_right() + RIGHT * 0.5,
            end_point=func_box.get_right() + RIGHT * 0.5 + UP * 1.5 + LEFT * 0.5,
            angle=-PI/2,
            color=YELLOW
        )
        
        arrow_label = Text("calls itself", font_size=20, color=YELLOW)
        arrow_label.next_to(arrow, RIGHT, buff=0.1)

        self.play(Create(arrow), Write(arrow_label))
        self.wait(2)

        # Highlight the self-referential structure
        self.play(
            func_box.animate.set_fill(YELLOW, opacity=0.5),
            arrow.animate.set_stroke(width=5),
            run_time=1
        )
        self.wait(2)
