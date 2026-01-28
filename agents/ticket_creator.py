import uuid
import json

def create_ticket(source_id, category, title, description, metadata, priority):
    return {
        "ticket_id": f"TCK-{uuid.uuid4().hex[:8]}",
        "source_id": source_id,
        "category": category,
        "priority": priority,
        "title": title,
        "description": description,
        "metadata": json.dumps(metadata)
    }
