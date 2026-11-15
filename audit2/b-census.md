# Coverage recount

This is an offline census of the frozen figure and the supplied saved aggregator pages. All scripts are in this directory; no web request was made. `coverage_audit.py` independently parses links and text with the standard-library HTML parser. It imports only the already-read, side-effect-free scope function to compare its stated rule with the published classification; it does not use that function to judge relevance.

The frozen input hashes match INPUTS.sha256.json. The per-row result is in [coverage_checks.csv](coverage_checks.csv). The source lookup normalizes HTML entities, curly quotation marks, dashes and whitespace, and follows the published address-identity rule, including meaningful query strings on script/root addresses. This tests saved support and dates, not the accuracy of an outlet's allegations.

| Check | Recount | Result |
|---|---|---|
| Drawn piece rows | 2225 | Census, not a sample |
| Headline passage absent | 0 | All drawn passages located |
| Wrong earliest saved listing day | 0 | Every drawn day agrees with harvest and independent raw-link census |
| Wrong day-page capture/date/address | 0 | Every named timed capture matches its claimed day and contains the address |
| Cited page lacks the piece address | 2 | CV0011; CV1086: sidebar headline support only; use the correct day_page source |

The two source-address qualifications above are the only row failures in the expanded address check; there are no headline or day failures to list. A timed URL identifies a historical capture even when it was downloaded later.

| Printed number or population | Independent recount | Comparison |
|---|---|---|
| Harvested links | 2465 | Matches footnote |
| Story scope | 2234 | Matches total card and source count |
| Wider fallout | 136 | Matches footnote |
| Other | 95 | Matches footnote |
| Dots / dated story pieces | 2225 | Matches plot title |
| Story pieces without day | 9 | Matches exclusion footnote |
| All harvested sites | 497 | Not printed as the story-site count |
| Story sites, including undated pieces | 481 | Matches total card |
| Sites among plotted dots | 480 | Matches coverage caption |
| Additional first-listed pieces Oct 30–Nov 4 | 2 | Matches the six-day caption |

| First-listed day | Pieces / dots | Figure column |
|---|---|---|
| 2026-10-29 | 59 | agrees |
| 2026-10-30 | 1 | agrees |
| 2026-10-31 | 0 | agrees |
| 2026-11-01 | 0 | agrees |
| 2026-11-02 | 1 | agrees |
| 2026-11-03 | 0 | agrees |
| 2026-11-04 | 0 | agrees |
| 2026-11-05 | 12 | agrees |
| 2026-11-06 | 22 | agrees |
| 2026-11-07 | 24 | agrees |
| 2026-11-08 | 172 | agrees |
| 2026-11-09 | 515 | agrees |
| 2026-11-10 | 233 | agrees |
| 2026-11-11 | 270 | agrees |
| 2026-11-12 | 916 | agrees |

The scope function uses `WHO` (including Huang, Jensen, Megaspeed and Alice), an unnamed-spy pattern, or Nvidia plus a generic/specific story word. A narrow OTHER pattern rejects some generic Nvidia matches; the remaining links can become fallout or other. The script is applied as written: [scope_rule_recount.csv](scope_rule_recount.csv) has no differences, with positive controls for all three classes. The earlier diagnostic `scope_rule_differences.csv` is superseded: it compared the empty result with the wrong class label; it is not an audit finding.

For the required manual read I used Python Random seed **2026111402**, sorting each pool by address, drawing 150 from `story` first and then 150 from the combined `fallout` + `other` pool. The selection is [scope_sample.csv](scope_sample.csv). I read all 300 listed headlines and addresses, then opened the indexed saved article text and read its metadata and relevant passages where available: 69 kept and 43 excluded articles. For 81 kept and 107 excluded addresses the article was unavailable through the supplied story-page index; those are gaps, not negative article findings. Two Slashdot text extractions largely contain comments, which I did not treat as the article. This is not a claim to have fully read 300 article bodies.

