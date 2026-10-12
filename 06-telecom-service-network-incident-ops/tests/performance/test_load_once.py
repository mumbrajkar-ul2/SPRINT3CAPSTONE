"""Stage S04-10 Half B. devices.csv is read once, however many calls follow.

The tests count how many times the file is opened. They do not time anything.
Timing is in docs/10-performance/measure.py.

Each test starts and ends with an empty cache, so no test depends on another.
"""

import threading
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from apps.api.main import app
from apps.api.services import audit, domain_service

HEADER = "device_id,hostname,site_id\n"


@pytest.fixture(autouse=True)
def empty_cache():
    domain_service.reset_cache()
    yield
    domain_service.reset_cache()


def count_opens(monkeypatch, target: Path) -> list:
    """Record every time `target` is opened. The real open still runs."""
    opens: list = []
    real_open = Path.open

    def counting_open(self, *args, **kwargs):
        if self == target:
            opens.append(self)
        return real_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", counting_open)
    return opens


def small_csv(tmp_path, monkeypatch, body: str) -> Path:
    """A small devices.csv in a temporary folder. Returns its path."""
    path = tmp_path / domain_service.PRIMARY
    path.write_text(HEADER + body, encoding="utf-8")
    monkeypatch.setattr(domain_service, "DATA_DIR", tmp_path)
    return path


def test_file_is_read_once_across_many_calls(tmp_path, monkeypatch):
    path = small_csv(tmp_path, monkeypatch, "DEV-1,alpha,SIT-1\nDEV-2,beta,SIT-2\n")
    opens = count_opens(monkeypatch, path)
    for index in range(1000):
        domain_service.load_record("DEV-1" if index % 2 == 0 else "DEV-NO-SUCH-ID")
    assert len(opens) == 1


def test_real_file_is_read_once_across_many_calls(monkeypatch):
    path = domain_service.DATA_DIR / domain_service.PRIMARY
    opens = count_opens(monkeypatch, path)
    for _ in range(200):
        assert domain_service.load_record("DEV-00002")["device_id"] == "DEV-00002"
        assert domain_service.load_record("DEV-00003")["device_id"] == "DEV-00003"
    assert len(opens) == 1


def test_reset_makes_the_next_call_read_again(tmp_path, monkeypatch):
    path = small_csv(tmp_path, monkeypatch, "DEV-1,alpha,SIT-1\n")
    opens = count_opens(monkeypatch, path)
    domain_service.load_record("DEV-1")
    domain_service.load_record("DEV-1")
    assert len(opens) == 1
    domain_service.reset_cache()
    domain_service.load_record("DEV-1")
    assert len(opens) == 2


def test_eight_threads_on_the_first_call_read_once(tmp_path, monkeypatch):
    path = small_csv(tmp_path, monkeypatch, "DEV-1,alpha,SIT-1\n")
    opens = count_opens(monkeypatch, path)
    barrier = threading.Barrier(8)
    answers = []

    def worker():
        barrier.wait()
        answers.append(domain_service.load_record("DEV-1")["device_id"])

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert answers == ["DEV-1"] * 8
    assert len(opens) == 1


def test_routes_read_the_file_once(tmp_path, monkeypatch):
    # The audit rows go to a temporary file, not to logs/audit.log.
    monkeypatch.setattr(audit, "LOG", tmp_path / "audit.log")
    path = domain_service.DATA_DIR / domain_service.PRIMARY
    opens = count_opens(monkeypatch, path)
    client = TestClient(app)
    for _ in range(20):
        response = client.get("/records/DEV-00002", headers={"X-User-Role": "operator"})
        assert response.status_code == 200
        assert response.json()["device_id"] == "DEV-00002"
    response = client.post("/ai/summarize/DEV-00002", headers={"X-User-Role": "operator"})
    assert response.status_code == 200
    assert len(opens) == 1


def test_result_is_a_copy(tmp_path, monkeypatch):
    small_csv(tmp_path, monkeypatch, "DEV-1,alpha,SIT-1\n")
    first = domain_service.load_record("DEV-1")
    first["hostname"] = "changed by a caller"
    assert domain_service.load_record("DEV-1")["hostname"] == "alpha"


def test_repeated_id_returns_the_first_row(tmp_path, monkeypatch):
    small_csv(tmp_path, monkeypatch, "DEV-1,first,SIT-1\nDEV-2,other,SIT-2\nDEV-1,second,SIT-3\n")
    assert domain_service.load_record("DEV-1")["hostname"] == "first"


def test_missing_id_still_returns_the_first_row(tmp_path, monkeypatch):
    # Unchanged on purpose. S04-03 and S07 have not changed this (defect F01).
    small_csv(tmp_path, monkeypatch, "DEV-1,first,SIT-1\nDEV-2,other,SIT-2\n")
    assert domain_service.load_record("DEV-NO-SUCH-ID")["device_id"] == "DEV-1"


def test_empty_file_gives_the_error_body(tmp_path, monkeypatch):
    small_csv(tmp_path, monkeypatch, "")
    assert domain_service.load_record("DEV-1") == {"error": "missing"}


def test_only_device_id_is_matched(tmp_path, monkeypatch):
    # Decision 1 of 2026-10-11. A site id or a hostname no longer finds a row (defect F17).
    small_csv(tmp_path, monkeypatch, "DEV-1,first,SIT-1\nDEV-2,other,SIT-2\n")
    assert domain_service.load_record("SIT-2")["device_id"] == "DEV-1"
    assert domain_service.load_record("other")["device_id"] == "DEV-1"
    assert domain_service.load_record("DEV-2")["device_id"] == "DEV-2"


def test_every_device_id_in_the_real_file_finds_its_first_row():
    import csv

    path = domain_service.DATA_DIR / domain_service.PRIMARY
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    first_row = {}
    for row in rows:
        first_row.setdefault(row["device_id"], row)
    assert len(first_row) == 351
    for device_id, expected in first_row.items():
        assert domain_service.load_record(device_id) == expected


def test_a_missing_file_raises_and_is_not_cached(tmp_path, monkeypatch):
    # The failure shows on the first call. The next call tries again.
    monkeypatch.setattr(domain_service, "DATA_DIR", tmp_path)
    with pytest.raises(FileNotFoundError):
        domain_service.load_record("DEV-1")
    (tmp_path / domain_service.PRIMARY).write_text(HEADER + "DEV-1,alpha,SIT-1\n", encoding="utf-8")
    assert domain_service.load_record("DEV-1")["device_id"] == "DEV-1"
