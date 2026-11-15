# Second independent audit: “Fifteen days, mapped” — part one

Frozen input audit; completed locally at 2026-11-15T00:19:16+00:00. All 84 manifest hashes still match. I wrote only under this lane’s `out/`, made no web requests, and did not read the other auditors’ folders. This is a reading of saved evidence, not independent confirmation of the underlying news allegations or a fresh retrieval audit.

The requested saved-source work is finished. Publication still needs the corrections and qualifications below. No source or public figure was edited by this auditor.

The most serious findings are:

1. **An Anthropic connection is missing from Cotton’s row.** The public tables record a $2,500 AnthroPAC contribution on Sep 30, 2026, AP100. The member-tie table marks TY104 `held`, so the visible row omits it while the “12 of 24” total includes it. Add the dated contribution. This is B-COTTON-PAC, not evidence of a motive.
2. **Singapore’s source was shortened in two consequential ways.** Its insufficient-evidence conclusion concerns the declarations being investigated, not all possible offences. Its saved original and the saved NBC report also say repeated requests to U.S. authorities yielded limited assistance concerning Supermicro. The first-audit disposition’s reason for rejecting the assistance point is contradicted by both saved files. See A-MA72, A-ST09 and the two Singapore figure findings.
3. **Two figure statements are factually stale.** Anthropic’s own channels were searched, contrary to its section note; its declined-to-comment response is also drawn. The source capture range still says Nov 12–13 although newly cited originals were saved Nov 14. See B-ANTHROPIC-SEARCH and B-FETCH-DATES.
4. **Eight joint-committee labels outrun the published classification evidence.** Receipt totals, anonymous donor counts and date ranges reproduce. But the eight committees behind the asserted joint-fundraising subtotals are absent from `joint_committees.csv`; the other public tables call them only “joint committee or leadership PAC.” That is an unresolved classification, not proof the labels are false. Publish their registrations and participants, or name the receipt committees without the joint-fundraising assertion.
5. **Dates and quote selection still need care.** Himes’s interview remains positioned Nov 12 despite the Nov 10 original. The 2025 intervention reported in TechCrunch is placed on a uniquely asserted Nov 10, 2026 date unsupported by its Nov 9–10 reporting range. Mast’s spliced quotation omits his stated support for Nvidia; the disputed Lutnick exchanges omit denials in their own cited relays. These are specific source limits, not judgments about the people involved.

**Part A — every changed non-coverage row.** `findings.csv` has exactly one finding for each of the 168 requested row keys, no duplicates, with passages no longer than 300 characters. Grades: 151 ok, 17 qualifications, 0 errors. I opened the cited saved sources and read enough to judge each whole claim; the extracted `q` passages were finding aids. When plain-text extraction omitted the article, I read the saved HTML, notably Singapore’s ministry, Meeks’s letter release and Global Times. This was not a script-only grading exercise.

| Row kind | Read | Ok | Qualification | Error |
|---|---:|---:|---:|---:|
| dated act of an actor | 75 | 67 | 8 | 0 |
| tie of a member of Congress | 61 | 53 | 8 | 0 |
| tie between two actors | 14 | 14 | 0 | 0 |
| note | 13 | 13 | 0 | 0 |
| background of a group of actors | 3 | 2 | 1 | 0 |
| count across Congress | 2 | 2 | 0 | 0 |

All 23 additions listed in `originals_added.tsv`, covering 20 rows, were checked in their saved originals. The Warren statement supports Oct 29; the filed complaint supports Nov 9. The Nov 4 House letter is now clearly distinguished from its Nov 5 release. Cotton’s 2025 letter is visibly outside the fifteen days. The Himes date problem remains.

Employee money was recomputed from the public receipt table using Decimal, distinct anonymous donor IDs, receipt dates and committee IDs. All 88 cited receipt records behind the eleven changed positive gift rows match the saved FEC bulk/API originals on committee, date, amount and employer. The 28 changed zero lines have the stated record-window bound and positive controls. This checks these supplied receipts; it does not establish that the builder collected every filing or independently prove anyone’s employment. Lobbyists’ gifts remain their own money. I read the cited pack rows, checked firm/client records, and opened saved contribution payloads where a pack quotation did not settle the amount/date. The witness claim is now supported by an actual spoken hearing transcript, beyond the scheduled-witness roster.

