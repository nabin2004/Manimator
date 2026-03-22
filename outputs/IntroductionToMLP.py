
from manim import *

class Introductiontomlp(Scene):
    def construct(self):
        title = Text("Multilayer Perceptron (MLP)", font_size=48)
        title.to_edge(UP)
        
        subtitle = Text("The foundation of modern neural networks", font_size=24, color=BLUE)
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)

        input_rect = Rectangle(height=1.5, width=1.5, color=WHITE)
        input_rect.shift(LEFT * 4)
        input_label = Text("Input", font_size=24).next_to(input_rect, UP)
        input_data = VGroup(*[Line(LEFT*0.3, RIGHT*0.3) for _ in range(3)]).arrange(DOWN, buff=0.1)
        input_data.move_to(input_rect.get_center())

        black_box = Rectangle(height=3, width=4, fill_opacity=1, fill_color=GREY_E, color=WHITE)
        black_box_label = Text("Hidden Layers", font_size=24).next_to(black_box, UP)
        question_mark = Text("?", font_size=72, color=WHITE).move_to(black_box.get_center())

        output_rect = Rectangle(height=1.5, width=1.5, color=WHITE)
        output_rect.shift(RIGHT * 4)
        output_label = Text("Output", font_size=24).next_to(output_rect, UP)
        output_val = DecimalNumber(0.98, num_decimal_places=2, color=YELLOW).move_to(output_rect.get_center())

        arrow_in = Arrow(input_rect.get_right(), black_box.get_left(), buff=0.1)
        arrow_out = Arrow(black_box.get_right(), output_rect.get_left(), buff=0.1)

        self.play(
            Create(input_rect),
            Write(input_label),
            Create(input_data)
        )
        self.wait(0.5)

        self.play(
            Create(black_box),
            Write(black_box_label),
            Write(question_mark)
        )
        self.play(GrowArrow(arrow_in))
        self.wait(0.5)

        self.play(
            Create(output_rect),
            Write(output_label),
            Write(output_val)
        )
        self.play(GrowArrow(arrow_out))
        self.wait(1)

        pulse_box = black_box.copy().set_color(BLUE).set_stroke(width=8)
        self.play(
            pulse_box.animate.scale(1.1).set_opacity(0),
            run_time=1,
            rate_func=ease_out_sine
        )

        purpose_text = Text(
            "Mapping inputs to outputs through learned representations",
            font_size=28,
            slant=ITALIC
        ).to_edge(DOWN, buff=1)
        
        self.play(Write(purpose_text))
        self.wait(2)
