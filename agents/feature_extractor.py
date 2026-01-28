import re

def extract_feature(text: str) -> dict:
    text = text.lower()

    if "integrate" in text or "sync" in text:
        category = "Integration"
    elif "dark mode" in text or "ui" in text:
        category = "UI/UX"
    else:
        category = "Other"

    match = re.search(r"(add|please add|would like) ([^,.]+)", text)
    feature = match.group(2).capitalize() if match else "Feature enhancement"

    impact = "High" if "must" in text or "really need" in text else "Medium"

    return {
        "feature": feature,
        "category": category,
        "impact": impact,
        "summary": f"Requested feature: {feature} ({category})"
    }
