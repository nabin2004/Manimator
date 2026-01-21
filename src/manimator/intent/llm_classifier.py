from intent.schema import UserIntent

INTENT_PROMPT = """
Classify the topic below into structured fields.

Topic: "{topic}"

Return JSON with:
- domain
- audience
- visual_density
- preferred_style
"""

def classify_with_llm(llm, topic: str) -> dict:
    response = llm.invoke(INTENT_PROMPT.format(topic=topic))
    return response  
