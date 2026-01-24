
from manim import *

class Scene_01(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        question_mark = Tex("?", font_size=120)
        question_mark.set_color(YELLOW)
        question_mark.next_to(title, DOWN, buff=1.5)
        
        self.play(FadeIn(question_mark))
        self.wait(0.5)
        
        definition = Text("A method of solving a problem where", font_size=36)
        definition2 = Text("the solution depends on solutions to", font_size=36)
        definition3 = Text("smaller instances of the same problem.", font_size=36)
        definition_group = VGroup(definition, definition2, definition3).arrange(DOWN, buff=0.4)
        definition_group.next_to(question_mark, DOWN, buff=1.0)
        
        self.play(Write(definition_group))
        self.wait(2)
        
        self.play(FadeOut(question_mark), FadeOut(definition_group))
        
        func_box = Square(side_length=2, color=BLUE, fill_opacity=0.2)
        func_text = Text("Function", font_size=32)
        func_text.move_to(func_box.get_center())
        
        self.play(Create(func_box), Write(func_text))
        
        arrow_down = Arrow(func_box.get_bottom(), func_box.get_bottom() + DOWN * 1.5, buff=0.1)
        arrow_down.set_color(WHITE)
        
        self.play(GrowArrow(arrow_down))
        
        inner_box = Square(side_length=1.2, color=GREEN, fill_opacity=0.2)
        inner_text = Text("Function", font_size=20)
        inner_text.move_to(inner_box.get_center())
        
        inner_group = VGroup(inner_box, inner_text)
        inner_group.next_to(arrow_down, DOWN, buff=0.1)
        
        self.play(Create(inner_box), Write(inner_text))
        
        arrow_loop = CurvedArrow(
            inner_box.get_right() + RIGHT * 0.2, 
            func_box.get_right() + RIGHT * 0.2, 
            angle=-PI/2
        )
        arrow_loop.set_color(YELLOW)
        
        self.play(Create(arrow_loop))
        
        label = Text("Recursion", font_size=36, color=YELLOW)
        label.next_to(arrow_loop, RIGHT, buff=0.2)
        
        self.play(Write(label))
        self.wait(3)
