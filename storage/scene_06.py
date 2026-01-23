
from manim import *

class Scene_06(Scene):
    def construct(self):
        title = Text("Recursion: Pitfalls & Best Practices", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Section 1: Warning - Missing Base Case
        warning_group = VGroup()
        warning_title = Text("Pitfall: Missing Base Case", font_size=36, color=YELLOW)
        warning_title.next_to(title, DOWN, buff=0.5)
        
        # Warning Icon
        exclaim = Triangle(color=YELLOW, fill_opacity=0.2, fill_color=YELLOW)
        exclaim.scale(0.8)
        dot = Dot(color=YELLOW).scale(1.5)
        dot.move_to(exclaim.get_center() + UP*0.1)
        icon = VGroup(exclaim, dot)
        icon.next_to(warning_title, LEFT)
        
        # Infinite Recursion Diagram
        arrow1 = Arrow(LEFT, RIGHT, color=RED)
        func1 = Rectangle(height=0.8, width=2, color=WHITE).set_fill(BLUE, opacity=0.5)
        txt1 = Text("f(n)", font_size=24).move_to(func1)
        group1 = VGroup(func1, txt1)
        
        arrow2 = Arrow(LEFT, RIGHT, color=RED)
        func2 = Rectangle(height=0.8, width=2, color=WHITE).set_fill(BLUE, opacity=0.5)
        txt2 = Text("f(n)", font_size=24).move_to(func2)
        group2 = VGroup(func2, txt2)
        
        arrow3 = Arrow(LEFT, RIGHT, color=RED)
        func3 = Rectangle(height=0.8, width=2, color=WHITE).set_fill(BLUE, opacity=0.5)
        txt3 = Text("f(n)", font_size=24).move_to(func3)
        group3 = VGroup(func3, txt3)
        
        stack = VGroup(group1, group2, group3).arrange(DOWN, buff=0.2)
        stack.next_to(warning_title, DOWN, buff=0.5).shift(RIGHT*2)
        
        arrows = VGroup(arrow1, arrow2, arrow3)
        arrow1.next_to(group1, DOWN)
        arrow2.next_to(group2, DOWN)
        arrow3.next_to(group3, DOWN)
        
        infinite_sign = Text("∞", font_size=60, color=RED).next_to(stack, RIGHT)
        
        warning_group.add(warning_title, icon, stack, arrows, infinite_sign)
        
        self.play(FadeIn(warning_title), FadeIn(icon))
        self.play(Create(stack), Create(arrows))
        self.play(Write(infinite_sign))
        self.wait(2)
        
        # Stack Overflow Effect
        self.play(
            stack.animate.scale(1.2).set_color(RED),
            arrows.animate.set_color(RED),
            run_time=0.5
        )
        self.play(
            stack.animate.scale(0.8).set_color(WHITE),
            arrows.animate.set_color(RED),
            run_time=0.5
        )
        overflow_text = Text("Stack Overflow!", color=RED, font_size=36)
        overflow_text.move_to(stack.get_center())
        self.play(Write(overflow_text))
        self.wait(2)
        
        self.play(FadeOut(warning_group), FadeOut(overflow_text))

        # Section 2: Best Practices Checklist
        checklist_title = Text("Best Practices", font_size=36, color=GREEN)
        checklist_title.next_to(title, DOWN, buff=0.5)
        self.play(Write(checklist_title))
        
        items = VGroup()
        item1 = Text("1. Define Base Case", font_size=30)
        item2 = Text("2. Ensure Progress (Move towards base)", font_size=30)
        item3 = Text("3. Consider Tail Recursion", font_size=30)
        
        items.add(item1, item2, item3)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        items.next_to(checklist_title, DOWN, buff=0.5).shift(LEFT*1.5)
        
        checks = VGroup()
        for item in items:
            check = Checkmark(color=GREEN).scale(0.6)
            check.next_to(item, LEFT, buff=0.2)
            checks.add(check)
            
        self.play(FadeIn(items), FadeIn(checks))
        self.wait(2)
        
        # Visualizing Tail Recursion Optimization
        tail_title = Text("Tail Recursion Optimization", font_size=28, color=TEAL)
        tail_title.next_to(items, DOWN, buff=1)
        self.play(Write(tail_title))
        
        # Before Optimization
        before_label = Text("Standard Recursion", font_size=20).next_to(tail_title, DOWN).shift(LEFT*2)
        stack_before = VGroup()
        for i in range(3):
            rect = Rectangle(width=3, height=0.5, color=BLUE).set_fill(BLUE, opacity=0.3)
            txt = Text(f"Call {i+1}", font_size=18).move_to(rect)
            stack_before.add(VGroup(rect, txt))
        stack_before.arrange(DOWN, buff=0.1)
        stack_before.next_to(before_label, DOWN)
        
        # After Optimization (Tail Call)
        after_label = Text("Tail Recursive (O(1) space)", font_size=20).next_to(tail_title, DOWN).shift(RIGHT*2)
        single_rect = Rectangle(width=3, height=0.5, color=GREEN).set_fill(GREEN, opacity=0.3)
        single_txt = Text("Current State", font_size=18).move_to(single_rect)
        stack_after = VGroup(single_rect, single_txt)
        stack_after.next_to(after_label, DOWN)
        
        self.play(FadeIn(before_label), Create(stack_before))
        self.play(FadeIn(after_label), Create(stack_after))
        
        # Transform visualization
        self.play(
            stack_before.animate.scale(0.5).set_opacity(0.3),
            stack_after.animate.scale(1.2).set_color(YELLOW),
            run_time=1.5
        )
        self.play(
            stack_after.animate.scale(1/1.2).set_color(GREEN),
            run_time=0.5
        )
        
        self.wait(2)
        
        # Final Summary
        summary = Text("Correctness + Termination + Limits", font_size=32, color=YELLOW)
        summary.move_to(ORIGIN)
        self.play(FadeOut(VGroup(title, checklist_title, items, checks, tail_title, before_label, stack_before, after_label, stack_after)))
        self.play(Write(summary))
        self.wait(2)
