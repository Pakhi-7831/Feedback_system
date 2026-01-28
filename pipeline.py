import pandas as pd
from pathlib import Path

from agents.csv_reader import read_feedback
from agents.feedback_classifier import classify_feedback
from agents.bug_analysis import analyze_bug
from agents.feature_extractor import extract_feature
from agents.ticket_creator import create_ticket
from agents.quality_critic import review_ticket

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def run_pipeline():
    print("Starting Agentic Feedback Pipeline...")

    feedback_df = read_feedback()
    print(f"Loaded {len(feedback_df)} feedback items")

    tickets = []
    processing_logs = []

    for _, row in feedback_df.iterrows():
        classification = classify_feedback(row["text"])
        category = classification["category"]

        if category == "Bug":
            bug = analyze_bug(row["text"], row["platform"])

            priority_map = {
                "Critical": "Critical",
                "High": "High",
                "Medium": "Medium",
                "Low": "Low"
            }

            ticket = create_ticket(
                source_id=row["source_id"],
                category="Bug",
                title=f"[BUG] {bug['severity']} issue on {bug['platform']}",
                description=bug["summary"],
                metadata={
                    "platform": bug["platform"],
                    "steps_to_reproduce": bug["steps"]
                },
                priority=priority_map[bug["severity"]]
            )

        elif category == "Feature Request":
            feature = extract_feature(row["text"])

            ticket = create_ticket(
                source_id=row["source_id"],
                category="Feature Request",
                title=f"[FEATURE] {feature['feature']}",
                description=feature["summary"],
                metadata={
                    "category": feature["category"],
                    "impact": feature["impact"]
                },
                priority="Medium" if feature["impact"] == "High" else "Low"
            )

        else:
            continue

        review = review_ticket(ticket)

        processing_logs.append({
            "ticket_id": ticket["ticket_id"],
            "source_id": ticket["source_id"],
            "decision": "Approved" if review["approved"] else "Flagged",
            "issues": "; ".join(review["issues"]),
            "timestamp": review["timestamp"]
        })

        if review["approved"]:
            tickets.append(ticket)

    tickets_df = pd.DataFrame(tickets)
    logs_df = pd.DataFrame(processing_logs)

    tickets_df.to_csv(OUTPUT_DIR / "generated_tickets.csv", index=False)
    logs_df.to_csv(OUTPUT_DIR / "processing_log.csv", index=False)

    metrics = {
        "Total Feedback": len(feedback_df),
        "Tickets Generated": len(tickets_df),
        "Bug Tickets": len(tickets_df[tickets_df["category"] == "Bug"]),
        "Feature Tickets": len(tickets_df[tickets_df["category"] == "Feature Request"]),
        "Critical Bugs": len(
            tickets_df[
                (tickets_df["category"] == "Bug") &
                (tickets_df["priority"] == "Critical")
            ]
        )
    }

    metrics_df = pd.DataFrame([
        {"metric": k, "value": v} for k, v in metrics.items()
    ])

    metrics_df.to_csv(OUTPUT_DIR / "metrics.csv", index=False)

    print("Pipeline completed successfully!")
    print("Outputs written to /outputs")

if __name__ == "__main__":
    run_pipeline()
