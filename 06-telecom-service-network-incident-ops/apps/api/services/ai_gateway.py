import os, time

MODEL_VERSION = "local-sim-v1"
PROMPT_TEMPLATE = "Summarize this operational record and recommend next action: {record}"

def summarize_record(record: dict):
    # Brownfield issues: prompt is hardcoded, untrusted fields are interpolated, no schema validation.
    prompt = PROMPT_TEMPLATE.format(record=record)
    time.sleep(0.01)
    token_estimate = len(prompt.split()) * 2
    return {
        "model": MODEL_VERSION,
        "summary": "Synthetic summary for " + str(next(iter(record.values()), "unknown")),
        "recommendation": "Review and approve before action",
        "token_estimate": token_estimate,
        "source_count": 1,
        "guardrail_status": "not_enforced"
    }