| Sample | Plainly wrong | Unsettled generic headlines | Limit |
|---|---|---|---|
| Kept: 150 | 0 | 1 | No false inclusion established; article-copy gaps prevent a full-body error rate |
| Left out: 150 | 10 | 12 | 10 direct-story exclusions on the available evidence; not an estimate of every excluded article body |

I judged direct reporting about the relationship, investigation, government response or replacement as story; general financing, unrelated products, antitrust deals, ordinary chip supply and broader markets can remain outside. Borderline fallout was not automatically called wrong. The exclusions below are semantic weaknesses in a correctly applied word rule, not claims of selective intent.

| Sample | Address | Reason read from the available source |
|---|---|---|
| left-002 | https://www.washingtonsun.com/congress/gop-senators-demand-scrutiny-of-nvidia-fight-over-chip-exports | Saved article opens with senators investigating the Huang relationship and the suspected spy; this is a direct act in the story. |
| left-021 | https://gizmodo.com/china-is-racing-to-exploit-an-nvidia-loophole-before-the-trump-admin-slams-it-shut-2000839012 | Saved article leads with Huang resignation and recounts Alice Huang and Megaspeed; the listed wording masks its direct story focus. |
| left-041 | https://finance.yahoo.com/markets/stocks/articles/nvidia-slides-premarket-stock-futures-132000151.html | Saved page leads with the board investigation, the alleged spying relationship and possible replacement, rather than an independent stock-market event. |
| left-051 | https://ktvz.com/politics/cnn-us-politics/2026/11/11/bessent-confronts-lutnick-over-not-labeling-nvidia-customer-a-national-security-threat-sources-say/ | Saved CNN report is about the administration confrontation over Megaspeed and its handling of the Huang relationship. |
| left-062 | https://localnews8.com/politics/cnn-us-politics/2026/11/11/bessent-confronts-lutnick-over-not-labeling-nvidia-customer-a-national-security-threat-sources-say/ | Second address of the same CNN report: a distinct listed piece under the figure's address rule. |
| left-068 | https://www.sharecafe.com.au/2026/11/09/nvidias-china-links-under-fire-amid-ai-scrutiny/ | Saved article discusses Megaspeed, the personal revelations, no succession plan and the internal inquiry. It overlaps matters included elsewhere as story. |
| left-109 | https://seekingalpha.com/news/4671228-whos-next-in-line-to-lead-nvidia-prediction-markets-pick-their-favorites | The saved listed headline explicitly asks who is next to lead Nvidia: succession is within the stated story scope even without the trigger word successor. |
| left-115 | https://www.cbc.ca/news/world/nvidia-chips-china-ban-9.7416670 | Saved article subtitle and opening concern Alice Huang, the affair and alleged chip shipments; its account is directly about the story. |
| left-122 | https://finance.yahoo.com/markets/stocks/articles/nvidia-back-below-4-trillion-141310709.html | Saved article leads with reports of ousting Huang after two affairs and the search for replacements. |
| left-149 | https://abc17news.com/politics/national-politics/cnn-us-politics/2026/11/12/us-intel-isnt-sure-if-businesswoman-spied-on-nvidia-for-china-doesnt-mean-she-wasnt-a-risk-sources-say/ | The saved listed headline asks whether the businesswoman spied on Nvidia for China, the central disputed allegation. The word rule misses spied. |

All judgments, including the unsettled items, are in [scope_sample_judgments.csv](scope_sample_judgments.csv). No model script made these relevance judgments. The observed exclusion mismatch is 10/150 (6.67%); a nominal Wilson 95% interval is 3.66%–11.83%. It describes these available-text judgments, not a fully observed article-level population. The kept sample establishes no plain mismatch; it does not establish a zero population error rate.

