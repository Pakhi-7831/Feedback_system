import re

def analyze_bug(text: str, platform_hint=None) -> dict:
    text = text.lower()

    if "android" in text:
        platform = "Android"
    elif "ios" in text or "iphone" in text:
        platform = "iOS"
    elif platform_hint:
        platform = platform_hint
    else:
        platform = "Unknown"

    if "crash" in text or "freeze" in text:
        severity = "Critical"
    elif "cannot" in text or "fails" in text:
        severity = "High"
    elif "slow" in text:
        severity = "Medium"
    else:
        severity = "Low"

    steps = re.findall(r"(when|after|while) [^,.]+", text)
    steps = steps or ["Steps not clearly specified"]

    return {
        "platform": platform,
        "severity": severity,
        "steps": steps,
        "summary": f"Issue on {platform}, severity {severity}: {text}"
    }
