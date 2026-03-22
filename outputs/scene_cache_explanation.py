
from manim import *

class Scene_cache_explanation(Scene):
    def construct(self):
        # Title
        title = Text("Why is the website not updating?", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Filing Cabinet (The Cache)
        cabinet_frame = Rectangle(height=3, width=2, color=GRAY_B, fill_opacity=1, fill_color=GRAY_D)
        drawer1 = Rectangle(height=0.8, width=1.8, color=WHITE).move_to(cabinet_frame.get_center() + UP * 0.8)
        drawer2 = Rectangle(height=0.8, width=1.8, color=WHITE).move_to(cabinet_frame.get_center() + DOWN * 0.8)
        handle1 = Line(LEFT*0.2, RIGHT*0.2, color=WHITE).move_to(drawer1.get_center())
        handle2 = Line(LEFT*0.2, RIGHT*0.2, color=WHITE).move_to(drawer2.get_center())
        cabinet = VGroup(cabinet_frame, drawer1, drawer2, handle1, handle2).shift(LEFT * 3)
        cabinet_label = Text("Browser Cache", font_size=24).next_to(cabinet, DOWN)

        # Clock Icon (Yesterday's Data)
        clock_circle = Circle(radius=0.6, color=YELLOW)
        clock_hand_h = Line(clock_circle.get_center(), clock_circle.get_center() + UP * 0.4, color=YELLOW)
        clock_hand_m = Line(clock_circle.get_center(), clock_circle.get_center() + RIGHT * 0.3, color=YELLOW)
        clock_text = Text("Yesterday's Data", font_size=20, color=YELLOW).next_to(clock_circle, UP)
        clock_group = VGroup(clock_circle, clock_hand_h, clock_hand_m, clock_text).shift(RIGHT * 3 + UP * 1.5)

        # Documents
        doc_new = Rectangle(height=1.2, width=0.9, color=BLUE, fill_opacity=0.8).shift(RIGHT * 3 + DOWN * 1.5)
        doc_new_text = Text("New Version", font_size=14).move_to(doc_new)
        
        doc_old = Rectangle(height=1.2, width=0.9, color=GRAY, fill_opacity=0.8).move_to(drawer1.get_center())
        doc_old_text = Text("Old Data", font_size=14, color=BLACK).move_to(doc_old)
        old_doc_group = VGroup(doc_old, doc_old_text)

        # Animation Sequence
        self.play(Create(cabinet), Write(cabinet_label))
        self.play(FadeIn(clock_group))
        self.wait(0.5)

        # Show the new version exists but is ignored
        self.play(FadeIn(doc_new, doc_new_text))
        cross = Cross(VGroup(doc_new, doc_new_text))
        self.play(Create(cross))
        self.wait(0.5)

        # Pulling old document from cabinet
        explanation_text = Text("The browser shows old saved data", font_size=28, color=RED).to_edge(DOWN)
        
        self.play(
            old_doc_group.animate.shift(RIGHT * 3),
            Write(explanation_text),
            run_time=2
        )
        
        # Highlight the cause
        self.play(Indicate(old_doc_group))
        self.play(Indicate(clock_group))
        
        self.wait(2)
