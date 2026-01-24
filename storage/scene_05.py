
from manim import *

class Scene_05(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Create side-by-side panels
        left_panel = Rectangle(width=6, height=5, color=BLUE, fill_opacity=0.1)
        right_panel = Rectangle(width=6, height=5, color=GREEN, fill_opacity=0.1)
        left_panel.shift(LEFT * 3.5)
        right_panel.shift(RIGHT * 3.5)
        
        left_label = Text("Recursion", font_size=24).next_to(left_panel, UP)
        right_label = Text("Iteration", font_size=24).next_to(right_panel, UP)
        
        self.play(Create(left_panel), Create(right_panel))
        self.play(Write(left_label), Write(right_label))
        self.wait(0.5)

        # Recursion flowchart
        rec_box1 = Rectangle(width=2, height=0.8, color=BLUE).move_to(left_panel.get_center() + UP * 1.5)
        rec_text1 = Text("factorial(n)", font_size=18).move_to(rec_box1.get_center())
        rec_box2 = Rectangle(width=2, height=0.8, color=BLUE).move_to(left_panel.get_center())
        rec_text2 = Text("n <= 1?", font_size=18).move_to(rec_box2.get_center())
        rec_box3 = Rectangle(width=2, height=0.8, color=BLUE).move_to(left_panel.get_center() + DOWN * 1.5)
        rec_text3 = Text("return 1", font_size=18).move_to(rec_box3.get_center())
        rec_box4 = Rectangle(width=2, height=0.8, color=BLUE).move_to(left_panel.get_center() + DOWN * 3)
        rec_text4 = Text("return n * factorial(n-1)", font_size=18).move_to(rec_box4.get_center())
        
        rec_arrow1 = Arrow(rec_box1.get_bottom(), rec_box2.get_top(), buff=0.1, color=BLUE)
        rec_arrow2 = Arrow(rec_box2.get_bottom(), rec_box3.get_top(), buff=0.1, color=BLUE)
        rec_arrow3 = Arrow(rec_box2.get_right(), rec_box4.get_left(), buff=0.1, color=BLUE)
        
        self.play(
            Create(rec_box1), Write(rec_text1),
            Create(rec_box2), Write(rec_text2),
            Create(rec_box3), Write(rec_text3),
            Create(rec_box4), Write(rec_text4),
            Create(rec_arrow1), Create(rec_arrow2), Create(rec_arrow3)
        )
        self.wait(1)

        # Iteration flowchart
        iter_box1 = Rectangle(width=2, height=0.8, color=GREEN).move_to(right_panel.get_center() + UP * 1.5)
        iter_text1 = Text("result = 1", font_size=18).move_to(iter_box1.get_center())
        iter_box2 = Rectangle(width=2, height=0.8, color=GREEN).move_to(right_panel.get_center())
        iter_text2 = Text("for i in range(1, n+1)", font_size=18).move_to(iter_box2.get_center())
        iter_box3 = Rectangle(width=2, height=0.8, color=GREEN).move_to(right_panel.get_center() + DOWN * 1.5)
        iter_text3 = Text("result *= i", font_size=18).move_to(iter_box3.get_center())
        iter_box4 = Rectangle(width=2, height=0.8, color=GREEN).move_to(right_panel.get_center() + DOWN * 3)
        iter_text4 = Text("return result", font_size=18).move_to(iter_box4.get_center())
        
        iter_arrow1 = Arrow(iter_box1.get_bottom(), iter_box2.get_top(), buff=0.1, color=GREEN)
        iter_arrow2 = Arrow(iter_box2.get_bottom(), iter_box3.get_top(), buff=0.1, color=GREEN)
        iter_arrow3 = Arrow(iter_box3.get_bottom(), iter_box4.get_top(), buff=0.1, color=GREEN)
        
        self.play(
            Create(iter_box1), Write(iter_text1),
            Create(iter_box2), Write(iter_text2),
            Create(iter_box3), Write(iter_text3),
            Create(iter_box4), Write(iter_text4),
            Create(iter_arrow1), Create(iter_arrow2), Create(iter_arrow3)
        )
        self.wait(1)

        # Code snippets
        code_title = Text("Code Comparison", font_size=32).next_to(left_panel, DOWN, buff=0.5)
        self.play(Write(code_title))
        self.wait(0.5)

        # Recursive code
        rec_code = VGroup(
            Text("def factorial(n):", font_size=16),
            Text("    if n <= 1:", font_size=16),
            Text("        return 1", font_size=16),
            Text("    return n * factorial(n-1)", font_size=16)
        )
        rec_code.arrange(DOWN, aligned_edge=LEFT)
        rec_code.move_to(left_panel.get_center() + DOWN * 2.5)
        
        # Iterative code
        iter_code = VGroup(
            Text("def factorial(n):", font_size=16),
            Text("    result = 1", font_size=16),
            Text("    for i in range(1, n+1):", font_size=16),
            Text("        result *= i", font_size=16),
            Text("    return result", font_size=16)
        )
        iter_code.arrange(DOWN, aligned_edge=LEFT)
        iter_code.move_to(right_panel.get_center() + DOWN * 2.5)

        self.play(Write(rec_code), Write(iter_code))
        self.wait(1)

        # Pros/Cons icons
        pros_cons_title = Text("Trade-offs", font_size=32).to_edge(DOWN)
        self.play(Write(pros_cons_title))
        self.wait(0.5)

        # Recursion pros/cons
        rec_pros = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.3),
            Text("✓", font_size=20, color=GREEN)
        ).arrange(RIGHT, buff=0.1)
        rec_pros_label = Text("Elegant", font_size=16).next_to(rec_pros, RIGHT)
        
        rec_cons = VGroup(
            Circle(radius=0.3, color=RED, fill_opacity=0.3),
            Text("✗", font_size=20, color=RED)
        ).arrange(RIGHT, buff=0.1)
        rec_cons_label = Text("Stack overflow", font_size=16).next_to(rec_cons, RIGHT)
        
        rec_pros.move_to(left_panel.get_center() + DOWN * 4.5)
        rec_pros_label.next_to(rec_pros, RIGHT)
        rec_cons.move_to(left_panel.get_center() + DOWN * 5.5)
        rec_cons_label.next_to(rec_cons, RIGHT)

        # Iteration pros/cons
        iter_pros = VGroup(
            Circle(radius=0.3, color=GREEN, fill_opacity=0.3),
            Text("✓", font_size=20, color=GREEN)
        ).arrange(RIGHT, buff=0.1)
        iter_pros_label = Text("Efficient", font_size=16).next_to(iter_pros, RIGHT)
        
        iter_cons = VGroup(
            Circle(radius=0.3, color=RED, fill_opacity=0.3),
            Text("✗", font_size=20, color=RED)
        ).arrange(RIGHT, buff=0.1)
        iter_cons_label = Text("Verbose", font_size=16).next_to(iter_cons, RIGHT)
        
        iter_pros.move_to(right_panel.get_center() + DOWN * 4.5)
        iter_pros_label.next_to(iter_pros, RIGHT)
        iter_cons.move_to(right_panel.get_center() + DOWN * 5.5)
        iter_cons_label.next_to(iter_cons, RIGHT)

        self.play(
            Create(rec_pros), Write(rec_pros_label),
            Create(rec_cons), Write(rec_cons_label),
            Create(iter_pros), Write(iter_pros_label),
            Create(iter_cons), Write(iter_cons_label)
        )
        self.wait(2)

        # Final summary
        summary = Text("Choose recursion for clarity, iteration for performance", font_size=24)
        summary.move_to(ORIGIN + DOWN * 3.5)
        self.play(Write(summary))
        self.wait(2)
