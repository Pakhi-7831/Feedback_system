import streamlit as st
import pandas as pd
import json
from pathlib import Path

OUTPUT_DIR = Path("outputs")

TICKETS_PATH = OUTPUT_DIR / "generated_tickets.csv"
LOGS_PATH = OUTPUT_DIR / "processing_log.csv"
METRICS_PATH = OUTPUT_DIR / "metrics.csv"

st.set_page_config(
    page_title="Agentic Feedback System",
    layout="wide"
)

st.title("Agentic User Feedback Analysis System")

@st.cache_data
def load_csv(path):
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

tickets_df = load_csv(TICKETS_PATH)
logs_df = load_csv(LOGS_PATH)
metrics_df = load_csv(METRICS_PATH)

st.sidebar.header("Configuration Panel")

priority_override = st.sidebar.selectbox(
    "Default Feature Priority",
    ["Low", "Medium", "High"],
    index=1
)

auto_approve = st.sidebar.checkbox(
    "Auto-approve valid tickets",
    value=True
)

st.sidebar.markdown(
    "_Configuration options are demonstrative for human-in-the-loop control._"
)

st.subheader("System Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Tickets", len(tickets_df))
col2.metric("Processing Logs", len(logs_df))
col3.metric(
    "Critical Bugs",
    len(
        tickets_df[
            (tickets_df["category"] == "Bug") &
            (tickets_df["priority"] == "Critical")
        ]
    ) if not tickets_df.empty else 0
)

st.divider()

st.subheader("Generated Tickets")

if tickets_df.empty:
    st.warning("No tickets found. Run pipeline.py first.")
else:
    st.dataframe(tickets_df, use_container_width=True)

st.divider()
st.subheader("Manual Override & Approval")

if not tickets_df.empty:
    selected_ticket = st.selectbox(
        "Select Ticket ID",
        tickets_df["ticket_id"]
    )

    ticket_row = tickets_df[tickets_df["ticket_id"] == selected_ticket].iloc[0]

    st.markdown("**Ticket Details**")
    st.json({
        "title": ticket_row["title"],
        "description": ticket_row["description"],
        "metadata": json.loads(ticket_row["metadata"])
    })

    new_priority = st.selectbox(
        "Update Priority",
        ["Critical", "High", "Medium", "Low"],
        index=["Critical", "High", "Medium", "Low"].index(ticket_row["priority"])
    )

    approve_ticket = st.checkbox("Approve this ticket", value=True)

    if st.button("Apply Changes"):
        tickets_df.loc[
            tickets_df["ticket_id"] == selected_ticket, "priority"
        ] = new_priority

        tickets_df.to_csv(TICKETS_PATH, index=False)
        st.success("Ticket updated successfully.")

else:
    st.info("No tickets available for override.")

st.divider()
st.subheader("Analytics & Metrics")

if not metrics_df.empty:
    st.dataframe(metrics_df, use_container_width=True)

    if not tickets_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(tickets_df["category"].value_counts())

        with col2:
            st.bar_chart(tickets_df["priority"].value_counts())
else:
    st.info("Metrics not available.")

st.divider()
st.subheader("Processing History")

if not logs_df.empty:
    st.dataframe(logs_df, use_container_width=True)
else:
    st.info("No processing logs found.")
