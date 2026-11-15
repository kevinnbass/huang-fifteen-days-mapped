# A last, very short reading of six changes to a public figure: "Fifteen days, mapped"

Owner: the session that built the figure. You are the auditor; you did not build this figure. Work only inside audit2; write only under its out/. Change nothing else. No web. Read each item yourself against its source.

The figure covers Oct 29 to Nov 12, 2026, the fortnight in which reports about Nvidia's founder, Jensen Huang, led to his resignation. `public/` is the repository as pushed (commit in `public/COMMIT.txt`); `public/figures/nv8-fifteen-days-mapped.html` is the figure. Five readings by auditors of your model family came before. The fifth (`public/audit2/REPORT-f.md`, `f-*.csv`) found no problem in 44 rows and raised four points on wording and one on a chip. The builder (a model made by Anthropic, one of the companies in the figure) made six changes in answer (`private/DISPOSITIONS-audit_nv8_s7f.csv`). Say whether each is right, and whether it brought in anything wrong. Nothing else is asked.

Never write the name of a donor or of a lobbyist in a file under out/.

A source id in `rows.jsonl` (`src`) is the folder `research/primary/<id>/` (`text.txt`, sometimes `text.article.txt` or `body.html`). The fifth reading's copy, for comparison: `lanes/audit_nv8_s7f/public/`.

## The six changes
1. Footnote, own channels: the count of chips' originals now separates those read at the search (35) from five saved afterwards and cited now, with 77 still not opened, 2 refused, 7 not found, 1 in part. In `public/research/nv8_s6_items.tsv` the lines of part "original of a chip" with keys MA06, MA08, MA101, MA69 and MA85 changed (the earlier table is `private/nv8_s6_items.before-s7f.tsv`). For each of the five: does the saved page the line names exist, is it the publisher's own page for what the chip reports, and does the chip (in `rows.jsonl`) cite it? Recount the six chip classes of `public/research/nv8_s6_counts.tsv` from the table by the rule in `public/scripts/as_built/nv8_s6_counts.py`.
2. Footnote, lobbyists: "they do not show whether a client asked for it. Whether the firm had the client when the gift was made is taken from the firm's registration dates, which the published table gives beside each gift." Is that what `public/research/lobbyist_gifts_map.csv` gives (columns `registered_from`, `registration_ended`), and is every counted gift inside its dates?
3. Footnote, own channels: "for 25 a channel that could be read showed no item about the affair in these fifteen days".
4. The status sentence at the foot of the figure: it now counts five readings and says what each found. Check each number it gives for the fourth and fifth readings against `public/audit2/e-*.csv` and `f-*.csv`.
5. Chip MA148 (two podcast releases of Nov 9) now ends "The recordings were not heard". Read the chip as a whole against its two sources.
6. Anything else in the visible text that differs from the fifth reading's copy of the figure (find by script, then read): report any other change you find and whether it is right.

## Out
`out/findings.csv` (header `finding_id,grade,what,problem,suggested_wording`): one line per change (G1 to G6, more lines if a change has several parts); `grade` is `ok`, `qualification` or `error`. `out/REPORT.md`: what you checked, the grades, anything you could not check; last line by itself `audit: complete` or `audit: incomplete <reason>`. `out/ROUNDS.md`: ten lines on what you did.
