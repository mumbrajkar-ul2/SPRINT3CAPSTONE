"""The page at /. Stage S07. PRD RQ-62 to RQ-65.

These tests read the page source. They do not run its JavaScript. A person ran the page in a
browser for the demo, and docs/demo/evidence.md says what that run showed.
"""

import re

import pytest

LABELS = {"REAL", "PRECOMPUTED", "SIMULATED", "EDUCATIONAL"}
# The fields of the replies that hold a number.
NUMERIC_NAMES = ("raw_count", "deduped_count", "flagged_count", "row_count", "tokens", "latency_ms", "status")


@pytest.fixture
def page(client):
    response = client.get("/")
    assert response.status_code == 200
    return response.text


def script_of(page):
    return re.search(r"<script>(.*?)</script>", page, re.S).group(1)


def num_calls(script):
    """The arguments of every call of num(), as a list of top-level pieces. The definition is skipped."""
    found = []
    script = re.sub(r"(?m)^\s*//.*$", "", script)  # comments are not calls
    for match in re.finditer(r"(?<![\w.])num\(", script):
        if script[max(0, match.start() - 9):match.start()] == "function ":
            continue
        depth, start, pieces, quote = 1, match.end(), [], None
        for index in range(match.end(), len(script)):
            char = script[index]
            if quote:
                if char == quote:
                    quote = None
                continue
            if char in "\"'":
                quote = char
            elif char in "([{":
                depth += 1
            elif char in ")]}":
                depth -= 1
                if depth == 0:
                    pieces.append(script[start:index].strip())
                    break
            elif char == "," and depth == 1:
                pieces.append(script[start:index].strip())
                start = index + 1
        found.append(pieces)
    return found


def visible_text(page):
    """The words a reader sees before any script runs. Tags, styles and scripts are removed."""
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", page, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def test_page_serves_and_names_every_demo_step(client, page):
    response = client.get("/")
    assert response.headers["content-type"].startswith("text/html")
    text = visible_text(page)
    for heading in (
        "Step one. Pick a storm and read its alarms",
        "Step two. Look up one device",
        "Step three. Ask for a recommendation",
        "Step four. A person decides",
        "Step five. Read the audit chain",
    ):
        assert heading in text
    script = script_of(page)
    # The routes the steps call, and the one case id sent with every call.
    for route in ("/alarms/storms/", "/records/", "/ai/recommend/", "/approvals/", "/audit/", "/health"):
        assert route in script
    assert script.count('"X-Correlation-Id": correlationId') == 1  # one place builds the headers for every call
    assert "X-User-Role" in script
    # The device list comes from the storm reply (rows and held_aside) and skips a blank id.
    assert "data.rows.concat(data.held_aside)" in script
    assert "if (r.device_id && " in script
    # The chosen device is the {id} of the lookup, the recommendation and the decision.
    assert script.count("selectedDevice()") >= 3
    # The page has no way to ask for EXECUTE.
    # EXECUTE appears once, as the name of an outcome whose count the audit table shows (it stays zero).
    assert not re.search(r"api\([^)]*execute", script, re.I)
    assert not re.search(r"/execute", page, re.I)
    assert script.lower().count("execute") == 1


def test_every_number_on_the_page_has_a_label(page):
    script = script_of(page)
    text = visible_text(page)
    # 1. The text before any script runs holds no digit, apart from ids such as STO-00002.
    without_ids = re.sub(r"\b[A-Za-z][\w-]*\d[\w-]*\b", "", text)
    assert not re.search(r"\d", without_ids), without_ids
    # 2. Every call of num() names one of the four labels. badge() refuses any other word.
    calls = num_calls(script)
    assert len(calls) >= 10
    for arguments in calls:
        assert arguments[-1] in {f'"{label}"' for label in LABELS}, arguments
    assert "if (!LABELS.includes(label)) { throw" in script
    # 3. A line that reads a number from a reply shows it through num() or a labelled text helper.
    for name in NUMERIC_NAMES:
        for line in script.splitlines():
            if re.search(rf"\b(data|r|item)\.{name}\b", line) and "if (" not in line and "status !==" not in line:
                assert "num(" in line or "textWithLabel(" in line, line
    # 4. Every status the page shows is labelled REAL.
    assert 'statusChip(status) { return el("span", { class: "status" }, ["HTTP status ", num(status, "REAL")]) }' in script.replace("\n", " ") or 'num(status, "REAL")' in script
    # 5. The four label words are explained to the reader.
    for word in LABELS:
        assert word in text


def test_held_case_shows_the_reason_and_no_text(page):
    script = script_of(page)
    hold_branch = re.search(r"if \(!hasText\) \{(.*?)\n  \} else \{", script, re.S).group(1)
    assert "A person must review this case" in hold_branch
    assert "data.reasons" in hold_branch
    # The branch for a held or blocked reply never reads the two text fields.
    assert "data.summary" not in hold_branch
    assert "data.recommendation" not in hold_branch
    # The text is shown only when the server sent a recommendation sentence.
    assert "const hasText = data.recommendation !== null && data.recommendation !== undefined;" in script
    # Model text goes into the page as text, never as HTML.
    assert "innerHTML" not in script
    assert "insertAdjacentHTML" not in script


def test_page_shows_the_cannot_prove_list_and_the_role_it_sent(page):
    script = script_of(page)
    text = visible_text(page)
    assert "data.cannot_prove" in script
    assert "What this log cannot prove" in script
    assert "Role sent for this read: admin (claimed role)" in script
    assert "Role (claimed)" in script and "Actor (claimed)" in script
    assert "Approver (claimed role, set by the server)" in script
    assert 'api("GET", "/audit/" + encodeURIComponent(correlationId), "admin")' in script
    assert "claimed role" in text
    assert "Nothing proves who the caller is" in text
