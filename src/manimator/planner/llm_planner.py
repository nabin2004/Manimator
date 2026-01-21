from manimator.planner.schema import SceneSpec, ScriptPlan

LLM_SCENE_PROMPT = """
Given a topic "{topic}" and constraints:
- total_duration_sec: {duration}
- audience: {audience}
- visual_density: {density}

Return a JSON array of scenes. Each scene must have:
- scene_id
- goal
- visual_elements
- estimated_duration_sec
- narrative_intent
"""

def create_llm_plan(llm, intent) -> ScriptPlan:
    prompt = LLM_SCENE_PROMPT.format(
        topic=intent.topic,
        duration=120,
        audience=intent.audience,
        density=intent.visual_density
    )
    response = llm.invoke(prompt)
    
    # validate and parse
    scenes = [SceneSpec(**s) for s in response["scenes"]]
    return ScriptPlan(topic=intent.topic, total_duration_sec=120, scenes=scenes)
