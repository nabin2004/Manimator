from manimator.planner.schema import SceneSpec, ScriptPlan
import json 

LLM_SCENE_PROMPT = """
You are generating a structured animation plan.

Topic: "{topic}"
Constraints:
- total_duration_sec: {duration}
- audience: {audience}
- visual_density: {density}

Return ONLY valid JSON matching this schema:

{{
  "scenes": [
    {{
      "scene_id": string,
      "goal": string,
      "visual_elements": [
        "element 1",
        "element 2"
        ],
      "estimated_duration_sec": integer,
      "narrative_intent": string
    }}
  ]
}}

Rules:
- Sum of all estimated_duration_sec MUST be <= total_duration_sec
- scene_id must be unique and it will be used as the class name for the scene
- visual_elements should be concrete items to visualize
- JSON must be valid
- No extra keys
- No explanation, no markdown
"""

def create_llm_plan(llm, intent) -> ScriptPlan:
    prompt = LLM_SCENE_PROMPT.format(
        topic=intent.topic,
        duration=120,
        audience=intent.audience,
        density=intent.visual_density
    )
    response = llm.invoke(prompt)
    
    response = json.loads(response.content)

    with open("debug_plan_response1.json", "w") as f:
        json.dump(response, f, indent=2)
    print("Wrote debug_plan_response.json")
    # quit()

    # validate and parse
    scenes = [SceneSpec(**s) for s in response["scenes"]]
    return ScriptPlan(topic=intent.topic, total_duration_sec=120, scenes=scenes)
