"""Derive AnthroPAC's contribution tables from the saved FEC e-filed Schedule B lines.
Run: python3 -I scripts/build_anthropac.py
Reads research/primary/fec-efile-schedule_b-C00946111/page-*.json (raw e-filings, FEC committee C00946111).
Writes research/anthropac_disbursements.csv (one row per filed line, keyed by file_number + transaction_id) and
research/anthropac_by_recipient.csv (one row per recipient committee; voided lines net out).
A line is a duplicate only when file_number and transaction_id both match; nothing else is merged."""
import csv, glob, json, re
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
lines = []
for p in sorted(glob.glob(str(R / 'primary' / 'fec-efile-schedule_b-C00946111' / 'page-*.json'))):
    lines += json.load(open(p))['results']
seen = {}; dups = 0
for r in lines:
    k = (r['file_number'], r['transaction_id'])
    if k in seen:
        assert seen[k]['disbursement_amount'] == r['disbursement_amount'] and seen[k]['recipient_name'] == r['recipient_name'], k
        dups += 1; continue
    seen[k] = r
rows = sorted(seen.values(), key=lambda r: (r['disbursement_date'] or '', r['recipient_name'] or ''))
with open(R / 'anthropac_disbursements.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['row_id', 'date', 'recipient', 'amount_usd', 'description', 'line_number', 'candidate_office', 'recipient_state', 'file_number', 'transaction_id', 'report_coverage_end', 'source'])
    for i, r in enumerate(rows, 1):
        fil = r.get('filing') or {}
        w.writerow([f'AP{i:03d}', (r['disbursement_date'] or '')[:10], r['recipient_name'], r['disbursement_amount'], r.get('disbursement_description') or '',
                    r.get('line_number') or '', r.get('candidate_office') or '', r.get('recipient_state') or '', r['file_number'], r['transaction_id'],
                    str(fil.get('coverage_end_date') or '')[:10], 'fec-efile-schedule_b-C00946111'])
agg = defaultdict(lambda: {'usd': 0.0, 'n': 0, 'dates': [], 'ids': [], 'desc': set(), 'office': set()})
for i, r in enumerate(rows, 1):
    d = (r.get('disbursement_description') or '').upper()
    if 'FEE' in d or (r.get('line_number') or '').upper().startswith('21'):
        continue
    a = agg[r['recipient_name'].strip().upper()]
    a['usd'] += float(r['disbursement_amount']); a['n'] += 1; a['dates'].append((r['disbursement_date'] or '')[:10]); a['ids'].append(f'AP{i:03d}')
    a['desc'].add(d); a['office'].add(r.get('candidate_office') or '')
with open(R / 'anthropac_by_recipient.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['recipient', 'net_usd', 'lines', 'first_date', 'last_date', 'candidate_office', 'row_ids'])
    for k, a in sorted(agg.items(), key=lambda x: (-x[1]['usd'], x[0])):
        w.writerow([k, f"{a['usd']:.2f}", a['n'], min(a['dates']), max(a['dates']), '/'.join(sorted(x for x in a['office'] if x)), ' '.join(a['ids'])])
print('filed lines', len(lines), 'exact duplicates dropped', dups, 'kept', len(rows), 'recipients', len(agg))
print('with candidate_office:', sum(1 for a in agg.values() if any(a['office'])), '| net total', sum(a['usd'] for a in agg.values()))
for name in ['SCHUMER', 'BANKS', 'MOOLENAAR', 'MAGAZINER', 'SUBRAMANYAM', 'BACON', 'COTTON', 'COONS', 'CRAMER', 'MAST', 'CRAWFORD', 'OBERNOLTE', 'WARREN', 'CORNYN', 'RISCH', 'HUIZENGA']:
    hits = [(k, a['usd'], a['dates'], sorted(a['office'])) for k, a in agg.items() if name in k]
    print(' ', name, hits or 'NONE')
