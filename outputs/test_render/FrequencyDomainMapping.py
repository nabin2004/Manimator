
from manim import *
import numpy as np

class FrequencyDomainMapping(Scene):
    def construct(self):
        # Colors
        COLOR_A = BLUE
        COLOR_B = RED
        COLOR_SUM = WHITE
        
        # Mathematical Notation
        formula = MathTex(
            r"\hat{g}(f) = \int_{-\infty}^{\infty} g(t) e^{-2\pi i f t} dt",
            font_size=36
        ).to_edge(UP)
        
        # Layout setup
        left_center = LEFT * 3.5 + DOWN * 0.5
        right_center = RIGHT * 3.5 + DOWN * 0.5
        
        # Left Side: Winding Circle
        winding_plane = ComplexPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_opacity": 0.4}
        ).move_to(left_center)
        
        circle = Circle(radius=2, color=GRAY_D, stroke_width=1).move_to(left_center)
        
        # Right Side: Frequency Plot
        freq_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 2, 1],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True}
        ).move_to(right_center)
        
        freq_label = freq_axes.get_x_axis_label("f", edge=RIGHT, direction=DOWN)
        amp_label = freq_axes.get_y_axis_label(r"|\hat{g}(f)|", edge=UP, direction=LEFT)
        
        # Signal parameters
        f1, f2 = 2.0, 3.5
        
        # Functions for winding
        def get_winding_path(freq, time_limit=2):
            return ParametricFunction(
                lambda t: winding_plane.coords_to_point(
                    (np.cos(2*np.pi*f1*t) + np.cos(2*np.pi*f2*t)) * np.cos(-2*np.pi*freq*t),
                    (np.cos(2*np.pi*f1*t) + np.cos(2*np.pi*f2*t)) * np.sin(-2*np.pi*freq*t)
                ),
                t_range=[0, time_limit],
                color=COLOR_SUM
            )

        # Center of mass dot
        com_dot = Dot(color=YELLOW)
        com_dot.add_updater(lambda d: d.move_to(winding_plane.coords_to_point(0, 0)))

        # Initial State
        self.play(Write(formula))
        self.play(
            Create(winding_plane),
            Create(circle),
            Create(freq_axes),
            Write(freq_label),
            Write(amp_label)
        )

        # Frequency Sweep Animation
        current_freq = ValueTracker(0.5)
        
        winding_path = always_redraw(lambda: get_winding_path(current_freq.get_value()))
        
        freq_indicator = always_redraw(lambda: Line(
            freq_axes.c2p(current_freq.get_value(), 0),
            freq_axes.c2p(current_freq.get_value(), 0.2),
            color=YELLOW
        ))

        self.add(winding_path, freq_indicator, com_dot)

        # Transition to first peak
        self.play(current_freq.animate.set_value(f1), run_time=3, rate_func=linear)
        
        # Spike 1
        spike1 = Line(freq_axes.c2p(f1, 0), freq_axes.c2p(f1, 1.5), color=COLOR_A, stroke_width=4)
        dot1 = Dot(freq_axes.c2p(f1, 1.5), color=COLOR_A)
        
        self.play(
            com_dot.animate.move_to(winding_plane.coords_to_point(0.8, 0)),
            Create(spike1),
            GrowFromCenter(dot1)
        )
        self.wait(1)

        # Transition to second peak
        self.play(current_freq.animate.set_value(f2), run_time=2, rate_func=linear)
        
        # Spike 2
        spike2 = Line(freq_axes.c2p(f2, 0), freq_axes.c2p(f2, 1.5), color=COLOR_B, stroke_width=4)
        dot2 = Dot(freq_axes.c2p(f2, 1.5), color=COLOR_B)
        
        self.play(
            com_dot.animate.move_to(winding_plane.coords_to_point(0.8, 0)),
            Create(spike2),
            GrowFromCenter(dot2)
        )
        
        # Final Mapping Highlight
        rect_left = SurroundingRectangle(winding_plane, color=YELLOW, buff=0.1)
        rect_right = SurroundingRectangle(freq_axes, color=YELLOW, buff=0.1)
        
        self.play(Create(rect_left))
        self.play(ReplacementTransform(rect_left, rect_right))
        self.play(FadeOut(rect_right))
        
        self.wait(2)
