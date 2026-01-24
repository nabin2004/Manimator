
from manim import *

class Scene_04(Scene):
    def construct(self):
        # Title
        title = Text("Factorial Recursion", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Formula
        formula = MathTex("n! = n \\times (n-1)!")
        formula.next_to(title, DOWN, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # Base case text
        base_case = MathTex("\\text{Base Case: } 0! = 1")
        base_case.next_to(formula, DOWN, buff=0.5)
        self.play(Write(base_case))
        self.wait(1)

        # Shift elements up to make room for stack
        self.play(
            title.animate.shift(UP * 1.5),
            formula.animate.shift(UP * 1.5),
            base_case.animate.shift(UP * 1.5)
        )

        # Stack setup
        stack_label = Text("Call Stack", font_size=24)
        stack_label.to_edge(LEFT).shift(RIGHT * 1.5)
        self.play(Write(stack_label))

        # Function to create a stack frame
        def create_frame(n_val, color=BLUE):
            frame = Rectangle(width=5, height=0.8, color=color, fill_opacity=0.2)
            text = MathTex(f"factorial({n_val})").scale(0.8)
            text.move_to(frame.get_center())
            group = VGroup(frame, text)
            return group

        # Initial frame for n=5
        current_n = 5
        frames = VGroup()
        frame_5 = create_frame(5)
        frames.add(frame_5)
        frame_5.move_to(stack_label.get_right() + RIGHT * 2 + UP * 2)
        
        self.play(FadeIn(frame_5))
        self.wait(0.5)

        # Recursive steps
        # Step 1: n=5 calls n=4
        current_n = 4
        frame_4 = create_frame(4)
        frames.add(frame_4)
        frame_4.next_to(frame_5, DOWN, buff=0.2)
        
        self.play(
            frame_5.animate.set_fill(opacity=0.05), # Dim previous
            FadeIn(frame_4)
        )
        self.wait(0.5)

        # Step 2: n=4 calls n=3
        current_n = 3
        frame_3 = create_frame(3)
        frames.add(frame_3)
        frame_3.next_to(frame_4, DOWN, buff=0.2)
        
        self.play(
            frame_4.animate.set_fill(opacity=0.05),
            FadeIn(frame_3)
        )
        self.wait(0.5)

        # Step 3: n=3 calls n=2
        current_n = 2
        frame_2 = create_frame(2)
        frames.add(frame_2)
        frame_2.next_to(frame_3, DOWN, buff=0.2)
        
        self.play(
            frame_3.animate.set_fill(opacity=0.05),
            FadeIn(frame_2)
        )
        self.wait(0.5)

        # Step 4: n=2 calls n=1
        current_n = 1
        frame_1 = create_frame(1)
        frames.add(frame_1)
        frame_1.next_to(frame_2, DOWN, buff=0.2)
        
        self.play(
            frame_2.animate.set_fill(opacity=0.05),
            FadeIn(frame_1)
        )
        self.wait(0.5)

        # Step 5: n=1 calls n=0 (Base Case)
        current_n = 0
        frame_0 = create_frame(0, color=YELLOW) # Highlight base case
        frames.add(frame_0)
        frame_0.next_to(frame_1, DOWN, buff=0.2)
        
        self.play(
            frame_1.animate.set_fill(opacity=0.05),
            FadeIn(frame_0)
        )
        
        # Indicate base case reached
        base_indicator = Text("Base Case Reached!", color=YELLOW, font_size=24)
        base_indicator.next_to(frame_0, DOWN, buff=0.5)
        self.play(Write(base_indicator))
        self.wait(1)

        # Unwinding the stack
        # Return 1 to n=1
        self.play(FadeOut(base_indicator))
        
        # n=0 disappears, n=1 lights up
        return_val_1 = MathTex("= 1", color=GREEN).next_to(frame_1, RIGHT)
        self.play(
            FadeOut(frame_0),
            frame_1.animate.set_fill(opacity=0.2, color=GREEN),
            Write(return_val_1)
        )
        self.wait(0.5)

        # n=1 disappears, n=2 lights up
        return_val_2 = MathTex("= 2 \\times 1", color=GREEN).next_to(frame_2, RIGHT)
        self.play(
            FadeOut(frame_1),
            FadeOut(return_val_1),
            frame_2.animate.set_fill(opacity=0.2, color=GREEN),
            Write(return_val_2)
        )
        self.wait(0.5)

        # n=2 disappears, n=3 lights up
        return_val_3 = MathTex("= 3 \\times 2", color=GREEN).next_to(frame_3, RIGHT)
        self.play(
            FadeOut(frame_2),
            FadeOut(return_val_2),
            frame_3.animate.set_fill(opacity=0.2, color=GREEN),
            Write(return_val_3)
        )
        self.wait(0.5)

        # n=3 disappears, n=4 lights up
        return_val_4 = MathTex("= 4 \\times 6", color=GREEN).next_to(frame_4, RIGHT)
        self.play(
            FadeOut(frame_3),
            FadeOut(return_val_3),
            frame_4.animate.set_fill(opacity=0.2, color=GREEN),
            Write(return_val_4)
        )
        self.wait(0.5)

        # n=4 disappears, n=5 lights up
        return_val_5 = MathTex("= 5 \\times 24", color=GREEN).next_to(frame_5, RIGHT)
        self.play(
            FadeOut(frame_4),
            FadeOut(return_val_4),
            frame_5.animate.set_fill(opacity=0.2, color=GREEN),
            Write(return_val_5)
        )
        self.wait(0.5)

        # Final result
        final_result = MathTex("5! = 120", font_size=48, color=GREEN)
        final_result.move_to(stack_label.get_right() + RIGHT * 3)
        
        self.play(
            FadeOut(frames),
            FadeOut(return_val_5),
            Transform(title, final_result)
        )
        
        self.wait(2)
