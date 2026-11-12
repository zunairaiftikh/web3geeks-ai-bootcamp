# Netixsol AI Client Intake & Project Scoping Agent

**Project type:** RAG + AI Agent + Automation  
**Target users:** Prospective Netixsol clients  
**Delivery goal:** Working Friday demo

## 1. Problem, users and proposed value

Prospective clients exploring software, AI or blockchain services need a clear way to understand relevant capabilities and explain their project requirements. Initial enquiries can require repeated clarification and manual routing.

This prototype will:
- answer service questions from approved sources;
- gather a concise project brief; and
- prepare an enquiry for human review.

This is a proposed use case; the actual workflow and business need will be validated with a Netixsol mentor.

## 2. Knowledge sources and permissions

Initial sources: approved, publicly accessible Netixsol website pages describing the company, service areas and published engagement process. Target: 5–8 pages (final page count and extracted word count to be recorded during ingestion).

Boundaries and permissions:
- No private client records or confidential internal documents will be used.
- Public availability does not itself establish permission for every use; source selection and educational-prototype use will be confirmed with the mentor.
- If approval is not granted, only alternative materials explicitly approved by the mentor will be used.

## 3. Example questions and expected answers

| Example question | Expected agent behaviour |
|---|---|
| What services does Netixsol offer? | Summarize only service areas supported by retrieved pages and cite the relevant source. |
| Can you help scope a decentralized exchange with wallet integration? | Retrieve relevant published blockchain/DeFi information, then ask focused questions about network, existing contracts and required components. |
| What happens after I submit a project brief? | Describe the documented engagement steps; do not invent timelines, prices or guarantees. |

## 4. Real action and guardrail

After collecting the customer's project description and optional contact details, the agent will show a structured enquiry preview. Only after explicit confirmation will it create one row in an approved Google Sheet (or call an approved n8n webhook), recording category, requirements, consent/status and timestamp.

The action is deliberately limited to creating a pending enquiry:
- no pricing, commitments, project acceptance, contract changes or external messages;
- only necessary information is collected, and sensitive data is not stored; and
- every enquiry carries a human-review status.

## 5. Evaluation plan

Test 10 questions covering service discovery, project scoping, engagement process and out-of-scope requests. For each, record retrieved sources, answer correctness and groundedness.

Groundedness rubric:
1. Unsupported
2. Mostly unsupported
3. Partly supported
4. Mostly supported
5. Fully supported by retrieved evidence

Report mean groundedness score (out of 5), count of answers containing unsupported material claims, whether the agent correctly abstains when evidence is missing, and verification of the confirmation gate and successful creation of a single test row.

## 6. Build plan, deliverables and scope control

| Day | Focus |
|---|---|
| Monday | Prompt design and structured project-intake output. |
| Tuesday | Approved-source ingestion, chunking, embeddings, ChromaDB retrieval and five source-grounded examples. |
| Wednesday | Intake agent and confirmed Google Sheets/n8n action. |
| Thursday | 10-question evaluation, groundedness review, FastAPI or Streamlit interface and demo rehearsal. |
| Friday | Runnable prototype, source-backed answers, controlled enquiry action, test results and short demo. |

If time is limited, advanced UI and multi-step agent autonomy will be cut first. The priorities to preserve are reliable retrieval, clear abstention, human confirmation and one working action.
