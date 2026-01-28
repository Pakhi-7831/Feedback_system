import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def read_feedback():
    """
    Reads and normalizes feedback from app store reviews
    and support emails CSV files.
    """

    app_reviews = pd.read_csv(DATA_DIR / "app_store_reviews.csv")
    support_emails = pd.read_csv(DATA_DIR / "support_emails.csv")

    app_norm = pd.DataFrame({
        "source_id": app_reviews["review_id"],
        "source_type": "review",
        "text": app_reviews["review_text"],
        "platform": app_reviews["platform"],
        "rating": app_reviews["rating"],
        "timestamp": app_reviews["date"]
    })

    email_norm = pd.DataFrame({
        "source_id": support_emails["email_id"],
        "source_type": "email",
        "text": support_emails["subject"] + " | " + support_emails["body"],
        "platform": "Support Email",
        "rating": None,
        "timestamp": support_emails["timestamp"]
    })

    return pd.concat([app_norm, email_norm], ignore_index=True)
