from manimator.codegen.llm_codegen import PROMPT_VERSION
from manimator.intent.schema import UserIntent
from manimator.exception.exception import ManimatorException
from manimator.logging.logger import logging
from pydantic import ValidationError
import sys 
import json

PROMPT_VERSION = "intent_classification_v1"

INTENT_PROMPT = """
Classify the topic below into structured fields.

Topic: "{topic}"

Return JSON with ONLY the following allowed values:

domain: one of ["mathematics", "physics", "AI/CS"]
audience: one of ["school", "undergrad", "grad", "general"]
visual_density: one of ["low", "medium", "high"]
preferred_style: one of ["intuition", "formal", "mixed"]

Return valid JSON ONLY. No extra explanation, no markdown.
"""

def classify_with_llm(llm, topic: str) -> dict:
    logging.info(f"Classifying topic with LLM: {topic}")
    response = llm.invoke(INTENT_PROMPT.format(topic=topic), phase="intent_classification", prompt_version=PROMPT_VERSION)
    logging.info("LLM classification completed.")
    logging.debug(f"LLM Response: {response}")
    content = response.content

    data = json.loads(content)
    # string to dict
    try:
        logging.debug("Parsing LLM response to UserIntent...")
        data["topic"] = topic
        return UserIntent(**data).dict()
    except ValidationError as e:
        raise ManimatorException(
            message="LLM output does not match UserIntent schema",
            cause=e,
            context={
                "topic": topic,
                "llm_output": json.loads(content),
                "validation_errors": e.errors(),
            },
        ) from None
