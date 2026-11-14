# Fifteen days, mapped: the coverage of the Huang affair, who acted, and the documented ties

**Status: draft.** Every quoted passage has been matched by script to a saved copy of its source, and the counts in the
figure are recomputed from the tables here by `scripts/verify_nv8.py`. A tie is a dated record, not a motive. Nothing
here says why anyone acted.

![The figure](figures/nv8-fifteen-days-mapped.png)

Also as [HTML](figures/nv8-fifteen-days-mapped.html) (point at a dot to read the headline it stands for) and
[JPG](figures/nv8-fifteen-days-mapped.jpg). The image is tall: open it and zoom in.

## What this is

On Oct 29, 2026 The New York Times reported that U.S. officials saw Jensen Huang, the founder and then chief executive of
Nvidia, as the target of a Chinese spy plot. Fifteen days later he had resigned as chief executive and three House
committees had called him to answer questions. This figure puts three things on one sheet for those fifteen days:

- **The coverage.** One dot for each of the 2,225 pieces that two news aggregators, Techmeme and Memeorandum, listed
  on the story, on the first day a saved page lists it (2,234 pieces from 481 sites in all; 9 seen only on undated pages are
  not drawn).
- **Who acted.** One row for each actor (newspapers, reporters, analysts, 23 members of Congress, the administration,
  Nvidia, others) and one chip for each dated act: 73 acts, each worded from a saved report.
- **The documented ties.** At the left, the records that tie those actors to a party with something at stake in the
  matter: the AI company Anthropic, its people and its PAC; groups that Anthropic or the foundation Open Philanthropy
  has funded; and Nvidia itself. There are 92 lines for the 23 members of Congress (gifts by each company's
  employees, lobbying reports that name a member's bill, fellows and former staff, lobbyists' gifts, ads), a line on
  AnthroPAC's contribution for each member who received one, and 55 records among the other actors.

Why those parties: the matter touches the export of the AI chips that Nvidia sells. On the record here: Anthropic backs
"smart export controls on AI chips" and gave $40 million to the group Public First Action; members of Congress drawn
here sponsor bills on chip exports (one, the AI OVERWATCH Act, would let Congress block advanced chip exports); both
Anthropic's and Nvidia's lobbying reports name those bills; AMD and Broadcom compete with Nvidia for AI chip sales. The
figure's own boxes say, for each group of actors, what is on the record about it and what no document here shows.

A line ends at a person or a body, never at an act. The figure sets the records side by side; it does not say that any
of them caused a report, a post or a statement.

## The numbers

| Day first listed | Pieces drawn |
|---|---|
| 2026-10-29 | 59 |
| 2026-10-30 | 1 |
| 2026-11-02 | 1 |
| 2026-11-05 | 12 |
| 2026-11-06 | 22 |
| 2026-11-07 | 24 |
| 2026-11-08 | 172 |
| 2026-11-09 | 515 |
| 2026-11-10 | 233 |
| 2026-11-11 | 270 |
| 2026-11-12 | 916 |

