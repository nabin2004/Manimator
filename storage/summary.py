
from manim import *

class Summary(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        checklist_items = [
            "Base Case: The stopping condition",
            "Recursive Step: Reducing the problem size",
            "Call Stack: Managing function calls",
            "Think: Divide and Conquer"
        ]

        checklist = VGroup()
        for i, item_text in enumerate(checklist_items):
            if i == 3:
                # Make the final item distinct
                text = Text(item_text, font_size=36, color=GREEN)
            else:
                text = Text(item_text, font_size=36)
            
            # Create a checkbox
            box = Square(side_length=0.5, color=WHITE, stroke_width=2)
            check = VGroup(
                Line(box.get_corner(UL) + UR * 0.2, box.get_center() + DR * 0.1, color=GREEN, stroke_width=4),
                Line(box.get_center() + DR * 0.1, box.get_corner(DR) + UL * 0.2, color=GREEN, stroke_width=4)
            )
            
            item = VGroup(box, check, text)
            item.arrange(RIGHT, buff=0.5)
            item.move_to(UP * (1.5 - i * 1.2))
            checklist.add(item)

        # Animate checklist items
        for item in checklist:
            self.play(
                Create(item[0]), 
                Create(item[1]), 
                Write(item[2]), 
                run_time=0.8
            )
            self.wait(0.2)

        self.wait(1)

        # Transition to Credits/End Screen
        self.play(
            FadeOut(title),
            FadeOut(checklist),
            run_time=1
        )

        # Credits/End Screen
        end_text = Text("Credits", font_size=40, color=BLUE).to_edge(UP)
        credits = VGroup(
            Text("Created with Manim", font_size=32),
            Text("Reinforce Learning Objectives", font_size=32, color=YELLOW)
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        self.play(Write(end_text))
        self.play(FadeIn(credits, shift=UP))
        self.wait(2)

        # Final fade out
        self.play(FadeOut(end_text), FadeOut(credits))
        self.wait(0.5)
