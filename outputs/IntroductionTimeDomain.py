
from manim import *
import numpy as np

class Introductiontimedomain(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-4, 4, 2],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False}
        ).to_edge(DOWN)

        labels = axes.get_axis_labels(x_label="t", y_label="A(t)")

        freqs = [0.5, 1.2, 2.5]
        amps = [1.5, 0.8, 0.4]
        colors = [BLUE_B, GREEN_B, YELLOW_B]

        def get_sine_wave(freq, amp, color, opacity=0.3):
            return axes.plot(
                lambda x: amp * np.sin(2 * np.pi * freq * x),
                color=color
            ).set_stroke(opacity=opacity)

        ghost_waves = VGroup(*[
            get_sine_wave(f, a, c) for f, a, c in zip(freqs, amps, colors)
        ])

        composite_wave = axes.plot(
            lambda x: sum(a * np.sin(2 * np.pi * f * x) for f, a in zip(freqs, amps)),
            color=WHITE
        ).set_stroke(width=4)

        cursor_line = Line(
            axes.c2p(0, -3.5), axes.c2p(0, 3.5),
            color=RED
        ).set_stroke(width=2)

        time_tracker = ValueTracker(0)
        cursor_line.add_updater(lambda m: m.move_to(axes.c2p(time_tracker.get_value(), 0)))

        def get_dynamic_label():
            t = time_tracker.get_value()
            val = sum(a * np.sin(2 * np.pi * f * t) for f, a in zip(freqs, amps))
            lbl = DecimalNumber(val, num_decimal_places=2, include_sign=True)
            lbl.scale(0.8).next_to(cursor_line, UP)
            return lbl

        dynamic_amp = always_redraw(get_dynamic_label)

        title = Text("Complex Signal in Time Domain", font_size=36).to_edge(UP)
        subtitle = Text("Sum of hidden periodic components", font_size=24, color=GRAY).next_to(title, DOWN)

        self.play(Write(title), Create(axes), Write(labels))
        self.wait(0.5)
        
        self.play(Create(composite_wave), run_time=2)
        self.play(FadeIn(subtitle))
        self.wait(1)

        self.play(
            FadeIn(ghost_waves),
            composite_wave.animate.set_stroke(opacity=0.5)
        )
        
        self.add(cursor_line, dynamic_amp)
        self.play(
            time_tracker.animate.set_value(10),
            run_time=10,
            rate_func=linear
        )
        
        self.play(
            FadeOut(cursor_line),
            FadeOut(dynamic_amp),
            composite_wave.animate.set_stroke(opacity=1, width=5),
            ghost_waves.animate.set_stroke(opacity=0.1)
        )
        self.wait(2)
