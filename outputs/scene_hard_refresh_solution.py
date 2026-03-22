
from manim import *

class Scene_hard_refresh_solution(Scene):
    def construct(self):
        ctrl_key = VGroup(RoundedRectangle(height=1, width=1.5, corner_radius=0.1), Text("Ctrl", font_size=24))
        shift_key = VGroup(RoundedRectangle(height=1, width=1.8, corner_radius=0.1), Text("Shift", font_size=24))
        r_key = VGroup(RoundedRectangle(height=1, width=1, corner_radius=0.1), Text("R", font_size=24))
        
        keyboard = VGroup(ctrl_key, shift_key, r_key).arrange(RIGHT, buff=0.2)
        keyboard.to_edge(UP, buff=1.5)

        screen_rect = Rectangle(height=3, width=5, color=WHITE)
        screen_rect.to_edge(DOWN, buff=1)
        
        old_content = VGroup(
            Rectangle(height=0.5, width=4, fill_opacity=0.5, color=GRAY),
            Rectangle(height=0.2, width=3, fill_opacity=0.3, color=GRAY),
            Rectangle(height=0.2, width=3.5, fill_opacity=0.3, color=GRAY)
        ).arrange(DOWN, buff=0.2).move_to(screen_rect.get_center())

        new_content = VGroup(
            Rectangle(height=0.5, width=4, fill_opacity=0.8, color=BLUE),
            Rectangle(height=0.2, width=3, fill_opacity=0.6, color=BLUE),
            Rectangle(height=0.2, width=3.5, fill_opacity=0.6, color=BLUE)
        ).arrange(DOWN, buff=0.2).move_to(screen_rect.get_center())

        progress_bar_bg = Rectangle(height=0.2, width=4, color=WHITE).next_to(screen_rect, UP, buff=0.2)
        progress_bar_fill = Rectangle(height=0.2, width=0, color=GREEN, fill_opacity=1).align_to(progress_bar_bg, LEFT)

        self.add(keyboard, screen_rect, old_content)
        self.wait(0.5)

        glow_color = YELLOW
        self.play(
            ctrl_key[0].animate.set_stroke(glow_color, width=8),
            shift_key[0].animate.set_stroke(glow_color, width=8),
            r_key[0].animate.set_stroke(glow_color, width=8),
            run_time=0.3
        )

        self.add(progress_bar_bg, progress_bar_fill)
        self.play(
            progress_bar_fill.animate.stretch_to_fit_width(4).align_to(progress_bar_bg, LEFT),
            run_time=0.8,
            rate_func=linear
        )

        self.play(
            FadeOut(old_content),
            FadeIn(new_content),
            ctrl_key[0].animate.set_stroke(WHITE, width=2),
            shift_key[0].animate.set_stroke(WHITE, width=2),
            r_key[0].animate.set_stroke(WHITE, width=2),
            FadeOut(progress_bar_bg),
            FadeOut(progress_bar_fill),
            run_time=0.4
        )

        success_text = Text("Hard Refresh Complete", color=GREEN, font_size=32).next_to(screen_rect, DOWN, buff=0.3)
        self.play(Write(success_text))
        self.wait(2)
