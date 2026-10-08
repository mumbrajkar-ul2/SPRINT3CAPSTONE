import argparse, csv
from pathlib import Path

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--sample', action='store_true')
    args=parser.parse_args()
    data=Path(__file__).resolve().parents[1]/'data'/'synthetic'/'devices.csv'
    bad=0; total=0
    with data.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            total += 1
            if any(v == '' for v in row.values()):
                bad += 1
                # Brownfield issue: malformed records counted but not quarantined.
                continue
    print({"processed": total, "malformed": bad, "sample": args.sample})

if __name__ == '__main__':
    main()
