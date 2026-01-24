
from manim import *

class Recursion_vs_iteration(Scene):
    def construct(self):
        title = Text("Recursion vs Iteration", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Define code strings
        recursive_code = '''def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)'''

        iterative_code = '''def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result'''

        # Create CodeMobjects
        recursive_code_mob = Code(
            code=recursive_code,
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=BLUE_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        )
        recursive_code_mob.scale(0.6)
        recursive_code_mob.to_corner(UL)

        iterative_code_mob = Code(
            code=iterative_code,
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=GREEN_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        )
        iterative_code_mob.scale(0.6)
        iterative_code_mob.to_corner(UR)

        # Labels
        rec_label = Text("Recursive Factorial", color=BLUE).scale(0.7)
        rec_label.next_to(recursive_code_mob, UP)
        itr_label = Text("Iterative Factorial", color=GREEN).scale(0.7)
        itr_label.next_to(iterative_code_mob, UP)

        self.play(
            FadeIn(recursive_code_mob),
            Write(rec_label),
            FadeIn(iterative_code_mob),
            Write(itr_label)
        )
        self.wait(2)

        # Highlight function call vs loop
        # Recursive highlight: the recursive call line
        rec_highlight = SurroundingRectangle(recursive_code_mob.code[3], color=YELLOW, buff=0.1)
        rec_text = Text("Function Call Stack", color=YELLOW).scale(0.5)
        rec_text.next_to(rec_highlight, DOWN)

        # Iterative highlight: the for loop line
        itr_highlight = SurroundingRectangle(iterative_code_mob.code[2], color=YELLOW, buff=0.1)
        itr_text = Text("Loop Control", color=YELLOW).scale(0.5)
        itr_text.next_to(itr_highlight, DOWN)

        self.play(Create(rec_highlight), Write(rec_text))
        self.play(Create(itr_highlight), Write(itr_text))
        self.wait(2)

        # Transition to Pros and Cons
        self.play(
            FadeOut(rec_highlight),
            FadeOut(rec_text),
            FadeOut(itr_highlight),
            FadeOut(itr_text),
            FadeOut(recursive_code_mob),
            FadeOut(rec_label),
            FadeOut(iterative_code_mob),
            FadeOut(itr_label)
        )

        pros_cons_title = Text("Trade-offs", font_size=36)
        pros_cons_title.to_edge(UP)
        self.play(Write(pros_cons_title))

        # Pros/Cons Lists
        pros = VGroup(
            Text("Pros:", color=GREEN),
            Text("- Readability (Divide & Conquer)", font_size=24),
            Text("- Elegant for tree/graph problems", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        pros.to_edge(LEFT).shift(RIGHT * 1.5)

        cons = VGroup(
            Text("Cons:", color=RED),
            Text("- Memory Usage (Stack Frames)", font_size=24),
            Text("- Risk of Stack Overflow", font_size=24),
            Text("- Slower due to overhead", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        cons.to_edge(RIGHT).shift(LEFT * 1.5)

        self.play(FadeIn(pros), FadeIn(cons))
        self.wait(2)

        # Visualizing Memory Usage
        # Stack vs Heap/Loop visual
        stack_group = VGroup()
        stack_label = Text("Recursion: Stack", font_size=20).next_to(pros, DOWN).shift(RIGHT*0.5)
        stack_group.add(stack_label)
        
        # Draw stack boxes
        boxes = VGroup()
        for i in range(3):
            box = Rectangle(width=2, height=0.5, color=BLUE, fill_opacity=0.5)
            if i == 0:
                box.next_to(stack_label, DOWN)
            else:
                box.next_to(boxes[-1], DOWN)
            boxes.add(box)
            text = Text(f"fact({3-i})", font_size=16).move_to(box)
            boxes.add(text)
        
        stack_group.add(boxes)

        loop_group = VGroup()
        loop_label = Text("Iteration: Variables", font_size=20).next_to(cons, DOWN).shift(LEFT*0.5)
        loop_group.add(loop_label)
        
        # Draw loop variables
        var_box = Rectangle(width=2, height=1.5, color=GREEN, fill_opacity=0.5)
        var_box.next_to(loop_label, DOWN)
        var_text = Text("result = 6\ni = 3", font_size=16).move_to(var_box)
        loop_group.add(var_box, var_text)

        self.play(
            TransformFromCopy(pros[0], stack_group[0]),
            FadeIn(boxes),
            TransformFromCopy(cons[0], loop_group[0]),
            FadeIn(var_box),
            Write(var_text)
        )
        self.wait(3)

        # Conclusion
        conclusion = Text("Choose based on context!", font_size=32, color=YELLOW)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
