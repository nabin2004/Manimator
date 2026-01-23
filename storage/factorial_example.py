
from manim import *

class Factorial_example(Scene):
    def construct(self):
        title = Text("Recursive Factorial", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Equation: n! = n * (n-1)!
        equation = MathTex("n!", "=", "n", "\\times", "(n-1)!")
        equation.next_to(title, DOWN, buff=0.8)
        self.play(Write(equation))
        self.wait(1)

        # Highlight the recursive part
        recursive_part = equation[4]
        self.play(recursive_part.animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(recursive_part.animate.set_color(WHITE))
        
        # Define stack positions (from top to bottom)
        # We will show factorial(4) -> factorial(3) -> factorial(2) -> factorial(1) -> factorial(0)
        stack_y_start = 0.5
        stack_y_step = -1.2
        stack_x = -5.5
        
        # Create stack frames
        frames = VGroup()
        texts = VGroup()
        
        calc_values = [4, 3, 2, 1, 0]
        
        for i, val in enumerate(calc_values):
            # Frame rectangle
            rect = RoundedRectangle(width=3, height=0.8, corner_radius=0.1)
            rect.set_fill(BLACK, opacity=0.8)
            rect.set_stroke(WHITE, width=2)
            rect.move_to([stack_x, stack_y_start + i * stack_y_step, 0])
            
            # Text inside frame
            txt = MathTex(f"\\text{{factorial}}({val})")
            txt.scale(0.8)
            txt.move_to(rect.get_center())
            
            frames.add(rect)
            texts.add(txt)

        # Animate stack buildup
        self.play(
            LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.2),
            LaggedStart(*[FadeIn(t) for t in texts], lag_ratio=0.2),
            run_time=2
        )
        self.wait(1)

        # Base case handling: factorial(0) = 1
        base_frame = frames[4]
        base_text = texts[4]
        base_result = MathTex("= 1").next_to(base_frame, RIGHT, buff=0.2)
        
        self.play(base_frame.animate.set_fill(BLUE_E, opacity=0.5))
        self.play(Write(base_result))
        self.wait(0.5)

        # Return arrows showing multiplication results
        # We go up the stack: 1 -> 1*1 -> 2*1 -> 3*2 -> 4*6
        # Actually: 
        # fact(1) returns 1 * fact(0)=1 -> 1
        # fact(2) returns 2 * fact(1)=1 -> 2
        # fact(3) returns 3 * fact(2)=2 -> 6
        # fact(4) returns 4 * fact(3)=6 -> 24
        
        results = [1, 1, 2, 6, 24] # Index 0 is fact(4), index 4 is fact(0)
        # Wait, let's trace carefully:
        # fact(0) -> 1
        # fact(1) -> 1 * 1 = 1
        # fact(2) -> 2 * 1 = 2
        # fact(3) -> 3 * 2 = 6
        # fact(4) -> 4 * 6 = 24
        
        # We will animate the return path from bottom (index 4) to top (index 0)
        # But the calculation happens as we return.
        
        # Let's show the return values next to the frames
        return_values = VGroup()
        
        # Base case return
        ret_0 = MathTex("1").scale(0.8).set_color(GREEN).next_to(frames[4], RIGHT, buff=0.2)
        self.play(Transform(base_result, ret_0))
        self.wait(0.5)
        
        # Step up to fact(1)
        # 1 * 1 = 1
        ret_1_val = MathTex("1 \\times 1 = 1").scale(0.7).set_color(GREEN)
        ret_1_val.next_to(frames[3], RIGHT, buff=0.2)
        
        # Arrow from fact(0) result to fact(1)
        arrow_1 = Arrow(frames[4].get_right(), frames[3].get_right(), buff=0.1, color=YELLOW)
        
        self.play(GrowArrow(arrow_1))
        self.play(Write(ret_1_val))
        self.wait(0.5)
        
        # Step up to fact(2)
        # 2 * 1 = 2
        ret_2_val = MathTex("2 \\times 1 = 2").scale(0.7).set_color(GREEN)
        ret_2_val.next_to(frames[2], RIGHT, buff=0.2)
        
        arrow_2 = Arrow(frames[3].get_right(), frames[2].get_right(), buff=0.1, color=YELLOW)
        
        self.play(GrowArrow(arrow_2))
        self.play(Write(ret_2_val))
        self.wait(0.5)
        
        # Step up to fact(3)
        # 3 * 2 = 6
        ret_3_val = MathTex("3 \\times 2 = 6").scale(0.7).set_color(GREEN)
        ret_3_val.next_to(frames[1], RIGHT, buff=0.2)
        
        arrow_3 = Arrow(frames[2].get_right(), frames[1].get_right(), buff=0.1, color=YELLOW)
        
        self.play(GrowArrow(arrow_3))
        self.play(Write(ret_3_val))
        self.wait(0.5)
        
        # Step up to fact(4)
        # 4 * 6 = 24
        ret_4_val = MathTex("4 \\times 6 = 24").scale(0.7).set_color(GREEN)
        ret_4_val.next_to(frames[0], RIGHT, buff=0.2)
        
        arrow_4 = Arrow(frames[1].get_right(), frames[0].get_right(), buff=0.1, color=YELLOW)
        
        self.play(GrowArrow(arrow_4))
        self.play(Write(ret_4_val))
        self.wait(1)
        
        # Final result highlight
        final_res = MathTex("4! = 24").scale(1.2).set_color(GREEN)
        final_res.next_to(frames[0], DOWN, buff=1)
        
        self.play(Write(final_res))
        self.wait(2)
