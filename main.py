from src.manimator.orchestration.langgraph_pipeline import run_pipeline
from src.manimator.intent.resolve import resolve_intent
from src.manimator.planner.resolve import plan_topic
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Hello from Manimator!")

def test_pipeline():
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
    os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

    llm = ChatOpenAI(model="xiaomi/mimo-v2-flash:free",temperature=0.0)
 
    # Step 1: User input
    topic = "Explain the concept of recursion in computer science."

    # Step 2: Intent resolution
    intent = resolve_intent(topic, llm=llm)
    print("Resolved Intent:", type(intent))

    # Step 3: Planner generates ScriptPlan
    plan = plan_topic(intent, llm=llm)
    print("Generated Plan type:", type(plan))
    print("Generated Plan JSON:", plan)

    # Step 4: Run the LangGraph orchestration
    output_dir = "./storage"
    pipeline_state = run_pipeline(llm=llm, plan=plan, output_dir=output_dir)

    print("Pipeline finished!")
    print(pipeline_state.json(indent=2))

if __name__ == "__main__":
    main()
    test_pipeline()
