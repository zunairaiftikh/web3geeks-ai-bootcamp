# Week 4 Capstone: Netixsol AI Client Intake & Project Scoping Agent

## Evaluation Results

| Metric | Result |
|---|---:|
| Questions evaluated | 10 |
| Groundedness score | 20/20 |
| Behaviour checks passed | 10/10 |

Scores were manually recorded against retrieved evidence. See `eval_final.csv` and `eval_retrieval_evidence.json`.

## Project Overview

This project is a Retrieval-Augmented Generation (RAG) AI agent for Netixsol. It answers prospective client questions using approved company information and helps clients prepare structured project enquiries.

## Problem and Target Audience

Prospective clients need accurate information about Netixsol services and guidance when describing their software projects.

The target audience includes businesses interested in AI agents, blockchain development, DeFi, and product engineering.

## Technologies Used

- Python 3.14.7
- Google Gemini API
- ChromaDB
- Pydantic
- Streamlit
- python-dotenv
- Requests
- n8n webhook integration
- Google Sheets

## System Architecture

1. User submits a question through the Streamlit chat interface.
2. The agent retrieves relevant information from ChromaDB.
3. Gemini generates an answer using retrieved information.
4. The agent asks follow-up questions to understand project requirements.
5. Pydantic validates the enquiry information.
6. The user reviews an enquiry preview.
7. The user must provide the exact confirmation token.
8. The configured n8n webhook can process the confirmed enquiry.

## Installation and Setup

Run these commands from the repository root:

    .\.venv\Scripts\Activate.ps1
    python -m pip install -r .\week4\requirements-day3.txt
    python -m pip install streamlit

Create `week4/.env` using the variable names in `.env.example`. Add your own API credentials locally. Never commit secrets.

## Run the Application

    python -m streamlit run .\week4\app.py

The application provides a chat interface, displays relevant sources, and supports project enquiry previews.

## Evaluation Method

The final evaluation contains 10 questions. Each answer was reviewed against retrieved evidence.

Groundedness scoring:

- 2: Supported by retrieved evidence and cited, or a correct refusal/scoping response.
- 1: Mostly supported but contains one unsupported detail or missing source.
- 0: Invented facts or an unsafe/incorrect action.

The evaluation file records answers, finish reasons, cited sources, retrieved sources, groundedness, behaviour checks, unsupported claims, and notes.

## Application and Safety Tests

The application was tested with questions about services, DEX development, pricing, delivery guarantees, website requirements, and confidential client information.

The offline self-test passed:

- Exact-preview confirmation checks
- Duplicate prevention
- Changed-preview token invalidation
- Injection protection
- Email validation
- Project category validation
- Consent validation

The webhook was mocked during the offline self-test. No real external request was made.

A separate two-browser-tab test confirmed that a confirmation token from one tab could not confirm the other tab's pending preview.

## Guardrails

- Answers should use retrieved Netixsol information.
- The agent must not invent prices or delivery guarantees.
- Confidential client information must not be disclosed.
- Enquiry information is validated.
- User consent is required.
- A preview must be reviewed before confirmation.
- Only the exact confirmation token approves that preview.
- Duplicate saved enquiry IDs are blocked.

## Limitations and Future Improvements

The current knowledge base is small. For a larger collection of approximately 200 pages, improvements could include:

- Better document chunking and metadata.
- Hybrid keyword and semantic retrieval.
- Tuning the number of retrieved chunks (top-k).
- Similarity thresholds and reranking.
- Precision and recall evaluation.
- More out-of-scope question testing.
- Persistent storage, monitoring, and stronger concurrent-session handling.

## Reflection

The initial retrieval experiment used a small corpus of five chunks and retrieved four. This is a useful prototype test but does not establish performance on a large knowledge base.

For a larger corpus, I would improve chunking, metadata filtering, retrieval quality, and evaluation using both in-scope and out-of-scope questions.

## Main Project Files

- `agent.py` - Agent, retrieval, and tool logic.
- `app.py` - Streamlit user interface.
- `run_evaluation.py` - Evaluation runner.
- `eval_final.csv` - Final evaluation results.
- `eval_retrieval_evidence.json` - Retrieved evidence.
- `rag_results.csv` - RAG test results.
- `requirements-day3.txt` - Project dependencies.
- `.env.example` - Environment variable names only.
- `slides.pdf` - Capstone presentation.
