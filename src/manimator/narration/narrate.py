"""LLM-based narration script generator for Manim scenes.

Takes scene metadata (goal, narrative_intent, visual_elements) and asks the
LLM to write a concise spoken narration suitable for TTS synthesis.
"""

from __future__ import annotations

import json

NARRATION_PROMPT = """You are writing a narration script for an educational animation.

Scene: "{scene_id}"
Goal: {goal}
Narrative intent: {narrative_intent}
Visual elements shown: {visual_elements}
Estimated duration: {duration} seconds

Write a clear, concise narration script that a text-to-speech engine will read
aloud while the animation plays. Rules:
- Keep it under {duration} seconds when spoken at normal pace (~150 words/min)
- Use simple, conversational language suitable for students
- Do NOT include stage directions, timestamps, or formatting
- Do NOT start with "In this scene" or similar meta-references
- Just provide the spoken text, nothing else
- No markdown, no quotes around the text

Narration:"""


def generate_narration(llm, scene_spec) -> str:
    """Generate a narration script for one scene.

    Parameters
    ----------
    llm : LLMWithMetrics
        The LLM client to use for generation.
    scene_spec : SceneSpec
        A planner SceneSpec with scene_id, goal, narrative_intent, etc.

    Returns
    -------
    str
        The narration script text.
    """
    prompt = NARRATION_PROMPT.format(
        scene_id=scene_spec.scene_id,
        goal=scene_spec.goal,
        narrative_intent=scene_spec.narrative_intent,
        visual_elements=", ".join(scene_spec.visual_elements),
        duration=scene_spec.estimated_duration_sec,
    )

    response = llm.invoke(prompt, phase="narration", prompt_version="narration_v1")
    return response.content.strip()
