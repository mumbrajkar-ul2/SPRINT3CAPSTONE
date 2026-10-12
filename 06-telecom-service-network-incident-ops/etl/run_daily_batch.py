import argparse, csv, sys
from pathlib import Path

# Stage S04-11 Half B. `processed`, `malformed`, and `sample` mean what they meant before.
# `malformed` still counts rows with a blank cell. `quarantined` is new. It counts every row
# held aside: a blank cell, a short row, a long row, and a row with bytes that are not valid
# UTF-8. The run goes on with the rest. Each held-aside row is named on stderr by file line.
# No file is written (operating contract rows 1 and 6). Decision D-7.
# Open question for S03: the YAML has no rule id for "a bad row is held aside and the batch
# goes on". metric.quarantine_rate counts such rows.


def bad_row_reason(row):
    """Why a row is held aside, or None when it is fine."""
    if None in row:
        return "long row"
    if any(v is None for v in row.values()):
        return "short row"
    for v in row.values():
        try:
            v.encode('utf-8')
        except UnicodeEncodeError:
            return "bytes that are not valid UTF-8"
    if any(v == '' for v in row.values()):
        return "blank cell"
    return None


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sample', action='store_true')
    args=parser.parse_args()
    data=Path(__file__).resolve().parents[1]/'data'/'synthetic'/'devices.csv'
    bad=0; total=0; quarantined=0; last_error_line=-1
    # surrogateescape keeps a bad byte as a marker instead of stopping the run.
    with data.open(newline='', encoding='utf-8', errors='surrogateescape') as f:
        reader = csv.DictReader(f)
        while True:
            try:
                row = next(reader)
            except StopIteration:
                break
            except csv.Error as err:
                if reader.line_num == last_error_line:
                    break  # the reader did not move on, so stop instead of looping
                last_error_line = reader.line_num
                total += 1
                quarantined += 1
                print(f"quarantined: file line {reader.line_num}: {err}", file=sys.stderr)
                continue
            total += 1
            if any(v == '' for v in row.values()):
                bad += 1
            reason = bad_row_reason(row)
            if reason is not None:
                quarantined += 1
                print(f"quarantined: file line {reader.line_num}: {reason}", file=sys.stderr)
    print({"processed": total, "malformed": bad, "sample": args.sample, "quarantined": quarantined})

if __name__ == '__main__':
    main()
