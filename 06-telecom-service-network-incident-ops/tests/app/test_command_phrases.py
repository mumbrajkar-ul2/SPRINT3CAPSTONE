"""Command text in a recommendation. Stage S07. PRD RQ-30 and RQ-71.

The start list (D-08) has seven phrases. The near-miss list is a PROPOSED draft in
semantic-layer/ai-context-policy.yaml (ADR 0005). Both lists miss phrases that mean the same.
"""

import json

import pytest

from apps.api.services import ai_gateway
from tests.app.helpers import GOOD_ID, OPERATOR

REASON = "failmode.command_text_in_recommendation"
START_LIST = ("reboot", "restart", "shut down", "delete", "clear config", "push config", "apply")


def recommend(client):
    return client.post(f"/ai/recommend/{GOOD_ID}", headers=OPERATOR)


def assert_held_with_no_text(client, audit_log, phrase_text):
    response = recommend(client)
    assert response.status_code == 202
    body = response.json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["summary"] is None
    assert body["recommendation"] is None
    assert body["reasons"] == [REASON]
    assert phrase_text not in response.text
    rows = audit_log()
    assert [row["action"] for row in rows] == ["policy.hold"]
    assert rows[0]["outcome"] == "HOLD_FOR_REVIEW"
    # The audit row stores the action word and the outcome. It stores no reason and no text.
    assert "failmode" not in json.dumps(rows[0])
    assert phrase_text not in json.dumps(rows[0])


def test_the_start_list_is_the_seven_phrases_of_decision_d_08():
    assert set(START_LIST) <= set(ai_gateway.RECOMMEND_COMMAND_PHRASES)
    assert len(ai_gateway.RECOMMEND_COMMAND_PHRASES) == len(START_LIST)


@pytest.mark.parametrize("phrase", START_LIST)
def test_each_listed_phrase_is_held_with_no_text(client, fake_model, audit_log, phrase):
    text = f"Please {phrase} on this device tonight"
    fake_model(recommendation=text)
    assert_held_with_no_text(client, audit_log, text)


@pytest.mark.parametrize("phrase", START_LIST)
def test_a_listed_phrase_in_capitals_or_in_the_summary_is_held(client, fake_model, audit_log, phrase):
    text = f"Plan to {phrase.upper()} soon"
    fake_model(summary=text)
    assert_held_with_no_text(client, audit_log, text)


@pytest.mark.parametrize("phrase", ai_gateway.RECOMMEND_NEAR_MISS_PHRASES)
def test_a_near_miss_phrase_is_held(client, fake_model, audit_log, phrase):
    text = f"The next step is to {phrase} for this device"
    fake_model(recommendation=text)
    assert_held_with_no_text(client, audit_log, text)


def test_the_near_miss_list_is_not_empty_and_shares_no_entry_with_the_start_list():
    assert ai_gateway.RECOMMEND_NEAR_MISS_PHRASES
    assert not set(ai_gateway.RECOMMEND_NEAR_MISS_PHRASES) & set(ai_gateway.RECOMMEND_COMMAND_PHRASES)


def test_a_phrase_inside_a_longer_word_is_not_held(client, fake_model):
    # Whole words only. "reapplied" holds the listed word "applied" inside a longer word.
    fake_model(recommendation="Review the reapplied checklist and the prerestart notes")
    body = recommend(client).json()
    assert body["outcome"] == "HOLD_FOR_REVIEW"
    assert body["recommendation"] is not None
    assert body["reasons"] == ["ai_use.next_action_recommendation"]


def test_a_phrase_that_is_not_on_either_list_gets_through():
    # Limit (D-08, SB-05). The lists are short. A phrase that means the same as a listed one,
    # but is not listed, is shown. A person reads the sentence before any decision.
    assert ai_gateway.answer_check_reasons("x", "cycle the power of the chassis", {}) == []
