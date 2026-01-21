def normalize_topic(raw_topic: str) -> str:
    return raw_topic.strip().lower()


def infer_domain(topic: str) -> str:
    keywords = {
        "math": ["gradient", "matrix", "derivative"],
        "ai/cs": ["algorithm", "dl", "network"],
        "physics": ["force", "energy", "wave"],
    }

    for domain, words in keywords.items():
        if any(w in topic for w in words):
            return domain

    return "general"
