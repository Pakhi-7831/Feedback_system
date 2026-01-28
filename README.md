# Feedback_system

This project implements a multi-agent AI pipeline that processes user feedback from multiple sources (app store reviews and support emails), extracts actionable insights, generates structured engineering tickets, and provides a human-in-the-loop Streamlit dashboard for monitoring, overrides, and analytics.

The system is designed to be fully offline, reproducible, and API-agnostic, emphasizing explainable AI agents rather than external LLM dependencies.

While we have used sample datasets as input files (in the folder data) to test our project, user may use any dataset, provided it follows the required structuring, to test the project. 


---

## ✨ Features

* **Automated Feedback Ingestion**: Reads and normalizes user feedback from CSV files (app store reviews & support emails).
* **AI-Driven Classification**: Classifies feedback into:Bug, Feature Request, Praise, Complaint, Spam

---

## 🛠️ Tech Stack

* **Backend & Agents**: Python (Rule-based AI / NLP heuristics)
* **Data Processing**: Pandas
* **Dashboard**: Streamlit
* **Architecture**: Modular Multi-Agent Pipeline

---

## Getting Started

### Prerequisites

*   Python 3.8 - 3.10.1
*   pip
*   virtual environment

### Installation

1.  Clone the repository:

        git clone https://github.com/your-username/agentic-feedback-system
    
        cd Feedback-system

2.  Create and activate a virtual environment:

        python -3.10 -m venv .venv
        source .venv/bin/activate
    On Windows, use

        .venv\Scripts\activate
    

5.  Install the required packages:

        pip install -r requirements.txt
    

### Running the Application

* **Running the backend pipeline**
1. Run the following command:

        python pipeline.py
After succesful execution, the following files should be created: 

  outputs/
    ├── generated_tickets.csv
    ├── processing_log.csv
    └── metrics.csv


2.  Run the Streamlit dashboard:

        streamlit run dashboard/app.py
    

2.  Open your browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

