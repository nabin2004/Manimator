
from manim import *

class Factorial_example(Scene):
    def construct(self):
        title = Text("Recursion: Factorial Example", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Mathematical definition
        definition = MathTex("n! = n \\times (n-1)!")
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait(1)

        # Visual Tree Setup
        tree_group = VGroup()
        
        # Level 0: Factorial(4)
        node_4 = VGroup(
            RegularPolygon(6, color=BLUE, fill_opacity=0.2).scale(0.8),
            MathTex("4!").scale(0.8)
        )
        node_4.arrange()
        node_4.move_to(LEFT * 4 + UP * 1.5)
        
        # Level 1: Factorial(3)
        node_3 = VGroup(
            RegularPolygon(6, color=TEAL, fill_opacity=0.2).scale(0.8),
            MathTex("3!").scale(0.8)
        )
        node_3.arrange()
        node_3.move_to(LEFT * 2 + UP * 0.5)

        # Level 2: Factorial(2)
        node_2 = VGroup(
            RegularPolygon(6, color=GREEN, fill_opacity=0.2).scale(0.8),
            MathTex("2!").scale(0.8)
        )
        node_2.arrange()
        node_2.move_to(RIGHT * 0 + UP * 0.5)

        # Level 3: Factorial(1)
        node_1 = VGroup(
            RegularPolygon(6, color=YELLOW, fill_opacity=0.2).scale(0.8),
            MathTex("1!").scale(0.8)
        )
        node_1.arrange()
        node_1.move_to(RIGHT * 2 + UP * 0.5)

        # Level 4: Base Case (1)
        node_base = VGroup(
            RegularPolygon(6, color=RED, fill_opacity=0.2).scale(0.8),
            MathTex("1").scale(0.8)
        )
        node_base.arrange()
        node_base.move_to(RIGHT * 4 + UP * 0.5)

        # Connectors
        line_4_3 = Line(node_4.get_bottom(), node_3.get_top(), buff=0.1)
        line_3_2 = Line(node_3.get_bottom(), node_2.get_top(), buff=0.1)
        line_2_1 = Line(node_2.get_bottom(), node_1.get_top(), buff=0.1)
        line_1_base = Line(node_1.get_bottom(), node_base.get_top(), buff=0.1)

        # Animate Tree Construction
        self.play(
            FadeIn(node_4),
            FadeIn(node_3),
            FadeIn(node_2),
            FadeIn(node_1),
            FadeIn(node_base)
        )
        
        self.play(
            Create(line_4_3),
            Create(line_3_2),
            Create(line_2_1),
            Create(line_1_base)
        )
        self.wait(1)

        # Step-by-step Calculation Overlay
        calc_title = Text("Calculation Trace", font_size=32)
        calc_title.next_to(definition, DOWN, buff=0.8)
        calc_title.shift(LEFT * 3.5)
        self.play(Write(calc_title))

        # Trace arrows
        trace_group = VGroup()
        trace_text = MathTex("4 \\to 3 \\to 2 \\to 1 \\to 1")
        trace_text.scale(1.2)
        trace_text.next_to(calc_title, DOWN)
        
        self.play(Write(trace_text))
        self.wait(1)

        # Highlight expansion
        self.play(node_4[0].animate.set_fill(BLUE, opacity=0.5))
        self.wait(0.2)
        self.play(node_3[0].animate.set_fill(TEAL, opacity=0.5))
        self.wait(0.2)
        self.play(node_2[0].animate.set_fill(GREEN, opacity=0.5))
        self.wait(0.2)
        self.play(node_1[0].animate.set_fill(YELLOW, opacity=0.5))
        self.wait(0.2)
        self.play(node_base[0].animate.set_fill(RED, opacity=0.5))
        self.wait(1)

        # Final Result
        result_box = SurroundingRectangle(trace_text, color=YELLOW, buff=0.2)
        result_text = MathTex("4! = 24").scale(1.5)
        result_text.next_to(trace_text, DOWN, buff=0.5)
        
        self.play(Create(result_box))
        self.play(Write(result_text))
        self.wait(2)
