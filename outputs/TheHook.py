
from manim import *

class Thehook(Scene):
    def construct(self):
        person = VGroup()
        head = Circle(radius=0.3, color=WHITE)
        body = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.8)
        arms = Line(LEFT * 0.4, RIGHT * 0.4).move_to(body.get_center() + UP * 0.1)
        legs = VGroup(
            Line(body.get_end(), body.get_end() + DOWN * 0.5 + LEFT * 0.3),
            Line(body.get_end(), body.get_end() + DOWN * 0.5 + RIGHT * 0.3)
        )
        person.add(head, body, arms, legs).scale(0.8).shift(LEFT * 3)

        mirror_frame = Rectangle(height=4, width=2.5, color=BLUE_D)
        mirror_surface = Rectangle(height=3.8, width=2.3, fill_opacity=0.2, fill_color=BLUE_B)
        mirror = VGroup(mirror_frame, mirror_surface).shift(RIGHT * 2)

        tunnel = VGroup()
        num_layers = 12
        for i in range(num_layers):
            scale_factor = (0.75) ** i
            opacity = 1.0 - (i / num_layers)
            layer = mirror.copy().scale(scale_factor)
            layer.set_stroke(opacity=opacity)
            layer.set_fill(opacity=opacity * 0.2)
            tunnel.add(layer)

        tunnel.move_to(mirror.get_center())

        text = Text("Recursion = A function calling itself", font_size=36)
        text.to_edge(UP)

        self.play(Create(person), Create(mirror))
        self.wait(0.5)
        
        self.play(Write(text))
        self.wait(0.5)

        self.play(
            LaggedStart(
                *[FadeIn(layer, shift=IN) for layer in tunnel],
                lag_ratio=0.1,
                run_time=3
            )
        )

        self.play(
            tunnel.animate.scale(1.1).set_color(BLUE_A),
            rate_func=there_and_back,
            run_time=2
        )

        self.wait(2)
