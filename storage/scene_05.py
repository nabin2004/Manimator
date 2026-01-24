
from manim import *

class Scene_05(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Create sections
        # Left side: Recursion
        # Right side: Iteration
        
        # 1. Visual Diagrams
        # Recursive Tree (Left)
        rec_title = Text("Recursive Tree", font_size=28).shift(LEFT * 3.5 + UP * 2.5)
        
        # Nodes for recursion
        root = Circle(radius=0.3, color=BLUE).shift(LEFT * 3.5 + UP * 1.5)
        root_label = Text("f(n)", font_size=20).move_to(root)
        
        child1 = Circle(radius=0.3, color=BLUE).shift(LEFT * 4.5 + DOWN * 0.5)
        child1_label = Text("f(n-1)", font_size=18).move_to(child1)
        
        child2 = Circle(radius=0.3, color=BLUE).shift(LEFT * 2.5 + DOWN * 0.5)
        child2_label = Text("f(n-1)", font_size=18).move_to(child2)
        
        leaf1 = Circle(radius=0.2, color=TEAL).shift(LEFT * 5.0 + DOWN * 2.0)
        leaf1_label = Text("f(0)", font_size=14).move_to(leaf1)
        
        leaf2 = Circle(radius=0.2, color=TEAL).shift(LEFT * 4.0 + DOWN * 2.0)
        leaf2_label = Text("f(0)", font_size=14).move_to(leaf2)
        
        leaf3 = Circle(radius=0.2, color=TEAL).shift(LEFT * 3.0 + DOWN * 2.0)
        leaf3_label = Text("f(0)", font_size=14).move_to(leaf3)
        
        leaf4 = Circle(radius=0.2, color=TEAL).shift(LEFT * 2.0 + DOWN * 2.0)
        leaf4_label = Text("f(0)", font_size=14).move_to(leaf4)

        rec_lines = VGroup(
            Line(root.get_bottom(), child1.get_top()),
            Line(root.get_bottom(), child2.get_top()),
            Line(child1.get_bottom(), leaf1.get_top()),
            Line(child1.get_bottom(), leaf2.get_top()),
            Line(child2.get_bottom(), leaf3.get_top()),
            Line(child2.get_bottom(), leaf4.get_top())
        )

        rec_group = VGroup(rec_title, root, root_label, child1, child1_label, child2, child2_label, 
                           leaf1, leaf1_label, leaf2, leaf2_label, leaf3, leaf3_label, leaf4, leaf4_label, rec_lines)

        # Iteration Loop (Right)
        iter_title = Text("Loop Counter", font_size=28).shift(RIGHT * 3.5 + UP * 2.5)
        
        # Visual representation of a loop
        loop_box = Rectangle(width=3, height=2, color=YELLOW).shift(RIGHT * 3.5 + DOWN * 0.5)
        loop_text = Text("for i in range(n):", font_size=22).next_to(loop_box, UP)
        
        counter_box = Rectangle(width=2, height=0.8, color=GREEN, fill_opacity=0.2).shift(RIGHT * 3.5 + DOWN * 1.5)
        counter_text = Text("i = 0, 1, ... n-1", font_size=20).move_to(counter_box)
        
        iter_group = VGroup(iter_title, loop_box, loop_text, counter_box, counter_text)

        self.play(
            Create(rec_group),
            Create(iter_group)
        )
        self.wait(2)

        # 2. Code Snippets
        # Move diagrams up slightly to make room
        self.play(
            rec_group.animate.scale(0.8).shift(UP * 0.5),
            iter_group.animate.scale(0.8).shift(UP * 0.5)
        )

        # Recursive Code
        rec_code_str = """def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)"""
        rec_code = Code(code=rec_code_str, language="python", font="Monospace", background="rectangle", 
                        background_stroke_color=BLUE_D, background_fill_opacity=0.8)
        rec_code.scale(0.5).shift(LEFT * 3.5 + DOWN * 2.5)
        
        # Iterative Code
        iter_code_str = """def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result"""
        iter_code = Code(code=iter_code_str, language="python", font="Monospace", background="rectangle",
                         background_stroke_color=YELLOW_D, background_fill_opacity=0.8)
        iter_code.scale(0.5).shift(RIGHT * 3.5 + DOWN * 2.5)

        self.play(
            FadeIn(rec_code),
            FadeIn(iter_code)
        )
        self.wait(3)

        # 3. Pros/Cons Table
        # Clear code and move diagrams/code up more
        self.play(
            FadeOut(rec_code),
            FadeOut(iter_code),
            rec_group.animate.scale(1.25).shift(UP * 0.5 + LEFT * 0.5), # Adjust to top left
            iter_group.animate.scale(1.25).shift(UP * 0.5 + RIGHT * 0.5) # Adjust to top right
        )

        table_title = Text("Comparison", font_size=32).next_to(title, DOWN, buff=0.5)
        self.play(Write(table_title))

        # Table Data
        headers = ["Aspect", "Recursion", "Iteration"]
        rows_data = [
            ["Readability", "High (for tree problems)", "High (linear logic)"],
            ["Performance", "Overhead (stack calls)", "Faster (no overhead)"],
            ["Memory", "Uses Stack Space", "Uses Heap/Variables"],
            ["Use Case", "Trees, Divide & Conquer", "Simple Repetition"]
        ]

        # Create table manually for better control
        col_widths = [2.5, 3.5, 3.5]
        row_height = 0.6
        start_pos = LEFT * 5 + DOWN * 0.5
        
        table_entries = VGroup()
        
        # Headers
        h1 = Text(headers[0], font_size=24, color=YELLOW).move_to(start_pos + RIGHT * 1.25)
        h2 = Text(headers[1], font_size=24, color=BLUE).move_to(start_pos + RIGHT * 4.5)
        h3 = Text(headers[2], font_size=24, color=YELLOW).move_to(start_pos + RIGHT * 8.0)
        
        table_entries.add(h1, h2, h3)
        
        # Rows
        for i, row in enumerate(rows_data):
            y_offset = (i + 1) * row_height
            t1 = Text(row[0], font_size=20).move_to(start_pos + RIGHT * 1.25 + DOWN * y_offset)
            t2 = Text(row[1], font_size=18, color=BLUE).move_to(start_pos + RIGHT * 4.5 + DOWN * y_offset)
            t3 = Text(row[2], font_size=18, color=YELLOW).move_to(start_pos + RIGHT * 8.0 + DOWN * y_offset)
            table_entries.add(t1, t2, t3)

        # Draw lines
        h_line = Line(start_pos, start_pos + RIGHT * 9.5, stroke_width=2)
        v1_line = Line(start_pos + RIGHT * 2.5, start_pos + DOWN * (len(rows_data) + 1) * row_height, stroke_width=2)
        v2_line = Line(start_pos + RIGHT * 6.0, start_pos + DOWN * (len(rows_data) + 1) * row_height, stroke_width=2)
        
        lines = VGroup(h_line, v1_line, v2_line)

        self.play(Create(lines), Write(table_entries))
        self.wait(3)

        # Conclusion
        conclusion = Text("Choose based on problem structure!", font_size=30, color=GREEN)
        conclusion.next_to(lines, DOWN, buff=1)
        
        self.play(Write(conclusion))
        self.wait(2)
