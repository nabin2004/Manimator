
from manim import *
import numpy as np

class Inverseandapplications(Scene):
    def construct(self):
        title = Text("FFT: Noise Reduction & Reconstruction", font_size=36).to_edge(UP)
        self.play(Write(title))

        # 1. FFT Matrix Visualization
        matrix_group = VGroup()
        n = 8
        matrix_grid = VGroup()
        for i in range(n):
            for j in range(n):
                val = np.exp(-2j * np.pi * i * j / n)
                color = interpolate_color(BLUE, RED, (np.angle(val) + np.pi) / (2 * np.pi))
                rect = Rectangle(width=0.4, height=0.4, fill_opacity=0.8, fill_color=color, stroke_width=1)
                rect.move_to(np.array([j * 0.45, -i * 0.45, 0]))
                matrix_grid.add(rect)
        
        matrix_label = Text("DFT Matrix (W)", font_size=24).next_to(matrix_grid, UP)
        matrix_group.add(matrix_grid, matrix_label).center().shift(LEFT * 3 + DOWN * 0.5)
        
        self.play(FadeIn(matrix_group))
        self.wait(1)

        # 2. Spectrogram / Frequency Domain
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 5, 1],
            axis_config={"include_tip": False},
            x_length=5, y_length=3
        ).shift(RIGHT * 3 + UP * 1)
        
        freq_label = Text("Frequency Spectrum", font_size=24).next_to(axes, UP)
        
        # Signal with noise spike
        def get_spectrum_path(noise=True):
            points = []
            for x in np.linspace(0, 10, 100):
                y = 0.5 * np.exp(-(x-2)**2 / 0.2) + 0.3 * np.exp(-(x-5)**2 / 0.5)
                if noise:
                    y += 3.0 * np.exp(-(x-8)**2 / 0.05) # High freq noise spike
                points.append(axes.c2p(x, y))
            return VMobject(color=YELLOW).set_points_as_corners(points)

        spectrum_noisy = get_spectrum_path(noise=True)
        self.play(Create(axes), Write(freq_label))
        self.play(Create(spectrum_noisy))
        self.wait(1)

        # 3. Filtering Animation
        filter_rect = Rectangle(width=1.0, height=4.0, color=RED, fill_opacity=0.3)
        filter_rect.move_to(axes.c2p(8, 2))
        filter_text = Text("Filter Noise", font_size=20, color=RED).next_to(filter_rect, DOWN)
        
        self.play(FadeIn(filter_rect), Write(filter_text))
        
        spectrum_clean = get_spectrum_path(noise=False)
        self.play(
            Transform(spectrum_noisy, spectrum_clean),
            filter_rect.animate.set_opacity(0),
            run_time=2
        )
        self.remove(filter_rect, filter_text)
        self.wait(1)

        # 4. Reconstruction (Inverse FFT)
        time_axes = Axes(
            x_range=[0, 10, 1], y_range=[-1.5, 1.5, 1],
            axis_config={"include_tip": False},
            x_length=5, y_length=2
        ).shift(RIGHT * 3 + DOWN * 2)
        
        time_label = Text("Reconstructed Signal (iFFT)", font_size=24).next_to(time_axes, UP)
        
        def get_time_signal():
            points = []
            for x in np.linspace(0, 10, 200):
                y = np.sin(1.2 * x) + 0.5 * np.cos(3.0 * x)
                points.append(time_axes.c2p(x, y))
            return VMobject(color=GREEN).set_points_as_corners(points)

        recon_signal = get_time_signal()
        
        arrow = Arrow(axes.get_bottom(), time_axes.get_top(), buff=0.2)
        ifft_text = Text("Inverse Transform", font_size=20).next_to(arrow, RIGHT)

        self.play(Create(time_axes), Write(time_label))
        self.play(GrowArrow(arrow), Write(ifft_text))
        self.play(Create(recon_signal), run_time=2)
        self.wait(2)

        # Final Summary
        summary = Text("Cleaned & Compressed", font_size=32, color=GOLD).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(2)
