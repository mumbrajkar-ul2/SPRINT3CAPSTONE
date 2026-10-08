from fastapi.testclient import TestClient
from apps.api.main import app

client = TestClient(app)

def test_health_contract():
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'ok'

def test_ai_summary_has_minimum_contract():
    r = client.post('/ai/summarize/REC-0001')
    assert r.status_code == 200
    body = r.json()
    assert 'summary' in body
    assert 'model' in body
    assert 'guardrail_status' in body
