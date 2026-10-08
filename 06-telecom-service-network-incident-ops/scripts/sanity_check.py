from pathlib import Path
import csv, json, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    'README.md',
    'requirements.txt',
    'apps/api/main.py',
    'docs/transformation-roadmap.md',
    'docs/domain-specific-spec.md',
    'PRODUCTION_EVIDENCE_PACK_TEMPLATE.md'
]
forbidden = [
    'docs/PARTICIPANT_BRIEF.md',
    'docs/discovery/prompt-pack.md',
    'docs/challenges/moonshot-tasks.md',
    'docs/workshop-scorecard.md'
]
missing = [p for p in required if not (ROOT / p).exists()]
forbidden_present = [p for p in forbidden if (ROOT / p).exists()]
manifest = json.loads((ROOT / 'data' / 'manifest.json').read_text())
row_failures = []
for name, expected in manifest['csv_files'].items():
    path = ROOT / 'data' / 'synthetic' / name
    with path.open(newline='', encoding='utf-8') as f:
        actual = sum(1 for _ in csv.DictReader(f))
    if actual != expected:
        row_failures.append((name, expected, actual))
event_count = sum(1 for _ in (ROOT / 'data' / 'synthetic' / 'events.jsonl').open(encoding='utf-8'))
if missing or forbidden_present or row_failures or event_count != manifest['jsonl_events']:
    print({'missing': missing, 'forbidden_present': forbidden_present, 'row_failures': row_failures, 'event_count': event_count})
    sys.exit(1)
print({'status': 'ok', 'repo': manifest['repo'], 'csv_files': len(manifest['csv_files']), 'events': event_count, 'clean_repo_contract': True})
