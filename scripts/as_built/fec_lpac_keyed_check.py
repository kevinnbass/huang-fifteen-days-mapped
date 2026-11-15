"""The leadership PACs that the congress evidence set keys to one member, checked against each PAC's own FEC record.

Run: python3 -I scripts/fec_lpac_keyed_check.py <done marker>
Why: research/committee_keys.csv ties 51 committees to a member on the evidence set's reviewed key alone (kind "joint committee or
leadership PAC", committee type leadership_pac). The reading of the corrections (Nov 15, 2026) could not check them from the public
tables. A leadership PAC's FEC record names its sponsor by candidate id; this reads each record through the host's FEC queue and
compares the sponsor with the keyed member: the same candidate id as the evidence set gives the member, or, for a member who has run
for another office, a candidate of the same surname and state in the FEC's candidate file (cn26).
Writes research/lpac_keyed_check.csv: committee_id, committee, bioguide, member_name, sponsor_candidate_ids (as served),
member_candidate_ids, outcome (agrees / differs / no sponsor in the record / not read), source.
A saved record is kept and reused; a record that could not be read is a gap, never a "none". No person other than members."""
import csv, re, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fec_get_pull import get, PRIMARY
R = Path(__file__).resolve().parents[1] / 'research'
DAY = datetime.now(timezone.utc).strftime('%Y%m%d')


def main():
    marker = Path(sys.argv[1])
    ck = list(csv.DictReader(open(R / 'committee_keys.csv', newline='')))
    cand = {}
    for r in ck:                                  # the candidate ids FEC links to each member, from the member's own committees
        if r['kind'] == 'candidate committee':
            cand.setdefault(r['bioguide'], set()).update(r['fec_candidate_ids_linked'].split())
    # the member's own candidate id as the congress evidence set gives it, and the FEC's candidate file for ids of other offices
    for r in csv.DictReader(l for l in open('EVIDENCE_SETS/congress/research/member_join.csv', newline='') if not l.startswith('#')):
        if r.get('fec_candidate_id'):
            cand.setdefault(r['member_bioguide'], set()).add(r['fec_candidate_id'])
    CM = sorted(PRIMARY.glob('fec-bulk-committees-2026-*'))[-1]
    cn = {}
    for ln in subprocess.run(['unzip', '-p', str(CM / 'cn26.zip')], capture_output=True, check=True).stdout.decode('utf-8', 'replace').splitlines():
        f = ln.split('|')
        if len(f) > 5:
            cn[f[0]] = (f[1].split(',')[0].strip().upper(), f[4])            # surname as filed, state of the office
    last = lambda name: re.sub(r',? (Jr\.?|Sr\.?|II|III|IV)$', '', name.strip()).split()[-1].upper()
    def same_person(sp, r):
        if sp & cand.get(r['bioguide'], set()):
            return 'agrees'
        if any(c in cn and cn[c][1] == r['state'] and cn[c][0].split()[-1] == last(r['member_name']) for c in sp):
            return 'agrees (the sponsor is a candidate of the same surname and state under another office\'s id)'
        return 'differs' if all(c in cn for c in sp) else 'sponsor id not in the candidate file of this cycle'
    want = [r for r in ck if r['kind'] == 'joint committee or leadership PAC' and 'committee type leadership_pac' in r['basis']]
    out = []
    for r in want:
        cid = r['committee_id']
        ex = sorted(d for d in PRIMARY.glob(f'fec-committee-{cid.lower()}-*') if (d / 'page-001.json').exists())
        d = ex[-1] if ex else PRIMARY / f'fec-committee-{cid.lower()}-{DAY}'; d.mkdir(parents=True, exist_ok=True)
        row = {'committee_id': cid, 'committee': r['committee'], 'bioguide': r['bioguide'], 'member_name': r['member_name'],
               'sponsor_candidate_ids': '', 'member_candidate_ids': ' '.join(sorted(cand.get(r['bioguide'], ()))), 'outcome': 'not read', 'source': ''}
        try:
            c = (get(f'https://api.open.fec.gov/v1/committee/{cid}/', d / 'page-001.json').get('results') or [{}])[0]
            sp = set(c.get('sponsor_candidate_ids') or [])
            for x in sorted(sp - set(cn)):               # a sponsor id of an earlier cycle: read that candidate's own FEC record
                ex2 = sorted(q for q in PRIMARY.glob(f'fec-candidate-{x.lower()}-*') if (q / 'page-001.json').exists())
                d2 = ex2[-1] if ex2 else PRIMARY / f'fec-candidate-{x.lower()}-{DAY}'; d2.mkdir(parents=True, exist_ok=True)
                k = (get(f'https://api.open.fec.gov/v1/candidate/{x}/', d2 / 'page-001.json').get('results') or [{}])[0]
                if k.get('name'):
                    cn[x] = (k['name'].split(',')[0].strip().upper(), k.get('state') or ''); row['source'] = d.name + '; ' + d2.name
            row.update(sponsor_candidate_ids=' '.join(sorted(sp)), source=row['source'] or d.name,
                       outcome='no sponsor in the record' if not sp else same_person(sp, r))
        except (Exception, SystemExit) as e:
            row['outcome'] = f'not read: {type(e).__name__}'
        out.append(row)
        with open(R / 'lpac_keyed_check.csv', 'w', newline='') as f:      # rewritten after every record, so a stop loses nothing
            w = csv.DictWriter(f, fieldnames=list(row), lineterminator='\n'); w.writeheader(); w.writerows(out)
    from collections import Counter
    print(len(out), 'committees;', dict(Counter(o['outcome'].split(' (')[0].split(':')[0] for o in out)))
    marker.parent.mkdir(parents=True, exist_ok=True); marker.write_text(datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ') + '\n')


if __name__ == '__main__':
    main()
