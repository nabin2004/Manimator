
from manim import *

class Scene_04(Scene):
    def construct(self):
        # Title
        title = Text("Factorial Computation Trace", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # --- Setup Flowchart Nodes ---
        # Coordinates for the flowchart (vertical stack)
        y_positions = [2.5, 1.0, -0.5, -2.0]
        
        # Node 1: factorial(3)
        node1_rect = RoundedRectangle(width=3, height=1, corner_radius=0.2, color=BLUE)
        node1_text = MathTex(r"\text{factorial}(3)", font_size=36)
        node1_group = VGroup(node1_rect, node1_text).move_to([0, y_positions[0], 0])
        
        # Node 2: factorial(2)
        node2_rect = RoundedRectangle(width=3, height=1, corner_radius=0.2, color=BLUE)
        node2_text = MathTex(r"\text{factorial}(2)", font_size=36)
        node2_group = VGroup(node2_rect, node2_text).move_to([0, y_positions[1], 0])
        
        # Node 3: factorial(1)
        node3_rect = RoundedRectangle(width=3, height=1, corner_radius=0.2, color=BLUE)
        node3_text = MathTex(r"\text{factorial}(1)", font_size=36)
        node3_group = VGroup(node3_rect, node3_text).move_to([0, y_positions[2], 0])
        
        # Node 4: Base Case (1)
        node4_rect = RoundedRectangle(width=3, height=1, corner_radius=0.2, color=GREEN)
        node4_text = MathTex(r"\text{Base Case: return } 1", font_size=36)
        node4_group = VGroup(node4_rect, node4_text).move_to([0, y_positions[3], 0])

        # --- Animate Flowchart Construction (Downward) ---
        self.play(Create(node1_rect), Write(node1_text))
        self.wait(0.2)
        
        arrow1 = Arrow(node1_group.get_bottom(), node2_group.get_top(), buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow1))
        self.play(Create(node2_rect), Write(node2_text))
        self.wait(0.2)
        
        arrow2 = Arrow(node2_group.get_bottom(), node3_group.get_top(), buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow2))
        self.play(Create(node3_rect), Write(node3_text))
        self.wait(0.2)
        
        arrow3 = Arrow(node3_group.get_bottom(), node4_group.get_top(), buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow3))
        self.play(Create(node4_rect), Write(node4_text))
        self.wait(0.5)

        # --- Animate Stack Unwinding (Upward) with Multiplication ---
        
        # Step 1: factorial(1) returns 1
        ret_val_1 = MathTex(r"\Rightarrow 1", color=GREEN).next_to(node4_group, RIGHT, buff=0.2)
        self.play(Write(ret_val_1))
        self.wait(0.5)

        # Step 2: factorial(2) calculation
        # Show multiplication: 2 * 1
        calc_2 = MathTex(r"2 \times 1 = 2", color=YELLOW).move_to([-4, y_positions[1], 0])
        self.play(Write(calc_2))
        
        # Return value for factorial(2)
        ret_val_2 = MathTex(r"\Rightarrow 2", color=GREEN).next_to(node2_group, RIGHT, buff=0.2)
        self.play(Transform(calc_2, ret_val_2))
        self.wait(0.5)

        # Step 3: factorial(3) calculation
        # Show multiplication: 3 * 2
        calc_3 = MathTex(r"3 \times 2 = 6", color=YELLOW).move_to([-4, y_positions[0], 0])
        self.play(Write(calc_3))
        
        # Return value for factorial(3)
        ret_val_3 = MathTex(r"\Rightarrow 6", color=GREEN).next_to(node1_group, RIGHT, buff=0.2)
        self.play(Transform(calc_3, ret_val_3))
        self.wait(1)

        # Final highlight
        final_result = Text("Result: 6", font_size=40, color=GOLD).move_to([0, -3.5, 0])
        self.play(Write(final_result))
        self.wait(2)
