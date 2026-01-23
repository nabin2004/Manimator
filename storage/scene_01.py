
from manim import *

class Scene_01(Scene):
    def construct(self):
        title = Text("Recursion", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create a simple function box
        func_box = Rectangle(width=3, height=1.5, color=WHITE, fill_opacity=0.2)
        func_text = Text("Function", font_size=24).move_to(func_box)
        func_group = VGroup(func_box, func_text)
        func_group.move_to(LEFT * 3)
        
        # Create a smaller copy for the recursive call
        rec_box = Rectangle(width=2, height=1, color=WHITE, fill_opacity=0.2)
        rec_text = Text("Function", font_size=18).move_to(rec_box)
        rec_group = VGroup(rec_box, rec_text)
        rec_group.move_to(RIGHT * 3)

        # Arrow pointing from function to itself
        arrow = Arrow(start=func_box.get_right(), end=rec_box.get_left(), buff=0.2, color=YELLOW)
        arrow_label = Text("calls", font_size=20).next_to(arrow, UP, buff=0.1)

        self.play(Create(func_group))
        self.wait(0.5)
        
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(0.5)
        
        self.play(Create(rec_group))
        self.wait(1)

        # Create a question mark icon
        question_mark = Text("?", font_size=60, color=RED)
        question_mark.next_to(rec_group, DOWN, buff=0.5)
        
        self.play(Write(question_mark))
        self.wait(1)

        # Highlight the self-referential nature
        self.play(
            Indicate(func_group, color=YELLOW),
            Indicate(rec_group, color=YELLOW),
            Indicate(arrow, color=YELLOW),
            run_time=1.5
        )
        self.wait(2)
