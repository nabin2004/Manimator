
from manim import *

class Scene_02(Scene):
    def construct(self):
        title = Text("Base Case: The stopping condition", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Flowchart node
        node_box = RoundedRectangle(height=2, width=4, color=GREEN, fill_opacity=0.2)
        node_text = Text("Base Case", font_size=36)
        node_group = VGroup(node_box, node_text).move_to(LEFT * 3.5)
        
        checkmark = Checkmark(color=GREEN).scale(1.5)
        checkmark.next_to(node_group, RIGHT, buff=0.5)
        
        self.play(Create(node_box), Write(node_text))
        self.play(Create(checkmark))
        self.wait(1)

        # Counter example
        example_title = Text("Example:", font_size=32, color=YELLOW)
        example_title.next_to(node_group, DOWN, buff=1)
        
        code_text = Text("countdown(0) stops", font_size=36)
        code_text.next_to(example_title, DOWN, buff=0.5)
        
        self.play(Write(example_title))
        self.play(Write(code_text))
        self.wait(1)

        # Emphasis text
        emphasis = Text("Every recursive solution needs a base case\nto prevent infinite recursion.", 
                       font_size=32, color=RED, line_spacing=1.2)
        emphasis.to_edge(DOWN)
        
        self.play(Write(emphasis))
        self.wait(2)
