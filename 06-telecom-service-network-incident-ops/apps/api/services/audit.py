import json
import threading
import uuid
from datetime import datetime
from pathlib import Path

_WRITE_LOCK = threading.Lock()

LOG = Path(__file__).resolve().parents[3] / "logs" / "audit.log"

# Persona word stored in actor. operator and engineer follow the Inference in
# access-semantics.yaml. ai_agent is the persona name. Other header words have
# no persona, so actor stays null.
_ACTOR_FOR_ROLE = {
    "operator": "noc_operator",
    "engineer": "network_engineer",
    "ai_agent": "ai_agent",
}

SCHEMA_KEYS = (
    "ts",
    "correlation_id",
    "actor",
    "role",
    "action",
    "resource",
    "policy_decision",
    "approval_id",
    "model",
    "model_version",
    "prompt_hash",
    "tokens",
    "latency_ms",
    "outcome",
    # S04-12 Half B. A fifteenth key. It says how `tokens` was worked out, so the
    # EDUCATIONAL label travels with the number. Null when `tokens` is null.
    # Open question for S03: the YAML and log-schema.md have no id for this field.
    "token_estimate_method",
)


def correlation_id_from_header(value):
    """Keep a non-empty header. A missing or blank header becomes a new UUID."""
    if value is None:
        return str(uuid.uuid4())
    text = str(value).strip()
    if text == "":
        return str(uuid.uuid4())
    return text


def actor_for_role(role):
    """Persona word for a role header. None when the header has no persona."""
    if role is None:
        return None
    return _ACTOR_FOR_ROLE.get(str(role).strip())


def write_event(
    action,
    *,
    correlation_id,
    actor,
    role,
    resource,
    outcome=None,
    model=None,
    model_version=None,
    prompt_hash=None,
    tokens=None,
    latency_ms=None,
    token_estimate_method=None,
):
    """Append one audit row. policy_decision and approval_id stay null.

    Stage S04-12 Half B: `token_estimate_method` names the formula behind `tokens`.
    It is stored only when `tokens` has a value. A row with no token count has no method.

    Stage S04-09: the five provenance values are written when a model call
    ran. They stay null on a call that stopped before the model. The row
    never stores the prompt text, mgmt_ip, credential_profile, or a secret.
    prompt_hash stands in for the prompt text.
    """
    if correlation_id is None or str(correlation_id).strip() == "":
        raise ValueError("correlation_id is required")
    event = {
        "ts": datetime.utcnow().isoformat(),
        "correlation_id": str(correlation_id).strip(),
        "actor": actor,
        "role": role,
        "action": action,
        "resource": resource,
        "policy_decision": None,
        "approval_id": None,
        "model": model,
        "model_version": model_version,
        "prompt_hash": prompt_hash,
        "tokens": tokens,
        "latency_ms": latency_ms,
        "outcome": outcome,
        "token_estimate_method": token_estimate_method if tokens is not None else None,
    }
    line = json.dumps(event) + "\n"
    # Stage S04-11 Half B (decision D-3). One thread writes at a time. Without the lock,
    # 8 threads writing 250 rows each lost 71 to 109 of 2000 rows on Windows
    # (docs/11-reliability/probe-output.json, check P9). The lock covers one process.
    # Two server processes still write the same file without a lock between them.
    with _WRITE_LOCK:
        LOG.parent.mkdir(exist_ok=True)
        with LOG.open("a", encoding="utf-8") as handle:
            handle.write(line)
