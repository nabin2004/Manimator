
from manim import *

class Scene_03(Scene):
    def construct(self):
        # Title
        title = Text("Call Stack for factorial(3)", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Stack container
        stack_group = VGroup()
        stack_group.move_to(ORIGIN).shift(DOWN * 0.5)

        # Colors for stack frames
        colors = [BLUE, GREEN, YELLOW]

        # Helper to create a stack frame box
        def create_frame(label_text, index):
            rect = Rectangle(width=4, height=1.2, color=colors[index], fill_opacity=0.2, stroke_width=3)
            text = Text(label_text, font_size=24)
            text.move_to(rect.get_center())
            frame = VGroup(rect, text)
            return frame

        # Initial state: Empty stack
        empty_text = Text("Stack: Empty", font_size=24).move_to(ORIGIN)
        self.play(Write(empty_text))
        self.wait(0.5)

        # Step 1: Push factorial(3)
        self.play(FadeOut(empty_text))
        
        frame_3 = create_frame("factorial(3)", 0)
        frame_3.move_to(stack_group.get_center())
        
        # Arrow for push
        arrow_push_3 = Arrow(LEFT * 3, frame_3.get_left(), buff=0.1, color=WHITE)
        label_push_3 = Text("push", font_size=20).next_to(arrow_push_3, UP, buff=0.1)

        self.play(GrowArrow(arrow_push_3), Write(label_push_3))
        self.play(FadeIn(frame_3))
        self.wait(0.5)
        self.play(FadeOut(arrow_push_3), FadeOut(label_push_3))

        # Step 2: Push factorial(2)
        frame_2 = create_frame("factorial(2)", 1)
        frame_2.next_to(frame_3, DOWN, buff=0.2)
        
        arrow_push_2 = Arrow(LEFT * 3, frame_2.get_left(), buff=0.1, color=WHITE)
        label_push_2 = Text("push", font_size=20).next_to(arrow_push_2, UP, buff=0.1)

        self.play(GrowArrow(arrow_push_2), Write(label_push_2))
        self.play(FadeIn(frame_2))
        self.wait(0.5)
        self.play(FadeOut(arrow_push_2), FadeOut(label_push_2))

        # Step 3: Push factorial(1)
        frame_1 = create_frame("factorial(1)", 2)
        frame_1.next_to(frame_2, DOWN, buff=0.2)
        
        arrow_push_1 = Arrow(LEFT * 3, frame_1.get_left(), buff=0.1, color=WHITE)
        label_push_1 = Text("push", font_size=20).next_to(arrow_push_1, UP, buff=0.1)

        self.play(GrowArrow(arrow_push_1), Write(label_push_1))
        self.play(FadeIn(frame_1))
        self.wait(0.5)
        self.play(FadeOut(arrow_push_1), FadeOut(label_push_1))

        # Wait to show full stack
        self.wait(1)

        # Step 4: Pop factorial(1)
        arrow_pop_1 = Arrow(frame_1.get_right(), RIGHT * 3, buff=0.1, color=WHITE)
        label_pop_1 = Text("pop", font_size=20).next_to(arrow_pop_1, UP, buff=0.1)

        self.play(GrowArrow(arrow_pop_1), Write(label_pop_1))
        self.play(FadeOut(frame_1))
        self.wait(0.5)
        self.play(FadeOut(arrow_pop_1), FadeOut(label_pop_1))

        # Step 5: Pop factorial(2)
        arrow_pop_2 = Arrow(frame_2.get_right(), RIGHT * 3, buff=0.1, color=WHITE)
        label_pop_2 = Text("pop", font_size=20).next_to(arrow_pop_2, UP, buff=0.1)

        self.play(GrowArrow(arrow_pop_2), Write(label_pop_2))
        self.play(FadeOut(frame_2))
        self.wait(0.5)
        self.play(FadeOut(arrow_pop_2), FadeOut(label_pop_2))

        # Step 6: Pop factorial(3)
        arrow_pop_3 = Arrow(frame_3.get_right(), RIGHT * 3, buff=0.1, color=WHITE)
        label_pop_3 = Text("pop", font_size=20).next_to(arrow_pop_3, UP, buff=0.1)

        self.play(GrowArrow(arrow_pop_3), Write(label_pop_3))
        self.play(FadeOut(frame_3))
        self.wait(0.5)
        self.play(FadeOut(arrow_pop_3), FadeOut(label_pop_3))

        # Final state: Stack empty
        final_text = Text("Stack: Empty", font_size=24).move_to(ORIGIN)
        self.play(Write(final_text))
        self.wait(1)
