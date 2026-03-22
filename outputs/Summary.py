
from manim import *

class Summary(Scene):
    def construct(self):
        title = Text("Divide & Conquer Mindset", color=BLUE).scale(0.8).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        checklist_title = Text("Checklist:", color=YELLOW).scale(0.6).next_to(title, DOWN, buff=0.5).align_to(title, LEFT)
        item1 = Text("1. Base Case?", color=WHITE).scale(0.5)
        item2 = Text("2. Smaller Subproblem?", color=WHITE).scale(0.5)
        
        checklist = VGroup(checklist_title, item1, item2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=1.5)
        
        self.play(FadeIn(checklist_title))
        self.play(Write(item1))
        self.play(Write(item2))
        self.wait(1)

        doll_group = VGroup()
        colors = [RED_E, RED_D, RED_C, RED_B]
        sizes = [1.5, 1.1, 0.7, 0.4]
        
        for color, size in zip(colors, sizes):
            body = Intersection(
                Rectangle(width=size, height=size*1.2, fill_opacity=1, color=color),
                Circle(radius=size/2, fill_opacity=1, color=color).shift(UP * size * 0.4),
                fill_opacity=1, color=color
            )
            doll_group.add(body)

        doll_group.arrange(RIGHT, buff=0.2).shift(RIGHT * 3)
        
        self.play(Create(doll_group))
        self.wait(0.5)

        center_pos = doll_group[0].get_center()
        closing_animations = []
        for i in range(len(doll_group)-1, 0, -1):
            closing_animations.append(
                doll_group[i].animate.move_to(center_pos).set_opacity(0)
            )
        
        self.play(Succession(*closing_animations, run_time=2))
        self.play(doll_group[0].animate.scale(1.2).set_color(GOLD))
        
        doll_label = Text("Recursive Structure", color=GOLD).scale(0.4).next_to(doll_group[0], DOWN)
        self.play(Write(doll_label))
        self.wait(1)

        summary_box = SurroundingRectangle(VGroup(checklist, doll_group), color=WHITE, buff=0.5)
        final_text = Text("Solve small. Combine all.", slant=ITALIC).scale(0.7).to_edge(DOWN, buff=1)
        
        self.play(Create(summary_box))
        self.play(FadeIn(final_text, shift=UP))
        self.play(Indicate(final_text, color=BLUE))
        
        self.wait(3)
