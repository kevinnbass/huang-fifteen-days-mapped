"""The kicker and the status sentence of the map figure (nv8, "Fifteen days, mapped"), in one place so that the project's
generator and the public build (build_nv8.py) print the same words."""
KICKER = 'Huang resignation · dated public records, Nov 2026 · draft'
STATUS = ('<b>Status:</b> draft of Nov 14, 2026. Each passage behind a drawn item was matched by script to a saved copy of its source. '
          'An independent audit by another company\'s model read the 230 rows that are not listed pieces against the saved copies, recounted the pieces and recomputed the members\' lines. '
          'It graded no row an error and 49 as needing a qualification, and raised 56 points on the figure, three of them errors (a site count, one piece\'s day, a sentence that claimed too much). '
          'Each has a written disposition, published with the tables. The audit did not fetch the originals again, and the changes made after it were checked by script only.')
# what changed after the audit read the figure (the README of the public copy lists these under the audit)
AFTER_AUDIT = [
    'Five pieces were added and one moved from Nov 8 to Nov 12 (1,726 pieces became 1,731; 1,662 drawn became 1,667): six articles of one site share an address apart from the query string and had been counted as one. No row id was renumbered.',
    'Ninety more aggregator pages were saved on Nov 14 (noon, 4 pm, 8 pm and 11 pm Eastern for every day, so Nov 12 is now counted to 11 pm and not to 2 pm). The figure now counts 2,234 pieces and draws 2,225; 9 have no day (64 before). Of the pieces the audit read, 90 moved to an earlier day and 55 gained a day; 503 are new. No row id was renumbered.',
    'Six records that the audit found in cited sources and missing from the figure were added as lines in the actors\' rows (rows MT27 to MT32), and twelve notes behind new footnote sentences were bound to their passages (NT05 to NT16).',
    'Wording was changed as `audit/DISPOSITIONS.csv` lists: 45 lines in members\' rows (28 on employees\' gifts, 17 on lobbyists\' gifts), three other members\' lines, nine chips, arcs and section notes, the dots\' caption and the footnote.',
    'Eighteen actors who are quoted or named as acting on three or more saved pages and had no row were added on Nov 14, with 22 chips: the secretaries of State, Commerce and the Treasury, the trade representative, White House spokespeople and the Justice Department; Nvidia\'s interim chief, its new chair and the shareholders suing it; Megaspeed, the Chinese embassy, Taiwan\'s interior minister and a Chinese newspaper; four executives and investors and a broadcaster; and a chip for an Anthropic spokesperson who declined to comment. They were found by listing every attributed remark in the saved pages (`scripts/nv8_gaps.py`); the first pass of that list was made with the help of a program, and a full reading is still running.',
    'Three tables were added so that a reader can recompute what the figure states: `research/coverage_day_pages.tsv`, `research/coverage_scope.tsv` and `research/member_selection.tsv`.',
]
