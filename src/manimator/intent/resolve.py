from intent.schema import UserIntent
from intent.normalize import normalize_topic, infer_domain
from intent.llm_classifier import classify_with_llm


def resolve_intent(raw_topic: str, llm=None) -> UserIntent:
    topic = normalize_topic(raw_topic)
    domain = infer_domain(topic)

    if llm is None:
        return UserIntent(
            topic=topic,
            domain=domain,
            audience="general",
            visual_density="medium",
            preferred_style="mixed",
        )

    llm_data = classify_with_llm(llm, topic)

    return UserIntent(
        topic=topic,
        domain=domain,
        **llm_data
    )
