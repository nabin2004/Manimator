
from manim import *

class Lossandbackpropagation(Scene):
    def construct(self):
        # Create Neural Network Layers
        layers = [3, 4, 4, 1]
        network = VGroup()
        layer_groups = []
        
        for i, num_nodes in enumerate(layers):
            layer = VGroup(*[Circle(radius=0.2, color=WHITE, fill_opacity=1) for _ in range(num_nodes)])
            layer.arrange(DOWN, buff=0.3)
            layer.shift(RIGHT * (i * 2 - 3))
            layer_groups.append(layer)
            network.add(layer)

        connections = VGroup()
        for i in range(len(layer_groups) - 1):
            for node_a in layer_groups[i]:
                for node_b in layer_groups[i+1]:
                    line = Line(node_a.get_right(), node_b.get_left(), stroke_width=1, color=GRAY_C)
                    connections.add(line)

        self.play(Create(network), Create(connections))
        self.wait(0.5)

        # Forward Pass Visualization
        forward_dots = VGroup()
        for i in range(len(layer_groups) - 1):
            for node in layer_groups[i]:
                dot = Dot(node.get_center(), color=YELLOW, radius=0.05)
                forward_dots.add(dot)
        
        self.play(LaggedStart(*[dot.animate.shift(RIGHT*2) for dot in forward_dots], lag_ratio=0.1), run_time=1.5)
        self.remove(forward_dots)

        # Predicted vs Actual
        output_node = layer_groups[-1][0]
        pred_label = Text("Predicted: 0.8", font_size=24).next_to(output_node, RIGHT, buff=0.5).set_color(YELLOW)
        actual_label = Text("Actual: 1.0", font_size=24).next_to(pred_label, DOWN, buff=0.2).set_color(GREEN)
        
        self.play(Write(pred_label), Write(actual_label))
        self.wait(0.5)

        # Loss Calculation
        loss_val = Text("Loss: 0.04", font_size=36, color=RED).to_edge(UP)
        self.play(Write(loss_val))
        self.play(Flash(loss_val, color=RED, flash_radius=0.5))
        self.play(loss_val.animate.scale(1.2), run_time=0.2)
        self.play(loss_val.animate.scale(1/1.2), run_time=0.2)

        # Backpropagation - Arrows moving backward
        back_arrows = VGroup()
        for i in range(len(layer_groups) - 1, 0, -1):
            for node in layer_groups[i]:
                arrow = Arrow(node.get_left(), layer_groups[i-1].get_right(), color=RED, buff=0.1, stroke_width=2)
                back_arrows.add(arrow)

        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in back_arrows[::-1]], lag_ratio=0.05), run_time=2)

        # Weight Updates - Changing thickness and color
        updated_connections = connections.copy()
        self.play(
            *[line.animate.set_stroke(color=BLUE, width=4) for line in updated_connections[::3]],
            *[line.animate.set_stroke(color=ORANGE, width=0.5) for line in updated_connections[1::3]],
            run_time=2
        )
        
        # Feedback Loop Text
        feedback_text = Text("Optimizing Weights via Gradient Descent", font_size=30).to_edge(DOWN)
        self.play(Write(feedback_text))
        self.wait(2)

        # Final cleanup
        self.play(
            FadeOut(back_arrows),
            FadeOut(pred_label),
            FadeOut(actual_label),
            FadeOut(loss_val),
            FadeOut(feedback_text)
        )
        self.wait(1)
