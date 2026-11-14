
"""Safely rerun only the failed Week 4 evaluation questions."""

import csv
import json
import re
from pathlib import Path

import agent

WEEK4 = Path(__file__).resolve().parent
OUTPUT_CSV = WEEK4 / "eval_final.csv"
EVIDENCE_JSON = WEEK4 / "eval_retest_evidence.json"
TARGET_IDS = {"3", "5", "6", "7"}

OUTPUT_COLUMNS = [
    "id", "question", "category", "answer", "finish_reason",
    "cited_sources", "retrieved_sources", "grounded",
    "behaviour_ok", "unsupported_claims", "notes",
]


def extract_urls(text):
    found = re.findall(r"https?://[^\s)\]>,\"']+", text or "")
    result = []
    for url in found:
        url = url.rstrip(".,;:")
        if url not in result:
            result.append(url)
    return result


def unique_urls(matches):
    urls = []
    for match in matches:
        url = match.get("source_url", "")
        if url and url not in urls:
            urls.append(url)
    return urls


def blocked_confirmation(*args, **kwargs):
    return {
        "status": "blocked",
        "reason": "Evaluation mode blocks all enquiry submissions.",
        "submitted": False,
    }


def main():
    if not OUTPUT_CSV.exists():
        raise FileNotFoundError(f"Missing evaluation CSV: {OUTPUT_CSV}")

    with OUTPUT_CSV.open("r", newline="", encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    if len(rows) != 10:
        raise ValueError(f"Expected 10 rows, found {len(rows)}.")

    found_ids = {row["id"] for row in rows}
    if not TARGET_IDS.issubset(found_ids):
        raise ValueError("One or more target question IDs are missing.")

    # Preserve original safety settings and restore them afterwards.
    original_webhook = agent.N8N_WEBHOOK_URL
    original_confirmation = agent.confirm_and_send
    original_search = agent.search_netixsol

    agent.N8N_WEBHOOK_URL = None
    agent.confirm_and_send = blocked_confirmation

    current_question_id = [None]
    evidence_records = []

    def traced_search(query):
        result = original_search(query)
        evidence_records.append({
            "current_question_id": current_question_id[0],
            "query": query,
            "matches": result.get("matches", []),
        })
        return result

    agent.search_netixsol = traced_search

    try:
        for row in rows:
            question_id = row["id"]

            if question_id not in TARGET_IDS:
                continue

            print("\n" + "=" * 65)
            print(f"Retesting question {question_id}: {row['question']}")
            print("=" * 65)

            current_question_id[0] = question_id
            agent.conversation_history = []
            agent.pending_preview = None
            agent.last_turn_finish_reasons = []

            start_count = len(evidence_records)

            try:
                answer = str(agent.run_agent_turn(row["question"]))
            except Exception as exc:
                answer = f"ERROR: {type(exc).__name__}: {str(exc)[:500]}"

            reasons = list(agent.last_turn_finish_reasons)

            question_evidence = evidence_records[start_count:]
            matches = [
                match
                for record in question_evidence
                for match in record["matches"]
            ]

            row["answer"] = answer
            row["finish_reason"] = (
                "; ".join(reasons) if reasons else "NO_RESPONSE"
            )
            row["cited_sources"] = json.dumps(
                extract_urls(answer), ensure_ascii=False
            )
            row["retrieved_sources"] = json.dumps(
                unique_urls(matches), ensure_ascii=False
            )

            # These questions must be manually rescored after the rerun.
            row["grounded"] = ""
            row["behaviour_ok"] = ""
            row["unsupported_claims"] = ""
            row["notes"] = (
                "Retested after prompt improvement. "
                "Manual grounding and behaviour rescoring required."
            )

            evidence_records.append({
                "current_question_id": question_id,
                "evaluation_metadata": {
                    "finish_reasons": reasons,
                    "submission_blocked": True,
                    "webhook_disabled": True,
                },
            })

            print(f"Finish reasons: {reasons}")
            print(f"Retrieved sources: {unique_urls(matches)}")
            print("External submission: BLOCKED")

            agent.pending_preview = None
            agent.conversation_history = []

    finally:
        agent.search_netixsol = original_search
        agent.confirm_and_send = original_confirmation
        agent.N8N_WEBHOOK_URL = original_webhook
        agent.pending_preview = None
        agent.conversation_history = []

    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    with EVIDENCE_JSON.open("w", encoding="utf-8") as file:
        json.dump(evidence_records, file, indent=2, ensure_ascii=False)

    print("\n" + "=" * 65)
    print("TARGETED RETEST COMPLETE")
    print(f"Updated CSV: {OUTPUT_CSV}")
    print(f"New evidence: {EVIDENCE_JSON}")
    print("Questions retested: 3, 5, 6, 7")
    print("Manual scores for retested questions: CLEARED FOR RESCORING")
    print("Other six questions: PRESERVED")
    print("External enquiry submissions: BLOCKED")


if __name__ == "__main__":
    main()
