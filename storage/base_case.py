
from manim import *

class Base_case(Scene):
    def construct(self):
        title = Text("Base Case: The stopping condition", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))

        countdown_group = VGroup()
        numbers = ["3", "2", "1", "0"]
        countdown_texts = []
        
        for i, num in enumerate(numbers):
            text = Text(num, font_size=120)
            countdown_texts.append(text)
            countdown_group.add(text)
            if i == 0:
                self.play(Write(text))
            else:
                self.play(Transform(countdown_texts[i-1], text))
            self.wait(0.8)
        
        stop_text = Text("Stop", font_size=120, color=RED)
        self.play(Transform(countdown_texts[-1], stop_text))
        self.wait(1.5)
        
        self.play(FadeOut(countdown_group))

        # Diagram showing recursive chain terminating at base case
        # Create nodes
        node_font_size = 36
        node_radius = 0.5
        
        # Recursive calls
        node1 = Circle(radius=node_radius, color=BLUE).set_fill(BLUE, opacity=0.5)
        text1 = Text("f(n)", font_size=node_font_size)
        group1 = VGroup(node1, text1).move_to(UP * 3 + LEFT * 3)
        
        node2 = Circle(radius=node_radius, color=BLUE).set_fill(BLUE, opacity=0.5)
        text2 = Text("f(n-1)", font_size=node_font_size)
        group2 = VGroup(node2, text2).next_to(group1, DOWN, buff=1.5)
        
        node3 = Circle(radius=node_radius, color=BLUE).set_fill(BLUE, opacity=0.5)
        text3 = Text("f(n-2)", font_size=node_font_size)
        group3 = VGroup(node3, text3).next_to(group2, DOWN, buff=1.5)
        
        # Base case
        node_base = Circle(radius=node_radius, color=GREEN).set_fill(GREEN, opacity=0.5)
        text_base = Text("f(0)", font_size=node_font_size)
        group_base = VGroup(node_base, text_base).next_to(group3, DOWN, buff=1.5)
        
        # Arrows
        arrow1 = Arrow(group1.get_bottom(), group2.get_top(), buff=0.1)
        arrow2 = Arrow(group2.get_bottom(), group3.get_top(), buff=0.1)
        arrow3 = Arrow(group3.get_bottom(), group_base.get_top(), buff=0.1)
        
        # Labels
        label_recursive = Text("Recursive calls", font_size=28).next_to(group2, RIGHT, buff=1)
        label_base_case = Text("Base case (terminates)", font_size=28, color=GREEN).next_to(group_base, RIGHT, buff=1)
        
        # Animate
        self.play(Create(group1))
        self.wait(0.5)
        self.play(Create(arrow1))
        self.play(Create(group2))
        self.wait(0.5)
        self.play(Create(arrow2))
        self.play(Create(group3))
        self.wait(0.5)
        self.play(Create(arrow3))
        self.play(Create(group_base))
        
        self.play(Write(label_recursive))
        self.play(Write(label_base_case))
        
        self.wait(3)
        
        # Highlight the termination
        self.play(node_base.animate.scale(1.2), run_time=0.5)
        self.play(node_base.animate.scale(1/1.2), run_time=0.5)
        
        self.wait(2)
