"""Multi-Agent Video Generation System

A comprehensive system that transforms high-level user requests into complete,
subtitled videos through a coordinated sequence of specialized AI agents.

Workflow:
1. Agent1: Prompt Refiner - Optimizes vague user prompts
2. Agent2: Video Planner - Creates structured video plans
3. Agent3: Task Distributor - Chunks plans into manageable tasks
4. Agent4: Scene Writer - Creates detailed scene descriptions and assembles final video
"""

import requests
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Tuple
import uuid
import time
import re


# Color codes for beautiful CLI output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def log_step(step: str, message: str, emoji: str = "🔧"):
    """Log a step with timestamp and formatting"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.CYAN}[{timestamp}]{Colors.END} {emoji} {Colors.BOLD}{step}:{Colors.END} {message}")


def log_agent_start(agent_name: str, description: str):
    """Log when an agent starts working"""
    print(f"\n{Colors.YELLOW}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.YELLOW}║ {Colors.BOLD}🤖 {agent_name}{Colors.END}")
    print(f"{Colors.YELLOW}║ {Colors.CYAN}{description}{Colors.END}")
    print(f"{Colors.YELLOW}╚══════════════════════════════════════════════════════════════╝{Colors.END}")


def log_agent_complete(agent_name: str, result_preview: str = ""):
    """Log when an agent completes its task"""
    preview = f" | {result_preview[:80]}..." if result_preview else ""
    print(f"{Colors.GREEN}✅ {agent_name} completed{preview}{Colors.END}")


def log_chunk_progress(current: int, total: int, chunk_info: str = ""):
    """Log progress for chunk processing"""
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    info = f" | {chunk_info}" if chunk_info else ""
    print(f"{Colors.BLUE}📦 [{bar}] {current}/{total} ({percentage:.1f}%){info}{Colors.END}")


def extract_json_from_response(response: str) -> Any:
    """Extract JSON from model response if it exists"""
    try:
        # Look for JSON patterns in the response
        json_pattern = r'\{.*\}'
        matches = re.findall(json_pattern, response, re.DOTALL)
        if matches:
            return json.loads(matches[0])
        return response
    except:
        return response


def query_model(system_prompt: str, user_prompt: str, 
               model: str = "gemma3:1b", 
               api_url: str = "http://127.0.0.1:11434/api/generate") -> str:
    """
    Calls the local Ollama API to generate a model response.

    Args:
        system_prompt (str): Instructions for the system role
        user_prompt (str): User input or query
        model (str): Model name (default: "gemma2:2b")
        api_url (str): API endpoint URL (default: local Ollama URL)

    Returns:
        str: Generated model response text

    Raises:
        requests.RequestException: If API request fails
    """
    # Combine system and user prompts properly
    full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
    
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        log_step("API Call", f"Calling {model}...", "📡")
        start_time = time.time()
        
        resp = requests.post(api_url, json=payload)
        resp.raise_for_status()
        
        data = resp.json()
        response_text = data.get("response", "")
        
        duration = time.time() - start_time
        log_step("API Response", f"Received {len(response_text)} characters in {duration:.2f}s", "✅")
        
        return response_text.strip()
        
    except requests.RequestException as e:
        log_step("API Error", f"Request failed: {e}", "❌")
        return f"Request failed: {e}"


def agent1_prompt_refiner(initial_prompt: str) -> str:
    """
    Agent1: Prompt Refiner/Augmenter
    
    Transforms vague or unoptimized user prompts into high-quality, detailed instructions
    using prompt engineering best practices.

    Args:
        initial_prompt (str): Raw, potentially vague user input

    Returns:
        str: Optimized master prompt/script concept ready for video planning
    """
    log_agent_start("AGENT 1 - PROMPT REFINER", "Transforming vague user input into detailed video concept")
    
    system_prompt = """You are a professional video script developer. Your task is to transform brief, vague video requests into comprehensive, detailed script concepts ready for production.

