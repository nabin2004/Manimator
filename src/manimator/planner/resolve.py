from manimator.planner.llm_planner import create_llm_plan

def plan_topic(intent, llm=None):
    plan = create_llm_plan(llm, intent)

    return plan
