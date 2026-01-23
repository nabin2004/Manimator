
from manim import *

class Base_case(Scene):
    def construct(self):
        # Create the two boxes
        recursive_box = Rectangle(width=3, height=1.5, color=BLUE, fill_opacity=0.2)
        recursive_text = Text("Recursive Case", font_size=24).move_to(recursive_box.get_center())

        base_box = Rectangle(width=3, height=1.5, color=GREEN, fill_opacity=0.2).next_to(recursive_box, DOWN, buff=1)
        base_text = Text("Base Case", font_size=24).move_to(base_box.get_center())

        # Create checkmark
        checkmark = Checkmark(color=GREEN).scale(1.5).next_to(base_box, LEFT, buff=0.5)

        # Create stop sign
        stop_sign_group = VGroup()
        stop_sign = RegularPolygon(n=8, color=RED, fill_opacity=0.8, fill_color=RED)
        stop_sign.scale(0.5)
        stop_text = Text("STOP", color=WHITE, font_size=18, weight=BOLD).move_to(stop_sign.get_center())
        stop_sign_group.add(stop_sign, stop_text)
        stop_sign_group.next_to(base_box, RIGHT, buff=0.5)

        # Animation sequence
        self.play(Create(recursive_box), Write(recursive_text))
        self.wait(0.5)
        self.play(Create(base_box), Write(base_text))
        self.wait(0.5)
        
        # Emphasize the base case
        self.play(
            base_box.animate.set_fill(GREEN, opacity=0.5),
            base_text.animate.scale(1.2),
            run_time=0.5
        )
        self.play(
            base_box.animate.set_fill(GREEN, opacity=0.2),
            base_text.animate.scale(1/1.2),
            run_time=0.5
        )
        
        # Add checkmark and stop sign
        self.play(FadeIn(checkmark), FadeIn(stop_sign_group))
        self.wait(1)
