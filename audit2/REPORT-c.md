Second independent audit, part three: selection, remarks and omissions

Round 2 finish-only report, recorded 2026-11-15T02:43:43.280360+00:00. **42 findings — 5 errors and 37 qualifications. Part C remains unfinished.** This report retains round 1’s source readings and corrected judgments; round 2 checked the saved deliverable tables and finalized the handoff. No evidence-set search, source-tree walk or web fetch was repeated. The frozen-input hash checks and search-mechanics totals below are retained round-1 results, not newly run checks. The unadjudicated lookup remainder is not certified. Audit writes remain confined to out/.

The strongest omitted record is Fazl Barez’s person-specific research support. The complete saved Reuben College biography says his research is supported by Anthropic, NVIDIA, OpenAI and Schmidt Sciences. The saved Nov 9 Al Jazeera page carries his current remark. This contradicts the explanation that only an Oxford award to another institute was held and defeats the claimed exhaustive seven-analyst selection. It is research support, with no amount or support dates stated; it is not evidence of employment, personal remuneration or a motive. See C08 and [additional_originals.csv](audit2/out/additional_originals.csv).

Two chips use the relay day despite an explicit act day: Maguire’s post is Sunday Nov 8 in saved Semafor, but MA88 sits on Nov 9; Himes’s NPR interview is Nov 10, but MA42 sits on Nov 12. The other errors concern counting two read IAPS background memos as items on this matter and the Anthropic panel’s stale claim that its own channels were not searched. The footnote and own-channel register say that search occurred.

Important omitted qualifications cut in both directions. The board’s Nov 8 confidence in Huang, Nvidia’s stated security answers, Mast’s praise of Nvidia, and the limits in Fedasiuk’s, Moolenaar’s and Jeffries’s statements are missing from the relevant chips. Maguire’s criticism of Huang’s conduct and Ackman’s express national-security condition are missing from supportive rows. These are attributed positions, not findings that the positions were true.

The authoritative grades are in [selection_findings_final.csv](audit2/out/selection_findings_final.csv). The required append-only [selection_findings.csv](audit2/out/selection_findings.csv) retains earlier wording and grades. [adjudication_corrections.csv](audit2/out/adjudication_corrections.csv) records the conservative C01 and C09 grade corrections and the other source/date clarifications; do not add the successive materializations together.

| Part | Reading/count coverage | Errors | Qualifications |
|---|---|---:|---:|
| A | 24 excluded entries on at least three pages; eight drawn exceptions; two proved alias joins | 0 | 5 |
| B | All 472 remark-register lines, 451 distinct keys | 2 | 11 |
| C | 269 analyst and 729 byline memberships recounted; 57 lookup judgments; hit adjudication unfinished | 1 | 11 |
| D | 111 original-chip entries, 63 actor groups and all 45 additional-item lines | 2 | 5 |
| E | Long footnote and the reported omitted-role, policy and interested-voice sources | 0 | 5 |
| Total | 42 findings | 5 | 37 |

**Part A — who is drawn.** [selection.csv](audit2/out/selection.csv) contains every required comparison. A speaker count is a register label, not necessarily a distinct person. Delangue’s proved name variants reach five distinct pages; Zhao’s name/CZ variants reach four. Both are omitted supportive reactions. Rao’s three Yahoo versions identify him as Unconventional AI’s founder and CEO; “cannot tell” about funding is not an identity-based reason to exclude him. McGee has four speaking pages and Culpan three, yet authored pieces exclude them while one authored piece is enough for Hashim and Kubinec. There are weaker drawn page records; the declared tie-based exception explains some, but the exception and occupational boundaries are not applied consistently.

| Required comparison | Labels | Support Huang/Nvidia or oppose removal | Press Huang/Nvidia | Both |
|---|---:|---:|---:|---:|
| Drawn speaker entries | 58 | 15 | 26 | 3 |
| Excluded entries on at least three pages | 24 | 3 | 7 | 1 |
| Additional proved alias groups | 2 | 2 | 0 | 0 |

