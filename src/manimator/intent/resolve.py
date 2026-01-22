from manimator.intent.schema import UserIntent
from manimator.intent.normalize import normalize_topic, infer_domain
from manimator.intent.llm_classifier import classify_with_llm


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
    print("LLM Data:", llm_data)
    # print("Resolved Intent:", llm_data.content)
    # dicted = llm_data
    # print("As dict:", dicted)
    # print("As dict type:", type(dicted))
    # quit()

    return UserIntent(
        topic=topic,
        domain=llm_data['domain'],
        # **llm_data
        audience=llm_data['audience'],
        visual_density=llm_data['visual_density'],
        preferred_style=llm_data['preferred_style'],
    )
