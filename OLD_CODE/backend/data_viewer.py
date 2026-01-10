import json
from datetime import datetime

def format_timestamp(timestamp):
    """Convert ISO timestamp to readable format"""
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp

def display_workflow_summary(workflow):
    """Display the main workflow information"""
    print("=" * 70)
    print("🎬 VIDEO CREATION WORKFLOW SUMMARY")
    print("=" * 70)
    
    print(f"📋 Workflow ID: {workflow['workflow_id']}")
    print(f"🎯 User Request: {workflow['user_query']}")
    print(f"⏰ Started: {format_timestamp(workflow['start_time'])}")
    print(f"✅ Status: {workflow['status'].upper()}")
    
    if workflow['status'] == 'completed':
        duration = workflow['final_result']['duration_seconds']
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"🎞️  Final Video: {workflow['final_result']['final_video']}")

def display_agent_steps(agents):
    """Display each agent's contribution in the workflow"""
    print("\n" + "=" * 70)
    print("🔄 WORKFLOW STEPS")
    print("=" * 70)
    
    agent_order = ['agent1_prompt_refiner', 'agent2_video_planner', 
                   'agent3_task_distributor', 'agent4_scene_writer', 'final_assembly']
    
    for agent_key in agent_order:
        if agent_key in agents:
            agent = agents[agent_key]
            print(f"\n{'━' * 50}")
            
            # Format agent name for display
            agent_name = agent_key.replace('_', ' ').title().replace('Agent', 'Agent')
            print(f"🔹 {agent_name}")
            print(f"   ⏰ {format_timestamp(agent['timestamp'])}")
            
            if agent_key == 'agent1_prompt_refiner':
                print(f"\n   📥 Input: {agent['input']}")
                print(f"\n   📤 Output:")
                print("   " + "-" * 40)
                # Clean up the output text
                output_lines = agent['output'].split('\n')
                for line in output_lines[:10]:  # Show first 10 lines
                    if line.strip():
                        print(f"      {line}")
                if len(output_lines) > 10:
                    print(f"      ... and {len(output_lines)-10} more lines")
                    
            elif agent_key == 'agent2_video_planner':
                plan = agent['output']
                print(f"\n   🎯 Video Structure:")
                print(f"      • Opening: {plan['opening']} ({plan['timestamps']['opening']})")
                print(f"      • Middle: {len(plan['mid_intervals'])} segments ({plan['timestamps']['middle']})")
                print(f"      • Closing: {plan['closing']} ({plan['timestamps']['closing']})")
                
            elif agent_key == 'agent3_task_distributor':
                tasks = agent['output']
                print(f"\n   📋 Task Breakdown ({len(tasks)} chunks):")
                for task in tasks:
                    priority_icon = "🔴" if task['priority'] == 'high' else "🟡"
                    print(f"      {priority_icon} Chunk {task['chunk_id']}: {task['segment_description']}")
                    print(f"        ⏱️  {task['estimated_duration']} | Priority: {task['priority']}")
                    
            elif agent_key == 'agent4_scene_writer':
                chunks = agent['chunks_processed']
                print(f"\n   ✍️  Scene Writing ({len(chunks)} chunks processed)")
                for chunk in chunks:
                    print(f"      • Chunk {chunk['chunk_id']}: {chunk['output']['task_chunk']['segment_description']}")
                    print(f"        🎬 Visuals: {chunk['output']['visual_descriptions']}")
                    print(f"        🔊 Audio: {chunk['output']['audio_cues']}")
                    
            elif agent_key == 'final_assembly':
                print(f"\n   🎉 Final Assembly Complete!")
                print(f"   🎬 Output File: {agent['output']}")

def display_final_result(final_result):
    """Display the final workflow result"""
    print("\n" + "=" * 70)
    print("✅ FINAL RESULT")
    print("=" * 70)
    
    print(f"📊 Workflow Complete: {final_result['workflow_complete']}")
    print(f"🎞️  Video File: {final_result['final_video']}")
    print(f"⏱️  Total Duration: {final_result['duration_seconds']:.2f} seconds")
    
    print(f"\n📋 Task Chunks Created: {len(final_result['task_chunks'])}")
    for chunk in final_result['task_chunks']:
        status_icon = "✅" if chunk['priority'] == 'high' else "☑️"
        print(f"   {status_icon} {chunk['segment_description']} ({chunk['estimated_duration']})")

def main(json_file_path):
    """Main function to load and display the workflow data"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Assuming the JSON is an array with one workflow object
        workflow = data[0]
        
        # Display all sections
        display_workflow_summary(workflow)
        display_agent_steps(workflow['agents'])
        display_final_result(workflow['final_result'])
        
        print("\n" + "=" * 70)
        print("🎊 WORKFLOW COMPLETE! 🎊")
        print("=" * 70)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON format in '{json_file_path}'.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# If you want to run this directly with your JSON file:
if __name__ == "__main__":
    # Replace 'your_file.json' with the actual path to your JSON file
    json_file_path = "video_workflow_history.json"
    
    # Alternatively, if you have the JSON as a string variable:
    # You can modify the script to accept the JSON string directly
    
    main(json_file_path)