These flags overlap. Ten of the 24 excluded entries are collective labels, six of them pressure labels already represented by named actors. After removing those represented collectives and adding the two proved alias groups, five of 20 supportive voice labels are excluded, against one of 27 pressure voice labels. This suggests an imbalance **within this required comparison**, not a population-wide bias estimate: ordinary under-three-page exclusions were not all reread, and several drawn entries receive a separate occupational/tie exception. Rob Wiblin’s additional one-page criticism, discussed below, is outside this denominator. Bases are in [stance_counts.csv](audit2/out/stance_counts.csv) and [stance_alias_adjustments.csv](audit2/out/stance_alias_adjustments.csv).

| Drawn below three speaking pages | Pages | Recorded ground |
|---|---:|---|
| Grunewald; Stapp | 2 each | Current analyst remarks plus named IAPS/CNAS or IFP roles |
| King; Nie | 1 each | Current analyst remarks plus named institutional/fellowship roles |
| Hashim | 1 | Current authored piece plus Tarbell team record |
| Anthropic | 1 | Core subject/network context and the offering act; not an ordinary three-page speaker selection |
| McCaul; Wyden | 2 each | Three relevant named pages in the separate published congressional selection table; speaking-page and named-page denominators differ |

A complete Anthropic-versus-Nvidia tie-selection rate is not established and cannot be finished from the saved tables with a few targeted reads (round2:Part-A-comparable-tie-selection-rates in gaps.csv). The observed counts themselves show different rules: all seven selected analyst labels have an Anthropic/Open Philanthropy/group connection; 262 other analyst labels are not drawn. The register’s Nvidia-kind speaker labels split five drawn, one excluded on at least three pages, and 28 below three pages, many merely board/CEO/name variants. Those are not comparable person populations. This reading additionally identifies Barez with support from **both** companies, two omitted Hugging Face leaders with a reported pending Nvidia acquisition, and Wiblin with an Open Philanthropy-funded organisational role. The figure foregrounds Anthropic-related connections while leaving material records on both sides out.

**Part B — what the chips carry.** All 472 lines have individual decisions in [remarks_lines.csv](audit2/out/remarks_lines.csv): 172 hold, 67 hold partly and 233 do not hold. The corrected 451-key view in [remarks_effective.csv](audit2/out/remarks_effective.csv) has 169 yes, 60 partial and 222 no. A failed mapping is not automatically a false chip: many statuses matched a different sentence of the same statement, and some words appear on a different chip. The original [remarks.csv](audit2/out/remarks.csv) preserves the per-key notes and all repeated indices.

| Material omission or mapping problem | Effect on the row |
|---|---|
| Board confidence; Nvidia’s claimed threat-notification/security response; Huang’s claim to have checked GPU deployments | Removes the stated assurance or claimed basis of a denial |
| Mast’s praise; Fedasiuk’s favourable assessment; Moolenaar’s national-interest qualification | Makes a critical row less qualified than the saved statement |
| Maguire’s conduct criticism; Ackman’s explicit condition | Makes supportive rows less conditional than the saved statements |
| Trump’s Oct 31 conditions; Singapore’s stated information limit; Lutnick’s reported trade-policy objection | Loses sequence, uncertainty or policy explanation |
| Warren’s Nov 12 statement assigned to Oct 29 MA19; Huang’s Nov 8 memo assigned to Oct 29 MA106 | Wrong register matches; Warren’s statement is actually on MA99 |

**Part C — analysts, bylines and repeat lookups.** The printed totals are register units. [lookup_count_membership_effective.csv](audit2/out/lookup_count_membership_effective.csv) lists every contributing key.

| Analyst status | Labels |
|---|---:|
| Selected analyst entries in the speaker register | 7 |
| none found | 243 |
| none found for the person | 7 |
| cannot tell | 6 |
| not drawn | 4 |
| institution only | 2 |
| Total | 269 |

“Nine more” can be reconstructed as six institution-linked people — Schloetzer, Yoffie, Larcker, Barez, Chan and O’Hanlon — plus Carson, Epoch AI and CSIS. That uses ten register labels because Schloetzer has two. It is not a direct status sum and does not share the 269-label unit cleanly. The six unresolved entries cannot safely be described as absence of a record. The Epoch page gives the estimate’s coverage endpoint, not its publication day.

