
from manim import *

class Scene_04(Scene):
    def construct(self):
        # Title
        title = Text("Call Stack Visualization", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Stack container (bottom to top)
        stack_group = VGroup()
        stack_group.next_to(title, DOWN, buff=1)

        # Colors for frames
        colors = [BLUE, GREEN, YELLOW, RED]
        
        # Helper to create a frame
        def create_frame(label_text, color):
            rect = Rectangle(width=4, height=0.8, color=color, fill_opacity=0.2)
            text = Text(label_text, font_size=24)
            text.move_to(rect.get_center())
            frame = VGroup(rect, text)
            return frame

        # Helper to update stack positions
        def update_stack_positions():
            for i, frame in enumerate(stack_group):
                target_y = stack_group.get_bottom()[1] + i * 0.9
                frame.move_to([0, target_y, 0], aligned_edge=DOWN)

        # Initial state: Stack is empty
        self.wait(1)

        # Push factorial(3)
        frame_3 = create_frame("factorial(3)", colors[0])
        arrow_push_3 = Arrow(start=LEFT * 3 + UP * 2, end=frame_3.get_top(), buff=0.1, color=WHITE)
        
        self.play(GrowArrow(arrow_push_3))
        self.play(FadeIn(frame_3))
        stack_group.add(frame_3)
        self.play(Transform(arrow_push_3, Arrow(start=arrow_push_3.get_start(), end=frame_3.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeOut(arrow_push_3))
        self.wait(0.5)

        # Highlight top frame (factorial(3))
        self.play(frame_3[0].animate.set_fill(opacity=0.5))
        self.wait(1)
        self.play(frame_3[0].animate.set_fill(opacity=0.2))

        # Push factorial(2)
        frame_2 = create_frame("factorial(2)", colors[1])
        frame_2.next_to(frame_3, DOWN, buff=0)
        arrow_push_2 = Arrow(start=LEFT * 3 + UP * 2, end=frame_2.get_top(), buff=0.1, color=WHITE)
        
        self.play(GrowArrow(arrow_push_2))
        self.play(FadeIn(frame_2))
        stack_group.add(frame_2)
        update_stack_positions()
        self.play(Transform(arrow_push_2, Arrow(start=arrow_push_2.get_start(), end=frame_2.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeOut(arrow_push_2))
        self.wait(0.5)

        # Highlight top frame (factorial(2))
        self.play(frame_2[0].animate.set_fill(opacity=0.5))
        self.wait(1)
        self.play(frame_2[0].animate.set_fill(opacity=0.2))

        # Push factorial(1)
        frame_1 = create_frame("factorial(1)", colors[2])
        frame_1.next_to(frame_2, DOWN, buff=0)
        arrow_push_1 = Arrow(start=LEFT * 3 + UP * 2, end=frame_1.get_top(), buff=0.1, color=WHITE)
        
        self.play(GrowArrow(arrow_push_1))
        self.play(FadeIn(frame_1))
        stack_group.add(frame_1)
        update_stack_positions()
        self.play(Transform(arrow_push_1, Arrow(start=arrow_push_1.get_start(), end=frame_1.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeOut(arrow_push_1))
        self.wait(0.5)

        # Highlight top frame (factorial(1))
        self.play(frame_1[0].animate.set_fill(opacity=0.5))
        self.wait(1)
        self.play(frame_1[0].animate.set_fill(opacity=0.2))

        # Push factorial(0)
        frame_0 = create_frame("factorial(0)", colors[3])
        frame_0.next_to(frame_1, DOWN, buff=0)
        arrow_push_0 = Arrow(start=LEFT * 3 + UP * 2, end=frame_0.get_top(), buff=0.1, color=WHITE)
        
        self.play(GrowArrow(arrow_push_0))
        self.play(FadeIn(frame_0))
        stack_group.add(frame_0)
        update_stack_positions()
        self.play(Transform(arrow_push_0, Arrow(start=arrow_push_0.get_start(), end=frame_0.get_top(), buff=0.1, color=WHITE)))
        self.play(FadeOut(arrow_push_0))
        self.wait(0.5)

        # Highlight top frame (factorial(0))
        self.play(frame_0[0].animate.set_fill(opacity=0.5))
        self.wait(1)
        self.play(frame_0[0].animate.set_fill(opacity=0.2))

        # Pop factorial(0)
        arrow_pop_0 = Arrow(start=frame_0.get_bottom(), end=LEFT * 3 + DOWN * 2, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow_pop_0))
        self.play(FadeOut(frame_0), FadeOut(arrow_pop_0))
        stack_group.remove(frame_0)
        self.wait(0.5)

        # Pop factorial(1)
        arrow_pop_1 = Arrow(start=frame_1.get_bottom(), end=LEFT * 3 + DOWN * 2, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow_pop_1))
        self.play(FadeOut(frame_1), FadeOut(arrow_pop_1))
        stack_group.remove(frame_1)
        self.wait(0.5)

        # Pop factorial(2)
        arrow_pop_2 = Arrow(start=frame_2.get_bottom(), end=LEFT * 3 + DOWN * 2, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow_pop_2))
        self.play(FadeOut(frame_2), FadeOut(arrow_pop_2))
        stack_group.remove(frame_2)
        self.wait(0.5)

        # Pop factorial(3)
        arrow_pop_3 = Arrow(start=frame_3.get_bottom(), end=LEFT * 3 + DOWN * 2, buff=0.1, color=WHITE)
        self.play(GrowArrow(arrow_pop_3))
        self.play(FadeOut(frame_3), FadeOut(arrow_pop_3))
        stack_group.remove(frame_3)
        self.wait(0.5)

        # End text
        end_text = Text("Stack Empty", font_size=36)
        end_text.move_to(ORIGIN)
        self.play(Write(end_text))
        self.wait(2)
