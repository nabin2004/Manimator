
from manim import *

class Scene_03(Scene):
    def construct(self):
        # Title
        title = Text("Recursive Step", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Flowchart setup
        flowchart_group = VGroup()
        
        # Box for current call
        current_box = Rectangle(width=3, height=1.5, color=BLUE, fill_opacity=0.2)
        current_text = Text("factorial(n)", font_size=24).move_to(current_box)
        current_group = VGroup(current_box, current_text)
        current_group.move_to(LEFT * 4 + UP * 1)
        
        # Box for recursive call
        recursive_box = Rectangle(width=3, height=1.5, color=GREEN, fill_opacity=0.2)
        recursive_text = Text("factorial(n-1)", font_size=24).move_to(recursive_box)
        recursive_group = VGroup(recursive_box, recursive_text)
        recursive_group.move_to(RIGHT * 4 + DOWN * 1)
        
        # Arrow from current to recursive
        arrow_down = Arrow(current_box.get_bottom(), recursive_box.get_top(), buff=0.1, color=YELLOW)
        arrow_down_label = Text("Recursive Call", font_size=20).next_to(arrow_down, RIGHT)
        
        # Arrow looping back (curved)
        arrow_loop = CurvedArrow(recursive_box.get_left(), current_box.get_left(), angle=PI/2, color=RED)
        arrow_loop_label = Text("Loop Back", font_size=20).next_to(arrow_loop, LEFT)
        
        flowchart_group.add(current_group, recursive_group, arrow_down, arrow_down_label, arrow_loop, arrow_loop_label)
        
        self.play(Create(current_group), Create(recursive_group))
        self.play(GrowArrow(arrow_down), Write(arrow_down_label))
        self.play(GrowArrow(arrow_loop), Write(arrow_loop_label))
        self.wait(2)
        
        # Equation
        equation = MathTex(r"\text{factorial}(n) = n \times \text{factorial}(n-1)", font_size=40)
        equation.next_to(flowchart_group, DOWN, buff=1)
        
        self.play(Write(equation))
        self.wait(2)
        
        # Stack of blocks representing calls
        # Create 3 blocks for n, n-1, n-2
        stack_group = VGroup()
        blocks = []
        labels = []
        
        for i in range(3):
            block = Rectangle(width=2.5, height=0.8, color=PURPLE, fill_opacity=0.3)
            if i == 0:
                label = MathTex(r"n", font_size=24)
            elif i == 1:
                label = MathTex(r"n-1", font_size=24)
            else:
                label = MathTex(r"n-2", font_size=24)
            label.move_to(block)
            block_group = VGroup(block, label)
            blocks.append(block_group)
            labels.append(label)
        
        # Position stack to the right
        stack_pos = RIGHT * 4 + UP * 1
        blocks[0].move_to(stack_pos)
        blocks[1].move_to(stack_pos + DOWN * 1)
        blocks[2].move_to(stack_pos + DOWN * 2)
        
        stack_group.add(*blocks)
        
        # Animate stack building
        self.play(FadeOut(flowchart_group), FadeOut(equation))
        self.play(Write(Text("Stack of Calls", font_size=30).move_to(UP * 3)))
        
        self.play(Create(blocks[0]))
        self.wait(0.5)
        self.play(Create(blocks[1]))
        self.wait(0.5)
        self.play(Create(blocks[2]))
        self.wait(2)
        
        # Highlight the recursive step in the stack
        self.play(blocks[1].animate.set_fill(RED, opacity=0.5))
        self.wait(1)
        self.play(blocks[1].animate.set_fill(PURPLE, opacity=0.3))
        
        # Fade out
        self.play(FadeOut(stack_group))
        self.wait(1)
