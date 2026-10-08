from apps.api.services import domain_service

def test_legacy_missing_record_behavior_is_characterized():
    row = domain_service.load_record('DOES-NOT-EXIST')
    assert isinstance(row, dict)
    # This captures current brownfield behavior; transformation should replace it with 404 semantics.
    assert row
