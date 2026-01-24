
from manim import *

class Factorial_example(Scene):
    def construct(self):
        # Title
        title = Text("Recursion: Factorial Example", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Base Equation
        equation = MathTex("n! = n \\times (n-1)!")
        equation.next_to(title, DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait(1)

        # Specific Example
        example = MathTex("5! = 5 \\times 4!").scale(1.2)
        example.move_to(equation)
        self.play(Transform(equation, example))
        self.wait(1)

        # Setup for Tree Visualization
        self.play(FadeOut(equation))
        
        # Tree Nodes positions (Calculated for 5! depth)
        # Level 0: 5!
        # Level 1: 4!
        # Level 2: 3!
        # Level 3: 2!
        # Level 4: 1!
        
        # Define nodes as VGroups
        nodes = VGroup()
        node_map = {}
        
        # Helper to create node
        def create_node(text, pos):
            circle = Circle(radius=0.4, color=BLUE, fill_opacity=0.2)
            label = MathTex(text, font_size=24)
            node = VGroup(circle, label)
            node.move_to(pos)
            return node

        # Calculate positions
        # Vertical spacing
        y_start = 3
        y_step = -1.5
        # Horizontal spacing (centered)
        x_center = 0
        
        # Level 0
        pos_5 = [x_center, y_start, 0]
        n_5 = create_node("5!", pos_5)
        node_map["5!"] = n_5
        
        # Level 1
        pos_4 = [x_center, y_start + y_step, 0]
        n_4 = create_node("4!", pos_4)
        node_map["4!"] = n_4
        
        # Level 2
        pos_3 = [x_center, y_start + 2*y_step, 0]
        n_3 = create_node("3!", pos_3)
        node_map["3!"] = n_3
        
        # Level 3
        pos_2 = [x_center, y_start + 3*y_step, 0]
        n_2 = create_node("2!", pos_2)
        node_map["2!"] = n_2
        
        # Level 4
        pos_1 = [x_center, y_start + 4*y_step, 0]
        n_1 = create_node("1!", pos_1)
        node_map["1!"] = n_1
        
        # Base case result
        pos_0 = [x_center, y_start + 5*y_step, 0]
        n_0 = create_node("1", pos_0)
        n_0[0].set_color(GREEN)
        node_map["1"] = n_0

        nodes.add(n_5, n_4, n_3, n_2, n_1, n_0)

        # Lines connecting nodes
        lines = VGroup()
        line_5_4 = Line(n_5.get_bottom(), n_4.get_top(), buff=0.1)
        line_4_3 = Line(n_4.get_bottom(), n_3.get_top(), buff=0.1)
        line_3_2 = Line(n_3.get_bottom(), n_2.get_top(), buff=0.1)
        line_2_1 = Line(n_2.get_bottom(), n_1.get_top(), buff=0.1)
        line_1_0 = Line(n_1.get_bottom(), n_0.get_top(), buff=0.1)
        lines.add(line_5_4, line_4_3, line_3_2, line_2_1, line_1_0)

        # Animation: Building the Tree (Call Stack)
        self.play(LaggedStart(
            Write(n_5),
            GrowFromCenter(line_5_4),
            Write(n_4),
            GrowFromCenter(line_4_3),
            Write(n_3),
            GrowFromCenter(line_3_2),
            Write(n_2),
            GrowFromCenter(line_2_1),
            Write(n_1),
            GrowFromCenter(line_1_0),
            Write(n_0),
            lag_ratio=0.5
        ))
        self.wait(1)

        # Text for "Base Case Reached"
        base_text = Text("Base Case Reached (1! = 1)", font_size=24, color=GREEN)
        base_text.next_to(n_0, DOWN, buff=0.5)
        self.play(Write(base_text))
        self.wait(1)

        # Animation: Unwinding the Stack (Calculation)
        # We will show the results popping up
        
        # 1! = 1 (Already shown as '1')
        
        # 2! = 2 * 1!
        res_2 = MathTex("= 2 \\times 1 = 2", color=YELLOW).scale(0.7)
        res_2.next_to(n_2, RIGHT)
        self.play(Write(res_2))
        self.play(n_2[0].animate.set_color(GREEN))
        self.wait(0.5)

        # 3! = 3 * 2!
        res_3 = MathTex("= 3 \\times 2 = 6", color=YELLOW).scale(0.7)
        res_3.next_to(n_3, RIGHT)
        self.play(Write(res_3))
        self.play(n_3[0].animate.set_color(GREEN))
        self.wait(0.5)

        # 4! = 4 * 3!
        res_4 = MathTex("= 4 \\times 6 = 24", color=YELLOW).scale(0.7)
        res_4.next_to(n_4, RIGHT)
        self.play(Write(res_4))
        self.play(n_4[0].animate.set_color(GREEN))
        self.wait(0.5)

        # 5! = 5 * 4!
        res_5 = MathTex("= 5 \\times 24 = 120", color=YELLOW).scale(0.7)
        res_5.next_to(n_5, RIGHT)
        self.play(Write(res_5))
        self.play(n_5[0].animate.set_color(GREEN))
        self.wait(1)

        # Final Result Display
        final_result = Text("5! = 120", font_size=48, color=GREEN)
        final_result.move_to([0, -3.5, 0])
        self.play(Write(final_result))
        self.wait(2)