**Part B — the complete figure.** I read all 708 nonempty visible body-text nodes, including every actor row, chip, tie line of text, repeated section note and every sentence of the footnote. The unit is a body text node, not a sentence count. The document title duplicates the visible title; 2,225 hover-only SVG titles were checked mechanically against coverage rows. All 109 tie strokes remain left of the act calendar in the SVG coordinates; none enters a chip. This was a static HTML/SVG read, not a browser screenshot or a font/clipping certification.

| Figure checks | Result |
|---|---|
| Substantive problem lines | 23: 2 errors, 21 qualifications |
| Closing record | B-CLOSE, one ok closing line |
| Coverage populations | 2,234 table pieces, 2,225 plotted dated pieces, 9 undated pieces omitted from dots |
| Normalized domains | 480 among dots; 481 including undated pieces |
| Actor and act totals | 66 distinct actor rows; 119 dated acts in the fortnight; 2 act records without a fortnight day |
| Congress drawn | 24: 11 Democrats, 13 Republicans; 17 employee-gift recipients on the Anthropic side, 3 on Nvidia’s side |
| AnthroPAC | 12 drawn members have receipts; only 11 positive member lines are visible because Cotton’s is held |
| All candidate recipients of AnthroPAC | 81: 38 Democrats, 43 Republicans |
| Member-page counts | All 24 printed member counts reproduce from 1,086 distinct public page records |
| Visible row IDs or input filenames | Zero; hidden row list resolves completely |

The daily dot counts reproduce, including the empty days:

| First listed day | Dots |
|---|---:|
| 2026-10-29 | 59 |
| 2026-10-30 | 1 |
| 2026-10-31 | 0 |
| 2026-11-01 | 0 |
| 2026-11-02 | 1 |
| 2026-11-03 | 0 |
| 2026-11-04 | 0 |
| 2026-11-05 | 12 |
| 2026-11-06 | 22 |
| 2026-11-07 | 24 |
| 2026-11-08 | 172 |
| 2026-11-09 | 515 |
| 2026-11-10 | 233 |
| 2026-11-11 | 270 |
| 2026-11-12 | 916 |

The public scope table has 2,234 story-class links, 136 fallout links and 95 other links, totaling 2,465. That verifies its arithmetic, not a reading census of topical relevance. The known midterms/buildout piece remains counted under the disclosed Huang-name rule, so the earlier topical objection is only partly answered.

Across the supplied Congress receipt table:

| Employer as filed | Receipt lines | Recipient members | Anonymous donor IDs | Dollars | Recipient parties | Latest line |
|---|---:|---:|---:|---:|---|---|
| Anthropic | 771 | 151 | 70 | $4,529,249.00 | {'R': 63, 'D': 87, 'I': 1} | 2026-10-05 |
| Nvidia | 533 | 65 | 83 | $172,590.00 | {'R': 5, 'D': 58, 'I': 2} | 2026-09-30 |

The 535 denominator is the population asserted in the supplied rates table; this lane did not independently reconstruct a sitting-member roster. The rates table says records were read through Oct 14; the latest campaign-committee receipt for each employer is Sep 30. The conduit counts/amounts reproduce the public rates entries: Anthropic 26/$2,740.76 and Nvidia 350/$14,345.33, including the two Nvidia conduit lines totaling $15 associated with Warren. These are table recounts, not a separate regulator-wide collection audit. Dec 3 is supported for post-general reports, not as a universal deadline for every committee type.

The published annual grant rows sum as follows; these are awards, not bank payments:

