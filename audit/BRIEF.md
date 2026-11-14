# Independent audit of one draft figure before it is made public: "Fifteen days, mapped", every drawn row against its saved original

Owner: the session that built the figure. You are the auditor. You did not build this figure. Work only inside audit; write only under audit/out/. Change nothing else anywhere. Do not fetch anything from the web.

The figure ("Fifteen days, mapped: the coverage, who acted, and the documented ties") covers the fortnight from Oct 29 to Nov 12, 2026 in which reports about Nvidia's founder, Jensen Huang, led to his resignation as chief executive. It shows: one dot per piece of coverage that two news aggregators listed; one row per actor (newspapers, reporters, analysts, 23 members of Congress, the administration, Nvidia, others) with a chip for each dated act; and, at the left, documented ties between those actors and the AI company Anthropic, its people and groups it or Open Philanthropy has funded. It will be published. The builder is a model made by Anthropic, so read with that in mind: look as hard for an understated or missing fact about Anthropic as for an overstated one, and check that other companies (Nvidia above all) are described with the same care. The figure's own rule is that a tie is a dated record, not a motive.

## The one hard rule about names
Some originals hold the names of private people: employees who gave money, and lobbyists. **Never write the name of a donor or of a lobbyist in any file you produce.** Refer to an FEC line by its SUB_ID or by committee, date and amount. Members of Congress, companies, organisations, firms, political committees, reporters and analysts the figure names, officials, and other public figures the figure itself names may be named. The figure names one person from a newspaper report as the subject of an intelligence finding: say whether each such naming is attributed to the report and kept to what the report says.

## Inputs (frozen; do not edit)
- `rows.jsonl`: 1,892 rows, one per line: `row_id`, `table` (what kind of row), `drawn_text` (the words the figure draws for it), other fields, `src` (a list of sources) and `q` (a list of passages, one per source, that a script has already found in that source).
- How to open a source named in `src`:
  - a bare id (for example `cnbc-1029-nvidia-responds`, `man-nyt-1029-01`, `techmeme-1105-h1700`): the folder `research/primary/<id>/` (`text.txt`, sometimes `text.reextract.txt`, `body.html` or `body.pdf`, `meta.json`, `*.json`, images).
  - `pack:<path>#<row id>`: the row with that id (first column or `row_id`) in `EVIDENCE_SETS/<path>`; a file may begin with comment lines starting `#`. Where the row has a `url` and a `quote_300`, and its `note` names a saved file under that pack's `research/primary/`, open the saved file when the row alone does not settle the point.
  - `table:<file>#<key>`: the row with that key (first column, `row_id` or `recipient`) in `tables/<file>`.
