
from manim import *

class Scene_02(Scene):
    def construct(self):
        # Title
        title = Text("Base Case in Recursion", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Flowchart setup
        start_node = Rectangle(width=2, height=1, color=BLUE, fill_opacity=0.2)
        start_text = Text("Start", font_size=24).move_to(start_node)
        start_group = VGroup(start_node, start_text)
        start_group.move_to(LEFT * 4 + UP * 1)

        arrow1 = Arrow(start_node.get_bottom(), start_node.get_bottom() + DOWN * 1.5, buff=0.1)

        recursive_node = Rectangle(width=3, height=1.5, color=YELLOW, fill_opacity=0.2)
        recursive_text = Text("Recursive Step", font_size=24).move_to(recursive_node)
        recursive_group = VGroup(recursive_node, recursive_text)
        recursive_group.next_to(arrow1, DOWN, buff=0)

        arrow2 = Arrow(recursive_node.get_bottom(), recursive_node.get_bottom() + DOWN * 1.5, buff=0.1)

        base_node = Rectangle(width=2.5, height=1.5, color=GREEN, fill_opacity=0.3)
        base_text = Text("Base Case", font_size=28, color=GREEN_D).move_to(base_node)
        base_group = VGroup(base_node, base_text)
        base_group.next_to(arrow2, DOWN, buff=0)

        # Checklist icon near Base Case
        checklist = VGroup(
            Square(side_length=0.3, color=GREEN, fill_opacity=0.5),
            Line(LEFT * 0.1 + UP * 0.05, RIGHT * 0.1 + DOWN * 0.1, color=WHITE, stroke_width=3),
            Line(RIGHT * 0.1 + DOWN * 0.1, RIGHT * 0.25 + UP * 0.15, color=WHITE, stroke_width=3)
        )
        checklist.next_to(base_node, LEFT, buff=0.5)
        checklist_label = Text("Base Case", font_size=20, color=GREEN).next_to(checklist, RIGHT, buff=0.2)

        # Example text
        example = Text("Example: factorial(0) = 1", font_size=30, color=WHITE)
        example.next_to(base_group, DOWN, buff=0.5)

        # Warning text for infinite loop
        warning_text = Text("Without Base Case: Infinite Recursion!", font_size=24, color=RED)
        warning_text.next_to(recursive_group, RIGHT, buff=1)

        # Draw flowchart
        self.play(Create(start_node), Write(start_text))
        self.play(Create(arrow1))
        self.play(Create(recursive_node), Write(recursive_text))
        self.play(Create(arrow2))
        self.play(Create(base_node), Write(base_text))
        self.wait(1)

        # Add checklist
        self.play(Create(checklist), Write(checklist_label))
        self.wait(0.5)

        # Show example
        self.play(Write(example))
        self.wait(1)

        # Highlight the importance
        self.play(Indicate(base_node, color=GREEN))
        self.wait(0.5)

        # Show warning (conceptual)
        self.play(Write(warning_text))
        self.wait(2)

        # Fade out warning and emphasize base case
        self.play(FadeOut(warning_text))
        self.play(Indicate(base_group, color=GREEN))
        self.wait(2)

        # Clean up
        self.play(FadeOut(VGroup(title, start_group, arrow1, recursive_group, arrow2, base_group, checklist, checklist_label, example)))
        self.wait(1)