| Saved-page check | Recount / limit |
|---|---|
| Pages read | 155: 153 timed and 2 undated/permalink pages |
| Cited by at least one drawn piece | 79 |
| Not cited by a drawn piece | 76 |
| Missing scheduled captures | None: all 150 combinations of two aggregators × 15 days × 09/12/16/20/23 hours are present; three extra timed captures are also present |
| Whole days without a saved page | None in Oct 29–Nov 12 |
| Hours without a capture | Each day has no capture at 00–08, 10–11, 13–15, 17–19, 21–22 Eastern; 14:00 is additionally present Nov 12. The exact per-day list is coverage_days.csv. These are harvest gaps, not zero-coverage claims. |
| Last column cutoff | Latest saved historical capture is 23:00 Eastern Nov 12 on both services. The footnote states the 11 pm schedule, but there is no capture for the remainder of the last hour; the old 14:00 cutoff is not the final cutoff. |
| Retrieval dates | 65 aggregator pages were retrieved Nov 12; 90 Nov 14. The figure footnote incorrectly says fetched Nov 12–13. |

Uncited pages are listed individually in [aggregator_pages.csv](aggregator_pages.csv), including citation and dating-use counts. An uncited later capture need not add a new first-listed story. The 09/12/16/20/23 schedule is a coarse observation grid on every day, and does not measure publication time, readership or the number of articles missed between snapshots.

For member counts I re-read the saved text for all 1,086 indexed pages and searched the named first-name/title patterns. All 31 actual member-name searches and all 35 title-word rows reproduce their published counts. Those are separate populations: the second Massie row, for example, counts only the word after a title. The 24 printed member counts also agree.

