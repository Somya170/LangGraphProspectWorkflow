🧠 LangGraph Prospect Workflow

LangGraphProspectWorkflow is an AI-driven automation system that streamlines the process of prospect identification, enrichment, scoring, outreach, and response tracking using LangGraph and autonomous agents.

⚙️ Features

🔍 Prospect Search Agent – Finds potential leads based on criteria.

🧩 Data Enrichment Agent – Enhances prospect data using APIs.

🧠 Scoring Agent – Assigns scores to prioritize leads.

✉️ Outreach Content Agent – Crafts personalized outreach messages.

🚀 Outreach Executor Agent – Automates outreach delivery.

📊 Response Tracker Agent – Tracks responses for analytics.

🔁 Feedback Trainer Agent – Continuously improves model performance.

🧩 Project Structure
LangGraphProspectWorkflow/
│
├── agents/
│   ├── data_enrichment_agent.py
│   ├── feedback_trainer_agent.py
│   ├── langgraph_builder.py
│   ├── outreach_content_agent.py
│   ├── outreach_executor_agent.py
│   ├── prospect_search_agent.py
│   ├── response_tracker_agent.py
│   ├── scoring_agent.py
│
├── workflow.json
├── requirements.txt
├── .env
└── venv/

🚀 Setup Instructions

Clone the repository

git clone https://github.com/Somya170/LangGraphProspectWorkflow.git
cd LangGraphProspectWorkflow


Create and activate virtual environment

python -m venv venv
venv\Scripts\activate   # for Windows


Install dependencies

pip install -r requirements.txt


Set up environment variables

Create a .env file in the root directory and add your API keys or credentials.

Run the workflow

python agents/langgraph_builder.py

📦 Requirements

All dependencies are listed in requirements.txt.

🧑‍💻 Author

Somya Jaiswal
GitHub
 | LinkedIn
