
from manimator.codegen.template import MANIM_SCENE_TEMPLATE, indent_code
from manimator.planner.schema import SceneSpec
import json

LLM_CODE_PROMPT = """
Generate Manim Python code for a scene with the following spec:
- Goal: {goal}
- Visual elements: {elements}
- Narrative intent: {narrative}

Constraints:
- Only use classes from manim import *
- Scene class name must be {scene_class_name}
- Indent properly
- No file IO, no shell, no randomness
- Return code only
- Don't include any explanations or comments
- Don't include ````python` or any markdown formatting
"""

def generate_scene_code(llm, scene: SceneSpec) -> str:
    scene_class_name = scene.scene_id.capitalize()
    prompt = LLM_CODE_PROMPT.format(
        goal=scene.goal,
        elements=", ".join(scene.visual_elements),
        narrative=scene.narrative_intent,
        scene_class_name=scene_class_name
    )
    scene_body = llm.invoke(prompt)
    response = scene_body.content
    return MANIM_SCENE_TEMPLATE.format(
        scene_class_name=scene_class_name,
        scene_body=indent_code(response)
    )