| Recipient | Award total | Years |
|---|---:|---|
| Americans for Responsible Innovation | $3,446,500 | 2024–2025 |
| Center for AI Safety | $12,485,288 | 2022–2023 |
| Center for a New American Security | $14,626,356 | 2017–2025 |
| Future of Life Institute | $1,912,000 | 2015–2020 |
| Institute for AI Policy and Strategy | $34,207,471 | 2024–2026 |
| Institute for Progress | $11,956,660 | 2021–2026 |
| Tarbell Center for AI Journalism | $5,291,930 | 2024–2025 |

The added FAI records give $552,500 in 2023 and $423,500 in 2024 for AI policy (the second an exit grant), plus $2,714,000 in 2026 for energy permitting. The cited OpenAI record gives a $30 million 2017 award. The CSET pack record supplies the $107.75 million total; it is not among the public annual grant rows above.

Other figure qualifications include unsupported direct-interview attribution to Quartz, omission of the separate rulemaking required after RASA, two Bresnick chips that omit available quotation content, unclear repeated network aliases, a direct quotation made from a reporter’s paraphrase of Nvidia’s statement, and funding chains left unestablished for some lobbying-firm clients. Every issue is individually identified in `figure_findings.csv`. I found no drawn causal arrow from a tie to an act, but “a party with something at stake” adds an unproved interest to historical records and should be narrowed. The broader exclusion/selection audit belongs to the parallel part, which I did not read.

**Part C — the first audit’s dispositions.** Every line was read against the earlier finding and current row/element. `earlier_dispositions.csv` preserves the original finding IDs.

| Dispositions checked | Holds yes | Partly | No |
|---:|---:|---:|---:|
| 106 | 91 | 15 | 0 |

The 15 partial responses concern the two Singapore findings, seven row-level client-chain findings plus their grouped figure finding, the now-positive Magaziner row whose disposition still describes a zero, the coverage rule/context objections, remaining source limits, and unpublished counts asserted for three omitted members. The source-supported fixes are credited: letter/release dates, Nvidia’s denial, the phase-out, the nuclear-fellowship label, actual hearing testimony, separated ARI-PAC disclosure systems and the new historical/institutional ties. The added OpenAI backstop answers that omission, although the builder’s “no unit” rationale is wrong: the next paragraph of the saved CNBC text says “$105 billion OpenAI deal.”

**Gaps and controls.** `gaps.csv` contains 114 gap records: 1 cited partial original, 81 inherited original-search gaps and 32 inherited own-channel access gaps. The cited partial original is the hand-saved Bloomberg teaser for MA106; the saved Taiwan News relay supports the words and date. The inherited gaps are carried from the supplied search ledger, not presented as new attempts by this auditor. No web request was made. A blocked or unsaved original was not treated as evidence of silence or absence.

`controls.csv` records 12 controls and corrections: input hashes; positive employer/recipient hits for zero checks; known joint-register hits; exact SUB_ID resolution; the Singapore warning and assistance passages in the same saved source; the Cotton PAC receipt and another visible PAC line; hidden versus visible IDs; geometric actor-row endpoints; exact tooltip correspondence; the limits of published member counts; and the private-name matcher’s positive control. C-VISIBLE-IDS-CORRECTION corrects a helper’s initial cardinality statement: the full hidden list has 2,530 IDs, while its narrower regex sees 2,527 because it excludes the three RU/EV event rows. Every hidden ID resolves, and the visible-ID/filename result is zero. Initial raw hostname counts are superseded by the normalized-domain counts: www/non-www spellings are not separate sites. In `employee_recounts.csv`, `joint_usd` means membership in the supplied committee register, which also includes leadership PACs; type was judged separately.

Before finishing, I searched every file under `out/` for donor and lobbyist names from the saved records, removed matches, and checked a real source-name positive control without writing it. The first scrub removed eight whole-name matches from three text files, including conservative redactions of firm-name overlaps. No private identity list was saved. The final scan includes this report and prints its result without creating another artifact.

No background work is running or armed. No external response is awaited and there is no pending deadline for this lane. The next step is the owner’s disposition of these findings and any requested fresh-source retrieval; this auditor made no production changes.

audit: incomplete originals not re-fetched
