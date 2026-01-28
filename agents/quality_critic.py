import json
from datetime import datetime

def review_ticket(ticket):
    required = ["ticket_id", "source_id", "category", "priority", "title", "description"]

    issues = [k for k in required if not ticket.get(k)]

    try:
        json.loads(ticket["metadata"])
    except Exception:
        issues.append("Invalid metadata")

    return {
        "approved": len(issues) == 0,
        "issues": issues,
        "timestamp": datetime.utcnow().isoformat()
    }
