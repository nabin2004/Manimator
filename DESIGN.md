# Manimator — Agentic System Design

## Core principle (non-negotiable)

> **LLMs propose. Deterministic systems decide.**

LLMs never:

* Execute code
* Decide retries
* Control file paths
* Decide success/failure


## 1. User Input Layer

**Responsibility:** Accept topic + constraints.

### Input:

```json
{
  "topic": "Backpropagation",
  "audience": "undergraduate",
  "duration_sec": 120,
  "style": "visual_intuition"
}
```

### Guarantees:

* Validate input schema
* Normalize topic
* Enforce duration limits

No LLM yet. Garbage in is blocked early.

---

## 2. Knowledge Report Generator (LLM)

**Responsibility:** Generate factual, structured understanding.

### Output contract (JSON only):

```json
{
  "learning_goal": "...",
  "key_concepts": ["...", "..."],
  "common_misconceptions": ["..."],
  "visual_metaphors": ["..."],
  "constraints": {
    "avoid_symbols": false,
    "math_level": "light"
  }
}
```

### Notes:

* No Manim
* No code
* No narration text yet
* Stored as immutable artifact

If this is wrong, the whole video will be wrong — so **validate here**.

---

## 3. Scene Planner (LLM)

**Responsibility:** Convert understanding → visual structure.

### Input:

* Knowledge report
* Duration constraints

### Output contract:

```json
{
  "scenes": [
    {
      "scene_id": "scene_01",
      "goal": "Explain intuition",
      "visual_elements": ["nodes", "arrows"],
      "estimated_duration_sec": 20
    }
  ]
}
```

### Deterministic checks:

* Sum(duration) ≤ max_duration
* Scene count limit
* Scene naming enforced

## 4. Script Planner (LLM)
**Responsibility:** Defines what each scene must show.

### Output per scene:

```json
{
  "scene_id": "scene_01",
  "objects": [
    {"type": "Circle", "count": 3},
    {"type": "Arrow", "count": 2}
  ],
  "animations": [
    "fade_in",
    "transform",
    "highlight"
  ],
  "narrative_intent": "Show error flowing backward"
}
```

## 5. Scene Code Generator (LLM)

**Responsibility:** Convert scene spec → Manim code.

### Hard constraints:

* Single Scene class
* Fixed imports
* No file IO
* No shell
* No randomness
* Max LOC enforced

### Output:

```python
class Scene01(Scene):
    def construct(self):
        ...
```

## 6. Python Code Validation (NO LLM)

**Responsibility:** Decide if code is acceptable.

### Checks:

* AST parsing (syntax)
* Import allowlist
* Manim API compatibility
* Scene class existence
* Runtime dry-run (optional)

If it fails → LLM is *not* trusted to decide why.

## 7. Renderer
**Responsibility:** Produce video deterministically.
### Guarantees:
* Dockerized Manim
* Version-locked
* Resource limits
* Log capture

### Output:
* mp4
* render logs
* execution metadata

## 8. Repair Loop (Agentic Core)

### Trigger:

* Validation failure
* Render failure

### Input to LLM:

* Failed code
* Error logs
* Scene spec
* Explicit instruction:

### Constraints:

* Max retries (e.g. 3)
* No cross-scene edits
* Diff-based comparison

## 9. Orchestration Layer (LangGraph)

### States:
* PLANNED
* CODE_GENERATED
* VALIDATED
* RENDERED
* FAILED

Each node:

* Takes state
* Returns updated state
* Has no side effects outside contract

## 10. Persistence Layer

**Artifacts are immutable.**

Store:
* Topic input
* Knowledge report
* Scene plans
* Generated code
* Render logs
* Final video


## 11. Observability (senior-level detail)

Track:

* Token usage per stage
* Retry counts
* Failure reasons
* Render time per scene
* Cost per video