Of the 92 lines for members of Congress, 46 are the two lines every member has, one on gifts by people who gave Anthropic as employer and one on Nvidia's (28 of the 46 say that none is on file). The other 46: 17 on gifts by lobbyists whose firms had clients among the groups drawn; 7 on contributions by the PAC of Americans for Responsible Innovation; 6 on a Horizon fellow placed in an office or with a committee; 5 on lobbying reports that name the member's chip-export bill (both companies' counts); 2 on a former adviser who sits on Anthropic's advisory council; 2 on testimony by Anthropic's people at a hearing; 2 on an ad by Public First Action naming the member; 2 on a former committee staff member now at a funded group; 1 on a former aide who lobbied for a funder; 1 on witnesses from groups Open Philanthropy has funded; 1 on a fellow of a funded group described as an adviser to a committee.
Each member drawn is named on at least three of the 1,086 news pages saved for this project (`research/story_pages.tsv`
lists the pages by address and the members each names).

## The figure's own notes

**Reading it:** the dots count pieces, not readers; a piece is placed on the first day a saved Techmeme or Memeorandum page lists it (pages for 9 am, noon, 4 pm, 8 pm and 11 pm Eastern each day), and 9 more pieces seen only on undated pages are left out. A piece counts as on the story when its address or listed headline names Huang, Megaspeed or Alice Huang, tells of the spy affair without naming them, or names Nvidia with a word of the affair (resign, board, inquiry, chief, successor and the like). That rule was applied by script, not by reading each piece, to the 2,465 links on those pages that name Huang, Nvidia, Megaspeed or the spy story. It leaves out 136 links on the wider fallout (export controls, the Commerce secretary, the share price, Anthropic's stock offering) and 95 others; some of those bear on the matter, and a counted piece may name Huang for another reason. Every link and its class is published with the figure's tables. They are sorted into the three kinds by site and by the section named in the page address, not by reading them. A chip is one dated act, worded from a saved report; it starts on its day, and a long one may run on over empty days to its right. View counts are those shown when the posts were saved on Nov 12. An act is placed on the day its source gives or, failing that, the day the source was published: those chips have a dashed left edge, and the act itself may be earlier. Where a chip rests on one outlet's account of another's report, it says so. Grant figures are awards, not payments traced to a bank. An announced ad is not proof that it ran. Nvidia's board said on Nov 8 it had "no reason to believe" national security or company secrets were compromised, and NBC reported on Nov 12 that Alice Huang's "precise role" remained unclear. Members of Congress drawn are every current member named on three or more of the 1,086 saved pages for something said or done about the matter in these days; each one's count is in their row. Seven others named that often are not drawn, because the pages name them for other things: a leadership vote, a lost election, an impeachment bid, other inquiries and, for one senator, a letter of Oct 2025 asking the Commerce Department to investigate Megaspeed, a year before these days. The count for every name searched is published with the figure's tables. Analysts drawn are those found in the funding records, a selected set; others quoted in the same articles are not drawn, and no funding tie is implied for them. "No AnthroPAC contribution on file" means none in the PAC's filings with the Federal Election Commission for Jun 29 to Sep 30, 2026. A line that says no gift from a company's employees means that no FEC line for Jan 2025 to Sep 2026 gives that company as the donor's employer to a committee tied to the member; it is not proof that no employee gave. An employee's gift is counted from an FEC line on which the donor gave the company as employer, to a committee tied to the member; donors are counted, not named, and the two companies are counted by one rule, though not from equally deep records, as the next sentences say. Both companies' lines come from the FEC's bulk file of itemised individual contributions for the 2026 cycle, downloaded Nov 13, 2026 (it carries whole dollars), plus the lines its API holds and the file does not yet (nearly all dated Jul to Sep 2026): 51 for Anthropic, 21 for Nvidia. For 8 more lines the API's later filing replaces the file's copy. Nine Anthropic lines to Banks for Senate are counted from a copy of the committee's report saved in Sep 2026: its amended report leaves the employer blank. No earlier copy exists for Nvidia, so a Nvidia line blanked that way is missed. A lobbying report names a bill; it does not say which office was visited or what was asked. Fellows, advisers and former staff are as the programme's, the group's or Congress's own pages list them. A lobbyists' line names the clients that the lobbying reports held here list for the givers' firms. The reports give each gift as the lobbyist's own money; they do not show whether a client asked for it, or whether the firm had that client when the gift was made. Of those clients, Open Philanthropy's awards include $12.5M to the Center for AI Safety (2022–23) and $1.9M to the Future of Life Institute (2015–20); the grant records held here show none to Encode AI or Fathom, and IFP Action's funding was not looked up.

**What the record does not show:** who gave the intelligence assessment to reporters; whether it is correct; any contact between Anthropic, or anyone tied to it, and the reporters or their sources; any contact with a member of Congress about these reports or about what the member then said or did (earlier public contacts, such as testimony at a hearing, are drawn at left). The saved reports state limits of their own: the Times's first report says officials "did not believe" Huang knew the woman was gathering information when the president was first briefed, and that Huang "has not received a defensive briefing"; Nvidia said its customers get "zero information relevant to national security" and "do not ask Nvidia to press the U.S. government to change its policies on chip sales to China." The ties at left start from Anthropic, its people and Open Philanthropy; Nvidia's own political giving, business ties and former staff were not mapped to the same breadth, so the number of lines says nothing about either company's influence. The Times's reports are cited from its own articles, saved by hand; the Journal's and the FT's pages were not read (their sites turn away automated readers), so what they reported is taken from other outlets. No search was made of Anthropic's, Nvidia's or the rival chip makers' own channels.

**Source:** 2,234 links from saved aggregator pages; saved reports, posts and releases; committee filings; rows held in the congress, lineage, toner and evaluators packs. Fetched Nov 12–13, 2026.

**Status:** draft of Nov 14, 2026. Each passage behind a drawn item was matched by script to a saved copy of its source. An independent audit by another company's model read the 230 rows that are not listed pieces against the saved copies, recounted the pieces and recomputed the members' lines. It graded no row an error and 49 as needing a qualification, and raised 56 points on the figure, three of them errors (a site count, one piece's day, a sentence that claimed too much). Each has a written disposition, published with the tables. The audit did not fetch the originals again, and the changes made after it were checked by script only.

## Check it yourself

```
python3 scripts/verify_nv8.py
```

recounts the pieces, the sites and the pieces per day from `research/coverage_rows.tsv` and `research/harvest.tsv`, checks
that each piece's day is the day of the capture named for it in `research/coverage_day_pages.tsv`,
recomputes every member's line on employees' gifts from the FEC lines in `research/employee_gifts.csv`, checks that each of
the 2,473 rows the figure rests on has a source a reader can open, and looks up the 189 passages whose source is copied
here. It needs only Python. The other 2,553 passages are a link and the words to find there (`research/evidence.tsv`).

```
pip install playwright pillow && playwright install chromium
python3 scripts/build_nv8.py        # writes figures/nv8-fifteen-days-mapped.html, .png, .jpg
```

rebuilds the figure from the tables in `research/` and the row files in `scripts/`. It measures text with the Liberation
Sans fonts, so it needs them installed to give the same picture.

**One employee's gift.** `research/employee_gifts.csv` has one row per FEC line counted: the committee, the date, the
amount, the employer as filed, and the line's FEC identifiers; `fec_page_url` opens the page of the committee's report
that holds the line. Donors are numbered, not named: the names are on the FEC's pages, and this repository does not
repeat them. Lobbyists are not named either.

## The audit

An auditor from a different model family (GPT-6.1 Sol, run through Codex with no network access) read the 230 rows that are not listed pieces
against the saved originals: 181 ok, 49 qualifications, 0 errors. It read the figure element by element and raised 56 points,
3 of them graded errors (a site count, one piece's day, a sentence that claimed too much); it
recounted the listed pieces against the saved aggregator pages and recomputed the members' lines. Its closing line: `audit: incomplete originals not re-fetched`.
The brief, the report, the findings and the recounts are in `audit/`.

Each of its 105 findings has one written disposition, and so has 1 fault the builder found itself after the audit (93 applied, 12 applied in part, 1 stated as a limit): `audit/DISPOSITIONS.csv`. The auditor listed no source it could not open.

The audit did not fetch any original again, so a source that has changed since it was saved would not be caught. An earlier
audit round read an earlier version of this figure together with seven others; its files are not in this repository.

**Changed after the audit read the figure** (checked by script only; no auditor has read these changes):

- Five pieces were added and one moved from Nov 8 to Nov 12 (1,726 pieces became 1,731; 1,662 drawn became 1,667): six articles of one site share an address apart from the query string and had been counted as one. No row id was renumbered.
- Ninety more aggregator pages were saved on Nov 14 (noon, 4 pm, 8 pm and 11 pm Eastern for every day, so Nov 12 is now counted to 11 pm and not to 2 pm). The figure now counts 2,234 pieces and draws 2,225; 9 have no day (64 before). Of the pieces the audit read, 90 moved to an earlier day and 55 gained a day; 503 are new. No row id was renumbered.
- Six records that the audit found in cited sources and missing from the figure were added as lines in the actors' rows (rows MT27 to MT32), and twelve notes behind new footnote sentences were bound to their passages (NT05 to NT16).
- Wording was changed as `audit/DISPOSITIONS.csv` lists: 45 lines in members' rows (28 on employees' gifts, 17 on lobbyists' gifts), three other members' lines, nine chips, arcs and section notes, the dots' caption and the footnote.
- Three tables were added so that a reader can recompute what the figure states: `research/coverage_day_pages.tsv`, `research/coverage_scope.tsv` and `research/member_selection.tsv`.

## What is in this repository

| Path | What |
|---|---|
| `figures/` | the figure as .png, .jpg, .html |
| `research/nv8_rows.tsv` | every row the figure rests on (2,473): the words drawn, the sources cited and the passage found in each |
| `research/evidence.tsv` | one line per cited source of every row: what it is, its link, the passage, when it was saved, and where a copy sits in this repository if one does |
| `research/coverage_rows.tsv`, `harvest.tsv` | the pieces on the story with the headline as listed and the saved aggregator page each was first seen on; every link harvested from those pages |
| `research/coverage_day_pages.tsv` | for each piece, the timed capture of an aggregator's front page that dates it: the earliest one that lists its address |
| `research/member_ties.csv` | the records for members of Congress (the figure draws the `words` column) |
| `research/employee_gifts.csv`, `employee_gift_rates.csv`, `committee_keys.csv` | the FEC lines of gifts by people who gave Anthropic or Nvidia as employer (no names), the totals across the 535 members, and each committee with the member it is tied to |
| `research/anthropac_by_recipient.csv`, `anthropac_party.csv`, `pacs_by_member.csv` | AnthroPAC's contributions by recipient and by party; company PAC money by member |
| `research/chip_bills.csv`, `lobbying_bill_reports.csv` | the chip-export bills and the lobbying reports that name them |
| `research/grant_rows.csv` | the yearly award rows that the grant totals in the figure are sums of (from the funder's public grants index) |
| `research/story_pages.tsv` | the addresses of the 1,086 saved news pages and the members each names; no page text |
| `research/member_selection.tsv` | how the members drawn were chosen: every name searched with the number of pages naming it, whether it is drawn and, if not, why; then every other word found after a congressional title on three or more pages |
| `research/coverage_scope.tsv` | every link harvested from the aggregator pages with the class the word rule gives it (`story`, `fallout`, `other`); only `story` is counted and drawn. The rule is `scripts/story_scope.py` |
| `sources/` | copies of sources that are official records or the builder's own captures |
| `audit/` | the audit's brief, report, findings and recounts, and the disposition of every finding |
| `scripts/` | `build_nv8.py` and `verify_nv8.py` run on this copy, with the row files the figure is drawn from (`rows_ties.py` and `rows_events.py` are shared with other figures of the same project and also hold their rows); `as_built/` holds scripts as they were run, which need the builder's evidence sets and downloads |

News reports, the companies' and other organisations' pages and posts are linked and quoted in a sentence; they are not
copied. Headlines are given as the aggregators listed them.

## Who made this

The figure, the tables, the scripts and this file were drafted with Claude, a model made by Anthropic, working at the
direction of the repository's owner. Anthropic is one of the subjects of the figure. For that reason every statement is
tied to a record a reader can open, donors and lobbyists are counted and not named, and the work was audited by another
company's model.
