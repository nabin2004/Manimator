
from manim import *

class Scene_02(Scene):
    def construct(self):
        # Title
        title = Text("Recursive Function Structure", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Code snippet
        code_str = "def factorial(n):\n    if n <= 1:\n        return 1\n    else:\n        return n * factorial(n-1)"
        code = Code(code=code_str, language="python", font="Monospace", background="rectangle", background_stroke_color=WHITE, background_stroke_width=1, background_fill_color=BLACK, insert_line_no=False, style="monokai")
        code.scale(0.8)
        code.shift(DOWN * 0.5)
        
        self.play(Write(code))
        self.wait(1)

        # Highlight Base Case
        base_case_box = SurroundingRectangle(code.code[1:3], color=YELLOW, buff=0.15)
        base_case_label = Text("Base Case (Stopping Condition)", color=YELLOW, font_size=28)
        base_case_label.next_to(base_case_box, DOWN, buff=0.3)
        
        self.play(Create(base_case_box))
        self.play(Write(base_case_label))
        self.wait(2)
        
        self.play(FadeOut(base_case_box), FadeOut(base_case_label))

        # Highlight Recursive Step
        recursive_box = SurroundingRectangle(code.code[3:5], color=GREEN, buff=0.15)
        recursive_label = Text("Recursive Step (Reduces Problem Size)", color=GREEN, font_size=28)
        recursive_label.next_to(recursive_box, DOWN, buff=0.3)
        
        self.play(Create(recursive_box))
        self.play(Write(recursive_label))
        self.wait(2)

        # Arrow pointing to the recursive call specifically
        # code.code[4] is the line "        return n * factorial(n-1)"
        # We want to highlight the specific text "factorial(n-1)"
        # Since Code object breaks lines into VGroup of characters/words, we locate the substring.
        # Note: Accessing specific words in Code object depends on Manim version. 
        # A robust way is to create a separate highlight for the specific function call text.
        
        # Extract the specific part visually by creating a copy or overlay
        # Since exact sub-indexing in Code object is complex, we will highlight the whole line 
        # and then emphasize the specific call with a brace or arrow.
        
        call_text = Text("factorial(n-1)", font_size=24, color=WHITE)
        # Position approximation based on the code layout
        call_text.move_to(code.code[4]).shift(RIGHT * 1.5) 
        
        arrow = Arrow(call_text.get_left(), code.code[4].get_right() + RIGHT*0.5, buff=0.1, color=GREEN)
        
        self.play(GrowArrow(arrow), Write(call_text))
        self.wait(2)

        # Cleanup
        self.play(FadeOut(Group(title, code, recursive_box, recursive_label, arrow, call_text)))
