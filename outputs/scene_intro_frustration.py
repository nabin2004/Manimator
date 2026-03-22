
from manim import *

class Scene_intro_frustration(Scene):
    def construct(self):
        screen_frame = Rectangle(width=8, height=5, color=WHITE)
        screen_bg = Rectangle(width=7.8, height=4.8, fill_color=BLACK, fill_opacity=1)
        screen = VGroup(screen_bg, screen_frame)

        refresh_button = VGroup(
            RoundedRectangle(corner_radius=0.1, width=1.5, height=0.6, color=BLUE),
            Text("REFRESH", font_size=18, color=WHITE)
        ).shift(UP * 1.5)

        spinner = Arc(radius=0.5, start_angle=0, angle=TAU * 0.75, color=YELLOW)
        spinner.add_tip(tip_length=0.1)
        spinner.shift(DOWN * 0.5)

        cursor = VGroup(
            Polygon(ORIGIN, RIGHT * 0.3, DOWN * 0.3, color=WHITE, fill_opacity=1),
            Line(ORIGIN, DOWN * 0.4, color=WHITE)
        ).scale(0.8)
        cursor.move_to(refresh_button.get_center() + RIGHT * 0.5 + DOWN * 0.5)

        not_updating_bubble = VGroup(
            RoundedRectangle(corner_radius=0.2, width=3, height=1, color=RED, fill_color=RED, fill_opacity=0.2),
            Text("Not Updating", color=RED, font_size=24)
        ).shift(DOWN * 1.8)

        self.add(screen, refresh_button)
        self.play(Create(spinner))
        
        self.play(cursor.animate.move_to(refresh_button.get_center()))
        
        for _ in range(3):
            self.play(refresh_button.animate.scale(0.9), run_time=0.1)
            self.play(refresh_button.animate.scale(1.11), run_time=0.1)
            self.play(Rotate(spinner, angle=TAU), run_time=0.5)

        self.play(FadeIn(not_updating_bubble, shift=UP))
        
        self.play(
            spinner.animate.set_color(RED),
            refresh_button.animate.set_color(GRAY),
            Indicate(not_updating_bubble)
        )

        self.wait(2)
