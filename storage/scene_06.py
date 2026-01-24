
from manim import *

class Scene_06(Scene):
    def construct(self):
        warning_icon = self.create_warning_icon()
        warning_text = Text("Common Pitfalls", font_size=48, color=YELLOW).next_to(warning_icon, DOWN)
        warning_group = VGroup(warning_icon, warning_text)
        
        self.play(FadeIn(warning_icon), Write(warning_text))
        self.wait(1)
        self.play(warning_group.animate.scale(0.6).to_edge(UP))
        
        # Infinite Loop Animation
        infinite_title = Text("1. Infinite Recursion", font_size=36, color=RED).next_to(warning_group, DOWN, buff=0.5)
        spinning_circle = Circle(radius=0.8, color=ORANGE)
        arrow = Arrow(start=spinning_circle.get_right(), end=spinning_circle.get_top(), buff=0, color=YELLOW)
        
        self.play(Write(infinite_title))
        self.play(Create(spinning_circle), Create(arrow))
        self.play(Rotate(arrow, angle=2*PI, run_time=3, rate_func=linear))
        
        stack_overflow_text = Text("Stack Overflow!", font_size=30, color=RED).next_to(spinning_circle, DOWN)
        self.play(Write(stack_overflow_text))
        self.wait(1)
        
        self.play(FadeOut(spinning_circle), FadeOut(arrow), FadeOut(stack_overflow_text))
        
        # Missing Base Case
        base_case_title = Text("2. Missing Base Case", font_size=36, color=RED).next_to(infinite_title, DOWN, buff=1)
        
        # Visual representation of recursion tree
        node_radius = 0.25
        root = Circle(radius=node_radius, color=WHITE).move_to(LEFT * 3 + UP * 1)
        root_label = Text("n", font_size=20).move_to(root.get_center())
        
        child1 = Circle(radius=node_radius, color=WHITE).move_to(LEFT * 4 + DOWN * 0.5)
        child1_label = Text("n-1", font_size=20).move_to(child1.get_center())
        
        child2 = Circle(radius=node_radius, color=WHITE).move_to(LEFT * 2 + DOWN * 0.5)
        child2_label = Text("n-1", font_size=20).move_to(child2.get_center())
        
        line1 = Line(root.get_bottom(), child1.get_top(), color=WHITE)
        line2 = Line(root.get_bottom(), child2.get_top(), color=WHITE)
        
        # More nodes to show infinite nature
        child1_1 = Circle(radius=node_radius, color=WHITE).move_to(LEFT * 5 + DOWN * 2)
        child1_1_label = Text("n-2", font_size=20).move_to(child1_1.get_center())
        line3 = Line(child1.get_bottom(), child1_1.get_top(), color=WHITE)
        
        # Warning X marks
        x_mark1 = Cross(child1_1, stroke_color=RED, stroke_width=6)
        
        self.play(Write(base_case_title))
        self.play(Create(root), Write(root_label))
        self.wait(0.5)
        self.play(Create(line1), Create(line2), Create(child1), Create(child2), Write(child1_label), Write(child2_label))
        self.wait(0.5)
        self.play(Create(line3), Create(child1_1), Write(child1_1_label))
        self.wait(0.5)
        self.play(Create(x_mark1))
        
        no_base_text = Text("No stopping condition!", font_size=28, color=RED).next_to(child1_1, DOWN)
        self.play(Write(no_base_text))
        self.wait(2)
        
        # Solution
        solution_title = Text("Solution: Define Base Case", font_size=32, color=GREEN).to_edge(DOWN)
        
        # Correct example
        correct_root = Circle(radius=node_radius, color=GREEN).move_to(LEFT * 3 + UP * 0.5)
        correct_root_label = Text("n", font_size=20).move_to(correct_root.get_center())
        
        correct_child = Circle(radius=node_radius, color=GREEN).move_to(LEFT * 3 + DOWN * 1)
        correct_child_label = Text("n-1", font_size=20).move_to(correct_child.get_center())
        
        correct_line = Line(correct_root.get_bottom(), correct_child.get_top(), color=GREEN)
        
        base_node = Square(side_length=0.5, color=GREEN, fill_opacity=0.3).move_to(LEFT * 3 + DOWN * 2.5)
        base_label = Text("0", font_size=24).move_to(base_node.get_center())
        
        check_mark = Checkmark(base_node, color=GREEN, stroke_width=5)
        
        self.play(
            FadeOut(spinning_circle),
            FadeOut(arrow),
            FadeOut(stack_overflow_text),
            FadeOut(root), FadeOut(root_label),
            FadeOut(child1), FadeOut(child1_label),
            FadeOut(child2), FadeOut(child2_label),
            FadeOut(line1), FadeOut(line2),
            FadeOut(child1_1), FadeOut(child1_1_label),
            FadeOut(line3), FadeOut(x_mark1),
            FadeOut(no_base_text),
            FadeOut(infinite_title),
            FadeOut(base_case_title)
        )
        
        self.play(Write(solution_title))
        self.play(Create(correct_root), Write(correct_root_label))
        self.play(Create(correct_line), Create(correct_child), Write(correct_child_label))
        self.wait(0.5)
        self.play(Create(base_node), Write(base_label))
        self.play(Create(check_mark))
        
        final_text = Text("Always define a base case!", font_size=36, color=GREEN).next_to(base_node, DOWN, buff=1)
        self.play(Write(final_text))
        self.wait(2)
