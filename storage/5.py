
from manim import *

class FiveScene(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Left Side: Recursive Factorial
        recursive_label = Text("Recursive Factorial", font_size=28, color=BLUE)
        recursive_label.shift(LEFT * 3.5 + UP * 3)
        
        recursive_code = Code(
            code="""def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)""",
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=BLUE,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        )
        recursive_code.scale(0.6)
        recursive_code.next_to(recursive_label, DOWN, buff=0.5)

        # Right Side: Iterative Factorial
        iterative_label = Text("Iterative Factorial", font_size=28, color=YELLOW)
        iterative_label.shift(RIGHT * 3.5 + UP * 3)

        iterative_code = Code(
            code="""def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result""",
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=YELLOW,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        )
        iterative_code.scale(0.6)
        iterative_code.next_to(iterative_label, DOWN, buff=0.5)

        # Animate Code appearing
        self.play(
            Write(recursive_label),
            Write(recursive_code),
            Write(iterative_label),
            Write(iterative_code)
        )
        self.wait(1)

        # Transition to Flowchart Comparison
        self.play(
            FadeOut(recursive_label),
            FadeOut(recursive_code),
            FadeOut(iterative_label),
            FadeOut(iterative_code),
            FadeOut(title)
        )

        # Flowchart Title
        flow_title = Text("Control Flow Comparison", font_size=36)
        flow_title.to_edge(UP)
        self.play(Write(flow_title))

        # Iterative Flowchart (Loop)
        iter_group = VGroup()
        iter_title = Text("Iteration (Loop)", font_size=24, color=YELLOW).shift(LEFT * 3.5 + UP * 2)
        
        # Loop Box
        loop_box = Rectangle(width=2.5, height=1.5, color=YELLOW)
        loop_text = Text("For i in range", font_size=20).move_to(loop_box)
        loop_group = VGroup(loop_box, loop_text)
        
        # Loop Arrows
        arrow_down = Arrow(loop_box.get_bottom(), loop_box.get_bottom() + DOWN * 1.5, buff=0.1, color=YELLOW)
        action_box = Rectangle(width=2, height=1, color=YELLOW).next_to(arrow_down, DOWN)
        action_text = Text("Multiply\nresult", font_size=18).move_to(action_box)
        
        arrow_return = Arrow(action_box.get_bottom(), loop_box.get_bottom() + DOWN * 0.5 + LEFT * 1.2, buff=0.1, color=YELLOW)
        arrow_return.rotate(-PI/2)
        
        iter_group.add(iter_title, loop_group, arrow_down, action_box, action_text, arrow_return)
        iter_group.shift(LEFT * 3.5)

        # Recursive Flowchart (Call Tree)
        rec_group = VGroup()
        rec_title = Text("Recursion (Call Tree)", font_size=24, color=BLUE).shift(RIGHT * 3.5 + UP * 2)

        # Tree Nodes
        root = Circle(radius=0.4, color=BLUE).shift(RIGHT * 3.5)
        root_label = Text("n=3", font_size=18).move_to(root)
        
        child1 = Circle(radius=0.4, color=BLUE).shift(RIGHT * 2.5 + DOWN * 1.5)
        child1_label = Text("n=2", font_size=18).move_to(child1)
        
        child2 = Circle(radius=0.4, color=BLUE).shift(RIGHT * 1.5 + DOWN * 3)
        child2_label = Text("n=1", font_size=18).move_to(child2)

        # Tree Edges
        edge1 = Line(root.get_bottom(), child1.get_top(), color=WHITE)
        edge2 = Line(child1.get_bottom(), child2.get_top(), color=WHITE)

        rec_group.add(rec_title, root, root_label, child1, child1_label, child2, child2_label, edge1, edge2)
        rec_group.shift(RIGHT * 0.5)

        self.play(
            Create(iter_group),
            Create(rec_group)
        )
        self.wait(2)

        # Highlight Memory Usage
        # Iterative: Constant memory
        iter_mem_box = SurroundingRectangle(iter_group, color=YELLOW, buff=0.2)
        iter_mem_text = Text("Constant Memory", font_size=18, color=YELLOW)
        iter_mem_text.next_to(iter_mem_box, DOWN)

        # Recursive: Growing memory
        rec_mem_box = SurroundingRectangle(rec_group, color=BLUE, buff=0.2)
        rec_mem_text = Text("Growing Stack", font_size=18, color=BLUE)
        rec_mem_text.next_to(rec_mem_box, DOWN)

        self.play(
            Create(iter_mem_box),
            Write(iter_mem_text),
            Create(rec_mem_box),
            Write(rec_mem_text)
        )
        self.wait(2)

        # Final Text
        self.play(
            FadeOut(iter_group),
            FadeOut(rec_group),
            FadeOut(iter_mem_box),
            FadeOut(iter_mem_text),
            FadeOut(rec_mem_box),
            FadeOut(rec_mem_text),
            FadeOut(flow_title)
        )

        final_text = Text("Recursion often trades memory for readability", font_size=36, color=TEAL)
        self.play(Write(final_text))
        self.wait(2)