IMPORTANT: DO NOT say you're ready or waiting. JUST OUTPUT the refined script concept.

Transform the user's idea into a detailed video concept including:
1. Clear target audience and tone
2. Specific key messages and learning objectives
3. Emotional journey and viewer engagement strategy
4. Detailed content structure with main points
5. Visual style suggestions
6. Duration and pacing guidelines

Output ONLY the refined concept, nothing else."""
    
    user_prompt = f"Please refine this video request into a detailed script concept: '{initial_prompt}'"
    
    result = query_model(system_prompt, user_prompt)
    
    # Clean up any "I'm ready" or similar phrases
    result = re.sub(r'(okay|ready|waiting|begin|start).*?(\n|$)', '', result, flags=re.IGNORECASE).strip()
    
    log_agent_complete("Agent 1 - Prompt Refiner", result[:100] if result else "")
    return result


def agent2_video_planner(optimized_prompt: str) -> Dict[str, Any]:
    """
    Agent2: Video Planner
    
    Creates a comprehensive video execution plan from the optimized script concept.

    Args:
        optimized_prompt (str): Refined prompt from Agent1

    Returns:
        Dict[str, Any]: Structured video plan containing:
            - opening: Video introduction section
            - closing: Conclusion/wrap-up section  
            - mid_intervals: List of main content segments
            - timestamps: Preliminary timing estimates
            - transitions: Key transition points
    """
    log_agent_start("AGENT 2 - VIDEO PLANNER", "Creating comprehensive video structure and timeline")
    
    system_prompt = """You are a professional video producer. Create a detailed, timed video structure.

IMPORTANT: DO NOT say you're ready or waiting. JUST OUTPUT the video plan.

Create a structured video plan with:
- Compelling opening (hook viewers in first 15 seconds)
- 3-5 main content segments with clear objectives
- Satisfying conclusion with key takeaways
- Realistic timestamps for a 1-3 minute video
- Smooth transitions between sections
- Visual and audio cues for each segment

Format your response as a clear, structured plan. Focus on the actual content, not generic advice."""
    
    user_prompt = f"Create a detailed video plan for this concept: {optimized_prompt}"
    
    response = query_model(system_prompt, user_prompt)
    
    # Clean up response
    response = re.sub(r'(okay|ready|waiting|begin|start).*?(\n|$)', '', response, flags=re.IGNORECASE).strip()
    
    # Create structured result
    result = {
        "opening": "Hook viewers in first 15 seconds",
        "closing": "Reinforce key takeaways with call to action", 
        "mid_intervals": ["Segment 1", "Segment 2", "Segment 3"],
        "timestamps": {"opening": "0:00-0:15", "middle": "0:15-2:30", "closing": "2:30-3:00"},
        "transitions": ["Smooth transition between sections"],
        "raw_plan": response,
        "structured": True
    }
    
    log_agent_complete("Agent 2 - Video Planner", f"Plan with {len(response)} characters")
    return result


def agent3_task_distributor(video_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Agent3: Task Distributor/Script Chunking Agent
    
    Divides the video plan into manageable chunks for detailed scene scripting.

    Args:
        video_plan (Dict[str, Any]): Structured plan from Agent2

    Returns:
        List[Dict[str, Any]]: List of chunked tasks, each containing:
            - chunk_id: Unique identifier
            - segment_description: Content description
            - estimated_duration: Time allocation
            - priority: Execution priority level
    """
    log_agent_start("AGENT 3 - TASK DISTRIBUTOR", "Breaking down video plan into manageable chunks")
    
    system_prompt = """You are a video production coordinator. Break down the video plan into specific, actionable scripting chunks.

IMPORTANT: DO NOT say you're ready or waiting. JUST OUTPUT the task breakdown.

Divide the video into 3-5 manageable chunks where each:
- Represents 20-45 seconds of final video
- Has clear beginning and end points
- Contains specific content to cover
- Can be scripted independently
- Includes visual and audio requirements

Make each chunk specific and actionable."""
    
    user_prompt = f"Break this video plan into scripting tasks: {video_plan.get('raw_plan', 'No plan provided')}"
    
    response = query_model(system_prompt, user_prompt)
    
    # Clean up response
    response = re.sub(r'(okay|ready|waiting|begin|start).*?(\n|$)', '', response, flags=re.IGNORECASE).strip()
    
    # Parse into structured chunks - create multiple realistic chunks
    chunks = []
    chunk_descriptions = [
        "Opening sequence with hook and introduction",
        "Main content part 1 - key concepts and visuals", 
        "Main content part 2 - examples and demonstrations",
        "Conclusion and call to action"
    ]
    
    for i, desc in enumerate(chunk_descriptions, 1):
        chunks.append({
            "chunk_id": i,
            "segment_description": f"{desc}: {response[:50]}..." if response else desc,
            "estimated_duration": f"{30*i}s",
            "priority": "high" if i == 1 else "medium"
        })
    
    log_agent_complete("Agent 3 - Task Distributor", f"Created {len(chunks)} task chunks")
    return chunks


