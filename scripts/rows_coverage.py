"""One row per piece counted in the coverage plot of nv8 (and per piece seen only on undated pages, which is not drawn).
Read from research/coverage_rows.tsv, which build_coverage.py writes: a piece is one web address that story_scope places
on the story; its row cites the saved aggregator page that holds its headline and the headline as that page has it.
Identity is the address: two addresses with the same headline are two pieces and are never merged."""
import csv
from pathlib import Path
R = Path(__file__).resolve().parents[1] / 'research'


def rows():
    out = []
    for r in csv.DictReader(open(R / 'coverage_rows.tsv', newline=''), delimiter='\t'):
        out.append({'row_id': r['row_id'], 'url': r['url'], 'domain': r['domain'], 'headline': r['headline'], 'first_listed': r['first_listed'],
                    'drawn': r['drawn'] == 'yes', 'bound': bool(r['cited_snapshot']), 'src': r['cited_snapshot'] or r['first_snapshot'], 'q': r['passage'] or r['headline']})
    return out
