
from manim import *

class Scene_02(Scene):
    def construct(self):
        title = Text("Components of a Recursive Function", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Checklist graphic
        checklist_box = Square(side_length=0.5, color=BLUE, fill_opacity=0.2)
        check1 = VGroup(checklist_box.copy(), LabeledDot("1", color=BLUE, radius=0.25)).arrange(RIGHT, buff=0.5)
        check2 = VGroup(checklist_box.copy(), LabeledDot("2", color=BLUE, radius=0.25)).arrange(RIGHT, buff=0.5)
        checklist = VGroup(check1, check2).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        checklist.next_to(title, DOWN, buff=1)

        self.play(Create(checklist))
        self.wait(0.5)

        # Base Case Text
        base_text = Text("Base Case: The stopping condition", font_size=36, color=GREEN)
        base_text.next_to(check1, RIGHT, buff=0.8)
        
        # Recursive Step Text
        recursive_text = Text("Recursive Step: The function calls itself", font_size=36, color=YELLOW)
        recursive_text.next_to(check2, RIGHT, buff=0.8)

        self.play(Write(base_text))
        self.wait(1)
        self.play(Write(recursive_text))
        self.wait(2)

        # Highlight the importance
        self.play(
            Indent(base_text, 0.5, rate_func=there_and_back),
            Indent(recursive_text, 0.5, rate_func=there_and_back),
            run_time=1.5
        )
        self.wait(1)
