
from manim import *

class Scene_server_sync(Scene):
    def construct(self):
        cloud = VGroup(
            Circle(radius=0.5).shift(LEFT * 0.4),
            Circle(radius=0.6).shift(UP * 0.2),
            Circle(radius=0.5).shift(RIGHT * 0.4),
            Rectangle(width=1.0, height=0.5).shift(DOWN * 0.1)
        ).set_fill(BLUE_B, opacity=1).set_stroke(WHITE, width=2)
        cloud.move_to(UP * 2 + LEFT * 3)
        cloud_label = Text("Cloud Server", font_size=24).next_to(cloud, UP)

        database = VGroup(
            Cylinder(radius=0.6, height=1.2, fill_color=GRAY_D, fill_opacity=1),
            Ellipse(width=1.2, height=0.4, color=GRAY_B, fill_opacity=1).shift(UP * 0.6),
            Ellipse(width=1.2, height=0.4, color=GRAY_B, fill_opacity=1).shift(UP * 0.2),
            Ellipse(width=1.2, height=0.4, color=GRAY_B, fill_opacity=1).shift(DOWN * 0.2)
        )
        database.move_to(UP * 2 + RIGHT * 3)
        db_label = Text("Database", font_size=24).next_to(database, UP)

        connection_line = Line(cloud.get_right(), database.get_left(), buff=0.2)
        
        sync_text = Text("Syncing...", font_size=32).move_to(DOWN * 0.5)
        bar_outline = Rectangle(width=4, height=0.4, color=WHITE).next_to(sync_text, DOWN)
        bar_fill = Rectangle(width=0.01, height=0.3, color=BLUE_C, fill_opacity=1).align_to(bar_outline, LEFT).shift(RIGHT * 0.05)

        explanation = Text(
            "Update is still processing on the server side.",
            font_size=28,
            color=YELLOW
        ).to_edge(DOWN, buff=1)

        self.play(Create(cloud), Write(cloud_label))
        self.play(Create(database), Write(db_label))
        self.play(Create(connection_line))
        self.wait(0.5)

        self.play(Write(sync_text), Create(bar_outline))
        
        dot = Dot(cloud.get_center(), color=WHITE)
        self.play(
            dot.animate.move_to(database.get_center()),
            bar_fill.animate.stretch_to_fit_width(3.9).align_to(bar_outline, LEFT).shift(RIGHT * 0.05),
            Write(explanation),
            run_time=3,
            rate_func=linear
        )
        self.remove(dot)

        checkmark = VGroup(
            Line(LEFT * 0.3 + DOWN * 0.1, ORIGIN, color=GREEN, stroke_width=8),
            Line(ORIGIN, RIGHT * 0.5 + UP * 0.6, color=GREEN, stroke_width=8)
        ).move_to(sync_text.get_center())

        self.play(
            FadeOut(sync_text),
            FadeOut(bar_outline),
            FadeOut(bar_fill),
            FadeOut(explanation),
            Create(checkmark)
        )
        
        complete_text = Text("Sync Complete", color=GREEN, font_size=32).next_to(checkmark, DOWN)
        self.play(Write(complete_text))
        self.wait(2)