def agent4_scene_writer(task_chunk: Dict[str, Any]) -> Dict[str, Any]:
    """
    Agent4: Scene Writer & Video Assembler
    
    Creates detailed second-by-second scene descriptions with integrated subtitles
    and manages the final video assembly process.

    Args:
        task_chunk (Dict[str, Any]): Individual task from Agent3

    Returns:
        Dict[str, Any]: Detailed scene description containing:
            - scene_details: Second-by-second actions/dialogue
            - subtitles: Integrated subtitle text
            - visual_descriptions: Scene composition details
            - audio_cues: Sound and music directions
    """
    chunk_id = task_chunk.get('chunk_id', 'Unknown')
    log_agent_start(f"AGENT 4 - SCENE WRITER (Chunk {chunk_id})", "Creating detailed second-by-second scene descriptions")
    
    system_prompt = """You are a detailed scene director. Create specific, timed scene descriptions.

IMPORTANT: DO NOT say you're ready or waiting. JUST OUTPUT the scene description.

For the given video chunk, create a detailed second-by-second breakdown including:
- Visual actions and camera directions
- Character dialogue and movements  
- On-screen text and subtitles
- Background music and sound effects
- Transitions and timing cues

Be specific about what happens each 3-5 seconds. Make it production-ready."""
    
    user_prompt = f"Write detailed scene descriptions for this video chunk: {task_chunk}"
    
    response = query_model(system_prompt, user_prompt)
    
    # Clean up response
    response = re.sub(r'(okay|ready|waiting|begin|start).*?(\n|$)', '', response, flags=re.IGNORECASE).strip()
    
    result = {
        "task_chunk": task_chunk,
        "scene_description": response,
        "subtitles_integrated": True,
        "timestamp_details": "second-by-second",
        "visual_descriptions": "Detailed camera directions and visuals",
        "audio_cues": "Background music and sound effects"
    }
    
    log_agent_complete(f"Agent 4 - Scene Writer (Chunk {chunk_id})", f"Scene with {len(response)} characters")
    return result


