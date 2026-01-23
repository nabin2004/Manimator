
from manim import *

class Scene_03(Scene):
    def construct(self):
        # Title
        title = Text("Recursive Step", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Code snippet
        code_str = "return n + factorial(n-1)"
        code = Code(
            code=code_str,
            language="python",
            font="Monospace",
            background="rectangle",
            background_stroke_color=BLUE_D,
            background_stroke_width=2,
            background_fill_color=BLACK,
            background_fill_opacity=0.8,
            insert_line_no=False,
            style="monokai",
            font_size=32,
            tab_width=4
        )
        code.scale(0.8)
        code.shift(LEFT * 3.5)
        self.play(Write(code))
        self.wait(0.5)

        # Arrow looping back
        arrow = Arc(
            start_angle=PI/2,
            angle=-PI,
            radius=1.5,
            color=YELLOW
        )
        arrow.shift(RIGHT * 2.5 + DOWN * 0.5)
        arrow_label = Text("call", font_size=24, color=YELLOW)
        arrow_label.next_to(arrow, UP, buff=0.1)
        self.play(Create(arrow), Write(arrow_label))
        self.wait(0.5)

        # Stack of blocks labeled 'n-1'
        # Create a stack of 3 blocks
        block_width = 1.2
        block_height = 0.6
        block_color = TEAL
        block_stroke_color = WHITE
        block_stroke_width = 2

        blocks = VGroup()
        for i in range(3):
            rect = Rectangle(
                width=block_width,
                height=block_height,
                fill_color=block_color,
                fill_opacity=0.8,
                stroke_color=block_stroke_color,
                stroke_width=block_stroke_width
            )
            label = Text(f"n-{i}", font_size=24)
            label.move_to(rect.get_center())
            block_group = VGroup(rect, label)
            block_group.shift(RIGHT * 2.5 + DOWN * (1.5 + i * 0.7))
            blocks.add(block_group)

        self.play(FadeIn(blocks, shift=UP))
        self.wait(0.5)

        # Animate the arrow pointing to the stack
        self.play(
            arrow.animate.scale(0.8).move_to(blocks[0].get_top() + UP * 0.3),
            arrow_label.animate.scale(0.8).move_to(blocks[0].get_top() + UP * 0.8)
        )
        self.wait(1)

        # Highlight the recursive call
        self.play(
            code[0][10:22].animate.set_color(YELLOW),
            run_time=0.5
        )
        self.wait(0.5)

        # Fade out
        self.play(
            FadeOut(title),
            FadeOut(code),
            FadeOut(arrow),
            FadeOut(arrow_label),
            FadeOut(blocks)
        )
        self.wait(0.5)
