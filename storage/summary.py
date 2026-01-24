
from manim import *

class Summary(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        checklist_items = [
            "Base Case",
            "Recursive Step",
            "Call Stack",
            "Divide and Conquer strategy"
        ]

        checklist_group = VGroup()
        for i, item in enumerate(checklist_items):
            if item == "Divide and Conquer strategy":
                text = Text(item, font_size=32, color=TEAL)
            else:
                text = Text(item, font_size=32)
            
            if i < 3:
                box = Square(side_length=0.4, color=WHITE, stroke_width=2)
                box.next_to(text, LEFT, buff=0.5)
                item_group = VGroup(box, text)
            else:
                # Special formatting for the strategy text
                text.shift(DOWN * 0.5)
                item_group = VGroup(text)

            checklist_group.add(item_group)

        checklist_group.arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        checklist_group.next_to(title, DOWN, buff=1)

        self.play(LaggedStartMap(FadeIn, checklist_group, lag_ratio=0.3))
        self.wait(1)

        # Highlight items one by one
        for i in range(3):
            box = checklist_group[i][0]
            self.play(box.animate.set_fill(GREEN, opacity=0.5), run_time=0.5)
            self.wait(0.2)
            self.play(box.animate.set_fill(opacity=0), run_time=0.5)
        
        # Highlight strategy
        strategy_text = checklist_group[3][0]
        self.play(Indicate(strategy_text, color=TEAL))
        self.wait(1)

        # Transition to closing visual
        self.play(
            FadeOut(title),
            FadeOut(checklist_group),
            run_time=1
        )

        # Create closing visual: Function calling itself in a loop
        func_name = Text("factorial(n)", font_size=36, color=BLUE)
        func_name.move_to(UP * 1)
        
        arrow_down = Arrow(UP, DOWN, color=WHITE).next_to(func_name, DOWN)
        
        recursive_call = Text("factorial(n-1)", font_size=32, color=YELLOW)
        recursive_call.next_to(arrow_down, DOWN)
        
        arrow_loop = CurvedArrow(
            recursive_call.get_right() + RIGHT * 0.5,
            func_name.get_right() + RIGHT * 0.5,
            angle=-PI/2,
            color=GREEN
        )
        
        loop_text = Text("Loop", font_size=24, color=GREEN).next_to(arrow_loop, RIGHT, buff=0.2)

        self.play(Write(func_name))
        self.play(Create(arrow_down))
        self.play(Write(recursive_call))
        self.play(Create(arrow_loop))
        self.play(Write(loop_text))
        
        self.wait(2)

        # Final message
        conclusion = Text("Recursion mastered!", font_size=40, color=GOLD)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
