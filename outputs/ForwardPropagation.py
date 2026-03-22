
from manim import *

class Forwardpropagation(Scene):
    def construct(self):
        layers = [3, 4, 4, 1]
        layer_spacing = 3
        node_radius = 0.3
        
        network = VGroup()
        nodes_by_layer = []
        
        for i, num_nodes in enumerate(layers):
            layer_nodes = VGroup()
            for j in range(num_nodes):
                node = Circle(radius=node_radius, color=WHITE, stroke_width=2)
                node.set_fill(BLACK, opacity=1)
                node.move_to(
                    np.array([i * layer_spacing - (len(layers) - 1) * layer_spacing / 2,
                              j * 1.2 - (num_nodes - 1) * 1.2 / 2,
                              0])
                )
                layer_nodes.add(node)
            nodes_by_layer.append(layer_nodes)
            network.add(layer_nodes)

        connections = VGroup()
        connections_by_layer = []
        for i in range(len(layers) - 1):
            layer_conns = VGroup()
            for node_a in nodes_by_layer[i]:
                for node_b in nodes_by_layer[i+1]:
                    line = Line(node_a.get_right(), node_b.get_left(), stroke_width=1, stroke_opacity=0.3)
                    layer_conns.add(line)
            connections_by_layer.append(layer_conns)
            connections.add(layer_conns)

        input_labels = VGroup(*[MathTex(f"x_{i+1}").scale(0.7).next_to(nodes_by_layer[0][i], LEFT) for i in range(3)])
        output_label = MathTex("y = 0.87").scale(0.8).next_to(nodes_by_layer[-1][0], RIGHT).set_color(YELLOW)
        
        matrix_labels = VGroup()
        for i in range(len(layers) - 1):
            label = MathTex(f"W_{i+1}").scale(0.8).move_to(
                (nodes_by_layer[i].get_center() + nodes_by_layer[i+1].get_center()) / 2 + UP * 2.5
            )
            matrix_labels.add(label)

        self.play(Create(network), Create(connections))
        self.play(Write(input_labels))
        self.wait(0.5)

        for i in range(len(layers) - 1):
            self.play(Write(matrix_labels[i]), run_time=0.5)
            
            pulses = []
            for conn in connections_by_layer[i]:
                dot = Dot(radius=0.05, color=YELLOW).move_to(conn.get_start())
                dot.set_glow_factor(1)
                pulses.append(dot)
            
            self.play(
                *[node.animate.set_fill(YELLOW, opacity=0.8) for node in nodes_by_layer[i]],
                run_time=0.3
            )
            
            self.play(
                *[MoveAlongPath(pulse, connections_by_layer[i][idx], rate_func=linear) 
                  for idx, pulse in enumerate(pulses)],
                run_time=1.2
            )
            
            self.remove(*pulses)
            
            if i == len(layers) - 2:
                self.play(
                    nodes_by_layer[i+1][0].animate.set_fill(YELLOW, opacity=1),
                    Write(output_label),
                    run_time=0.5
                )
            else:
                self.play(
                    *[node.animate.set_fill(YELLOW, opacity=0.5) for node in nodes_by_layer[i+1]],
                    run_time=0.3
                )
            
            self.play(
                *[node.animate.set_fill(BLACK, opacity=1) for node in nodes_by_layer[i]],
                run_time=0.2
            )

        self.wait(2)