| Name / token | Kind | Published | Recount | Drawn or reason |
|---|---|---|---|---|
| Warren | member search | 62 | 62 | drawn |
| Coons | member search | 43 | 43 | drawn |
| Cramer | member search | 19 | 19 | drawn |
| Schumer | member search | 16 | 16 | drawn |
| Banks | member search | 15 | 15 | drawn |
| Cornyn | member search | 5 | 5 | drawn |
| Kennedy | member search | 5 | 5 | drawn |
| Thune | member search | 6 | 6 | drawn |
| Mast | member search | 88 | 88 | drawn |
| Crawford | member search | 69 | 69 | drawn |
| Meeks | member search | 8 | 8 | drawn |
| Himes | member search | 5 | 5 | drawn |
| Huizenga | member search | 4 | 4 | drawn |
| Moolenaar | member search | 78 | 78 | drawn |
| Jeffries | member search | 24 | 24 | drawn |
| Magaziner | member search | 4 | 4 | drawn |
| Subramanyam | member search | 3 | 3 | drawn |
| Bacon | member search | 3 | 3 | drawn |
| Johnson | member search | 6 | 6 | drawn |
| Blumenthal | member search | 3 | 3 | drawn |
| Wyden | member search | 3 | 3 | drawn |
| Ricketts | member search | 2 | 2 | named on fewer than three pages |
| McCaul | member search | 3 | 3 | drawn |
| Warner | member search | 3 | 3 | drawn |
| Cotton | member search | 5 | 5 | drawn |
| Jordan | member search | 12 | 12 | a current member the pages name for other things: his election as House minority leader |
| Stevens | member search | 7 | 7 | a current member the pages name for other things: an endorsement and an absence from a vote |
| Massie | member search | 5 | 5 | a current member the pages name for other things: his bid to impeach the defense secretary |
| Garcia | member search | 5 | 5 | a current member the pages name for other things: other inquiries he plans as incoming oversight chair |
| Hyde-Smith | member search | 4 | 4 | a current member the pages name for other things: losing her Senate race |
| Sanders | member search | 3 | 3 | a current member the pages name for other things: the Senate leadership contest and his own AI bill |
| Brian | word after title | 66 | 66 | a word found after a congressional title: part of a name searched above |
| John | word after title | 58 | 58 | a word found after a congressional title: part of a name searched above |
| Elizabeth | word after title | 52 | 52 | a word found after a congressional title: part of a name searched above |
| Rick | word after title | 28 | 28 | a word found after a congressional title: part of a name searched above |
| Chris | word after title | 24 | 24 | a word found after a congressional title: part of a name searched above |
| Kevin | word after title | 21 | 21 | a word found after a congressional title: part of a name searched above |
| Hakeem | word after title | 17 | 17 | a word found after a congressional title: part of a name searched above |
| Jim | word after title | 15 | 15 | a word found after a congressional title: part of a name searched above |
| Chuck | word after title | 11 | 11 | a word found after a congressional title: part of a name searched above |
| Greer | word after title | 8 | 8 | a word found after a congressional title: not a current member: the U.S. trade representative |
| Gregory | word after title | 8 | 8 | a word found after a congressional title: part of a name searched above |
| Jamieson | word after title | 8 | 8 | a word found after a congressional title: not a current member: the U.S. trade representative |
| Mike | word after title | 7 | 7 | a word found after a congressional title: part of a name searched above |
| Eric | word after title | 6 | 6 | a word found after a congressional title: not a current member: a former member (Swalwell) |
| Bill | word after title | 5 | 5 | a word found after a congressional title: part of a name searched above |
| Garcia | word after title | 5 | 5 | a word found after a congressional title: part of a name searched above |
| Harvey | word after title | 5 | 5 | a word found after a congressional title: not a current member: Nvidia's board chair |
| Jones | word after title | 5 | 5 | a word found after a congressional title: not a current member: Nvidia's board chair |
| Robert | word after title | 5 | 5 | a word found after a congressional title: part of a name searched above |
| Thomas | word after title | 5 | 5 | a word found after a congressional title: part of a name searched above |
| Cindy | word after title | 4 | 4 | a word found after a congressional title: part of a name searched above |
| Hyde-Smith | word after title | 4 | 4 | a word found after a congressional title: part of a name searched above |
| Michael | word after title | 4 | 4 | a word found after a congressional title: part of a name searched above |
| Seth | word after title | 4 | 4 | a word found after a congressional title: part of a name searched above |
| Swalwell | word after title | 4 | 4 | a word found after a congressional title: not a current member: a former member |
| Tom | word after title | 4 | 4 | a word found after a congressional title: part of a name searched above |
| Anthony | word after title | 3 | 3 | a word found after a congressional title: not a current member: a former member (Weiner) |
| Jensen | word after title | 3 | 3 | a word found after a congressional title: not a current member: Huang ("Nvidia Leader ... Jensen Huang") |
| Mark | word after title | 3 | 3 | a word found after a congressional title: part of a name searched above |
| Massie | word after title | 3 | 3 | a word found after a congressional title: part of a name searched above |
| Richard | word after title | 3 | 3 | a word found after a congressional title: part of a name searched above |
| Ron | word after title | 3 | 3 | a word found after a congressional title: part of a name searched above |
| Suhas | word after title | 3 | 3 | a word found after a congressional title: part of a name searched above |
| Tae-won | word after title | 3 | 3 | a word found after a congressional title: not a current member: the chairman of a Korean company |
| Weiner | word after title | 3 | 3 | a word found after a congressional title: not a current member: a former member |

The whole supplied sitting-cohort roster was also searched by full names and, where unambiguous, title/surname. Its only additional three-plus-page flags were Eric Swalwell (the selection table explicitly annotates him as a former member) and Marco Rubio (already drawn as Secretary of State, as the saved reports describe him). Neither is an unexplained omitted actor. The six current-name exclusions have explicit reasons in member_selection.tsv. This checks that a reason is listed; part three, not this lane, judges all those selection reasons. The frozen roster's use of `sitting` is taken as the requested denominator, not independently certified as an office-holding roster for every date.

Controls are in [controls.csv](controls.csv): real headline/address hits, an invented headline rejected, three real scope classes, actual Warren/Mast member hits, actual title-word hits, and a full-roster Warren hit. Every census result is bounded by the saved corpus. Gaps and privacy checking are carried in REPORT.md. No conclusion here attributes a motive.

Measured interval correction: direct calculation in validate_audit.py gives 3.66%–11.84%; this supersedes the earlier upper endpoint printed as 11.83%.