| Byline status | Outlet/byline entries |
|---|---:|
| none found | 653 |
| cannot tell, including agencies, pseudonyms and incomplete labels | 72 |
| drawn | 3 |
| record of another kind, not drawn | 1 |
| Total | 729 |

There are 681 distinct printed byline strings, not 681 proved people. The denominator includes Jason Ly’s October 2025 background release. His CSET staff role is affirmative in the held tables despite a none-found status. Five author-URL labels were resolved from saved HTML and searched under their actual names; a URL-only lookup does not look up its author’s full name.

| Selected or held cohort | Reading result |
|---|---|
| Seven selected analysts | All have person-specific professional records and current material. McGuire’s Anthropic link is a scheduled shared session, not funding or proof of attendance. Institutional funding does not prove a payment to the analyst. |
| Three selected bylines | Saved bios/team records affirm personal Tarbell support or roles and current pieces. Kubinec’s affirmative bio is outside the four table roots. |
| Schloetzer, Yoffie, Larcker | The examined grants concern another university unit or researcher; a whole-university award is not personal support. |
| Barez | Exclusion reason fails: the complete biography expressly attaches research support to him. |
| Chan and O’Hanlon | Current news names their Brookings posts. The held record has a 2026 award as well as 2015, and no consistent unit/temporal rule explains why these institutional posts are weaker than all selected ones. |
| Carson; CSIS; Epoch | Carson’s quote is expressly February 2025; CSIS is historical survey background. Epoch’s publication day remains a gap; its grant summary also omits a 2025 award. |
| Bair; Biderman | RAND trusteeship is a personal post, but overlap with the later award is not established. Biderman’s EleutherAI role and the held OpenAI institutional grant require a disposition beyond the paper-credit-only explanation; no direct Anthropic or personal grant is proved. |
| Cain | A 2021 congressional fellowship and held 2025 programme award do not establish funded current journalism; this is weaker temporal evidence than the selected contemporary Tarbell cases. |

See [drawn_people.csv](audit2/out/drawn_people.csv), [held_people.csv](audit2/out/held_people.csv) and [lookups_effective.csv](audit2/out/lookups_effective.csv). Perlo’s complete saved Tarbell bio also states a prior GovAI Winter Fellowship and CeSIA work. The GovAI role is omitted despite held institutional awards; the bio does not supply the fellowship year or establish personal payment.

The recursive search included every readable CSV/TSV path in the four research roots, including large bulk tables and nested test/audit copies. File-content reuse required equal full-file SHA256; this was not entity deduplication. Exact table paths, sizes, hashes and statuses are in [tables_searched_final.csv](audit2/out/tables_searched_final.csv); private name components of source paths are withheld.

| Root | Readable table paths | Apparent bytes |
|---|---:|---:|
| congress/research | 2,522 | 12,550,358,940 |
| lineage/research | 159 | 496,531,865 |
| toner/research | 163 | 736,079,792 |
| evaluators-deep/research | 180,526 | 89,686,522,918 |

The 183,370 readable paths have 10,101 content hashes. The final parser completed 7,414 candidate files; 2,687 others completed the literal full-name/surname prefilter. There are 1,043 unreadable fixture paths, recorded as gaps. These facts certify search mechanics, not people or ties.

**The requested complete hit reading was not achieved.** Round 2 does not attempt that substantial new job. The explicit remainder is now also recorded as round2:Part-C-hit-reading-unfinished in gaps.csv; it limits exhaustive omitted-tie conclusions in Part E. Only 57 source records have manual lookup judgments. The broad initial pass admitted unrelated given names sharing an initial and agency codes; its millions of candidates must not be called people. The historical displayed snapshot has 87,954 groups and 95,424 register/group pending lines. A further 59 parser-repaired tables, with 180,605 matching locations, fall outside that snapshot. [lookups_pending.csv](audit2/out/lookups_pending.csv) and [lookup_parser_repair_remainder.csv](audit2/out/lookup_parser_repair_remainder.csv) carry this remainder. Pass labels were unioned within displayed groups, so the first source anchor need not be the one with a full-name match.

