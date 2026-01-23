
from manim import *

class RecursionInComputerScience(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48, color=BLUE)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        flowchart_group = VGroup()
        
        func_box = Rectangle(width=3, height=1.5, color=WHITE, fill_opacity=0.2)
        func_text = Text("Function", font_size=24).move_to(func_box.get_center())
        func_group = VGroup(func_box, func_text)
        
        arrow = Arrow(start=func_box.get_bottom(), end=func_box.get_top() + DOWN * 0.5, buff=0.1, color=YELLOW)
        
        arrow_label = Text("calls itself", font_size=20, color=YELLOW).next_to(arrow, RIGHT)
        
        flowchart_group.add(func_group, arrow, arrow_label)
        flowchart_group.move_to(ORIGIN)
        
        self.play(Create(func_box), Write(func_text))
        self.wait(1)
        self.play(GrowArrow(arrow), Write(arrow_label))
        self.wait(1)
        
        overlay_text = Text("A function that calls itself", font_size=36, color=GREEN)
        overlay_text.to_edge(DOWN)
        
        self.play(Write(overlay_text))
        self.wait(3)
