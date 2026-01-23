
from manim import *

class FourScene(Scene):
    def construct(self):
        title = Text("Call Stack in Recursion", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        stack_group = VGroup()
        stack_group.next_to(title, DOWN, buff=1.0)
        
        def create_frame(label, color):
            rect = RoundedRectangle(width=4, height=0.8, corner_radius=0.1, color=color, fill_opacity=0.2, stroke_width=2)
            text = Text(label, font_size=24).move_to(rect)
            return VGroup(rect, text)

        colors = [BLUE, GREEN, YELLOW, RED, PURPLE]
        
        # Call fact(3)
        frame3 = create_frame("fact(3)", colors[0])
        frame3.move_to(stack_group.get_bottom() + DOWN * 0.9 if stack_group else DOWN * 2)
        self.play(FadeIn(frame3))
        stack_group.add(frame3)
        self.wait(0.5)

        # Call fact(2)
        frame2 = create_frame("fact(2)", colors[1])
        frame2.move_to(stack_group.get_bottom() + DOWN * 0.9)
        self.play(FadeIn(frame2))
        stack_group.add(frame2)
        self.wait(0.5)

        # Call fact(1)
        frame1 = create_frame("fact(1)", colors[2])
        frame1.move_to(stack_group.get_bottom() + DOWN * 0.9)
        self.play(FadeIn(frame1))
        stack_group.add(frame1)
        self.wait(0.5)

        # Call fact(0) - Base case
        frame0 = create_frame("fact(0)", colors[3])
        frame0.move_to(stack_group.get_bottom() + DOWN * 0.9)
        self.play(FadeIn(frame0))
        stack_group.add(frame0)
        self.wait(0.5)

        # Return 1 from fact(0)
        return_val = Text("return 1", font_size=20, color=WHITE)
        return_val.next_to(frame0, RIGHT, buff=0.2)
        self.play(Write(return_val))
        self.wait(0.2)
        
        self.play(FadeOut(frame0), FadeOut(return_val))
        stack_group.remove(frame0)
        self.wait(0.5)

        # Return 1 to fact(1)
        return_val1 = Text("return 1", font_size=20, color=WHITE)
        return_val1.next_to(frame1, RIGHT, buff=0.2)
        self.play(Write(return_val1))
        self.wait(0.2)
        
        self.play(FadeOut(frame1), FadeOut(return_val1))
        stack_group.remove(frame1)
        self.wait(0.5)

        # Return 2 to fact(2)
        return_val2 = Text("return 2", font_size=20, color=WHITE)
        return_val2.next_to(frame2, RIGHT, buff=0.2)
        self.play(Write(return_val2))
        self.wait(0.2)
        
        self.play(FadeOut(frame2), FadeOut(return_val2))
        stack_group.remove(frame2)
        self.wait(0.5)

        # Return 6 to fact(3)
        return_val3 = Text("return 6", font_size=20, color=WHITE)
        return_val3.next_to(frame3, RIGHT, buff=0.2)
        self.play(Write(return_val3))
        self.wait(0.2)
        
        self.play(FadeOut(frame3), FadeOut(return_val3))
        stack_group.remove(frame3)
        self.wait(0.5)

        # Final explanation
        explanation = Text("Stack grows down, returns shrink up", font_size=32)
        explanation.move_to(ORIGIN)
        self.play(Write(explanation))
        self.wait(2)
