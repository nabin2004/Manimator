
from manim import *

class Thestructure(Scene):
    def construct(self):
        title = Text("Anatomy of Recursion", font_size=48).to_edge(UP)
        divider = Line(start=DOWN * 3, end=UP * 1, color=WHITE)
        
        self.play(Write(title))
        self.play(Create(divider))

        base_case_group = VGroup()
        bc_title = Text("1. Base Case", color=RED).scale(0.8)
        bc_desc = Text("The stopping condition", font_size=24).next_to(bc_title, DOWN)
        
        stop_sign = VGroup()
        octagon = RegularPolygon(n=8, color=RED, fill_opacity=1).scale(1.2)
        stop_text = Text("STOP", weight=BOLD).scale(0.6)
        stop_sign.add(octagon, stop_text)
        
        base_case_group.add(bc_title, bc_desc, stop_sign)
        base_case_group.arrange(DOWN, buff=0.5).shift(LEFT * 3.5 + DOWN * 0.5)

        recursive_step_group = VGroup()
        rs_title = Text("2. Recursive Step", color=BLUE).scale(0.8)
        rs_desc = Text("The self-referential call", font_size=24).next_to(rs_title, DOWN)
        
        loop_arrow = Arc(radius=0.8, start_angle=0, angle=TAU * 0.8, color=BLUE)
        loop_arrow.add_tip()
        loop_icon = VGroup(loop_arrow, Dot(radius=0.05).move_to(loop_arrow.get_start()))
        
        recursive_step_group.add(rs_title, rs_desc, loop_icon)
        recursive_step_group.arrange(DOWN, buff=0.5).shift(RIGHT * 3.5 + DOWN * 0.5)

        self.play(
            FadeIn(bc_title, shift=RIGHT),
            FadeIn(bc_desc, shift=UP)
        )
        self.play(DrawBorderThenFill(stop_sign))
        self.wait(1)

        self.play(
            FadeIn(rs_title, shift=LEFT),
            FadeIn(rs_desc, shift=UP)
        )
        self.play(Create(loop_arrow), FadeIn(loop_icon[1]))
        self.play(Rotate(loop_arrow, angle=TAU, about_point=loop_arrow.get_center()))
        self.wait(1)

        theory_box = SurroundingRectangle(VGroup(base_case_group, recursive_step_group), color=YELLOW, buff=0.5)
        theory_text = Text("Theoretical Framework: Solve smaller sub-problems until the base is reached.", font_size=20, color=YELLOW).to_edge(DOWN)
        
        self.play(Create(theory_box))
        self.play(Write(theory_text))
        self.wait(3)
