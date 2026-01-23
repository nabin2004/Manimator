
from manim import *

class Scene_06(Scene):
    def construct(self):
        title = Text("Recursion: Pitfalls & Best Practices", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Warning Section
        warning_group = VGroup()
        warning_title = Text("⚠️ Common Pitfalls", font_size=36, color=YELLOW)
        warning_title.next_to(title, DOWN, buff=0.5)
        
        warning_icon = SVGMobject("warning.svg") if "warning.svg" in [f.name for f in os.scandir(".")] else Circle(color=YELLOW, fill_opacity=0.2).set_fill(YELLOW, opacity=0.2)
        # Fallback if no SVG: create a simple triangle
        if isinstance(warning_icon, Circle):
            warning_icon = Triangle(color=YELLOW, fill_opacity=0.2).set_fill(YELLOW, opacity=0.2).scale(0.5)
        
        warning_icon.next_to(warning_title, LEFT)
        
        warning_text = Text("Infinite Recursion leads to Stack Overflow", font_size=24)
        warning_text.next_to(warning_title, DOWN)
        
        warning_group.add(warning_title, warning_icon, warning_text)
        self.play(FadeIn(warning_group))
        self.wait(1)

        # Stack Overflow Graphic
        stack_title = Text("Stack Overflow", font_size=30, color=RED)
        stack_title.next_to(warning_text, DOWN, buff=0.5)
        
        # Create stack blocks
        stack_blocks = VGroup()
        num_blocks = 8
        for i in range(num_blocks):
            block = Rectangle(width=3, height=0.4, fill_color=BLUE, fill_opacity=0.8, stroke_width=1)
            block.move_to(UP * (2 - i * 0.45))
            stack_blocks.add(block)
        
        # Animate stack growing then crashing
        self.play(Write(stack_title))
        self.play(LaggedStart(*[GrowFromCenter(b) for b in stack_blocks], lag_ratio=0.1))
        self.wait(0.5)
        
        # Crash effect
        crash_text = Text("CRASH!", font_size=40, color=RED)
        crash_text.move_to(stack_blocks.get_center())
        self.play(Indicate(stack_blocks, color=RED, scale_factor=1.1))
        self.play(Write(crash_text))
        self.wait(1)
        
        self.play(FadeOut(warning_group), FadeOut(stack_title), FadeOut(stack_blocks), FadeOut(crash_text))

        # Best Practices Section
        best_practices_title = Text("✅ Best Practices", font_size=36, color=GREEN)
        best_practices_title.to_edge(UP)
        self.play(Transform(title, best_practices_title))
        
        # Checklist items
        checklist_items = VGroup()
        
        item1_text = Text("1. Define a Base Case", font_size=30)
        item1_tick = Checkmark(color=GREEN).scale(0.8)
        item1_tick.next_to(item1_text, LEFT)
        item1 = VGroup(item1_tick, item1_text).arrange(RIGHT, buff=0.3)
        item1.shift(UP * 1.5)
        
        item2_text = Text("2. Progress Toward Base Case", font_size=30)
        item2_tick = Checkmark(color=GREEN).scale(0.8)
        item2_tick.next_to(item2_text, LEFT)
        item2 = VGroup(item2_tick, item2_text).arrange(RIGHT, buff=0.3)
        item2.next_to(item1, DOWN, buff=0.5)
        
        item3_text = Text("3. Use Tail Recursion (if possible)", font_size=30)
        item3_tick = Checkmark(color=GREEN).scale(0.8)
        item3_tick.next_to(item3_text, LEFT)
        item3 = VGroup(item3_tick, item3_text).arrange(RIGHT, buff=0.3)
        item3.next_to(item2, DOWN, buff=0.5)
        
        checklist_items.add(item1, item2, item3)
        
        # Animate checklist
        self.play(FadeIn(item1))
        self.wait(0.5)
        self.play(FadeIn(item2))
        self.wait(0.5)
        self.play(FadeIn(item3))
        self.wait(1)
        
        # Detail explanation for Base Case
        base_case_detail = Text("Always have a condition to stop recursion", font_size=24, color=GRAY)
        base_case_detail.next_to(item1, DOWN)
        self.play(Write(base_case_detail))
        self.wait(0.5)
        
        # Detail explanation for Progress
        progress_detail = Text("Parameters must approach the base case", font_size=24, color=GRAY)
        progress_detail.next_to(item2, DOWN)
        self.play(Write(progress_detail))
        self.wait(0.5)
        
        # Detail explanation for Tail Recursion
        tail_detail = Text("Recursive call is the last operation", font_size=24, color=GRAY)
        tail_detail.next_to(item3, DOWN)
        self.play(Write(tail_detail))
        self.wait(1)
        
        # Final Summary
        summary = Text("Safe Recursion = Base Case + Progress", font_size=32, color=YELLOW)
        summary.move_to(UP * 0.5)
        
        self.play(
            FadeOut(checklist_items),
            FadeOut(base_case_detail),
            FadeOut(progress_detail),
            FadeOut(tail_detail),
            Transform(title, summary)
        )
        
        self.wait(2)
