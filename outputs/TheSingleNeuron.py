
from manim import *

class Thesingleneuron(Scene):
    def construct(self):
        # 1. Create the main node
        node_radius = 2.5
        node = Circle(radius=node_radius, color=WHITE, stroke_width=4)
        node.set_fill(BLUE_E, opacity=0.2)
        
        # 2. Internal components (Summation and Bias)
        summation = MathTex(r"\sum w_i x_i + b", font_size=48)
        summation.move_to(node.get_center())
        
        # 3. Incoming arrows and labels
        inputs = []
        arrows = []
        labels = []
        
        positions = [UP + LEFT*4, LEFT*4, DOWN + LEFT*4]
        weight_texts = [r"w_1", r"w_2", r"w_n"]
        input_texts = [r"x_1", r"x_2", r"x_n"]
        
        for i, pos in enumerate(positions):
            start_point = pos
            end_point = node.point_at_angle(PI + (PI/6 if i==0 else -PI/6 if i==2 else 0))
            
            arrow = Arrow(start_point, end_point, buff=0.1, color=GRAY)
            label = MathTex(weight_texts[i], font_size=36).next_to(arrow, UP, buff=0.1)
            input_val = MathTex(input_texts[i], font_size=36).next_to(start_point, LEFT)
            
            arrows.append(arrow)
            labels.append(label)
            inputs.append(input_val)

        # 4. Activation Function (ReLU) at the exit
        relu_axes = Axes(
            x_range=[-1, 1],
            y_range=[-0.2, 1],
            x_length=1.5,
            y_length=1.5,
            axis_config={"include_tip": False, "stroke_width": 2}
        ).move_to(node.get_right() + RIGHT * 0.5)
        
        relu_graph = relu_axes.plot(
            lambda x: max(0, x),
            x_range=[-1, 1],
            use_smoothing=False,
            color=YELLOW
        )
        
        relu_label = MathTex(r"\sigma", font_size=36, color=YELLOW).next_to(relu_axes, UP, buff=0.1)
        
        # 5. Output arrow
        output_arrow = Arrow(node.get_right(), node.get_right() + RIGHT * 3, color=WHITE)
        output_label = MathTex(r"a = \sigma(\sum w_i x_i + b)", font_size=40).next_to(output_arrow, RIGHT)

        # Animations
        self.play(Create(node))
        self.wait(0.5)
        
        self.play(
            *[Create(a) for a in arrows],
            *[Write(i) for i in inputs],
            *[Write(l) for l in labels]
        )
        self.wait(0.5)
        
        self.play(Write(summation))
        self.wait(1)
        
        self.play(
            Create(relu_axes),
            Create(relu_graph),
            Write(relu_label)
        )
        self.wait(0.5)
        
        self.play(
            GrowArrow(output_arrow),
            Write(output_label)
        )
        self.wait(2)
