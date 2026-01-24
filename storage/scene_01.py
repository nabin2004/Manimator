
from manim import *

class Scene_01(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48)
        self.play(Write(title))
        self.wait(2)
        self.play(title.animate.to_edge(UP))

        # Define shapes for the function diagram
        func_outer = RoundedRectangle(width=3, height=1.5, corner_radius=0.2, color=BLUE)
        func_outer_label = Text("Function", font_size=24).move_to(func_outer)
        
        func_inner = RoundedRectangle(width=2, height=1, corner_radius=0.15, color=TEAL)
        func_inner_label = Text("Function", font_size=18).move_to(func_inner)
        
        # Group inner function to sit inside the outer one
        func_group = VGroup(func_outer, func_outer_label)
        inner_group = VGroup(func_inner, func_inner_label)
        
        # Positioning
        diagram_group = VGroup(func_group, inner_group)
        diagram_group.arrange(DOWN, buff=0.5)
        diagram_group.shift(LEFT * 3)

        # Arrows indicating the call
        arrow = Arrow(start=func_outer.get_bottom(), end=func_inner.get_top(), buff=0.1, color=YELLOW)
        arrow_label = Text("calls", font_size=20).next_to(arrow, RIGHT)

        # Visual elements for the mirror analogy
        mirror_group = VGroup()
        frame = Rectangle(width=2, height=3, color=WHITE, fill_opacity=0.1)
        frame_label = Text("Mirror", font_size=20).next_to(frame, UP)
        
        # Reflection layers
        reflection_1 = Rectangle(width=1.6, height=2.4, color=GRAY, fill_opacity=0.3)
        reflection_1.move_to(frame.get_center())
        
        reflection_2 = Rectangle(width=1.2, height=1.8, color=WHITE, fill_opacity=0.5)
        reflection_2.move_to(frame.get_center())
        
        reflection_3 = Rectangle(width=0.8, height=1.2, color=YELLOW, fill_opacity=0.7)
        reflection_3.move_to(frame.get_center())

        mirror_group.add(frame, frame_label, reflection_1, reflection_2, reflection_3)
        mirror_group.shift(RIGHT * 3)

        # Animation sequence
        self.play(
            Create(func_outer),
            Write(func_outer_label)
        )
        self.wait(0.5)
        
        self.play(
            Create(func_inner),
            Write(func_inner_label)
        )
        self.wait(0.5)
        
        self.play(GrowArrow(arrow))
        self.play(Write(arrow_label))
        self.wait(2)

        # Transition to mirror analogy
        self.play(
            diagram_group.animate.scale(0.8).to_edge(LEFT),
            FadeOut(arrow_label)
        )
        
        self.play(
            Create(frame),
            Write(frame_label)
        )
        
        self.play(
            FadeIn(reflection_1),
            run_time=0.5
        )
        self.play(
            FadeIn(reflection_2),
            run_time=0.5
        )
        self.play(
            FadeIn(reflection_3),
            run_time=0.5
        )
        
        self.wait(2)

        # Add definition text
        definition = Text("Recursion: A function calling itself", font_size=32)
        definition.next_to(VGroup(diagram_group, mirror_group), DOWN, buff=1)
        
        self.play(Write(definition))
        self.wait(3)
