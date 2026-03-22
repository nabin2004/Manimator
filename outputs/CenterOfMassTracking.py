
from manim import *
import numpy as np

class CenterOfMassTracking(Scene):
    def construct(self):
        # Parameters
        freq1 = 2
        freq2 = 5
        duration = 2.0
        
        def signal_func(t):
            return np.cos(2 * PI * freq1 * t) + np.cos(2 * PI * freq2 * t)

        # Axes and Labels
        axes = Axes(
            x_range=[0, 6, 1], y_range=[-1.5, 1.5, 1],
            axis_config={"include_tip": False},
            x_length=5, y_length=2
        ).to_edge(UP).shift(RIGHT * 3)
        
        wrap_plane = PolarPlane(radius_max=2.5).scale(0.5).to_edge(LEFT, buff=1)
        
        mag_axes = Axes(
            x_range=[0, 7, 1], y_range=[0, 1.2, 0.5],
            x_length=5, y_length=2,
            axis_config={"include_tip": False}
        ).to_edge(DOWN).shift(RIGHT * 3)
        
        mag_label = Text("Distance from Origin", font_size=24).next_to(mag_axes, UP, buff=0.1)
        freq_label = Text("Winding Frequency (f)", font_size=24).next_to(mag_axes, RIGHT, buff=0.1).scale(0.8)

        # State variables
        winding_freq = ValueTracker(0.1)

        # Wrapped Shape
        def get_wrapped_shape():
            f = winding_freq.get_value()
            return ParametricFunction(
                lambda t: wrap_plane.coords_to_point(
                    signal_func(t), 2 * PI * f * t
                ),
                t_range=[0, duration],
                color=BLUE_B
            )

        wrapped_shape = always_redraw(get_wrapped_shape)

        # Center of Mass Calculation
        def get_com_pos():
            f = winding_freq.get_value()
            # Numerical integration for COM
            steps = 100
            dt = duration / steps
            points = [
                np.array([
                    signal_func(t) * np.cos(2 * PI * f * t),
                    signal_func(t) * np.sin(2 * PI * f * t),
                    0
                ]) for t in np.linspace(0, duration, steps)
            ]
            avg_pos = sum(points) / steps
            return wrap_plane.coords_to_point(avg_pos[0], np.arctan2(avg_pos[1], avg_pos[0]))

        com_dot = Dot(color=RED).add_updater(lambda d: d.move_to(get_com_pos()))
        
        # Trace of COM
        com_trace = TracingTail(com_dot, time_traced=3, stroke_width=4, stroke_color=RED)

        # Magnitude Graph
        def get_com_magnitude():
            p = get_com_pos()
            origin = wrap_plane.get_origin()
            return np.linalg.norm(p - origin) * 0.8 # Scale for visual graph

        mag_points = []
        mag_curve = VMobject(color=YELLOW)
        
        def update_mag_curve(mob):
            f = winding_freq.get_value()
            mag = get_com_magnitude()
            mag_points.append(mag_axes.c2p(f, mag))
            mob.set_points_as_corners(mag_points)

        mag_curve.add_updater(update_mag_curve)

        # Highlighting Logic
        highlight_rect = SurroundingRectangle(wrap_plane, color=WHITE, buff=0.1).set_opacity(0)
        
        def update_highlight(mob):
            f = winding_freq.get_value()
            if abs(f - freq1) < 0.2 or abs(f - freq2) < 0.2:
                mob.set_opacity(1)
            else:
                mob.set_opacity(0)
        
        highlight_rect.add_updater(update_highlight)

        # Animation
        self.add(wrap_plane, axes, mag_axes, mag_label, freq_label)
        self.add(wrapped_shape, com_dot, com_trace, mag_curve, highlight_rect)
        
        self.play(winding_freq.animate.set_value(7), run_time=15, rate_func=linear)
        self.wait(2)
