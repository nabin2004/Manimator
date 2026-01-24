from manimator.llm.llm import LLMWithMetrics
# from src.manimator.orchestration.langgraph_pipeline import run_pipeline
from src.manimator.orchestration.new_langgraph import run_pipeline
from src.manimator.intent.resolve import resolve_intent
from src.manimator.planner.resolve import plan_topic
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

from manimator.metrics.run_metrics import RunMetrics


load_dotenv()

def main():
    print("Hello from Manimator!")

def test_pipeline():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
    os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

    llm_base = ChatOpenAI(model="xiaomi/mimo-v2-flash:free",temperature=0.0)

    run_metrics = RunMetrics()
    # run_id = "run_2026_01_24_001"
    llm = LLMWithMetrics(llm_base)

    # result = llm.invoke("How are you today?")
    # print("DIR DIR DIR DIR:", result.response_metadata)
    # json.dump(result.response_metadata, open("metadata.json", "w"), indent=2)
    # quit()
 
    # Step 1: User input
    topic = "Explain the concept of recursion in computer science."

    # Step 2: Intent resolution
    intent = resolve_intent(topic, llm=llm)

    # Step 3: Planner generates ScriptPlan
    plan = plan_topic(intent, llm=llm)

    # Step 4: Run the LangGraph orchestration
    output_dir = "./storage"
    pipeline_state = run_pipeline(llm=llm, plan=plan, output_dir=output_dir)

    print("Pipeline finished!")
    # print(pipeline_state.json(indent=2))

if __name__ == "__main__":
    main()
    test_pipeline()
