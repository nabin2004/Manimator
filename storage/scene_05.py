
from manim import *

class Scene_05(Scene):
    def construct(self):
        # Title
        title = Text("Recursion vs Iteration", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Define code snippets
        recursive_code = '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)'''

        iterative_code = '''def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result'''

        # Create code blocks
        rec_code_mob = Code(
            code=recursive_code,
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=BLUE_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        ).scale(0.5)

        iter_code_mob = Code(
            code=iterative_code,
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=GREEN_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            insert_line_no=False,
            style="monokai"
        ).scale(0.5)

        # Position code side by side
        rec_code_mob.move_to(LEFT * 3.5)
        iter_code_mob.move_to(RIGHT * 3.5)

        # Labels
        rec_label = Text("Recursive", color=BLUE).scale(0.7).next_to(rec_code_mob, UP)
        iter_label = Text("Iterative", color=GREEN).scale(0.7).next_to(iter_code_mob, UP)

        self.play(
            FadeIn(rec_code_mob),
            FadeIn(rec_label),
            FadeIn(iter_code_mob),
            FadeIn(iter_label)
        )
        self.wait(2)

        # Visualize Recursion (Tree)
        # Create nodes for n=3: 3 -> 2 -> 1
        node_3 = Circle(radius=0.4, color=BLUE).set_fill(BLACK, opacity=1)
        text_3 = Text("3", font_size=24).move_to(node_3)
        group_3 = VGroup(node_3, text_3)
        group_3.move_to(LEFT * 3.5 + DOWN * 1.5)

        node_2 = Circle(radius=0.4, color=BLUE).set_fill(BLACK, opacity=1)
        text_2 = Text("2", font_size=24).move_to(node_2)
        group_2 = VGroup(node_2, text_2)
        group_2.move_to(LEFT * 3.5 + DOWN * 3)

        node_1 = Circle(radius=0.4, color=BLUE).set_fill(BLACK, opacity=1)
        text_1 = Text("1", font_size=24).move_to(node_1)
        group_1 = VGroup(node_1, text_1)
        group_1.move_to(LEFT * 3.5 + DOWN * 4.5)

        # Arrows for recursion
        arrow_3_2 = Arrow(group_3.get_bottom(), group_2.get_top(), buff=0.1, color=BLUE)
        arrow_2_1 = Arrow(group_2.get_bottom(), group_1.get_top(), buff=0.1, color=BLUE)

        self.play(
            Create(group_3),
            Create(group_2),
            Create(group_1),
            Create(arrow_3_2),
            Create(arrow_2_1)
        )
        
        # Highlight call stack behavior
        self.play(group_3.animate.set_fill(BLUE, opacity=0.5))
        self.wait(0.2)
        self.play(group_2.animate.set_fill(BLUE, opacity=0.5))
        self.wait(0.2)
        self.play(group_1.animate.set_fill(BLUE, opacity=0.5))
        self.wait(0.5)

        # Return values (unwind)
        ret_1 = Text("1", color=YELLOW, font_size=20).next_to(group_1, RIGHT)
        self.play(Write(ret_1))
        
        ret_2 = Text("2", color=YELLOW, font_size=20).next_to(group_2, RIGHT)
        self.play(Write(ret_2))

        ret_3 = Text("6", color=YELLOW, font_size=20).next_to(group_3, RIGHT)
        self.play(Write(ret_3))
        self.wait(1)

        # Visualize Iteration (Loop Counter)
        # Box representing memory
        memory_box = Rectangle(width=2, height=2, color=GREEN).move_to(RIGHT * 3.5 + DOWN * 2.5)
        memory_label = Text("Variables", font_size=20).next_to(memory_box, UP)
        
        # Initial state
        i_val = Text("i = 2", font_size=20, color=WHITE).move_to(memory_box.get_center() + UP * 0.4)
        res_val = Text("res = 1", font_size=20, color=WHITE).move_to(memory_box.get_center() + DOWN * 0.4)
        
        self.play(
            Create(memory_box),
            Write(memory_label),
            Write(i_val),
            Write(res_val)
        )

        # Loop flow arrows (horizontal)
        flow_y = memory_box.get_bottom()[1] - 1.0
        
        # Step 1: i=2
        step_1 = Text("res *= 2", font_size=18, color=YELLOW).move_to(RIGHT * 3.5 + DOWN * 4.5)
        arrow_1 = Arrow(memory_box.get_bottom(), step_1.get_top(), buff=0.1, color=GREEN)
        self.play(Create(arrow_1), Write(step_1))
        
        self.play(
            Transform(i_val.copy(), Text("i = 3", font_size=20, color=WHITE).move_to(memory_box.get_center() + UP * 0.4)),
            Transform(res_val.copy(), Text("res = 2", font_size=20, color=WHITE).move_to(memory_box.get_center() + DOWN * 0.4))
        )
        self.remove(i_val, res_val)
        i_val_new = Text("i = 3", font_size=20, color=WHITE).move_to(memory_box.get_center() + UP * 0.4)
        res_val_new = Text("res = 2", font_size=20, color=WHITE).move_to(memory_box.get_center() + DOWN * 0.4)
        self.add(i_val_new, res_val_new)
        self.wait(0.5)

        # Step 2: i=3
        step_2 = Text("res *= 3", font_size=18, color=YELLOW).move_to(RIGHT * 3.5 + DOWN * 4.5)
        arrow_2 = Arrow(step_1.get_bottom(), step_2.get_top(), buff=0.1, color=GREEN)
        self.play(
            FadeOut(step_1),
            FadeOut(arrow_1),
            Create(arrow_2),
            Transform(i_val_new, Text("i = 4", font_size=20, color=WHITE).move_to(memory_box.get_center() + UP * 0.4)),
            Transform(res_val_new, Text("res = 6", font_size=20, color=WHITE).move_to(memory_box.get_center() + DOWN * 0.4))
        )
        self.remove(i_val_new, res_val_new)
        i_val_final = Text("i = 4", font_size=20, color=WHITE).move_to(memory_box.get_center() + UP * 0.4)
        res_val_final = Text("res = 6", font_size=20, color=WHITE).move_to(memory_box.get_center() + DOWN * 0.4)
        self.add(i_val_final, res_val_final)
        self.play(Write(step_2))
        self.wait(0.5)

        # Comparison Text
        comparison_text = Text("Trade-offs", font_size=36, color=YELLOW).move_to(UP * 1.5)
        self.play(Write(comparison_text))

        points = VGroup(
            Text("Recursion: Readable, mirrors math", font_size=24).shift(UP * 0.5),
            Text("  - Overhead: Call stack", font_size=20, color=GRAY).shift(DOWN * 0.2),
            Text("Iteration: Efficient, low memory", font_size=24).shift(DOWN * 1.2),
            Text("  - Overhead: Manual state mgmt", font_size=20, color=GRAY).shift(DOWN * 1.9)
        )
        
        self.play(FadeIn(points))
        self.wait(3)

        # Cleanup
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
