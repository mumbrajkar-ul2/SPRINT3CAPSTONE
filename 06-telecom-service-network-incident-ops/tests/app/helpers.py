"""Constants shared by the tests in tests/app. Stage S07."""

OPERATOR = {"X-User-Role": "operator"}
ENGINEER = {"X-User-Role": "engineer"}
ADMIN = {"X-User-Role": "admin"}

# Rows in data/synthetic/devices.csv (verified on 2026-10-13).
GOOD_ID = "DEV-00002"  # stale_topology_flag false. Storm STO-00002 lists it.
STALE_ID = "DEV-00003"  # stale_topology_flag true
BLANK_FLAG_ID = "DEV-BAD1"  # stale_topology_flag blank
MISSING_ID = "DEV-00001"  # in alarms.csv (storm STO-00001), not in devices.csv
