# Manimator

**Text-to-Math-Animation** using Agentic AI and the **Manim** library.

Manimator takes natural language math explanations and turns them into executable Manim animations using an agent-based pipeline orchestrated with **LangGraph**.

---

## Architecture

The system is split into the following components:

1. **Intent Classifier**  
   Limit the scope to Math, CS and AI only so Manim can Handle user queries. Manim can't visualize other topics like heart blood flow or others succintly. 

2. **Planner Component**  
   Breaks the intent into structured animation scenes.

3. **CodeGen Component**  
   Takes the planner and generates the code using manim library.

4. **Validate & Route**  
   Validates the generated python code using Python AST

5. **Render Component**  
   Renders the final animation using Manim command.

---

## Demo
Demo on Youtube:



[![Watch the video](http://i3.ytimg.com/vi/LWFvuj6jeD0/hqdefault.jpg)](https://youtu.be/LWFvuj6jeD0)

---

## Tech Stack

- Python  
- Manim  
- langchain & LangGraph  
---

## Status

Experimental. Works, but expect rough edges.
