from planner.basic_planner import create_basic_plan
from planner.llm_planner import create_llm_plan

def plan_topic(intent, llm=None):
    # Start with deterministic skeleton
    plan = create_basic_plan(intent.topic)

    # Optional: enriches with LLM
    if llm is not None:
        plan = create_llm_plan(llm, intent)

    return plan
