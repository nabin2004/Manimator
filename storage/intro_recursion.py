
from manim import *

class Intro_recursion(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        definition = Text("A function that calls itself", font_size=36, color=YELLOW)
        definition.next_to(title, DOWN, buff=1)
        self.play(FadeIn(definition, shift=UP))
        self.wait(1)

        # Create a visual representation of recursion
        # A function box calling another identical function box
        
        # Outer function box
        outer_box = Rectangle(width=4, height=2, color=WHITE, stroke_width=2)
        outer_label = Text("func()", font_size=24).move_to(outer_box)
        outer_group = VGroup(outer_box, outer_label)
        outer_group.move_to(LEFT * 3)

        # Inner function box (representing the recursive call)
        inner_box = Rectangle(width=4, height=2, color=WHITE, stroke_width=2)
        inner_label = Text("func()", font_size=24).move_to(inner_box)
        inner_group = VGroup(inner_box, inner_label)
        inner_group.move_to(RIGHT * 3)

        # Arrow indicating the call
        arrow = Arrow(outer_box.get_right(), inner_box.get_left(), buff=0.5, color=GREEN)
        arrow_label = Text("calls", font_size=20, color=GREEN).next_to(arrow, UP)

        self.play(Create(outer_group))
        self.wait(0.5)
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.play(Create(inner_group))
        self.wait(2)

        # Fade out to end the scene
        self.play(FadeOut(VGroup(title, definition, outer_group, inner_group, arrow, arrow_label)))
