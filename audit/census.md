# Coverage census

Scope: frozen saved pages only. Script: `census.py`; per-piece results: `coverage_checks.csv`; saved-page inventory and hashes: `aggregator_pages.csv`. No network requests were made.

| Check | Result |
|---|---:|
| Rows checked against their cited saved page | 1,662 |
| Headline/passage absent after HTML entity, punctuation and whitespace normalization | 0 |
| First-listed day differs from the earliest dated harvest record for that address | 0 |
| Harvest addresses | 1,911 |
| Selected addresses, including undated ones | 1,726 |
| Dated selected addresses drawn as dots | 1,662 |
| Selected addresses without a date, not drawn | 64 |
| Sites among all selected addresses | 425 |
| Sites among the dated addresses actually drawn | 416 |

There are no row IDs to list for either of the two requested failure tests. Positive and negative controls passed: a real first row was found, an invented headline and address were rejected, and a wrong date was rejected. This checks presence in saved aggregators, not the truth of the underlying news.

An additional check against actual saved HTML anchors found a date problem hidden by the matching tables: CV0473 is assigned Nov 8 in both tables, but cites the Nov 12 morning page. Its address appears in the Nov 12 saved anchors and not in earlier saved anchors. Its own address also carries a Nov 12 key. Moving that one dot would change Nov 8 from 126 to 125 and Nov 12 from 647 to 648, before any scope corrections.

Eight addresses are not literal matches in the cited HTML. Six (CV0461–CV0466) differ only in the recorded http/https scheme. The other two, CV0011 and CV1086, cite an Oct 29 Memeorandum page whose footer contains current Nov 12 Techmeme headlines and links to Techmeme, rather than to the recorded news addresses. Their headline presence is real, and their recorded first day is Nov 12, but those citations do not directly bind the news address. A current cross-promotion footer must not be treated as historical Oct 29 coverage.

| First-listed day | Coverage table | SVG dots | Printed day count |
|---|---:|---:|---:|
| 2026-10-29 | 43 | 43 | 43 |
| 2026-10-30 | 1 | 1 | 1 |
| 2026-10-31 | 0 | 0 | blank (zero dots) |
| 2026-11-01 | 0 | 0 | blank (zero dots) |
| 2026-11-02 | 0 | 0 | blank (zero dots) |
| 2026-11-03 | 0 | 0 | blank (zero dots) |
| 2026-11-04 | 0 | 0 | blank (zero dots) |
| 2026-11-05 | 9 | 9 | 9 |
| 2026-11-06 | 18 | 18 | 18 |
| 2026-11-07 | 26 | 26 | 26 |
| 2026-11-08 | 126 | 126 | 126 |
| 2026-11-09 | 417 | 417 | 417 |
| 2026-11-10 | 196 | 196 | 196 |
| 2026-11-11 | 179 | 179 | 179 |
| 2026-11-12 | 647 | 647 | 647 |

The 1,662-dot total and all printed daily counts reproduce the coverage table. The 1,726 tile counts dated plus undated selections. The top caption’s 425-site number uses the larger population; only 416 sites occur among the plotted dots. Its statement that the six days after Oct 29 brought one more piece is correct for these selections, not an assertion that the world published only one piece.

Selection is not reproducible from a stated rule in these tables. `harvest.tsv` supplies addresses, anchor text and first observations. `coverage_rows.tsv` marks selected addresses and whether they are drawn, but gives no inclusion/exclusion reason. The figure’s site/opinion-section rule concerns its three display colours, not a definition of being on the story. Every address was checked for table membership; 185 harvested addresses are outside the selected table. The examples below are clear topical omissions from their saved aggregator descriptions, not an instruction to delete or merge anything.