Eight required controls have identified person/role records in the searched tables; a ninth has only a nested-fixture string/role record, and the tenth remains unmet. McGuire’s exact name/title occurs in a nested fixture and is only a string/role control. Kubinec’s sole loose IRS-registry match was not identified as the Dispatch/Tarbell reporter; his saved project bio cannot be silently substituted for a table hit. That required control remains unmet. The other positives demonstrate that the method can see held staff/fellow records. No no-record remainder is certified. [controls_identity.csv](audit2/out/controls_identity.csv) distinguishes these identity checks from historical raw string-match counts.

Nonpublication of the lists prevents readers from checking homonyms, missed posts, alias splits and exclusions. Publishing an unqualified list could imply that people were suspected of a tie, or were proved to have none. I would publish a versioned methods/selection ledger of public names, source scope, aliases, dates, positive records and unresolved matches, with an explicit incomplete status until this remainder is read. It should not label people “untied,” imply influence, or publish donor/lobbyist identities. The owner decides publication.

**Part D — actors’ own channels.** The numerical grouping reproduces the footnote’s historical search scope. The current figure has later added chips; these are baseline search counts, not a claim that 111 equals every current chip.

| Search group | Recount and membership |
|---|---|
| 111 original-chip entries | 30 found + one found with different words = 31; 72 blocked; eight not found |
| 132 own-channel lines | 45 item-not-in-chips; 33 item; 32 blocked; 22 nothing-on-matter-found |
| 63 actor groups | 30 have an item/item-not-in-chips status; otherwise 21 blocked, otherwise 12 nothing-found |
| All 45 additional-item lines | 12 exclusions hold, nine partly hold, 24 remain source gaps |

[own_channel_count_membership.csv](audit2/out/own_channel_count_membership.csv) gives the exact original line memberships and grouping precedence; [own_channel_items.csv](audit2/out/own_channel_items.csv) records every additional-item decision. The mechanical 30 includes the two read IAPS background memos explicitly disposed of as not mentioning this matter. FT links that could not be read remain gaps and are not evidence of silence or independently graded false reports. No invented corrected confirmed-actor total replaces 30.

The favourable qualifications in the FAI article and Moolenaar release, Jeffries’s stated lack of enough information, and the four-bill legislative demand deserve retention or a clear inclusion rule. The saved OpenAI PDF has a November 2026 cover date and the export-controls sentence relayed on MA69; it lacks a day, not a date altogether. A month label does not establish a particular day in the fortnight. Ministry originals support the relevant Chinese responses; unread embassy mirrors and Global Times full bodies remain gaps, with metadata-only support identified where used.

The long footnote generally treats blocked channels as gaps and expressly says nothing found is not proof of silence. The stale Anthropic panel contradicts that footnote and register. The off-matter IAPS classifications also overstate what the on-matter count establishes.

**Part E — omitted stakes, ties and limits.** Saved pages contain current voices not drawn with direct relevant interests: Hugging Face’s CEO and CTO in the reported pending Nvidia acquisition; Perplexity’s CEO; OpenAI employee Peter Steinberger; AI-platform founder Erik Voorhees; Unconventional AI’s Rao; Goldman’s CEO in the reported Nvidia-financing consortium; and Rebellions’ cancelled joint plans. These are saved-page roles and reported relationships, not assumptions about holdings or motives.

| Record class | Selection or omission |
|---|---|
| Eight interested voices identified above | Not a general census of interested companies, investors or their speakers |
| Barez’s Anthropic and NVIDIA research support | Person-specific support omitted on both sides |
| Perlo’s GovAI role; Wiblin’s 80,000 Hours role | Additional prior/current funded-group records omitted or excluded |
| Amodei’s January analogy | Historical policy strength understated; not a current act |
| Schneider’s matching-name CNAS post | Unresolved identity, not a proved added tie |

The saved Zvi page also quotes Rob Wiblin’s criticism. The complete 80,000 Hours staff page names him podcast founder/host and links the same account as the news embed; held rows record Open Philanthropy support for that organisation. His one-page “other” exclusion should be explained alongside the selected one-page commentators. The record does not show payment to him or prompting. Barez’s two-company research support and Perlo’s prior GovAI role are further omissions. Schneider remains an unresolved name match, not an added tie.

