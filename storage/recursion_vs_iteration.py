
from manim import *

class Recursion_vs_iteration(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration", font_size=48)
        title.set_color_by_gradient(BLUE, GREEN)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Create side-by-side layout
        left_code_title = Text("Recursive Factorial", font_size=30).to_edge(UP).shift(LEFT * 3.5)
        right_code_title = Text("Iterative Factorial", font_size=30).to_edge(UP).shift(RIGHT * 3.5)
        
        # Code snippets
        recursive_code = Code(
            code="""def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)""",
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=BLUE_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        ).scale(0.6).next_to(left_code_title, DOWN)

        iterative_code = Code(
            code="""def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result""",
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=GREEN_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        ).scale(0.6).next_to(right_code_title, DOWN)

        self.play(
            Write(left_code_title),
            Write(right_code_title),
            Write(recursive_code),
            Write(iterative_code)
        )
        self.wait(2)

        # Comparison Table
        table_title = Text("Comparison", font_size=36).to_edge(UP)
        self.play(
            FadeOut(left_code_title),
            FadeOut(right_code_title),
            FadeOut(recursive_code),
            FadeOut(iterative_code),
            Write(table_title)
        )

        headers = ["Aspect", "Recursion", "Iteration"]
        h_objects = [Text(h, font_size=24) for h in headers]
        
        # Position headers
        h_group = VGroup(*h_objects).arrange(RIGHT, buff=1).next_to(table_title, DOWN, buff=0.5)
        
        # Rows
        row1_data = ["Readability", "High (for recursive problems)", "Moderate"]
        row2_data = ["Stack Depth", "Limited (risk of overflow)", "Unlimited (safe)"]
        row3_data = ["Memory", "Uses stack frames", "Uses constant memory"]
        
        rows = []
        for data in [row1_data, row2_data, row3_data]:
            row_texts = [Text(d, font_size=20) for d in data]
            row_group = VGroup(*row_texts).arrange(RIGHT, buff=1)
            rows.append(row_group)

        rows_group = VGroup(*rows).arrange(DOWN, buff=0.4).next_to(h_group, DOWN, buff=0.3)
        
        # Draw table
        self.play(Write(h_group))
        self.wait(0.5)
        
        for row in rows_group:
            self.play(Write(row))
            self.wait(0.5)

        # Highlight Pros and Cons
        # Highlight Readability (Pros of Recursion)
        self.play(rows_group[0][1].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(rows_group[0][1].animate.set_color(WHITE))

        # Highlight Stack Depth (Cons of Recursion)
        self.play(rows_group[1][1].animate.set_color(RED))
        self.wait(0.5)
        self.play(rows_group[1][1].animate.set_color(WHITE))

        self.wait(1)

        # Transition to Graphic
        self.play(
            FadeOut(table_title),
            FadeOut(h_group),
            FadeOut(rows_group)
        )

        # Graphic: Tree / DFS
        graphic_title = Text("Why Recursion?", font_size=36).to_edge(UP)
        self.play(Write(graphic_title))

        # Draw a simple tree
        root = Circle(radius=0.4, color=BLUE).move_to(UP * 1.5)
        root_label = Text("A", font_size=20).move_to(root.get_center())
        
        left_child = Circle(radius=0.4, color=GREEN).move_to(UP * 0.5 + LEFT * 2)
        left_label = Text("B", font_size=20).move_to(left_child.get_center())
        
        right_child = Circle(radius=0.4, color=GREEN).move_to(UP * 0.5 + RIGHT * 2)
        right_label = Text("C", font_size=20).move_to(right_child.get_center())

        left_grandchild = Circle(radius=0.4, color=YELLOW).move_to(DOWN * 0.5 + LEFT * 2)
        left_gc_label = Text("D", font_size=20).move_to(left_grandchild.get_center())
        
        right_grandchild = Circle(radius=0.4, color=YELLOW).move_to(DOWN * 0.5 + RIGHT * 2)
        right_gc_label = Text("E", font_size=20).move_to(right_grandchild.get_center())

        # Lines
        line1 = Line(root.get_bottom(), left_child.get_top(), color=WHITE)
        line2 = Line(root.get_bottom(), right_child.get_top(), color=WHITE)
        line3 = Line(left_child.get_bottom(), left_grandchild.get_top(), color=WHITE)
        line4 = Line(right_child.get_bottom(), right_grandchild.get_top(), color=WHITE)

        tree_group = VGroup(
            root, root_label, 
            left_child, left_label, right_child, right_label,
            left_grandchild, left_gc_label, right_grandchild, right_gc_label,
            line1, line2, line3, line4
        )

        self.play(Create(tree_group))
        self.wait(1)

        # DFS Explanation
        dfs_text = Text("Natural fit for Trees, DFS, Backtracking", font_size=28, color=YELLOW)
        dfs_text.next_to(tree_group, DOWN, buff=0.5)
        
        self.play(Write(dfs_text))
        self.wait(2)

        # Final Conclusion
        conclusion = VGroup(
            Text("Use Recursion when:", font_size=30, color=BLUE),
            Text("- Problem is naturally recursive (Trees, Graphs)", font_size=24),
            Text("- Code clarity is prioritized over memory", font_size=24),
            Text("Use Iteration when:", font_size=30, color=GREEN),
            Text("- Deep recursion is needed (avoid stack overflow)", font_size=24),
            Text("- Performance is critical", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(
            FadeOut(tree_group),
            FadeOut(dfs_text),
            FadeOut(graphic_title)
        )
        
        self.play(Write(conclusion))
        self.wait(3)
