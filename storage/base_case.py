
from manim import *

class Base_case(Scene):
    def construct(self):
        title = Text("The Base Case: Stopping Recursion", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Diagram of recursive function
        diagram_group = VGroup()
        boxes = VGroup()
        labels = VGroup()
        
        # Create stacked boxes to represent recursion stack
        for i in range(4):
            box = RoundedRectangle(height=1.5, width=4, corner_radius=0.2)
            box.set_fill(BLUE, opacity=0.2)
            box.set_stroke(BLUE, width=2)
            box.shift(DOWN * (i * 1.8))
            boxes.add(box)
            
            label = Text(f"call({i+1})", font_size=24)
            label.move_to(box.get_center())
            labels.add(label)
            diagram_group.add(box, label)

        # Position the diagram
        diagram_group.shift(LEFT * 3.5)
        self.play(Create(boxes), Write(labels))
        self.wait(1)

        # Highlight base case condition
        base_case_box = RoundedRectangle(height=1.5, width=4, corner_radius=0.2)
        base_case_box.set_fill(GREEN, opacity=0.4)
        base_case_box.set_stroke(GREEN, width=3)
        base_case_box.next_to(boxes[-1], DOWN, buff=0.2)
        
        base_case_text = Text("Base Case: n == 0", font_size=24, color=GREEN)
        base_case_text.move_to(base_case_box.get_center())
        
        arrow = Arrow(boxes[-1].get_bottom(), base_case_box.get_top(), buff=0.1, color=GREEN)
        
        self.play(
            Create(base_case_box),
            Write(base_case_text),
            Create(arrow)
        )
        self.wait(1)

        # Countdown animation
        countdown_group = VGroup()
        countdown_title = Text("Countdown Example", font_size=32)
        countdown_title.next_to(diagram_group, RIGHT, buff=1)
        countdown_title.shift(UP * 2)
        self.play(Write(countdown_title))
        
        countdown_num = Text("5", font_size=72, color=YELLOW)
        countdown_num.next_to(countdown_title, DOWN, buff=0.5)
        self.play(Write(countdown_num))
        self.wait(0.5)

        # Animate countdown from 5 to 0
        for i in range(5, -1, -1):
            new_num = Text(str(i), font_size=72, color=YELLOW)
            new_num.move_to(countdown_num.get_center())
            
            if i == 0:
                # Highlight stopping at 0
                self.play(
                    Transform(countdown_num, new_num),
                    countdown_num.animate.set_color(GREEN).scale(1.2)
                )
                stop_text = Text("STOPPED", font_size=36, color=GREEN)
                stop_text.next_to(countdown_num, DOWN, buff=0.3)
                self.play(Write(stop_text))
            else:
                self.play(Transform(countdown_num, new_num))
            self.wait(0.3)

        self.wait(1)

        # Warning about infinite recursion
        warning_text = Text("Without a base case:", font_size=36, color=RED)
        warning_text.next_to(countdown_title, DOWN, buff=2)
        
        infinite_text = Text("Infinite Recursion", font_size=48, color=RED)
        infinite_text.next_to(warning_text, DOWN, buff=0.3)
        
        stack_text = Text("(Stack Overflow)", font_size=32, color=ORANGE)
        stack_text.next_to(infinite_text, DOWN, buff=0.2)
        
        self.play(Write(warning_text))
        self.wait(0.5)
        self.play(Write(infinite_text))
        self.wait(0.5)
        self.play(Write(stack_text))
        self.wait(2)

        # Final emphasis
        conclusion = Text("Always define a base case!", font_size=40, color=GREEN)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
