from planner.schema import SceneSpec, ScriptPlan

def create_basic_plan(topic: str, total_duration_sec: int = 120) -> ScriptPlan:
    scenes = [
        SceneSpec(
            scene_id=f"scene_{i+1:02}",
            goal=f"Explain part {i+1} of {topic}",
            visual_elements=["text", "arrow"],
            estimated_duration_sec=total_duration_sec // 3,
            narrative_intent=f"Introduce concept {i+1}"
        )
        for i in range(3)
    ]

    return ScriptPlan(
        topic=topic,
        total_duration_sec=total_duration_sec,
        scenes=scenes
    )