The saved TechCrunch page records Amodei’s much stronger January Davos chip-export analogy. It is historical policy background, not a current act or a motive. If the figure retains earlier policy context and Cotton’s historical exception, the mild Anthropic policy summary should either carry that strength accurately or explain the historical-context rule.

The long footnote usefully distinguishes dated ties from motives, protects unknown sources and prompting from inference, qualifies filing coverage, and distinguishes employee gifts from company money. It also admits that Nvidia’s former staff, business and political connections were mapped less broadly. The stated employee-employer giving rule is shared, but this is not an equally broad network comparison; this part does not independently certify the money sums. The unequal actor-selection rule should be visible near the title/rows, not left for a long footnote. The footnote’s no-record generalisation and stale search claims exceed the demonstrated search. Nothing read here establishes coordination, a reason for someone’s conduct, or that a tie caused the resignation.

**Gaps, controls and audit-tool limits.** [gaps.csv](audit2/out/gaps.csv) has 1,189 entries: the retained 1,187 source/control/identity and audit-artifact rows, plus two explicit round-2 scope/remainder gaps. The 1,043 unreadable recursive fixture paths are part of that count. The 24 additional-item gap verdicts overlap it; they are not 24 extra findings. Missing or unread originals were not graded as false facts. Specific remainder includes the Epoch publication day, inaccessible channels/full bodies, the unmet Kubinec table control and Schneider’s identity join.

The first privacy matcher was too broad and crossed field/public-name boundaries. It damaged 593 raw-hit records and 260 displayed packets and withheld some public labels. The 853 damaged records are now explicit unusable, parseable artifact-gap wrappers; originals remain available. This is my audit-tool defect, not a defect in the figure or a missing original. [artifact_gaps.csv](audit2/out/artifact_gaps.csv), [redaction_repairs.jsonl](audit2/out/redaction_repairs.jsonl) and [SEARCH_DESIGN.md](audit2/out/SEARCH_DESIGN.md) record it. Do not use those wrappers, merged query labels or broad candidates to infer identities or absence. Final count memberships and verdict files were rebuilt from the frozen register and manual decisions.

The saved round-1 validation records that all 84 frozen hashes matched and a deliberately wrong expected hash was rejected using actual input bytes. All 32 required A keys and all 472 B indices are covered. Deliverable checks found no malformed required CSV rows or Python syntax errors. A real held TSV row demonstrates that the old None-header sort fails and the corrected serializer retains the extra cells. Repeated deliverable checks do not pass the unfinished Part C audit gate. See [validation_final_v3.json](audit2/out/validation_final_v3.json) and [validation_passes.jsonl](audit2/out/validation_passes.jsonl).

Round 2’s privacy check was confined to the handover report, rounds and finding tables. The 20 unchanged tables exactly matched the SHA256 fingerprints of round 1’s completed field-aware donor/lobbyist-name screening; the original gap rows also matched before the two anonymous additions. Those checks were reused rather than repeated. The report and rounds were read in full for prohibited identities; named individuals in the report are public speakers, authors or officials covered by the brief, and the round-2 additions introduce no human names. No prohibited identity was found in that manual reading. The existing name-scanner positive control is a retained round-1 result (23 hits); round 2’s deliberately altered fingerprint was rejected. See [round2_checks.json](audit2/out/round2_checks.json) for the exact reused fingerprints and bounded checks.

The raw search dumps were left exactly as they were at the start of round 2. They hold copies of source rows, may contain private identities, and are excluded from the handover privacy claim. They were not opened for content, redacted, rewritten, moved or deleted in this round; metadata checks of the named dumps were unchanged. The earlier artifact damage described above is inherited from round 1. The owner handles those raw records.

[FINAL_FILES.md](audit2/out/FINAL_FILES.md) identifies the authoritative result views. The round-2 addition to [HANDOFF_RESTART.md](audit2/out/HANDOFF_RESTART.md) supersedes its earlier request to resume the large search. This finish-only lane is handed back to the owner for dispositions or a separately assigned lookup job. No audit job or watcher was launched or left intentionally running.

audit: incomplete Part C lookup control unmet and hit adjudication unfinished; originals not re-fetched
