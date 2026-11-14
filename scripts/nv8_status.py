"""The kicker and the status sentence of the map figure (nv8, "Fifteen days, mapped"), in one place so that the project's
generator and the public build (build_nv8.py) print the same words."""
KICKER = 'Huang resignation · dated public records, Nov 2026 · draft'
STATUS = ('<b>Status:</b> draft of Nov 14, 2026. Each passage behind a drawn item was matched by script to a saved copy of its source. '
          'An independent audit by another company\'s model read the 230 rows that are not listed pieces against the saved copies, recounted the pieces and recomputed the members\' lines. '
          'It graded no row an error and 49 as needing a qualification, and raised 56 points on the figure, three of them errors (a site count, one piece\'s day, a sentence that claimed too much). '
          'Each has a written disposition, published with the tables. The audit did not fetch the originals again, and the changes made after it were checked by script only.')
# what changed after the audit read the figure (the README of the public copy lists these under the audit)
AFTER_AUDIT = [
    'Five pieces were added and one moved from Nov 8 to Nov 12, so the figure now counts 1,731 pieces and draws 1,667 (the audit read 1,726 and 1,662). Six articles of one site share an address apart from the query string and had been counted as one. No row id was renumbered.',
    'Six records that the audit found in cited sources and missing from the figure were added as lines in the actors\' rows (rows MT27 to MT32), and twelve notes behind new footnote sentences were bound to their passages (NT05 to NT16).',
    'Wording was changed as `audit/DISPOSITIONS.csv` lists: 45 lines in members\' rows (28 on employees\' gifts, 17 on lobbyists\' gifts), three other members\' lines, nine chips, arcs and section notes, the dots\' caption and the footnote.',
    'Three tables were added so that a reader can recompute what the figure states: `research/coverage_day_pages.tsv`, `research/coverage_scope.tsv` and `research/member_selection.tsv`.',
]
