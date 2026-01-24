
from manim import *

class Scene_07(Scene):
    def construct(self):
        title = Text("Recursion: Wrap-up & Real-World Applications", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        applications = [
            "Tree Traversal",
            "Divide and Conquer",
            "Backtracking"
        ]
        
        app_texts = VGroup()
        for i, app in enumerate(applications):
            text = Text(f"• {app}", font_size=36)
            text.shift(RIGHT * 1.5 + UP * 1 - i * DOWN * 0.8)
            app_texts.add(text)
        
        self.play(LaggedStartMap(FadeIn, app_texts, lag_ratio=0.3))
        self.wait(1)

        summary_title = Text("Key Takeaways", font_size=36, color=YELLOW)
        summary_title.next_to(app_texts, DOWN, buff=0.8)
        
        points = [
            "Recursion breaks problems into smaller subproblems",
            "Base case is essential to prevent infinite loops",
            "Call stack manages function execution",
            "Often cleaner than iterative solutions"
        ]
        
        summary_group = VGroup(summary_title)
        for i, point in enumerate(points):
            p = Text(f"• {point}", font_size=28)
            p.next_to(summary_title, DOWN, buff=0.3 + i * 0.4)
            p.align_to(summary_title, LEFT)
            summary_group.add(p)
        
        self.play(Write(summary_title))
        self.play(LaggedStartMap(FadeIn, summary_group[1:], lag_ratio=0.2))
        self.wait(1.5)

        call_to_action = Text("Practice writing recursive functions!", font_size=42, color=GREEN)
        call_to_action.to_edge(DOWN)
        
        self.play(Indicate(call_to_action, scale_factor=1.2))
        self.play(Write(call_to_action))
        self.wait(2)

        self.play(FadeOut(Group(title, app_texts, summary_group, call_to_action)))
