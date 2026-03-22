
from manim import *
import numpy as np

class Conclusionsummary(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[0, 6, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 4, 1],
            x_length=6,
            y_length=4,
            z_length=4,
            axis_config={"include_tip": True}
        )
        
        labels = axes.get_axis_labels(
            x_label="t", 
            y_label="A", 
            z_label="f"
        )

        def wave_func(t, freq):
            return np.sin(freq * t) * np.exp(-0.1 * (t-3)**2)

        # Time domain curve (z=0)
        time_curve = ParametricFunction(
            lambda t: axes.c2p(t, wave_func(t, 2 * PI), 0),
            t_range=[0, 6],
            color=BLUE
        )

        # Frequency domain curve (x=6)
        freq_curve = ParametricFunction(
            lambda f: axes.c2p(6, 1.5 * np.exp(-5 * (f - 1)**2), f),
            t_range=[0, 4],
            color=YELLOW
        )

        # Waterfall surface
        waterfall = Surface(
            lambda t, f: axes.c2p(t, wave_func(t, 2 * PI * f) * np.exp(-2 * (f - 1)**2), f),
            u_range=[0, 6],
            v_range=[0.1, 3],
            resolution=(30, 30),
            fill_opacity=0.5,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        equation = MathTex(
            "F(\\omega) = \\int_{-\\infty}^{\\infty} f(t) e^{-i \\omega t} dt",
            font_size=48
        ).to_edge(UP)

        # Animation Sequence
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        self.add(axes, labels)
        self.play(Create(time_curve))
        self.wait(1)

        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(Create(waterfall), run_time=3)
        self.wait(1)

        self.play(Create(freq_curve))
        self.wait(1)

        self.stop_ambient_camera_rotation()
        self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.wait(1)

        # Final Synthesis
        self.add_fixed_in_frame_mobjects(equation)
        self.play(
            Write(equation),
            waterfall.animate.set_style(fill_opacity=0.2),
            run_time=2
        )
        
        # Morphing logic: Transform time curve to freq curve in 3D space
        self.play(
            ReplacementTransform(time_curve, freq_curve.copy().set_color(WHITE)),
            run_time=3
        )
        
        self.wait(3)
