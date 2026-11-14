# Independent audit: “Fifteen days, mapped”

The frozen draft needs changes before publication. The employee-gift arithmetic reproduces the supplied records, but coverage selection is not a documented census, one first-listed date is wrong, several relevant ties are omitted, and some limits and negative statements need correction. This audit does not establish that any tie caused a report or statement.

Work was confined to this lane’s `out/` directory. No web fetch was made and no input, public figure, repository table or rule file was changed. Sources were read from saved articles, HTML, structured filings, cited pack rows and, where needed, saved originals. The ad frames and platform screenshots were also inspected visually; no OCR was run.

## A. Row findings

| Result | Rows |
|---|---:|
| Read and graded | 230 |
| ok | 181 |
| qualification | 49 |
| error | 0 |

| Row class | ok | qualification | error |
|---|---:|---:|---:|
| dated act of an actor | 67 | 6 | 0 |
| note | 2 | 0 | 0 |
| tie between two actors | 24 | 2 | 0 |
| tie in the network at left | 23 | 0 | 0 |
| dated event before the fortnight | 2 | 0 | 0 |
| background of a group of actors | 6 | 3 | 0 |
| dated event | 1 | 0 | 0 |
| tie of a member of Congress | 54 | 38 | 0 |
| count across Congress | 2 | 0 | 0 |

`findings.csv` has one append-only judgment for every non-coverage row. `source_checks.csv` records all 232 distinct cited source references and their saved-file hashes; all were readable. Quotations are at most 300 characters. The 49 qualified rows include 28 instances of one corpus-bound problem and seven instances of an incompletely shown network chain; they are not 49 unrelated defects.

The most consequential findings are:

1. **The network omits relevant funding and business ties.** The saved grant index records funding to Ryan Fedasiuk’s current institution, the Foundation for American Innovation, while the figure draws only his former CSET role. It also records a 2017 Open Philanthropy award to OpenAI. Existing Nvidia–Anthropic and Nvidia–OpenAI business ties, Nvidia’s inaugural-fund contribution, and a CNAS publication link are in cited sources but omitted. These omissions should be handled with the same dated-record rule as the ties already drawn.
2. **The footnote’s no-contact claim is too broad.** The saved transcript establishes the Anthropic chief executive’s testimony at a hearing Blumenthal chaired. The figure can say that no saved document establishes contact to produce or prompt these reports; it cannot deny every contact with the members who spoke. Likewise, personal gift filings do not prove that no client ever directed a gift.
3. **The coverage has a selection and dating problem.** The figure reproduces the selected table, but clear topical harvested links are excluded without reasons. The plotted dots represent 416 sites; the caption’s 425 includes sites seen only among undated selections. CV0473 is assigned Nov 8 despite its cited snapshot and earliest saved address being Nov 12. Do not replace the total with a guessed corrected total: define the inclusion rule, then reapply it to both sides.
4. **Warner’s ARI PAC total is not reconciled across disclosure systems.** The FEC Schedule B entries total $5,000; a separate LD-203 record reports $2,500 for the same payer, payee and June 23 date as two FEC entries totalling $2,500. The displayed $7,500 adds them. That overlap needs disposition. I retain both records and do not claim proven duplicate identity or silently deduct the amount. A supported label can state the $5,000 FEC total and the separately reported LD-203 amount with overlap unresolved.
5. **A roster is drawn as completed testimony.** TY090’s cited saved API record lists the Anthropic co-founder as a witness and links to documents; it does not itself establish appearance. Use “listed as a witness” unless the transcript is checked. By contrast, TY029’s actual Senate transcript does establish the chief executive’s testimony and Blumenthal’s chairmanship.
6. **Limits are unevenly preserved.** Nvidia’s specific denial that customers received sensitive information, officials’ initial belief that Huang did not know, and the absence of a defensive briefing are not adequately shown. Singapore’s warning over inaccurate information and re-entry ban are omitted from the chip that selects the insufficient-evidence result. Preserve both adverse and limiting facts. Trump’s FBI quote drops his qualification about “something else.”
7. **The member-selection counts cannot be independently reconstructed from these inputs.** Each of the 23 displayed mention counts, the 1,086-page denominator and the seven exclusion decisions needs a supporting manifest/table. Comparable recipients who speak in cited reports are absent; that does not establish that they met the unpublished three-page threshold.

