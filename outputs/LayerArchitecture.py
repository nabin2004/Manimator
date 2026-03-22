
from manim import *

class LayerArchitecture(Scene):
    def construct(self):
        layer_sizes = [3, 4, 4, 1]
        layers = VGroup()
        connections = VGroup()

        # Create Nodes
        for i, size in enumerate(layer_sizes):
            layer = VGroup()
            for j in range(size):
                node = Circle(radius=0.25, color=BLUE, fill_opacity=1)
                node.move_to(
                    np.array([
                        i * 2.5 - (len(layer_sizes) - 1) * 1.25,
                        j * 1.2 - (size - 1) * 0.6,
                        0
                    ])
                )
                layer.add(node)
            layers.add(layer)

        # Create Connections (Dense/Fully Connected)
        for i in range(len(layers) - 1):
            current_layer = layers[i]
            next_layer = layers[i+1]
            for node_a in current_layer:
                for node_b in next_layer:
                    line = Line(
                        node_a.get_center(), 
                        node_b.get_center(), 
                        stroke_width=1, 
                        stroke_opacity=0.6,
                        color=WHITE
                    )
                    connections.add(line)

        # Labels
        input_label = Text("Input Layer", font_size=24).next_to(layers[0], UP, buff=0.5)
        hidden_label = Text("Hidden Layers", font_size=24).next_to(VGroup(layers[1], layers[2]), UP, buff=0.5)
        output_label = Text("Output Layer", font_size=24).next_to(layers[3], UP, buff=0.5)
        labels = VGroup(input_label, hidden_label, output_label)

        # Animations
        self.play(LaggedStart(*[Create(layer) for layer in layers], lag_ratio=0.3))
        self.wait(0.5)
        self.play(Create(connections), run_time=3)
        self.play(Write(labels))
        self.wait(2)

        # Highlight the "Fully Connected" nature
        self.play(
            connections.animate.set_stroke(color=YELLOW, opacity=1),
            rate_func=there_and_back,
            run_time=2
        )
        self.wait(2)
