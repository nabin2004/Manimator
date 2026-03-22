
from manim import *
import numpy as np

class Thewindingmachine(Scene):
    def construct(self):
        axes = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        ).add_coordinates()
        
        real_label = Text("Real", font_size=20).next_to(axes.x_axis.get_end(), DOWN)
        imag_label = Text("Imaginary", font_size=20).rotate(90 * DEGREES).next_to(axes.y_axis.get_end(), LEFT)
        
        freq_tracker = ValueTracker(0.1)
        
        def signal_func(t):
            return 1.0 + 0.5 * np.sin(2 * np.PI * 1.0 * t) + 0.3 * np.cos(2 * np.PI * 2.5 * t)

        def get_wrapped_point(t, freq):
            val = signal_func(t)
            angle = -2 * np.PI * freq * t
            return val * (np.cos(angle) * RIGHT + np.sin(angle) * UP)

        wrapped_curve = always_redraw(lambda:
            ParametricFunction(
                lambda t: get_wrapped_point(t, freq_tracker.get_value()),
                t_range=[0, 4, 0.02],
                color=YELLOW
            )
        )

        vector = always_redraw(lambda:
            Vector(get_wrapped_point(4, freq_tracker.get_value()), color=WHITE, stroke_width=2)
        )

        slider_group = VGroup()
        slider_line = Line(LEFT * 2, RIGHT * 2).to_edge(BOTTOM, buff=1)
        slider_label = Text("Winding Frequency (f):", font_size=24).next_to(slider_line, UP)
        
        slider_dot = always_redraw(lambda:
            Dot(slider_line.point_from_proportion(
                np.clip((freq_tracker.get_value() - 0.1) / 2.9, 0, 1)
            ), color=RED)
        )
        
        freq_value_text = always_redraw(lambda:
            DecimalNumber(freq_tracker.get_value(), num_decimal_places=2)
            .next_to(slider_label, RIGHT)
        )
        
        slider_group.add(slider_line, slider_label, slider_dot, freq_value_text)

        self.add(axes, real_label, imag_label)
        self.play(Create(wrapped_curve), FadeIn(vector))
        self.add(slider_group)
        
        self.play(freq_tracker.animate.set_value(1.0), run_time=4, rate_func=linear)
        self.wait(0.5)
        self.play(freq_tracker.animate.set_value(2.5), run_time=4, rate_func=linear)
        self.wait(0.5)
        self.play(freq_tracker.animate.set_value(0.5), run_time=3, rate_func=linear)
        self.wait(2)
