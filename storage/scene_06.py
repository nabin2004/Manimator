
from manim import *

class Scene_06(Scene):
    def construct(self):
        title = Text("Key Takeaways", font_size=48, color=YELLOW).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        checklist_items = [
            "Defined Base Case",
            "Recursive Step",
            "Call Stack Management"
        ]

        checklist_group = VGroup()
        for i, item_text in enumerate(checklist_items):
            text = Text(f"✓ {item_text}", font_size=36, color=GREEN)
            text.shift(RIGHT * 1.5 + DOWN * (i + 1) * 0.8)
            checklist_group.add(text)

        self.play(LaggedStart(*[Write(item) for item in checklist_group], lag_ratio=0.3))
        self.wait(1)

        advice_text = Text("Use recursion for tree structures", font_size=32, color=BLUE_C)
        advice_text2 = Text("and divide-and-conquer algorithms", font_size=32, color=BLUE_C)
        advice_text.next_to(checklist_group, DOWN, buff=1.0)
        advice_text2.next_to(advice_text, DOWN, buff=0.2)

        self.play(Write(advice_text), Write(advice_text2))
        self.wait(1)

        closing_graphic = VGroup()
        circle = Circle(radius=0.5, color=PURPLE, fill_opacity=0.2)
        line1 = Line(UP * 0.3, DOWN * 0.3, color=YELLOW)
        line2 = Line(LEFT * 0.3, RIGHT * 0.3, color=YELLOW)
        closing_graphic.add(circle, line1, line2)
        closing_graphic.scale(1.5)
        closing_graphic.to_edge(DOWN, buff=0.5)

        self.play(Create(closing_graphic))
        self.play(closing_graphic.animate.scale(1.2), run_time=0.5)
        self.play(closing_graphic.animate.scale(1/1.2), run_time=0.5)
        
        final_text = Text("Master the Recursion!", font_size=40, color=GOLD).next_to(closing_graphic, UP, buff=0.5)
        self.play(Write(final_text))
        self.wait(2)
