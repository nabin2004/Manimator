import asyncio
import json
from studio import run_video_workflow, load_workflow_history, get_workflow_by_id

async def test_basic_workflow():
    """Test the workflow with a simple query"""
    print("🚀 Testing Multi-Agent Video Generation System...")
    
    # Test with different types of queries
    test_queries = [
        "Create a short educational video about photosynthesis",
        "Make a tutorial video on how to bake chocolate chip cookies",
        "Create a promotional video for a new coffee shop",
        "Make a 2-minute explainer video about climate change"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*50}")
        print(f"Test {i}: {query}")
        print(f"{'='*50}")
        
        try:
            result = await run_video_workflow(query)
            
            print(f"✅ Workflow completed!")
            print(f"📋 Workflow ID: {result['workflow_id']}")
            print(f"🎬 Final video: {result['final_video']}")
            print(f"⏱️ Duration: {result.get('duration_seconds', 'N/A')} seconds")
            
        except Exception as e:
            print(f"❌ Error: {e}")

async def view_history():
    """View the saved workflow history"""
    print("\n📊 Viewing Workflow History...")
    
    history = load_workflow_history()
    print(f"Total workflow runs: {len(history)}")
    
    for i, workflow in enumerate(history[-3:], 1):  # Show last 3
        print(f"\n--- Workflow {i} ---")
        print(f"ID: {workflow.get('workflow_id')}")
        print(f"Query: {workflow.get('user_query')}")
        print(f"Status: {workflow.get('status')}")
        print(f"Agents: {list(workflow.get('agents', {}).keys())}")

if __name__ == "__main__":
    # Run the tests
    asyncio.run(test_basic_workflow())
    
    # Show history
    asyncio.run(view_history())