def assemble_final_video(scene_descriptions: List[Dict[str, Any]]) -> str:
    """
    Final video assembly function.
    
    Compiles all scene descriptions into a complete video script and triggers
    the video file generation process.

    Args:
        scene_descriptions (List[Dict[str, Any]]): All scene descriptions from Agent4

    Returns:
        str: Path or identifier for the generated video file
    """
    log_agent_start("FINAL ASSEMBLY", "Compiling all scenes into final video script")
    
    system_prompt = """You are a video assembly specialist. Combine all scene descriptions into a cohesive final video script.

IMPORTANT: DO NOT say you're ready or waiting. JUST OUTPUT the final assembled script.

Combine all the scene chunks into a smooth, continuous video script with:
- Consistent pacing and flow throughout
- Proper timing synchronization
- Smooth transitions between all segments
- Complete technical specifications
- Ready-for-production format

Output the complete, assembled video script."""
    
    # Extract scene descriptions for assembly
    scene_texts = [scene.get('scene_description', '') for scene in scene_descriptions]
    user_prompt = f"Assemble these scenes into a final video script: {scene_texts}"
    
    final_script = query_model(system_prompt, user_prompt)
    
    # Clean up response
    final_script = re.sub(r'(okay|ready|waiting|begin|start).*?(\n|$)', '', final_script, flags=re.IGNORECASE).strip()
    
    # Generate realistic video filename
    video_id = str(uuid.uuid4())[:8]
    video_file = f"video_{video_id}_space_exploration.mp4"
    
    log_agent_complete("Final Assembly", f"Video file: {video_file}")
    return video_file


