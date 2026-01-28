import re

def classify_feedback(text: str) -> dict:
    """
    Classifies feedback into:
    Bug, Feature Request, Praise, Complaint, Spam
    """

    text = text.lower().strip()

    keywords = {
        "Bug": ["crash", "error", "bug", "freeze", "not working", "fails"],
        "Feature Request": ["please add", "feature", "request", "would like"],
        "Praise": ["love", "amazing", "great", "awesome", "perfect"],
        "Complaint": ["slow", "expensive", "bad", "hate", "poor"]
    }

    scores = {k: sum(w in text for w in v) for k, v in keywords.items()}

    if len(text) < 5 or re.fullmatch(r"[\W_]+", text):
        return {"category": "Spam", "confidence": 0.6}

    category = max(scores, key=scores.get)

    if scores[category] == 0:
        return {"category": "Spam", "confidence": 0.5}

    return {
        "category": category,
        "confidence": min(0.7 + 0.1 * scores[category], 0.95)
    }