- `evidence.tsv`: the same sources as a reader of the public repository will see them (a link and a passage each).
- `tables/`: `member_ties.csv` (every tie of a member of Congress; the figure draws the `words` column), `coverage_rows.tsv` (the pieces listed) and `harvest.tsv` (every link harvested from the two aggregators' saved pages, with the day first listed), `anthropac_by_recipient.csv`, `anthropac_party.csv`, `employee_gifts.csv` (1,170 FEC lines of gifts by people who gave Anthropic or Nvidia as employer; donors are numbered), `employee_gift_rates.csv`, `committee_keys.csv`, `pacs_by_member.csv`, `chip_bills.csv`, `lobbying_bill_reports.csv`.
- `figures/nv8-fifteen-days-mapped.html`: the figure as drawn. It begins with an HTML comment listing the row ids it rests on.

## Part A: every row that is not a listed piece (230 rows)
For each row of `rows.jsonl` whose `table` is not `piece listed by an aggregator`, open every source it cites and read enough to judge the row; do not rely on `q` alone, and never take the row's own wording as evidence. Append one line to `out/findings.csv` (header `finding_id,row_id,grade,passage_found,problem,suggested_wording`):
- `grade`: `ok` (the sources support everything `drawn_text` says), `qualification` (supported, but the wording goes further than the source, drops a limit the source states, gives a date or an amount the source does not give, or leaves a reader with a wrong impression), or `error` (a fact in `drawn_text` is not in the sources or contradicts them).
- `passage_found`: the words in the source that decide your grade, at most 300 characters (never a donor's or lobbyist's name).
- `problem` and `suggested_wording` for `qualification` and `error` only; the suggestion must be something the sources support.
Also grade down, as a `qualification`, wording that states or implies a motive, describes a person's character, goes beyond a public role, or implies that one event caused another when no source says so.
Read these most closely:
- rows of `dated act of an actor`: is the act dated as the source dates it, attributed to the right actor, and worded as the source words it? Where a newspaper's report is restated, is it clear that it is the newspaper's report? Is any denial or limit in the same source left out?
- rows of `tie of a member of Congress`: recompute every amount, count of people and date range from `tables/employee_gifts.csv` and `tables/anthropac_by_recipient.csv`; for lines about lobbyists' gifts and about fellows, advisers, former staff and witnesses, open the pack rows. A witness list does not show who appeared; a lobbyist's gift is the lobbyist's own money unless the row is a firm's political committee; "no gift on file" must be bounded to the records searched.
- rows of `tie in the network at left` and `tie between two actors`: each named link, each grant total and its years (recompute from the rows cited), each post and its dates.
- rows of `background of a group of actors`: each sentence, and whether "no document here shows" is a fair statement of what the saved sources lack.

## Part B: the figure, element by element
Read all visible text of the figure (title, subtitle, the tiles, legend, the day axis and its counts, every actor's row and chip, every line of each member's ties, the network at left, section notes, the footnote). Append to `out/figure_findings.csv` (header `finding_id,grade,element_text,problem,rows_checked`) one line per problem, and a closing line `B-CLOSE` saying how many elements you read:
- a visible sentence or number that no listed row or table supports (recount every count the figure states: the pieces listed and the sites, the pieces drawn per day, the actors drawn, the members who received a gift from an Anthropic employee and from AnthroPAC, the party counts);
- a row id or a file name visible to a reader;
- wording that states or implies motive, coordination or cause; a line drawn from a tie to an act rather than to a person or body;
- a place where the figure should say what the record does not show and does not;
- a tie, an actor or an act that a reader new to the subject could not follow from the figure alone, or would misread;
- something in a row's sources that weakens or contradicts what is drawn and is left out.

## Part C: the coverage, recounted (a census, not a sample)
`rows.jsonl` has 1,662 rows of `piece listed by an aggregator`, each citing one saved aggregator page and the headline as listed. Write your own script (keep it in `out/`) and report in `out/census.md`:
1. For every such row: is the headline (the passage) in the saved page it cites? Is the day first listed the earliest saved page that lists that address in `tables/harvest.tsv`? Count failures and list up to 20 by row id.
2. Recount from `tables/harvest.tsv` and `tables/coverage_rows.tsv`: the pieces listed on the story, the number of sites, and the pieces per day; compare with the numbers the figure prints. Say how a piece was decided to be "on the story" as far as the tables show, and whether pieces that are plainly about something else are counted, or pieces plainly on the story left out (give up to 20 examples of each by address).
3. Whether every saved aggregator page in the range is cited by at least one row, and which hours or days have no saved page (a gap in the harvest, not a day without coverage).

## Part D: the members, recounted
For each of the 23 members of Congress the figure draws, recompute from the tables: gifts from people who gave Anthropic as employer (dollars, people, first and last date), gifts from people who gave Nvidia as employer, AnthroPAC money, and compare with the member's lines. Report in `out/members.md` a table and every difference. Say whether a member with a comparable record in the tables is not drawn, and by what rule members were chosen as far as the figure and tables show.

## Part E: what was left out
In `out/REPORT.md` say, from what you read: whether any tie between a drawn actor and Anthropic, Nvidia, or a group named in the figure is in the sources and not in the figure; whether any source the rows cite states a denial, a limit or a later correction the figure omits (Nvidia's replies above all); whether the figure treats Nvidia's ties to these actors with the same rule as Anthropic's, and says so where it does not; and whether the figure's footnote on what the record does not show is complete.

## Rules
- A missing file or an unreadable original is a gap, not a finding: write it to `out/gaps.csv` (`row_id,source,what_failed`) and go on. Never grade from memory or outside knowledge.
- Be exact and plain. No guesses about why anyone did anything.
- Append only; if `out/findings.csv` already has a line for a `row_id`, skip that row (this lane may be restarted).
- Before you finish, search every file under `out/` for the names of donors and lobbyists you met in the originals and remove any you find; say in the report that you did.

## Report
`out/REPORT.md`: rows read and counts by grade; the most serious findings in plain words; Part B by element; Parts C and D in short tables; Part E; gaps. End with exactly one line: `audit: complete` or `audit: incomplete <reason>`. This round fetches nothing, so it ends `audit: incomplete originals not re-fetched` unless something worse stops it. Write the report last, after every other file is final.
