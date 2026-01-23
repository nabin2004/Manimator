
from manim import *

class Scene_04(Scene):
    def construct(self):
        # Title
        title = Text("Call Stack Visualization: factorial(3)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Stack container (grows downward)
        stack_group = VGroup()
        stack_group.next_to(title, DOWN, buff=1)
        
        # Base coordinates for the bottom of the stack
        base_y = -3.0
        stack_x = -4.0
        frame_height = 0.8
        frame_width = 3.0
        
        # Helper to create a frame
        def create_frame(label_text, value_text, y_pos):
            frame = RoundedRectangle(
                width=frame_width, 
                height=frame_height, 
                corner_radius=0.1,
                color=BLUE,
                fill_opacity=0.2,
                stroke_width=2
            )
            frame.move_to([stack_x, y_pos, 0])
            
            label = Text(label_text, font_size=20, color=WHITE).next_to(frame, LEFT, buff=0.2)
            value = Text(value_text, font_size=20, color=YELLOW).next_to(frame, RIGHT, buff=0.2)
            
            return VGroup(frame, label, value)

        # Helper to create push arrow
        def create_push_arrow(y_pos):
            arrow = Arrow(
                start=[stack_x - 2, y_pos + 0.5, 0],
                end=[stack_x - 1.2, y_pos + 0.1, 0],
                buff=0.1,
                color=GREEN,
                max_tip_length_to_length_ratio=0.2
            )
            text = Text("Push", font_size=18, color=GREEN).next_to(arrow, LEFT, buff=0.1)
            return VGroup(arrow, text)

        # Helper to create pop arrow
        def create_pop_arrow(y_pos):
            arrow = Arrow(
                start=[stack_x - 1.2, y_pos - 0.1, 0],
                end=[stack_x - 2, y_pos - 0.5, 0],
                buff=0.1,
                color=RED,
                max_tip_length_to_length_ratio=0.2
            )
            text = Text("Pop", font_size=18, color=RED).next_to(arrow, LEFT, buff=0.1)
            return VGroup(arrow, text)

        # Initial stack state (empty)
        stack_label = Text("Stack", font_size=24).next_to(stack_group, LEFT, buff=1)
        self.play(Write(stack_label))
        
        # --- Phase 1: Pushing frames (Recursive Calls) ---
        
        # 1. factorial(3)
        frame_3 = create_frame("factorial(3)", "n=3", base_y)
        arrow_3 = create_push_arrow(base_y)
        
        self.play(FadeIn(frame_3), Write(arrow_3))
        self.wait(0.5)
        self.play(FadeOut(arrow_3))
        
        # 2. factorial(2)
        frame_2 = create_frame("factorial(2)", "n=2", base_y + 1.0)
        arrow_2 = create_push_arrow(base_y + 1.0)
        
        self.play(FadeIn(frame_2), Write(arrow_2))
        self.wait(0.5)
        self.play(FadeOut(arrow_2))
        
        # 3. factorial(1)
        frame_1 = create_frame("factorial(1)", "n=1", base_y + 2.0)
        arrow_1 = create_push_arrow(base_y + 2.0)
        
        self.play(FadeIn(frame_1), Write(arrow_1))
        self.wait(0.5)
        self.play(FadeOut(arrow_1))
        
        # 4. factorial(0) - Base Case
        frame_0 = create_frame("factorial(0)", "n=0", base_y + 3.0)
        arrow_0 = create_push_arrow(base_y + 3.0)
        
        self.play(FadeIn(frame_0), Write(arrow_0))
        self.wait(0.5)
        self.play(FadeOut(arrow_0))
        
        # Highlight base case
        self.play(frame_0[0].animate.set_fill(RED, opacity=0.5))
        base_text = Text("Base Case Reached!", font_size=20, color=RED)
        base_text.next_to(frame_0, RIGHT, buff=1.5)
        self.play(Write(base_text))
        self.wait(1)
        
        # --- Phase 2: Unwinding (Returns) ---
        
        # 1. Pop factorial(0)
        pop_arrow_0 = create_pop_arrow(base_y + 3.0)
        self.play(Write(pop_arrow_0))
        self.play(
            FadeOut(frame_0),
            FadeOut(pop_arrow_0),
            FadeOut(base_text)
        )
        
        # Return value 1 to factorial(1)
        ret_val_1 = Text("return 1", font_size=18, color=YELLOW)
        ret_val_1.move_to([stack_x + 2.5, base_y + 2.0, 0])
        self.play(Write(ret_val_1))
        self.wait(0.5)
        
        # 2. Pop factorial(1)
        pop_arrow_1 = create_pop_arrow(base_y + 2.0)
        self.play(Write(pop_arrow_1))
        self.play(
            FadeOut(frame_1),
            FadeOut(pop_arrow_1),
            FadeOut(ret_val_1)
        )
        
        # Return value 1 to factorial(2)
        ret_val_2 = Text("return 1", font_size=18, color=YELLOW)
        ret_val_2.move_to([stack_x + 2.5, base_y + 1.0, 0])
        self.play(Write(ret_val_2))
        self.wait(0.5)
        
        # 3. Pop factorial(2)
        pop_arrow_2 = create_pop_arrow(base_y + 1.0)
        self.play(Write(pop_arrow_2))
        self.play(
            FadeOut(frame_2),
            FadeOut(pop_arrow_2),
            FadeOut(ret_val_2)
        )
        
        # Return value 2 to factorial(3)
        ret_val_3 = Text("return 2", font_size=18, color=YELLOW)
        ret_val_3.move_to([stack_x + 2.5, base_y, 0])
        self.play(Write(ret_val_3))
        self.wait(0.5)
        
        # 4. Pop factorial(3)
        pop_arrow_3 = create_pop_arrow(base_y)
        self.play(Write(pop_arrow_3))
        self.play(
            FadeOut(frame_3),
            FadeOut(pop_arrow_3),
            FadeOut(ret_val_3)
        )
        
        # Final Result
        final_result = Text("Result: 6", font_size=32, color=GREEN)
        final_result.move_to([0, 0, 0])
        self.play(Write(final_result))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(stack_label), FadeOut(title), FadeOut(final_result))
        self.wait(1)