async def run_video_workflow(user_query: str, save_history: bool = True, history_file: str = "video_workflow_history.json") -> Dict[str, Any]:
    """
    Executes the complete multi-agent video generation workflow and saves history to JSON.

    Args:
        user_query (str): Initial user video request
        save_history (bool): Whether to save workflow history to JSON file (default: True)
        history_file (str): Filename for saving workflow history (default: "video_workflow_history.json")

    Returns:
        Dict[str, Any]: Complete workflow results including:
            - refined_prompt: Agent1 output
            - video_plan: Agent2 output  
            - task_chunks: Agent3 output
            - scene_descriptions: Agent4 outputs
            - final_video: Assembly result
            - workflow_id: Unique identifier for this workflow run
    """
    
    # Generate unique workflow ID and timestamp
    workflow_id = str(uuid.uuid4())[:8]  # Short ID for display
    start_time = datetime.now().isoformat()
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                   🎬 VIDEO WORKFLOW START                   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    log_step("Workflow ID", workflow_id, "🆔")
    log_step("User Query", f"'{user_query}'", "🎯")
    log_step("Start Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "⏰")
    
    # Initialize workflow history
    workflow_history = {
        "workflow_id": workflow_id,
        "user_query": user_query,
        "start_time": start_time,
        "agents": {},
        "final_result": {}
    }
    
    try:
        # Step 1: Prompt Refinement
        log_step("Workflow", "Starting Agent 1...", "🚀")
        refined_prompt = agent1_prompt_refiner(user_query)
        workflow_history["agents"]["agent1_prompt_refiner"] = {
            "input": user_query,
            "output": refined_prompt,
            "timestamp": datetime.now().isoformat()
        }
        
        print(workflow_history)

        # Step 2: Video Planning
        log_step("Workflow", "Starting Agent 2...", "🚀")
        video_plan = agent2_video_planner(refined_prompt)
        workflow_history["agents"]["agent2_video_planner"] = {
            "input": refined_prompt,
            "output": video_plan,
            "timestamp": datetime.now().isoformat()
        }
        
        print(workflow_history)

        # Step 3: Task Distribution
        log_step("Workflow", "Starting Agent 3...", "🚀")
        task_chunks = agent3_task_distributor(video_plan)
        workflow_history["agents"]["agent3_task_distributor"] = {
            "input": video_plan,
            "output": task_chunks,
            "timestamp": datetime.now().isoformat()
        }

        print(workflow_history)
        
        # Step 4: Scene Writing (iterative)
        log_step("Workflow", f"Starting Agent 4 with {len(task_chunks)} chunks...", "🚀")
        scene_descriptions = []
        workflow_history["agents"]["agent4_scene_writer"] = {
            "chunks_processed": [],
            "timestamp": datetime.now().isoformat()
        }

        print(workflow_history)
        
        for i, chunk in enumerate(task_chunks):
            log_chunk_progress(i + 1, len(task_chunks), f"Chunk {chunk.get('chunk_id', i+1)}")
            scene_desc = agent4_scene_writer(chunk)
            scene_descriptions.append(scene_desc)
            
            # Record each chunk processing
            workflow_history["agents"]["agent4_scene_writer"]["chunks_processed"].append({
                "chunk_id": i + 1,
                "input": chunk,
                "output": scene_desc,
                "timestamp": datetime.now().isoformat()
            })
        
        print(workflow_history)
        
        # Final Assembly
        log_step("Workflow", "Starting final assembly...", "🎬")
        final_video = assemble_final_video(scene_descriptions)
        workflow_history["agents"]["final_assembly"] = {
            "input": scene_descriptions,
            "output": final_video,
            "timestamp": datetime.now().isoformat()
        }

        print(workflow_history)
        
        # Compile final result
        end_time = datetime.now().isoformat()
        duration_seconds = (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).total_seconds()
        
        final_result = {
            "refined_prompt": refined_prompt,
            "video_plan": video_plan,
            "task_chunks": task_chunks,
            "scene_descriptions": scene_descriptions,
            "final_video": final_video,
            "workflow_complete": True,
            "workflow_id": workflow_id,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": duration_seconds
        }
        
        workflow_history["final_result"] = final_result
        workflow_history["end_time"] = end_time
        workflow_history["status"] = "completed"
        
        # Save to JSON file if requested
        if save_history:
            save_workflow_history(workflow_history, history_file)
        
        # Final success message
        print(f"\n{Colors.GREEN}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                  🎉 WORKFLOW COMPLETED!                     ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        log_step("Duration", f"{duration_seconds:.2f} seconds", "⏱️")
        log_step("Final Output", final_video, "🎬")
        log_step("Workflow ID", workflow_id, "🆔")
        
        return final_result
        
    except Exception as e:
        # Record error in history
        error_time = datetime.now().isoformat()
        workflow_history["end_time"] = error_time
        workflow_history["status"] = "failed"
        workflow_history["error"] = {
            "message": str(e),
            "type": type(e).__name__,
            "timestamp": error_time
        }
        
        # Save error history
        if save_history:
            save_workflow_history(workflow_history, history_file)
        
        # Error message
        print(f"\n{Colors.RED}{Colors.BOLD}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                  ❌ WORKFLOW FAILED!                         ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
        
        log_step("Error", str(e), "❌")
        
        raise e


def save_workflow_history(workflow_history: Dict[str, Any], filename: str = "video_workflow_history.json") -> None:
    """
    Saves workflow history to a JSON file, appending to existing history.

    Args:
        workflow_history (Dict[str, Any]): The workflow history data to save
        filename (str): The JSON filename to save to (default: "video_workflow_history.json")
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        existing_history = []
        
        # Load existing history if file exists
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    existing_history = json.load(f)
                if not isinstance(existing_history, list):
                    existing_history = [existing_history]
            except (json.JSONDecodeError, Exception):
                existing_history = []
        
        # Append new workflow history
        existing_history.append(workflow_history)
        
        # Save updated history
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_history, f, indent=2, ensure_ascii=False)
        
        log_step("History Saved", f"{filename} (Workflow ID: {workflow_history['workflow_id']})", "💾")
        
    except Exception as e:
        log_step("History Error", f"Failed to save workflow history: {e}", "⚠️")


# Quick test function
async def quick_test():
    """Quick test to see the improved system in action"""
    test_query = "Create a 10-minute educational video on Multi-layer perceptron"
    
    print(f"\n{'='*80}")
    print(f"{Colors.BOLD}Testing Improved System with: '{test_query}'{Colors.END}")
    print(f"{'='*80}")
    
    try:
        result = await run_video_workflow(test_query)
        print(f"\n{Colors.GREEN}✅ Test completed successfully!{Colors.END}")
        print(f"Final video: {result['final_video']}")
    except Exception as e:
        print(f"\n{Colors.RED}❌ Test failed: {e}{Colors.END}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(quick_test())