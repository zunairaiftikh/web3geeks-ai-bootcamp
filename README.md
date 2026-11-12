
cd F:\web3geeks-ai-bootcamp

@'
# Web3 Geeks AI Bootcamp

This repository contains my practical projects and exercises completed during the Web3 Geeks AI Bootcamp.

## Project structure

- `week1/` — Data analysis, NumPy, pandas and data cleaning.
- `week2/` — Machine learning, regression, classification and SQL.
- `week3/` — Machine learning application, model evaluation and deployment exercises.
- `week4/` — RAG-based AI agent and automated client enquiry workflow.

## Week 4 Capstone

### Netixsol AI Client Intake & Project Scoping Agent

**Project type:** Retrieval-Augmented Generation (RAG), AI Agent and Automation.

**Technology:**
- Python
- Google Gemini
- ChromaDB
- Pydantic
- n8n Webhook
- Google Apps Script
- Google Sheets

### Project purpose

The agent answers questions using approved Netixsol documentation and helps prospective clients prepare structured project enquiries.

### Main capabilities

1. Retrieves relevant information from a ChromaDB knowledge base.
2. Generates responses using Gemini.
3. Collects client enquiry information.
4. Validates email, project category and consent.
5. Displays an enquiry preview before submission.
6. Requires exact human confirmation before sending.
7. Prevents duplicate submissions.
8. Sends confirmed enquiries through an n8n webhook to Google Sheets.

### Security and validation

The application includes:
- Input validation.
- Explicit consent checking.
- Human confirmation.
- Preview invalidation when enquiry details change.
- Duplicate prevention.
- Bounded tool execution.
- Tool activity logging.

### Testing

The local self-test passed for:
- Exact-preview confirmation.
- Duplicate prevention.
- Changed-preview tokens.
- Prompt-injection handling.
- Email validation.
- Category validation.
- Consent validation.

Webhook delivery was mocked during the local self-test. A separate real test was documented as successfully reaching Google Sheets.

The 10-question evaluation dataset is included. A complete scored evaluation report remains to be documented.

### Installation

Open PowerShell in the `week4` directory:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-day3.txt
```

Create a private `.env` file using `.env.example` as a template and configure the required credentials locally.

Never commit `.env` or publish API keys and webhook secrets.

### Run

```powershell
python agent.py
```

Follow the agent prompts. An enquiry must be previewed and explicitly confirmed before external submission.

### Important files

- `week4/agent.py` — Main agent implementation.
- `week4/agent_demo.md` — Demo and testing documentation.
- `week4/capstone/capstone_proposal.md` — Capstone proposal.
- `week4/eval_questions.csv` — Evaluation questions.
- `week4/capstone_evaluation_results.csv` — Evaluation records.
- `week4/agent_log.csv` — Tool activity log.
- `week4/prompts/` — System prompt versions.

### Project status

The core agent and enquiry workflow have been demonstrated. Remaining submission work includes screenshot evidence, a scored evaluation report, and final security-key rotation.

'@ | Set-Content -Path .\README.md -Encoding UTF8

Write-Host "Main README created successfully."
