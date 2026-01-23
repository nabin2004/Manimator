
from manim import *

class Scene_01(Scene):
    def construct(self):
        title = Text("Recursion in Computer Science", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        problem_box = Square(side_length=2, color=BLUE, fill_opacity=0.2)
        problem_label = Text("Problem", font_size=24).move_to(problem_box)
        problem_group = VGroup(problem_box, problem_label)
        
        subproblem_box = Square(side_length=1, color=GREEN, fill_opacity=0.2)
        subproblem_label = Text("Subproblem", font_size=18).move_to(subproblem_box)
        subproblem_group = VGroup(subproblem_box, subproblem_label)

        problem_group.move_to(LEFT * 2)
        subproblem_group.move_to(RIGHT * 2)

        self.play(Create(problem_box), Write(problem_label))
        self.wait(0.5)
        
        arrow = Arrow(problem_box.get_right(), subproblem_box.get_left(), buff=0.5, color=YELLOW)
        self.play(GrowArrow(arrow))
        
        self.play(Create(subproblem_box), Write(subproblem_label))
        self.wait(2)
