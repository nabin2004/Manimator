
from manim import *

class Unwindingthestack(Scene):
    def construct(self):
        stack_frames = VGroup(*[
            VGroup(
                RoundedRectangle(height=0.8, width=3, corner_radius=0.1, color=BLUE_B, fill_opacity=0.2),
                Text(f"fact({i})", font_size=24)
            ) for i in range(4)
        ]).arrange(UP, buff=0.2)
        
        stack_frames.shift(UP * 0.5)
        self.add(stack_frames)

        base_case_text = Text("1", color=YELLOW).move_to(stack_frames[0])
        self.play(
            stack_frames[0][1].animate.set_color(YELLOW),
            FadeIn(base_case_text, shift=UP * 0.2)
        )
        self.wait(0.5)

        current_val = 1
        result_display = Text(str(current_val), font_size=36, color=GREEN).to_edge(DOWN, buff=1)
        
        for i in range(1, 4):
            prev_val = current_val
            current_val *= i
            
            frame_to_pop = stack_frames[i]
            multiplier_text = Text(f"× {i}", font_size=30, color=WHITE).next_to(frame_to_pop, RIGHT)
            
            self.play(
                frame_to_pop.animate.shift(RIGHT * 0.5).set_opacity(0.5),
                FadeIn(multiplier_text),
                base_case_text.animate.next_to(multiplier_text, LEFT)
            )
            
            new_result_text = Text(str(current_val), font_size=36, color=GREEN).move_to(result_display)
            
            self.play(
                FadeOut(frame_to_pop),
                FadeOut(multiplier_text),
                FadeOut(base_case_text),
                Transform(result_display, new_result_text)
            )
            
            base_case_text = new_result_text.copy()
            self.wait(0.3)

        final_label = Text("Result:", font_size=24).next_to(result_display, LEFT)
        self.play(
            Write(final_label),
            result_display.animate.scale(1.5).set_color(YELLOW)
        )
        self.wait(2)