| Clearly topical harvested address left out | Saved description |
|---|---|
| https://www.axios.com/2026/11/11/trump-lutnick-nvidia-china-chip-export-controls | Sources: Howard Lutnick has stalled curbs on companies suspected of diverting Nvidia chips to China; Trump approved curbs for a third time in 2026 on November 5 |
| https://www.axios.com/2026/11/12/trump-lutnick-nvidia | Trump sticks by Commerce Secretary Lutnick despite Nvidia inaction |
| https://www.businessinsider.com/former-cia-officer-says-what-nvidia-case-can-teach-companies-2026-11 | Former CIA officer says US companies are underestimating China intelligence risks |
| https://www.businesstimes.com.sg/international/global/empty-offices-ties-blacklisted-firms-inside-chinese-companies-us-cleared-nvidia-chips | Empty offices, ties to blacklisted firms: Inside the Chinese companies the US cleared for Nvidia chips |
| https://www.geekwire.com/2026/nvidia-founders-wife-faces-spotlight-that-mackenzie-scott-and-melinda-french-gates-know-well/ | Nvidia founder's wife faces spotlight that MacKenzie Scott and Melinda French Gates know well |
| https://gizmodo.com/howard-lutnick-doesnt-want-to-stop-the-flow-of-nvidia-chips-overseas-report-2000838506 | Howard Lutnick Doesn't Want to Stop the Flow of Nvidia Chips Overseas: Report |
| https://www.joemygod.com/2026/11/axios-lutnick-blocked-wh-crackdown-on-nvidia/ | Axios: Lutnick Blocked WH Crackdown On Nvidia |
| https://ktvz.com/politics/cnn-us-politics/2026/11/11/bessent-confronts-lutnick-over-not-labeling-nvidia-customer-a-national-security-threat-sources-say/ | Bessent confronts Lutnick over not labeling Nvidia customer a national security threat, sources say |
| https://lansinginstitute.org/2026/11/09/the-nvidia-case-the-chinese-human-intelligence-threat-to-americas-technology-sector/ | The Nvidia Case: The Chinese Human-Intelligence Threat to America's Technology Sector |
| https://www.lawyersgunsmoneyblog.com/2026/11/nvidia-and-the-government | Nvidia and the Government — Nvidia makes the chips that AI runs on. All of them, apparently. |
| https://localnews8.com/politics/cnn-us-politics/2026/11/11/bessent-confronts-lutnick-over-not-labeling-nvidia-customer-a-national-security-threat-sources-say/ | Bessent confronts Lutnick over not labeling Nvidia customer a national security threat, sources say |
| https://madrobot.blog/2026/11/07/nvidia-h200-china-licences-empty-offices | The US cleared Chinese firms with empty offices to handle Nvidia's top AI chips, NYT finds |
| https://www.politico.com/live-updates/2026/11/11/congress/nvidia-documents-coons-warren-01161917 | Warren, Coons tell Trump officials to preserve Nvidia chip export records |
| https://www.politico.com/news/2026/11/12/trump-apple-tim-cook-nvidia-01162128 | ‘A Legend replaces a Legend’: Trump floats Apple's Cook to head up Nvidia |
| https://www.reuters.com/legal/government/house-democratic-leader-says-lawmakers-need-answers-nvidia-wants-china-chip-2026-11-09/ | House Democratic leader says lawmakers need answers on Nvidia, wants China chip restrictions |
| https://www.reuters.com/world/china/lutnick-stalled-trump-crackdown-diversion-nvidia-chips-china-axios-reports-2026-11-11/ | Lutnick stalled Trump crackdown on diversion of Nvidia chips to China, Axios reports |
| https://seekingalpha.com/news/4671228-whos-next-in-line-to-lead-nvidia-prediction-markets-pick-their-favorites | Who's next in line to lead Nvidia? Prediction markets pick their favorites |
| https://tech.slashdot.org/story/26/11/09/1758238/commerce-dept-chip-inquiry-was-halted-after-nvidia-intervention | Commerce Dept. Chip Inquiry Was Halted After Nvidia Intervention |
| https://www.theverge.com/ai-artificial-intelligence/1029483/nvidia-ai-chips-china-blacklist-government | The US let Nvidia sell chips to an empty office in China |
| https://www.wsj.com/politics/policy/top-democrats-target-trump-administrations-nvidia-china-records-0c212746 | Top Democrats Target Trump Administration's Nvidia-China Records |

| Included address with a different stated subject | Why it needs a scope decision |
|---|---|
| https://www.wsj.com/tech/ai/the-election-day-revolt-that-threatens-americas-ai-boom-03a53b52 | CV1679 describes executives at Huang’s midterms event discussing data-centre election results and OpenAI capacity plans, rather than the intelligence/affair reports or resignation. It can be context, but the current on-story count does not distinguish context. |

Other broad market, succession and newsletter items can reasonably be related coverage. I do not infer their contents from titles or force twenty off-topic examples. The clear omissions show that the selected total is neither a documented census of the story nor a consistently bounded list of context. No corrected global total is justified until the owner states and applies the scope rule to both included and excluded addresses.

Saved aggregator folders: 65. Of these, 63 are hour-labelled captures (including one additional Nov 12 14:00 variant), and two are story pages without an hour. 28 folders have no citing piece row; the rest have at least one. Being uncited is not evidence that a page was missing.

All scheduled 09:00 and 20:00 Eastern capture slots exist for both aggregators from Oct 29 through Nov 11. On Nov 12 both have 09:00, 12:00 and 14:00 captures. No whole day in the range lacks a saved page. For Oct 29–Nov 11 the other 22 hourly slots each day are unsaved; on Nov 12, through 14:00, 00:00–08:00, 10:00–11:00 and 13:00 are unsaved. Nov 12 after 14:00 is outside the declared cutoff. Those intervals are harvest gaps, not proof of no coverage.

Uncited saved folders:

- `memeorandum-1030-h0900`
- `memeorandum-1030-h2000`
- `memeorandum-1031-h0900`
- `memeorandum-1031-h2000`
- `memeorandum-1101-h0900`
- `memeorandum-1101-h2000`
- `memeorandum-1102-h0900`
- `memeorandum-1102-h2000`
- `memeorandum-1103-h0900`
- `memeorandum-1103-h2000`
- `memeorandum-1104-h0900`
- `memeorandum-1104-h2000`
- `memeorandum-1105-h0900`
- `memeorandum-1105-h2000`
- `memeorandum-1106-h0900`
- `memeorandum-1108-h0900`
- `techmeme-1030-h2000`
- `techmeme-1031-h0900`
- `techmeme-1031-h2000`
- `techmeme-1101-h0900`
- `techmeme-1101-h2000`
- `techmeme-1102-h0900`
- `techmeme-1102-h2000`
- `techmeme-1103-h0900`
- `techmeme-1103-h2000`
- `techmeme-1104-h0900`
- `techmeme-1104-h2000`
- `techmeme-1112-h1400`