Other qualifications concern the Nov 4 date of the three chairs’ letter versus its Nov 5 release, the omitted six-month phase-out in the Anthropic government-use order, the nuclear scope of one Horizon fellowship, the meaning of “on file,” and an unsupported Nov 10 hiring date in ST08’s own citation set. The figure’s separately cited outside-counsel chip has a source for that date.

### Naming the subject of the reported intelligence finding

`named_subject_checks.csv` records 6 main-body/footnote namings and 87 coverage-tooltip namings of Alice Huang. Each main naming was checked as follows:

| Element | Attribution and scope |
|---|---|
| V0128 | The section’s Megaspeed affiliation is supported without asserting espionage; the long footnote explicitly attributes the unclear-role limit to NBC. See the element text in the naming ledger. |
| V0134 | The Times actor label explicitly says “what it reported, from its own pages.” Its surveillance chip stays within the saved Times account, which relies on people briefed on surveillance. |
| V0142 | The Journal actor label says this is its report as others describe it; the same chip includes Singapore’s next-day denial. The saved ministry statement is the source for the description. |
| V0326 | The chip explicitly says Himes told NPR, as NBC reports it, that her role needs clarification. That is what the NBC account says. |
| V0438 | The Ministry actor’s chip attributes the denial to Singapore and identifies it as a denial of the Journal account. It does not add a spy finding. |
| V0480 | The section’s Megaspeed affiliation is supported without asserting espionage; the long footnote explicitly attributes the unclear-role limit to NBC. See the element text in the naming ledger. |

The tooltip namings reproduce saved aggregator headlines labelled with the source site. Their presence and wording were checked, not the truth of the intelligence assessment. The main naming does not exceed the saved accounts when read with its actor labels. The assessment remains publicly untested; anonymous-source attribution and the denials must remain visible.

## B. Figure, element by element

The inventory contains 486 intended visible text segments, plus the 1,662 coverage tooltips checked by census. The figure has 43 actor rows, 72 dated chips, one explicitly undated podcast-summary item and 87 tie connectors. All 1,892 hidden IDs resolve; no row ID or filename appears in the visible text. The connectors stay left of the calendar and end at people or bodies, not dated acts. The title’s fifteen-day range is the inclusive Oct 29–Nov 12 range.

`figure_findings.csv` contains 56 problem entries (3 errors and 53 qualifications), followed by B-CLOSE. It includes a separate finding for each of the 23 unsupported member-frequency labels. The following overview identifies the other elements; full wording and row links are in that CSV. This was a text and geometry read of the supplied HTML, not a browser screenshot/clipping test.

