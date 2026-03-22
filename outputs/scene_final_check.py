
from manim import *

class Scene_final_check(Scene):
    def construct(self):
        title = Text("Troubleshooting Complete", font_size=44).to_edge(UP)
        
        checklist_items = VGroup(
            Text("Clear Cache", font_size=32),
            Text("Hard Refresh", font_size=32),
            Text("Wait for Sync", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(LEFT * 2)

        checks = VGroup(*[
            Square(side_length=0.4).next_to(item, LEFT, buff=0.4)
            for item in checklist_items
        ])

        marks = VGroup(*[
            Tex(r"$\checkmark$", color=GREEN).move_to(check.get_center())
            for check in checks
        ])

        checklist = VGroup(checklist_items, checks)

        user_head = Circle(radius=0.6, color=WHITE).set_fill(BLUE_B, opacity=0.5)
        eye_l = Dot().move_to(user_head.get_center() + LEFT * 0.2 + UP * 0.1)
        eye_r = Dot().move_to(user_head.get_center() + RIGHT * 0.2 + UP * 0.1)
        smile = Arc(radius=0.3, start_angle=-0.2 * PI, angle=-0.6 * PI).move_to(user_head.get_center() + DOWN * 0.15)
        user_avatar = VGroup(user_head, eye_l, eye_r, smile).shift(RIGHT * 3 + UP * 0.5)

        badge_rect = RoundedRectangle(corner_radius=0.2, height=0.8, width=2.0, color=GREEN, fill_opacity=0.8)
        badge_text = Text("FIXED", font_size=36, weight=BOLD, color=WHITE)
        badge = VGroup(badge_rect, badge_text).next_to(user_avatar, DOWN, buff=0.5)

        self.play(Write(title))
        self.wait(0.5)

        for i in range(len(checklist_items)):
            self.play(
                FadeIn(checks[i], shift=RIGHT * 0.2),
                Write(checklist_items[i]),
                run_time=0.6
            )
            self.play(Create(marks[i]), run_time=0.4)

        self.play(
            Create(user_avatar),
            run_time=1
        )
        
        self.play(
            user_avatar.animate.scale(1.1).set_color(YELLOW),
            rate_func=there_and_back,
            run_time=0.5
        )

        self.play(
            DrawBorderThenFill(badge_rect),
            Write(badge_text),
            badge.animate.scale(1.2),
            run_time=0.8
        )

        self.wait(2)
