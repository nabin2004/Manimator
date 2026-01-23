
from manim import *

class TwoScene(Scene):
    def construct(self):
        title = Text("Recursive Function Structure", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen setup
        left_box = Rectangle(width=FRAME_WIDTH/2 - 1, height=FRAME_HEIGHT - 2.5, color=BLUE, fill_opacity=0.1)
        left_label = Text("Base Case", font_size=36, color=BLUE).next_to(left_box, UP)
        left_group = VGroup(left_box, left_label)
        left_group.move_to(LEFT * (FRAME_WIDTH/4))

        right_box = Rectangle(width=FRAME_WIDTH/2 - 1, height=FRAME_HEIGHT - 2.5, color=GREEN, fill_opacity=0.1)
        right_label = Text("Recursive Step", font_size=36, color=GREEN).next_to(right_box, UP)
        right_group = VGroup(right_box, right_label)
        right_group.move_to(RIGHT * (FRAME_WIDTH/4))

        self.play(Create(left_box), Create(right_box))
        self.play(Write(left_label), Write(right_label))
        self.wait(0.5)

        # Left: Base Case (Stop Sign)
        stop_sign = RegularPolygon(n=8, color=RED, fill_color=RED, fill_opacity=0.8)
        stop_sign.scale(1.2)
        stop_sign.move_to(left_box.get_center() + UP * 0.5)
        
        stop_text = Text("STOP", font_size=28, color=WHITE).move_to(stop_sign.get_center())
        stop_group = VGroup(stop_sign, stop_text)

        base_desc = Text("Terminates recursion", font_size=24).next_to(stop_sign, DOWN, buff=0.5)
        base_code = Text("if n == 0:", font_size=22, color=YELLOW).next_to(base_desc, DOWN, buff=0.3)
        base_return = Text("    return 1", font_size=22, color=YELLOW).next_to(base_code, DOWN)

        self.play(DrawBorderThenFill(stop_sign), Write(stop_text))
        self.play(Write(base_desc))
        self.wait(0.3)
        self.play(Write(base_code), Write(base_return))
        self.wait(1)

        # Right: Recursive Step (Looping Arrow)
        arrow_path = Arc(radius=1.5, angle=TAU, color=GREEN)
        arrow_path.move_to(right_box.get_center() + UP * 0.2)
        
        arrow_head = Triangle(color=GREEN, fill_color=GREEN, fill_opacity=1)
        arrow_head.scale(0.15)
        arrow_head.next_to(arrow_path.point_at_angle(-PI/4), RIGHT, buff=0)
        arrow_head.rotate(-PI/4)

        arrow_group = VGroup(arrow_path, arrow_head)

        rec_desc = Text("Moves toward base case", font_size=24).next_to(arrow_path, DOWN, buff=0.5)
        rec_code = Text("return n + func(n-1)", font_size=22, color=YELLOW).next_to(rec_desc, DOWN, buff=0.3)

        self.play(Create(arrow_path), GrowArrow(arrow_head))
        self.play(Write(rec_desc))
        self.wait(0.3)
        self.play(Write(rec_code))
        self.wait(2)

        # Final Summary
        summary = Text("Both are required for a valid recursive function.", font_size=30, color=WHITE)
        summary.to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
