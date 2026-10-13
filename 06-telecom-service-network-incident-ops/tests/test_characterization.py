from apps.api.services import domain_service


def test_missing_record_returns_nothing():
    # S07 (PRD RQ-03). Replaces test_legacy_missing_record_behavior_is_characterized.
    # That test locked the first-row fallback. A missing id now gives back None.
    assert domain_service.load_record('DOES-NOT-EXIST') is None
