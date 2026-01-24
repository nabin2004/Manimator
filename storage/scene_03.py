
from manim import *

class Scene_03(Scene):
    def construct(self):
        # Title
        title = Text("Call Stack Mechanism", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Code snippet area (top right)
        code_text = Text("def func1():\n    func2()\n\ndef func2():\n    return", font_size=24)
        code_text.scale(0.8)
        code_text.to_corner(UR)
        code_box = SurroundingRectangle(code_text, color=BLUE, buff=0.2)
        code_group = VGroup(code_text, code_box)
        
        self.play(Create(code_box), Write(code_text))
        self.wait(1)

        # Stack area (left side)
        stack_label = Text("Call Stack", font_size=30)
        stack_label.move_to(LEFT * 4.5 + UP * 2)
        self.play(Write(stack_label))

        # Initial empty stack indicator
        empty_stack = Text("(Empty)", font_size=24, color=GRAY)
        empty_stack.move_to(LEFT * 4.5)
        self.play(FadeIn(empty_stack))
        self.wait(1)

        # Define frame creation function
        def create_frame(label_text, color):
            frame = Rectangle(width=3, height=1, color=color, fill_opacity=0.2, fill_color=color)
            text = Text(label_text, font_size=24)
            text.move_to(frame.get_center())
            return VGroup(frame, text)

        # Animation sequence
        
        # 1. Push Frame 1
        self.play(FadeOut(empty_stack))
        
        arrow_down_1 = Arrow(start=LEFT * 4.5 + UP * 1, end=LEFT * 4.5 + UP * 0.2, color=YELLOW)
        self.play(GrowArrow(arrow_down_1))
        self.wait(0.5)

        frame1 = create_frame("Frame 1", RED)
        frame1.move_to(LEFT * 4.5 + UP * 0.5)
        
        self.play(Transform(arrow_down_1, frame1))
        self.wait(1)

        # 2. Push Frame 2
        arrow_down_2 = Arrow(start=LEFT * 4.5 + UP * 0.5, end=LEFT * 4.5 + DOWN * 0.3, color=YELLOW)
        self.play(GrowArrow(arrow_down_2))
        self.wait(0.5)

        frame2 = create_frame("Frame 2", GREEN)
        frame2.move_to(LEFT * 4.5 + DOWN * 0.5)
        
        self.play(Transform(arrow_down_2, frame2))
        self.wait(1)

        # Highlight code execution
        self.play(code_text[0:8].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(code_text[0:8].animate.set_color(WHITE))
        self.play(code_text[9:16].animate.set_color(YELLOW))
        self.wait(0.5)
        self.play(code_text[9:16].animate.set_color(WHITE))
        self.wait(1)

        # 3. Pop Frame 2
        arrow_up_1 = Arrow(start=LEFT * 4.5 + DOWN * 0.5, end=LEFT * 4.5 + UP * 0.3, color=ORANGE)
        self.play(GrowArrow(arrow_up_1))
        self.wait(0.5)

        self.play(FadeOut(frame2), FadeOut(arrow_up_1))
        self.wait(0.5)

        # 4. Pop Frame 1
        arrow_up_2 = Arrow(start=LEFT * 4.5 + UP * 0.5, end=LEFT * 4.5 + UP * 1.3, color=ORANGE)
        self.play(GrowArrow(arrow_up_2))
        self.wait(0.5)

        self.play(FadeOut(frame1), FadeOut(arrow_up_2))
        self.wait(0.5)

        # Show stack is empty again
        self.play(FadeIn(empty_stack))
        self.wait(1)

        # Final message
        final_text = Text("Stack manages function execution order", font_size=32, color=BLUE)
        final_text.move_to(DOWN * 2)
        self.play(Write(final_text))
        self.wait(2)
