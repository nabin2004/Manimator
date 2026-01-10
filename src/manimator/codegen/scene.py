# src/manimator/codegen/scene.py
from ..planner.schemas import ScenePlan

def generate_manim_code(scene: ScenePlan) -> str:
    code_lines = ["from manim import *", "", "class GeneratedScene(Scene):", "    def construct(self):"]

    for obj in scene.objects:
        if obj.type == "circle":
            code_lines.append(f"{obj.id} = Circle(radius={obj.radius}, color={obj.color})")
            code_lines.append(f"self.add({obj.id})")
    
    for motion in scene.motions:
        if motion.motion == "rotation":
            code_lines.append(f"{motion.target}.rotate({motion.params['angular_speed']} * 0.02)")  
        elif motion.motion == "sinusoidal_path":
            code_lines.append(f"# TODO: add ValueTracker + updater for {motion.target} motion")
    
    return "\n".join(code_lines)
