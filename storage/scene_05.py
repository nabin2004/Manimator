
from manim import *

class Scene_05(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration: Factorial", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Left Panel: Recursive
        left_panel = Rectangle(width=5, height=6, color=BLUE)
        left_panel.shift(LEFT * 3.5)
        left_label = Text("Recursive", font_size=24, color=BLUE).next_to(left_panel, UP)
        
        rec_code = VGroup(
            Text("def fact(n):", font_size=20),
            Text("    if n == 0:", font_size=20),
            Text("        return 1", font_size=20),
            Text("    else:", font_size=20),
            Text("        return n * fact(n-1)", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT)
        rec_code.next_to(left_panel, DOWN, buff=0.5).shift(UP * 0.5)

        # Right Panel: Iterative
        right_panel = Rectangle(width=5, height=6, color=GREEN)
        right_panel.shift(RIGHT * 3.5)
        right_label = Text("Iterative", font_size=24, color=GREEN).next_to(right_panel, UP)

        iter_code = VGroup(
            Text("def fact(n):", font_size=20),
            Text("    res = 1", font_size=20),
            Text("    for i in range(1, n+1):", font_size=20),
            Text("        res *= i", font_size=20),
            Text("    return res", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT)
        iter_code.next_to(right_panel, DOWN, buff=0.5).shift(UP * 0.5)

        self.play(
            Create(left_panel), Write(left_label), 
            Create(right_panel), Write(right_label)
        )
        self.play(Write(rec_code), Write(iter_code))
        self.wait(2)

        # Transition to Table
        self.play(
            FadeOut(left_panel), FadeOut(left_label), FadeOut(rec_code),
            FadeOut(right_panel), FadeOut(right_label), FadeOut(iter_code),
            title.animate.scale(0.8).to_edge(UP)
        )

        # Table Setup
        headers = ["Metric", "Recursive", "Iterative"]
        data = [
            ["Lines of Code", "5", "5"],
            ["Readability", "High (Math def)", "High (Standard)"],
            ["Stack Usage", "O(n) (Risk of Overflow)", "O(1) (Constant)"],
            ["Performance", "Slower (Overhead)", "Faster"]
        ]

        # Create Table
        table = Table(
            data,
            col_labels=[Text(h, font_size=24) for h in headers],
            row_labels=None,
            include_outer_lines=True
        )
        table.scale(0.6)
        table.to_edge(DOWN, buff=0.5).shift(UP * 0.5)

        # Color coding for table
        # Column 1 (Metric) - White
        # Column 2 (Recursive) - Blue
        # Column 3 (Iterative) - Green
        
        # Apply colors to cells
        for i, row in enumerate(table.get_rows()):
            for j, cell in enumerate(row):
                if j == 0:
                    cell.set_color(WHITE)
                elif j == 1:
                    cell.set_color(BLUE)
                elif j == 2:
                    cell.set_color(GREEN)

        self.play(Create(table))
        self.wait(1)

        # Highlight Trade-offs
        # Highlight Stack Usage row
        stack_row = table.get_rows()[2]
        highlight_box = SurroundingRectangle(stack_row, color=YELLOW, buff=0.2)
        self.play(Create(highlight_box))
        
        # Explanation Text
        explanation = Text("Trade-off: Clarity vs Performance & Safety", font_size=32, color=YELLOW)
        explanation.next_to(table, UP, buff=0.5)
        self.play(Write(explanation))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(table), FadeOut(highlight_box), FadeOut(explanation), FadeOut(title))
        self.wait(1)