| Finding | Element | Issue |
|---|---|---|
| B01 | 425 sites appear | The caption describes the 1,662 plotted pieces, which have 416 domains. 425 is correct only for all 1,726 selected pieces, including 64 undated pieces. Label the two populations separately. |
| B02 | 126 (Nov 8); 647 (Nov 12) | These reproduce the table, but CV0473 is assigned Nov 8 although its cited snapshot and earliest saved HTML anchor are Nov 12. Moving that dot gives 125 and 648 respectively, before resolving coverage scope. |
| B03 | 1,662 pieces on the story, by the day first listed | The tables do not state a reproducible on-story selection rule and exclude clear topical pieces, including the Warren/Coons preservation letter, Huang successor proposals and the reported Commerce handling. The number is a selected-list total; a full harvested-s… |
| B04 | Sources: at Jensen Huang's midterms event, tech executives expressed concern over anti-data center res… | CV1679 has a different described subject, yet is counted as a piece on the allegations/resignation story. Decide and disclose a context category, applying the same rule to exclusions. |
| B05 | A newsletter says her Feb 2026 chip-bill announcement "came after" Anthropic's chief met Senate Bankin… | The wording states the limit, but the Anthropic-to-Warren line still implies a personal meeting not established by the newsletter. End at the committee or explicitly say Warren is not identified as an attendee. |
| B-MA37 | Letter asks Huang to brief three committees | Placed on Nov 5 as a dated act although the cited report dates the letter Nov 4; Nov 5 is its public release. The solid chip does not explain the distinction. Suggested: Letter dated Nov 4, released Nov 5, requests a joint closed-door briefing. |
| B-MA39 | Signs the letter to Huang | The signature belongs to the letter dated Nov 4. Nov 5 dates the release, not evidence of when he signed. Suggested: Co-signed the Nov 4 letter, released Nov 5. |
| B-MA47 | Signs the letter to Huang | The signature belongs to the letter dated Nov 4. Nov 5 dates the release, not evidence of when he signed. Suggested: Co-signed the Nov 4 letter, released Nov 5. |
| B-MA55 | "The FBI is looking into it" | Drops the same sentence's limit, "in terms of something else"; the shortened quote can imply a defined FBI investigation of the affair or a proven compromise. Suggested: Trump says the FBI is looking into it "in terms of something else"; he does not specify the … |
| B-MA57 | Says customer meetings are "part of a CEO's job" | The quoted defence is accurate, but omits Nvidia's specific denial in the same statement that customers received sensitive trade secrets or national-security information. The board's later statement is a different claim. Suggested: Says customer meetings are rou… |
| B-MA72 | As NBC reports its statement: interviewed her and held her passport in 2025; "insufficient evidence" o… | Selects the insufficient-evidence result but leaves out the same statement's adverse findings: a warning for inaccurate information and a re-entry ban. It also omits Singapore's complaint about limited U.S. assistance. Suggested: NBC relays Singapore: 2025 inter… |
| B06 | No gift from an Anthropic employee on file / No gift from an Nvidia employee on file | These 28 zeros reproduce the frozen employer extract, but the footnote defines on file using the PAC's Jun–Sep 2026 window. Use the employer extract's own 2026-cycle scope and Sep 30 cutoff, and distinguish no matching record from no gift ever. |
| B07 | Lobbyists whose firms had clients in the network | Some counted clients (ENCODE AI, Future of Life Institute, IFP Action, Center for AI Safety Action Fund) are absent from, or not connected in, the displayed network. Name each relevant client and its institutional chain; distinguish company, affiliate/action fun… |
| B-TY030 | Americans for Responsible Innovation's PAC: $7,500 · Apr 2025 to Jun 2025 | Adds FEC Schedule B entries to a same-payer/payee/date LD-203 amount without reconciling the two disclosure systems. The FEC entries total $5,000; the additional $2,500 may report the June 23 gifts already counted. Duplicate identity is not proven, so retain bot… |
| B-TY054 | A Horizon fellow placed with the committee he chairs, 2025–26 | Omits that this was a nuclear fellowship. In a figure about chip policy the unspecific label can suggest an AI fellowship. Suggested: Horizon lists a Nuclear Fellow placed with the House Foreign Affairs Committee, 2025–26. |
| B-TY090 | [private name omitted] testified before the committee he chairs · Jun 25, 2025 | The saved Congress API record is a witness roster, with document/video links and status Scheduled. It does not itself establish that the listed person appeared. The linked transcript was not among the cited originals read for this row. Suggested: Anthropic's co-… |
| B08 | Ordered agencies to stop using Anthropic, Feb 2026 | The same order allowed a six-month phase-out for existing agency use. Include that limit. |
| B09 | the board's inquiry found. Huang resigned before it reported. | No saved account gives the inquiry's findings. That bounded absence does not establish that no report had been issued anywhere when he resigned. Say the saved accounts do not give its findings. |
| B10 | any contact between Anthropic, or anyone tied to it, and the reporters, their sources or the members w… | This is too broad as written: actual earlier public contacts include the chief executive's testimony at a hearing Blumenthal chaired. Narrow the absence to contact about producing or prompting these reports/statements. It cannot deny every contact while mapping … |
| B11 | Gifts by lobbyists are second-hand: no client directed them. | Personal filings establish whose money was reported; they do not establish that no client ever directed a gift. The pack's repeated caution is not primary proof of a universal negative. Say no client direction is documented in these filings. |
| B12 | the two companies are counted one way | The employer/committee rules are shared, but historical coverage differs: nine Anthropic lines to Banks ($31,500) are restored from an earlier capture, with no equivalent Nvidia archive. This is disclosed later; state the comparison's limit alongside the equal-m… |
| B13 | Ryan Fedasiuk / Foundation for American Innovation | The network draws his former CSET role while omitting the saved grant link to his current institution. GR046 and the held grant index show a $2,714,000 2026 award for energy permitting reforms. The full held index also has 2023 and 2024 awards ($3,690,000 total … |
| B14 | OpenAI | The saved index used for the CSET money check also records a $30,000,000 Open Philanthropy award to OpenAI in 2017. That is a documented tie between a drawn actor and a named funder, absent from the network. Label it as a 2017 award, not present-day control. |
| B15 | One of seven companies that agreed to buy $26B of Anthropic stock, Nov 10 | This correctly reports the agreement, but the cited CNBC Nov 9 article already describes Nvidia as an investor in Anthropic and Anthropic as a significant customer. The existing relationship is omitted. Distinguish existing investment/supply from the prospective… |
| B16 | OpenAI / Nvidia | The cited Daily Caller account identifies Nvidia as OpenAI's key supplier; the cited CNBC live account also reports an August credit backstop. The network omits this commercial tie while showing Anthropic's ties. Apply the same dated-record rule or state an expl… |
| B17 | Nvidia gave $25M to his ballroom project, HuffPost reports | The ballroom amount is supported. The separately cited CNBC article also records $1M to the 2025 inaugural fund, absent from the network. Keep the two projects and dates distinct. |
| B18 | President Trump / Nvidia | Saved Al Jazeera and HuffPost accounts also describe Trump's own Nvidia stock transactions. These ties are absent. Attribute each account and period separately; their differently scoped amounts are not interchangeable. |
| B19 | Erich Grunewald / CNAS | The cited June 11, 2025 CNAS report names Grunewald as a co-author. This dated publication link to an institution already drawn at left is omitted. |
| B20 | No document here shows their sources. | The saved newspaper articles identify some public sources and spokespeople. What is not disclosed is the identity of confidential intelligence sources; narrow the sentence to that. |
| B21 | What the record does not show | Add the material limits in the saved reports: officials initially believed Huang did not know; he had not received a defensive briefing; which agencies, what information was passed and its value were unclear; Nvidia said no sensitive information was shared and c… |
| B22 | Seven others named that often for other things (a leadership vote, an election, an older letter) are n… | The seven identities, counts and exclusion dispositions are not in the supplied tables. Comparable gift recipients who act in cited reports are omitted, but the exact three-page threshold cannot be reconstructed. |
| B23 | Only analysts found in the funding records are drawn so far; a count of everyone quoted is under way. | The selective scope is candidly stated. The operational claim that a count is under way has no listed supporting row or table, and a reader still cannot see the unselected analyst population. Publish the roster or state simply that this is a selected set of anal… |
| B24 | One independent audit round read the first eight figures and their rows against the saved copies, and … | The provided inputs do not contain the earlier audit or its dispositions. Link them before relying on this status claim. This audit independently checks the current frozen figure, still without re-fetching originals. |
| B-FREQ-01 through B-FREQ-23 | Each member’s “Named on … of the 1,086 saved pages” label | No supplied row/table enumerates these counts or the denominator. Publish the count manifest and the seven exclusion dispositions. |

## C. Coverage census

| Measure | Recount |
|---|---:|
| Harvested addresses | 1,911 |
| Selected addresses / sites, including undated | 1,726 / 425 |
| Drawn dated addresses / sites | 1,662 / 416 |
| Undated selected addresses not drawn | 64 |
| Headline-presence failures | 0 |
| First-day failures against harvest table | 0 |
| Additional day failures against saved HTML anchors | 1 |
| Saved aggregator folders / uncited folders | 65 / 28 |

| Day | Oct 29 | Oct 30 | Oct 31–Nov 4 | Nov 5 | Nov 6 | Nov 7 | Nov 8 | Nov 9 | Nov 10 | Nov 11 | Nov 12 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Table and figure | 43 | 1 | 0 | 9 | 18 | 26 | 126 | 417 | 196 | 179 | 647 |

All plotted daily counts reproduce the coverage table; CV0473 shows why table agreement alone is insufficient. The additional address check found eight literal mismatches: six http/https differences and two current Techmeme cross-promotion headlines on an older Memeorandum page. The latter citations do not directly bind the news addresses. All checked passages equal the normalized full table headlines.

No whole day lacks a saved page, and every planned 09:00/20:00 Eastern slot exists through Nov 11. Nov 12 has 09:00, 12:00 and 14:00 captures for both aggregators. Other hourly slots are unsaved intervals, not days without coverage. `census.md` lists all uncited folders, the unsaved hours, twenty clear topical exclusions by address, and one included item whose described subject is a different midterms/AI-capacity story. There are 185 harvested addresses outside the selected table; the tables do not state an inclusion rule or reasons. No silent deletion, merger or reclassification was made.

## D. Members and money

| Check | Recount |
|---|---:|
| Employee-gift lines compared with displayed member lines | 46 matching lines |
| Supplied employee transactions matched to saved records | 1,170 |
| Drawn members with Anthropic-employer gifts | 15 of 23 |
| Drawn members with Nvidia-employer gifts | 3 of 23 |
| Drawn members with AnthroPAC money | 11 of 23 |
| AnthroPAC candidate recipients by party | 38 D + 43 R = 81 |
| All mapped Anthropic-employer recipients | 134; $3,481,696; 65 anonymous IDs |
| All mapped Nvidia-employer recipients | 63; $155,789; 77 anonymous IDs |

`members.md` contains all 23 members’ dollars, anonymous-person counts, first/last dates and AnthroPAC totals. Every employee and AnthroPAC figure matches its supplied table; the separate Warner ARI PAC overlap remains unresolved. `members_recount_final.csv` is authoritative. The preserved initial `members_recount.csv` missed Schumer’s join because he has no employee-gift committee key; the corrected join uses the explicit member key in the PAC table and includes his $3,500.

Obernolte ($36,073 from six Anthropic-employer donor IDs; $3,500 AnthroPAC), Rounds ($61,600 from ten; $1,500 AnthroPAC), Foster ($14,000 from three) and Cotton ($99,000 from fourteen; $2,500 AnthroPAC) illustrate comparable records not drawn. The first three also speak about the matter in cited reports. The stated choice rule is an action/mention threshold, not receipt of money, but its full count evidence is missing from the supplied inputs. Their omission is not treated as a proven violation of the three-page rule.

The companies share employer and committee matching rules, but their archival coverage is unequal: nine Anthropic-employer Banks lines, $31,500, use an earlier report capture; there is no equivalent Nvidia archive. The figure acknowledges this late in the footnote. Self-reported employer is the basis throughout. A gift is the individual’s money, not a company disbursement; committee gifts are not personal payments to members.

## E. Omissions, balance and the footnote

| Saved record omitted or insufficiently shown | Supported treatment |
|---|---|
| Foundation for American Innovation funding | The saved index gives $552,500 in 2023, $423,500 in 2024 and $2,714,000 in 2026: $3,690,000 total. The 2026 award is for energy permitting reforms. Show its tie to Fedasiuk’s institution without saying he personally received it or that it prompted his comments. GR046 is already cited in TY057. |
| Open Philanthropy–OpenAI | The CSET-check source’s saved index records a $30 million 2017 award to OpenAI. It is a dated grant, not a claim of present control. |
| Nvidia–Anthropic | CNBC’s cited Nov 9 article calls Nvidia an existing investor and Anthropic a significant customer. The figure shows only the later agreed stock purchase. |
| Nvidia–OpenAI | The cited Daily Caller account identifies Nvidia as OpenAI’s key supplier; the cited CNBC live account describes a credit backstop. Distinguish the relationship, date and attributed amount from claims about policy motive. |
| Nvidia–Trump projects and holdings | The cited CNBC article reports a separate $1 million 2025 inaugural-fund contribution in addition to the $25 million ballroom pledge. Saved Al Jazeera/HuffPost accounts also describe Trump’s Nvidia stock transactions; attribute their different periods and amounts separately. |
| Grunewald–CNAS | The cited June 11, 2025 CNAS report names him as a co-author. It is an omitted publication tie between a drawn actor and a named institution. |

Nvidia is given some comparable treatment: its employee gifts are shown by the same committee/employer rule; lobbying-report counts appear beside Anthropic’s for the same bills; its McCaul staffing tie, ballroom pledge and agreed Anthropic stock purchase are drawn. The network is nonetheless centred on Anthropic/its people/Open Philanthropy, rather than an equivalent census of Nvidia’s ties. It discloses selected analysts and the lack of searches of company channels. It does not clearly state that Nvidia’s political giving, commercial ties and former-staff network have not been mapped to the same breadth. Say that directly, or expand the mapping. Counts of lines or drawn ties cannot establish relative influence.

The footnote is useful but incomplete. It correctly distinguishes grants from bank-traced payments, announcements from ad runs, employee money from company money, bill mentions from office visits, source reporting from established intelligence findings, and current acts from older dated ties. It also includes the board’s no-reason-to-believe statement and NBC’s unclear-role limit. Add the following source limits:

- The Oct 29 Times account says officials initially did not believe Huang knew, he had not received a defensive briefing, and the agencies, information transferred and its value were unclear. Nvidia denied that customers received sensitive trade secrets or national-security information.
- The Nov 6 Times account includes Nvidia’s denial that customers asked it to press the U.S. government to change China chip-sale policy. It also reports Huang’s position that China should not receive Blackwell or Rubin. Do not collapse his position into opposition to every export restriction.
- Trump’s account that Huang said he did not know, and Trump’s own version of when he learned, should remain attributed and be presented beside the Times account. The shortened FBI quote needs its scope limit.
- Singapore’s Nov 12 account includes a warning for inaccurate police information, a re-entry ban and a complaint about limited U.S. assistance, alongside insufficient evidence of offences and no espionage investigation. The Oct 31 denial concerns the Journal’s specified account, not proof that she was never investigated for anything.
- The trust appointment source says trustees have no financial stake in Anthropic. Their governance role should not be read as equity ownership. The undated podcast-summary source also describes its speaker as wanting Nvidia to succeed and treating information-sharing as unknown; a title alone is not a recording or a dated act.

The ministry’s later statement is a substantive clarification of the earlier account. I did not find a separate formal correction notice in the cited saved news texts; the known ministry clarification provides a positive control that such a passage was detectable. This is bounded to these saved sources, not an assertion about all later reporting. The draft still has no saved finding of the board’s inquiry or public adjudication of the intelligence assessment.

A suitable replacement limit would be: “These saved records document dated relationships and attributed public accounts. They do not establish who supplied the confidential intelligence, whether the assessment is correct, or whether any mapped tie prompted coverage or statements. Earlier public contacts and institutional support are shown separately. The analyst selection is partial, company-channel searches were not made, and the companies’ historical filing coverage differs.” This wording must not be used to erase the omitted records above.

## Gaps, checks and handoff

`gaps.csv` has 0 missing/unreadable cited-file entries. That does not cure the absence of an actor-selection manifest or supply primary Journal/FT articles where only relayed accounts were cited. Every cited source reference was openable, but originals were not re-fetched. The audit checks the frozen claims against saved material, not the truth of the underlying allegations.

The required generic conformance command was attempted after reading its parser. It exited 1 because this audit lane has no `casework.json`; consequently it produced no G1–G6 verdict. I did not invent a configuration or claim those gates passed. The lane-specific ladder instead checked input hashes, row completeness, source reachability, coverage and gift censuses, figure closure, and restart skipping, with negative controls. It passed three consecutive times on the final audit scripts and findings; `validation.log` records the runs.

All 14 frozen input hashes remain unchanged. The pre-report name scan covered 35 files and found 0 remaining full-name matches. The scan used names from the saved donor and lobbyist originals, including name-order and filename-slug variants, with a positive detection control. Two full-name matches in quoted executive-appointment passages were removed under the naming rule; no finding, grade or row was removed. This report is screened by the same detector in memory before it is written. No donor or lobbyist identities are supplied.

The output round note and artifact hashes are in `ROUNDS.md` and `ARTIFACTS.sha256`. `READY_TO_CLOSE` hands the findings to the owner. No job remains running or armed by this audit. The owner’s next steps are to dispose each finding, state and rerun the coverage/member-selection rules, amend the figure, and audit the changed rows and counts; a later round must read both round notes and the frozen pins first. The publication/re-fetch decision remains with the owner.

audit: incomplete originals not re-fetched
