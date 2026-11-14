
"""Run the Week 4 evaluation against the real Netixsol agent.

Safety:
- Disables the n8n webhook.
- Blocks the confirmation function.
- Never supplies a confirmation token.
- Resets conversation state between questions.
- Preserves the original evaluation CSV.
"""

import csv
import json
import re
from pathlib import Path

import agent


WEEK4 = Path(__file__).resolve().parent
INPUT_CSV = WEEK4 / "capstone_evaluation_results.csv"
OUTPUT_CSV = WEEK4 / "eval_final.csv"
EVIDENCE_JSON = WEEK4 / "eval_retrieval_evidence.json"

OUTPUT_COLUMNS = [
    "id",
    "question",
    "category",
    "answer",
    "finish_reason",
    "cited_sources",
    "retrieved_sources",
    "grounded",
    "behaviour_ok",
    "unsupported_claims",
    "notes",
]


def extract_urls(text):
    """Extract URLs actually present in the generated answer."""
    found = re.findall(r"https?://[^\s)\]>,\"']+", text or "")
    cleaned = []
    for url in found:
        url = url.rstrip(".,;:")
        if url not in cleaned:
            cleaned.append(url)
    return cleaned


def unique_urls(matches):
    """Collect unique source URLs from retrieved chunks."""
    urls = []
    for match in matches:
        url = match.get("source_url", "")
        if url and url not in urls:
            urls.append(url)
    return urls


def blocked_confirmation(*args, **kwargs):
    """Emergency safety block: evaluation must never submit an enquiry."""
    return {
        "status": "blocked",
        "reason": "Evaluation mode blocks all enquiry submissions.",
        "submitted": False,
    }


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Evaluation questions not found: {INPUT_CSV}")

    with INPUT_CSV.open("r", newline="", encoding="utf-8-sig") as file:
        questions = list(csv.DictReader(file))

    if len(questions) != 10:
        raise ValueError(
            f"Expected 10 evaluation questions, found {len(questions)}."
        )

    # Additional safety: no external enquiry delivery during evaluation.
    agent.N8N_WEBHOOK_URL = None
    agent.confirm_and_send = blocked_confirmation

    # Capture every actual retrieval made by the agent.
    original_search = agent.search_netixsol
    all_rows = []
    evidence_records = []

    def traced_search(query):
        result = original_search(query)
        evidence_records.append({
            "current_question_id": current_question_id[0],
            "query": query,
            "matches": result.get("matches", []),
        })
        return result

    current_question_id = [None]
    agent.search_netixsol = traced_search

    try:
        for item in questions:
            question_id = item["id"]
            question = item["question"]
            category = item["category"]

            print("\n" + "=" * 70)
            print(f"Evaluation {question_id}/10: {question}")
            print("=" * 70)

            # Each question starts with a clean conversation and no preview.
            agent.conversation_history = []
            agent.pending_preview = None
            agent.last_turn_finish_reasons = []
            current_question_id[0] = question_id

            start_evidence_count = len(evidence_records)

            try:
                answer = agent.run_agent_turn(question)
                answer = str(answer)

            except Exception as exc:
                answer = f"ERROR: {type(exc).__name__}: {str(exc)[:500]}"
                print(answer)

            reasons = list(agent.last_turn_finish_reasons)

            question_evidence = evidence_records[start_evidence_count:]
            retrieved_matches = [
                match
                for record in question_evidence
                for match in record["matches"]
            ]

            cited = extract_urls(answer)
            retrieved = unique_urls(retrieved_matches)

            # Do not automatically award scores. These require human review.
            notes = "Manual grounding and behaviour review required."
            if answer.startswith("ERROR:"):
                notes = (
                    "Gemini or agent error. Investigate before scoring; "
                    "do not treat an API failure as a successful answer."
                )

            if agent.pending_preview is not None:
                preview_status = "preview_created_not_submitted"
            else:
                preview_status = "no_pending_preview"

            all_rows.append({
                "id": question_id,
                "question": question,
                "category": category,
                "answer": answer,
                "finish_reason": "; ".join(reasons) if reasons else "NO_RESPONSE",
                "cited_sources": json.dumps(cited, ensure_ascii=False),
                "retrieved_sources": json.dumps(retrieved, ensure_ascii=False),
                "grounded": "",
                "behaviour_ok": "",
                "unsupported_claims": "",
                "notes": notes,
            })

            evidence_records.append({
                "current_question_id": question_id,
                "evaluation_metadata": {
                    "finish_reasons": reasons,
                    "preview_status": preview_status,
                    "submission_blocked": True,
                    "webhook_disabled": True,
                },
            })

            print(f"\nFinish reasons: {reasons or 'No Gemini response'}")
            print(f"Cited sources: {len(cited)}")
            print(f"Retrieved sources: {len(retrieved)}")
            print(f"Preview status: {preview_status}")
            print("Submission: BLOCKED")

            # Clear any preview so it cannot affect the next question.
            agent.pending_preview = None
            agent.conversation_history = []

    finally:
        agent.search_netixsol = original_search
        agent.pending_preview = None
        agent.conversation_history = []

    # Save the required evaluation CSV.
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(all_rows)

    # Save retrieved chunk text separately for manual grounding review.
    with EVIDENCE_JSON.open("w", encoding="utf-8") as file:
        json.dump(evidence_records, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("EVALUATION RUN FINISHED")
    print("=" * 70)
    print(f"Evaluation CSV: {OUTPUT_CSV}")
    print(f"Retrieved evidence: {EVIDENCE_JSON}")
    print(f"Questions processed: {len(all_rows)}")
    print("Grounding and behaviour scores: NOT YET ASSIGNED")
    print("External enquiry submissions: BLOCKED")


if __name__ == "__main__":
    main()
