"""Assemble the frozen inputs of the independent audit of the map figure (nv8, "Fifteen days, mapped") in a lane folder.
Run: python3 -I scripts/make_audit_nv8.py <lane folder>      (the folder must not hold inputs yet)
Writes rows.jsonl, evidence.tsv, tables/, figures/, INPUTS.sha256.json. The brief (PROMPT.md) and run.sh are written beside them by hand."""
import csv, hashlib, json, shutil, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_public as N, nv13_public as P

L = Path(sys.argv[1]); assert not (L / 'rows.jsonl').exists(), 'inputs already written: an audit reads frozen inputs'
for d in ('tables', 'figures', 'out', 'log', 'done'):
    (L / d).mkdir(parents=True, exist_ok=True)
rows = N.figure_rows()
with open(L / 'rows.jsonl', 'x') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
ev = N.evidence()
with open(L / 'evidence.tsv', 'x', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(ev[0].keys()), delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(ev)
g = P.public_gifts()
with open(L / 'tables' / 'employee_gifts.csv', 'x', newline='') as f:
    w = csv.DictWriter(f, fieldnames=P.GIFT_COLS, lineterminator='\n'); w.writeheader(); w.writerows(g)
for name in ('member_ties.csv', 'coverage_rows.tsv', 'harvest.tsv', 'anthropac_by_recipient.csv', 'anthropac_party.csv', 'employee_gift_rates.csv', 'committee_keys.csv', 'pacs_by_member.csv',
             'chip_bills.csv', 'lobbying_bill_reports.csv', 'lobbying_family_reports.csv'):
    shutil.copyfile(R / name, L / 'tables' / name)
shutil.copyfile(ROOT / 'figures' / (N.STEM + '.html'), L / 'figures' / (N.STEM + '.html'))
sha = {str(p.relative_to(L)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(L.rglob('*')) if p.is_file() and (p.parts[len(L.parts)] in ('tables', 'figures') or p.name in ('rows.jsonl', 'evidence.tsv'))}
(L / 'INPUTS.sha256.json').write_text(json.dumps(sha, indent=1))
from collections import Counter
print('rows', len(rows), dict(Counter(r['table'] for r in rows)), '| evidence lines', len(ev), '| gift lines', len(g), '| files hashed', len(sha))
