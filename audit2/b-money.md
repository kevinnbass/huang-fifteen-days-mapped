# FEC money recount

The dollar, date and record counts below were recomputed from saved bulk lines and saved API JSON, not summed from the builder's employee-gifts table. The public table is used for the comparison and, in the explicitly conditional recount, its committee ownership keys. This distinction matters: **matching the published sums does not settle every committee's ownership**.

The independent statement parser and member mapping are in money_audit.py. It reads committee master/candidate-link/candidate-master ZIPs, the supplied sitting-cohort member IDs, the saved candidate cross-reference, API sponsor records and the original Form 1 files. Candidate aliases for another office require matching state, surname and a given name or conventional short form. Known IDs, rather than changing committee names, carry participant identity. A leadership PAC is attributed to its sponsor. No inference from a committee's name alone establishes that it has only one sitting member. All donor identity comparisons stayed in memory or were emitted as irreversible numbers; no donor or lobbyist names are in this report.

**1. Statements and ownership.** Every one of the 67 published rows was re-derived: 58 JFCs and 9 leadership PACs. The outcomes, sitting-member sets and statement participant counts agree; the raw-line dollar/line subtotals for all 67 also agree. The two placeholder-participant records remain unresolved, as the published table says. No second sitting member was found among the 34 published JFCs attributed to one member. This bounded negative has a positive control: the same parser identifies the multi-member Strongest America JFC, including members' campaign committees and leadership-PAC sponsor checks. The several-member committees remain attributed to none. Only after this reconstruction did I compare the private extractions: zero participant differences across the 58 JFCs and zero sponsor differences where independently compared.

| Committee | Kind | Participants | Sitting members | Independent outcome |
|---|---|---|---|---|
| C00406553 PROGRESSIVE VOTERS OF AMERICA | leadership PAC |  | Bernard Sanders | tied to its sponsor |
| C00536540 JOBS, FREEDOM, AND SECURITY PAC | leadership PAC |  | Ted Cruz | tied to its sponsor |
| C00673715 THUNE VICTORY COMMITTEE | joint fundraising committee | 3 | John Thune | tied to the one sitting member among its participants |
| C00676395 BLACKBURN TENNESSEE VICTORY FUND | joint fundraising committee | 3 | Marsha Blackburn | tied to the one sitting member among its participants |
| C00693796 BUCKEYE LIBERTY POLITICAL ACTION COMMITTEE | leadership PAC |  | Jim Jordan | tied to its sponsor |
| C00715136 OREGON BLUE VICTORY FUND | joint fundraising committee | 2 | Jeff Merkley | tied to the one sitting member among its participants |
| C00719062 THE EMPOWERMENT FUND | joint fundraising committee | 4 | André Carson; Ilhan Omar; Lateefah Simon; Rashida Tlaib | not attributed: 4 sitting members share it |
| C00744946 HARRIS VICTORY FUND | joint fundraising committee | 53 | none | no sitting member among its participants |
| C00750166 THE SQUAD VICTORY FUND | joint fundraising committee | 8 | Alexandria Ocasio-Cortez; Ilhan Omar; Ayanna Pressley; Rashida Tlaib | not attributed: 4 sitting members share it |
| C00764126 GOODEN VICTORY FUND | joint fundraising committee | 4 | Lance Gooden | not attributed: a participant could not be settled |
| C00765552 FALLON VICTORY FUND | joint fundraising committee | 3 | Pat Fallon | tied to the one sitting member among its participants |
| C00765727 TAHOMA PAC | leadership PAC |  | Marilyn Strickland | tied to its sponsor |
| C00772624 SHP VICTORY FUND | joint fundraising committee | 2 | Scott H. Peters | tied to the one sitting member among its participants |
| C00773416 GARBARINO VICTORY FUND | joint fundraising committee | 4 | Andrew R. Garbarino | tied to the one sitting member among its participants |
| C00773903 TEAM HILL | joint fundraising committee | 3 | J. French Hill | tied to the one sitting member among its participants |
| C00776526 TIM SCOTT VICTORY FUND | joint fundraising committee | 3 | Tim Scott | tied to the one sitting member among its participants |
| C00806620 JAKE AUCHINCLOSS VICTORY FUND | joint fundraising committee | 2 | Jake Auchincloss | tied to the one sitting member among its participants |
| C00814129 MORAN VICTORY FUND | joint fundraising committee | 3 | Nathaniel Moran | tied to the one sitting member among its participants |
| C00816025 LANDSMAN VICTORY FUND | joint fundraising committee | 3 | Greg Landsman | tied to the one sitting member among its participants |
| C00816611 TED LIEU VICTORY FUND | joint fundraising committee | 2 | Ted Lieu | tied to the one sitting member among its participants |
| C00817379 LAWLER VICTORY FUND | joint fundraising committee | 3 | Michael Lawler | tied to the one sitting member among its participants |
| C00818062 HOUCHIN VICTORY FUND | joint fundraising committee | 3 | Erin Houchin | tied to the one sitting member among its participants |
| C00825257 VICENTE GONZALEZ VICTORY FUND | joint fundraising committee | 2 | Vicente Gonzalez | tied to the one sitting member among its participants |
| C00826230 LAUREL LEE VICTORY FUND | joint fundraising committee | 5 | Laurel M. Lee | not attributed: a participant could not be settled |
| C00828541 NEVER SURRENDER, INC. | leadership PAC |  | none | sponsor is not a sitting member |
| C00829705 WINNING FOR AMERICA FUND | joint fundraising committee | 3 | Eric Schmitt | tied to the one sitting member among its participants |
| C00836304 COURAGE PAC | leadership PAC |  | Becca Balint | tied to its sponsor |
| C00836346 CAMPAIGN FOR DEMOCRACY COMMITTEE | joint fundraising committee | 2 | none | no sitting member among its participants |
| C00838250 TEAM FRY | joint fundraising committee | 3 | Russell Fry | tied to the one sitting member among its participants |
| C00838896 SCHIFF VICTORY FUND | joint fundraising committee | 3 | Adam B. Schiff | tied to the one sitting member among its participants |
| C00839886 SUPPORTING EFFECTIVE THOUGHTFUL LEADERSHIP PAC | leadership PAC |  | Seth Magaziner | tied to its sponsor |
| C00850925 BRANDON HERRERA VICTORY COMMITTEE | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00858373 GROW THE MAJORITY | joint fundraising committee | 89 | Tom Barrett; Nicholas J. Begich III; Robert P. Bresnahan, Jr.; Elijah Crane; Juan Ciscomani; Monica De La Cruz; Gabe Evans; Brian K. Fitzpatrick; Bill Huizenga; Jeff Hurd; Mike Johnson; Thomas H. Kean, Jr.; Jennifer A. Kiggans; Kevin Kiley; Nick LaLota; Michael Lawler; Mariannette Miller-Meeks; Ryan Mackenzie; Zachary Nunn; Scott Perry; Bryan Steil; David G. Valadao; Derrick Van Orden; Robert J. Wittman | not attributed: 24 sitting members share it |
| C00859058 EMMER MAJORITY BUILDERS | joint fundraising committee | 52 | Tom Barrett; Nicholas J. Begich III; Robert P. Bresnahan, Jr.; Elijah Crane; Juan Ciscomani; Jeff Crank; Monica De La Cruz; Tom Emmer; Gabe Evans; Brian K. Fitzpatrick; Brad Finstad; Bill Huizenga; Thomas H. Kean, Jr.; Jennifer A. Kiggans; Nick LaLota; Michael Lawler; Mariannette Miller-Meeks; Ryan Mackenzie; Zachary Nunn; Scott Perry; Bryan Steil; David G. Valadao; Derrick Van Orden | not attributed: 23 sitting members share it |
| C00868117 ADELANTE FUND | joint fundraising committee | 3 | Alex Padilla | tied to the one sitting member among its participants |
| C00873893 TRUMP NATIONAL COMMITTEE JFC, INC. | joint fundraising committee | 3 | J.D. Vance | tied to the one sitting member among its participants |
| C00878702 CHRIS PAPPAS VICTORY FUND | joint fundraising committee | 3 | Chris Pappas | tied to the one sitting member among its participants |
| C00887653 ROOTED IN MOVEMENT | joint fundraising committee | 2 | Delia C. Ramirez; Rashida Tlaib | not attributed: 2 sitting members share it |
| C00888388 SCOTT FITZGERALD VICTORY FUND | joint fundraising committee | 4 | Scott Fitzgerald | tied to the one sitting member among its participants |
| C00893388 JOYFULLY MOBILIZING ACTION AND COMMUNITY PAC - JMAC PAC | leadership PAC |  | Jennifer L. McClellan | tied to its sponsor |
| C00896225 MGP VICTORY FUND | joint fundraising committee | 3 | Marie Gluesenkamp Perez | tied to the one sitting member among its participants |
| C00896746 STRONGEST AMERICA JFC | joint fundraising committee | 10 | Bill Huizenga; Darrell Issa; Young Kim; Thomas H. Kean, Jr.; Anna Paulina Luna; Michael Lawler; Ryan Mackenzie; Scott Perry; Maria Elvira Salazar; Ryan K. Zinke | not attributed: 10 sitting members share it |
| C00896928 TEAM HUSTED | joint fundraising committee | 5 | none | no sitting member among its participants |
| C00898825 FRIENDS OF JIM RISCH | joint fundraising committee | 2 | James E. Risch | tied to the one sitting member among its participants |
| C00898957 KNOTT VICTORY COMMITTEE | joint fundraising committee | 3 | Brad Knott | tied to the one sitting member among its participants |
| C00900043 FISCHER VICTORY FUND | joint fundraising committee | 3 | Deb Fischer | tied to the one sitting member among its participants |
| C00905232 CAPITO VICTORY | joint fundraising committee | 3 | Shelley Moore Capito | tied to the one sitting member among its participants |
| C00907378 DEBBIE DINGELL MAJORITY FUND | joint fundraising committee | 2 | Debbie Dingell | tied to the one sitting member among its participants |
| C00908517 BALDERSON VICTORY FUND | joint fundraising committee | 3 | Troy Balderson | tied to the one sitting member among its participants |
| C00913574 COOPER VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00915140 ROUNDS VICTORY COMMITTEE | joint fundraising committee | 2 | Mike Rounds | tied to the one sitting member among its participants |
| C00916296 OHIO GRASSROOTS VICTORY FUND | joint fundraising committee | 4 | none | no sitting member among its participants |
| C00921353 KATIE HOBBS VICTORY FUND | joint fundraising committee | 1 | none | no sitting member among its participants |
| C00927939 CRAWFORD VICTORY COMMITTEE | joint fundraising committee | 3 | Eric A. "Rick" Crawford | tied to the one sitting member among its participants |
| C00931717 CLINE VICTORY COMMITTEE | joint fundraising committee | 3 | Ben Cline | tied to the one sitting member among its participants |
| C00933986 FISH FAMILY FREEDOM FUND | joint fundraising committee | 4 | none | no sitting member among its participants |
| C00943977 JULIANA VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00946483 AMERICAN DREAM FOR ALL PAC | leadership PAC |  | none | sponsor is not a sitting member |
| C00948497 TALARICO VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00949933 PAPPAS, PELTOLA, TALARICO, VINDMAN SENATE VICTORY FUND | joint fundraising committee | 6 | Chris Pappas; Adam B. Schiff | not attributed: 2 sitting members share it |
| C00950329 PULIDO VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00955781 MANNY RUTINEL VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00955807 MAINE VICTORY FUND 2026 | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00958066 ABDUL FOR MICHIGAN VICTORY FUND | joint fundraising committee | 3 | none | no sitting member among its participants |
| C00958561 NH MA VICTORY FUND | joint fundraising committee | 2 | Chris Pappas | tied to the one sitting member among its participants |
| C00958751 CAREGIVERS HOUSE VICTORY FUND | joint fundraising committee | 5 | Katherine M. Clark | tied to the one sitting member among its participants |
| C00959171 PERRIELLO VICTORY FUND | joint fundraising committee | 2 | none | no sitting member among its participants |

Each participant, its exact name on the statement, current committee name, committee ID, sponsor IDs and the resulting member is listed in [final_joint_participants_recount.csv](final_joint_participants_recount.csv). Raw statement paths are included. The raw comparison files [final_joint_differences.csv](final_joint_differences.csv) and [joint_amount_differences.csv](joint_amount_differences.csv) have headers and no differences.

| Missing from published joint table | Anthropic lines / dollars | Nvidia lines / dollars | Saved statement |
|---|---|---|---|
| C00487207 VAN HOLLEN VICTORY FUND | 7 / $84,000.00 | 0 / $0.00 | gap |
| C00492421 NANCY PELOSI VICTORY FUND | 0 / $0.00 | 1 / $500.00 | gap |
| C00548818 TEAM HUDSON | 2 / $50,000.00 | 0 / $0.00 | gap |
| C00580043 TEAM HUIZENGA | 1 / $9,000.00 | 0 / $0.00 | gap |
| C00583161 MAST VICTORY COMMITTEE | 2 / $17,000.00 | 0 / $0.00 | available; sponsor/participant checks still required |
| C00609255 SULLIVAN VICTORY | 3 / $51,000.00 | 0 / $0.00 | gap |
| C00616268 MORAN VICTORY COMMITTEE | 3 / $30,000.00 | 0 / $0.00 | gap |
| C00619486 TEAM LAHOOD | 4 / $30,500.00 | 0 / $0.00 | gap |
| C00624049 LOFGREN VICTORY FUND | 3 / $25,500.00 | 0 / $0.00 | gap |
| C00652644 TEAM FITZ | 1 / $500.00 | 0 / $0.00 | gap |
| C00678854 WITTMAN VICTORY COMMITTEE | 4 / $32,000.00 | 0 / $0.00 | gap |
| C00689836 RESCHENTHALER VICTORY FUND | 2 / $30,000.00 | 0 / $0.00 | gap |
| C00698340 MARKEY VICTORY FUND | 2 / $24,000.00 | 0 / $0.00 | gap |
| C00714527 MORELLE VICTORY FUND | 1 / $12,000.00 | 0 / $0.00 | gap |
| C00734319 BOOKER VICTORY FUND | 4 / $28,000.00 | 0 / $0.00 | gap |
| C00744599 HICKENLOOPER VICTORY FUND | 8 / $60,000.00 | 1 / $5,000.00 | gap |
| C00747840 AGUILAR LEADERSHIP FUND | 3 / $25,000.00 | 0 / $0.00 | gap |
| C00750919 OSSOFF VICTORY FUND | 18 / $212,999.00 | 2 / $1,250.00 | gap |
| C00753913 PFLUGER VICTORY COMMITTEE | 2 / $5,500.00 | 0 / $0.00 | gap |
| C00764373 BARRASSO VICTORY | 1 / $7,000.00 | 0 / $0.00 | gap |
| C00766790 BLUMENTHAL VICTORY FUND | 6 / $59,000.00 | 0 / $0.00 | gap |
| C00768762 GILLIBRAND VICTORY FUND | 4 / $48,000.00 | 0 / $0.00 | gap |
| C00772228 TEAM CRAMER | 6 / $50,000.00 | 0 / $0.00 | gap |
| C00774703 COTTON MAJORITY COMMITTEE | 7 / $67,500.00 | 0 / $0.00 | gap |
| C00779223 JOSH HAWLEY VICTORY COMMITTEE | 1 / $7,000.00 | 0 / $0.00 | gap |
| C00782698 TEAM RAJA VICTORY FUND | 1 / $2,000.00 | 0 / $0.00 | gap |
| C00788448 TEAM HAGERTY VICTORY | 1 / $7,000.00 | 0 / $0.00 | gap |
| C00812602 OBERNOLTE VICTORY FUND | 3 / $30,000.00 | 0 / $0.00 | gap |
| C00817874 BARRETT BRIGADE VICTORY FUND | 3 / $50,000.00 | 0 / $0.00 | gap |
| C00823930 TEAM KATIE | 7 / $54,500.00 | 0 / $0.00 | gap |
| C00823997 RUDY VICTORY FUND | 1 / $25,000.00 | 0 / $0.00 | gap |
| C00831669 KATHERINE CLARK MAJORITY FUND | 2 / $17,500.00 | 0 / $0.00 | gap |
| C00832949 PETE RICKETTS VICTORY FUND | 10 / $100,000.00 | 0 / $0.00 | gap |
| C00833319 MEEKS VICTORY | 3 / $25,000.00 | 0 / $0.00 | gap |
| C00842369 WHITESIDES VICTORY FUND | 3 / $25,000.00 | 0 / $0.00 | gap |
| C00845792 SHEEHY VICTORY COMMITTEE | 2 / $52,000.00 | 0 / $0.00 | gap |
| C00852012 TEAM MCCORMICK | 7 / $91,000.00 | 0 / $0.00 | gap |
| C00857615 TEAM JORDAN | 1 / $1,500.00 | 0 / $0.00 | gap |
| C00866947 CORNYN LONESTAR VICTORY FUND | 1 / $3,500.00 | 0 / $0.00 | gap |
| C00868091 LISA MCCLAIN LEADERSHIP FUND | 1 / $7,000.00 | 0 / $0.00 | gap |
| C00869719 TED BUDD MAJORITY COMMITTEE 2028 | 7 / $86,000.00 | 0 / $0.00 | gap |
| C00871152 GUTHRIE VICTORY FUND | 8 / $90,913.00 | 0 / $0.00 | gap |
| C00871244 KMR VICTORY FUND | 1 / $2,500.00 | 0 / $0.00 | gap |
| C00888156 TROY CARTER VICTORY FUND | 4 / $34,000.00 | 0 / $0.00 | gap |
| C00890137 GOODLANDER VICTORY FUND | 1 / $2,000.00 | 0 / $0.00 | gap |
| C00893230 LICCARDO VICTORY FUND | 3 / $25,000.00 | 0 / $0.00 | gap |
| C00895219 MARK WARNER VICTORY FUND | 5 / $50,000.00 | 0 / $0.00 | gap |
| C00896332 ASHLEY MOODY VICTORY FUND | 4 / $48,000.00 | 0 / $0.00 | gap |
| C00903658 FIRST STATE VICTORY FUND 2026 | 1 / $15,000.00 | 0 / $0.00 | gap |
| C00938720 TEAM ANDY KIM | 1 / $500.00 | 0 / $0.00 | gap |
| C00954172 JAKE JOHNSON VICTORY FUND | 0 / $0.00 | 1 / $3,000.00 | gap |
| C00957274 VILLEGAS VICTORY FUND | 1 / $2,000.00 | 0 / $0.00 | gap |
| C00957589 DARLINE GRAHAM MAJORITY FUND | 1 / $47,800.00 | 0 / $0.00 | gap |
| C00957605 MATSUI VICTORY FUND | 1 / $17,500.00 | 0 / $0.00 | gap |

There are 54 additional receiving committees designated J in the committee master. Their positive lines total $1,877,712 for Anthropic and $9,750 for Nvidia; the public gift table already counts $1,592,912 and $6,750 of those amounts respectively. Thus absence from joint_committees.csv is not the same as absence from the gift sum. For 53 the supplied committee folders contain no saved statement; the Mast statement is saved, but its leadership-PAC participant lacks an independently settled sponsor record here. Those gaps cannot establish a second member or an overstated total.

Across all employee-gift ownership keys, 90 committee assignments were not independently settled from the supplied original ownership records: 44 JFCs, 45 leadership PACs and one candidate committee (Raja for Illinois; the candidate master gives an initial rather than the member's searched given name). The missing-primary portions are [committee_ownership_not_settled.csv](committee_ownership_not_settled.csv) and gaps.csv, not false-attribution findings. The strictly settled current-record subtotal is 111 Anthropic member IDs / $2,488,837 and 62 Nvidia member IDs / $165,590. These are verification-coverage subtotals, **not corrected totals or estimates of the real total**. No committee excluded for an unresolved sponsor is declared unrelated.

**2. Raw lines by recipient kind.** [classified_fec_lines.csv](classified_fec_lines.csv) contains every latest transaction record, including excluded entities, memo lines and negatives. The first table below inventories distinct SUB_IDs from the two saved sources (bulk first where the same SUB_ID appears in both), before amendment/positive-line filtering; the second uses the latest file for a committee/transaction ID and the stated positive non-memo individual-receipt rule. These signed inventory sums are not a sum of independent gifts: conduit and recipient lines, and memo lines, can describe the same money.

all distinct SUB_ID lines.

| Employer | Committee kind | Lines | Dollars |
|---|---|---|---|
| anthropic | PAC | 590 | $6,455,325.02 |
| anthropic | candidate not mapped to a sitting member | 419 | $1,158,775.64 |
| anthropic | conduit | 1181 | $5,578,732.56 |
| anthropic | joint: no saved statement | 177 | $1,860,712.00 |
| anthropic | joint: no sitting member among its participants | 31 | $302,650.00 |
| anthropic | joint: not attributed: 10 sitting members share it | 1 | $13,000.00 |
| anthropic | joint: not attributed: 23 sitting members share it | 5 | $50,330.00 |
| anthropic | joint: not attributed: 24 sitting members share it | 2 | $22,000.00 |
| anthropic | joint: not attributed: a participant could not be settled | 6 | $69,000.00 |
| anthropic | joint: tied to the one sitting member among its participants | 97 | $977,553.00 |
| anthropic | leadership PAC: other or unresolved sponsor | 172 | $797,050.00 |
| anthropic | leadership PAC: sitting sponsor | 58 | $266,830.58 |
| anthropic | party committee | 172 | $1,938,883.77 |
| anthropic | sitting member campaign | 606 | $1,857,363.66 |
| nvidia | PAC | 381 | $371,813.75 |
| nvidia | candidate not mapped to a sitting member | 439 | $298,303.99 |
| nvidia | conduit | 6260 | $748,264.72 |
| nvidia | joint: no saved statement | 5 | $9,750.00 |
| nvidia | joint: no sitting member among its participants | 91 | $141,108.00 |
| nvidia | joint: not attributed: 2 sitting members share it | 2 | $1,500.00 |
| nvidia | joint: not attributed: 4 sitting members share it | 15 | $18,200.00 |
| nvidia | joint: tied to the one sitting member among its participants | 22 | $16,531.00 |
| nvidia | leadership PAC: other or unresolved sponsor | 11 | $2,001.67 |
| nvidia | leadership PAC: sitting sponsor | 1 | $270.00 |
| nvidia | party committee | 289 | $1,081,364.00 |
| nvidia | sitting member campaign | 541 | $166,976.50 |

latest positive non-memo individual lines since Jan 2025.

| Employer | Committee kind | Lines | Dollars |
|---|---|---|---|
| anthropic | PAC | 569 | $6,378,991.68 |
| anthropic | candidate not mapped to a sitting member | 406 | $1,137,175.64 |
| anthropic | conduit | 1181 | $5,578,732.56 |
| anthropic | joint: no saved statement | 177 | $1,860,712.00 |
| anthropic | joint: no sitting member among its participants | 31 | $302,650.00 |
| anthropic | joint: not attributed: 10 sitting members share it | 1 | $13,000.00 |
| anthropic | joint: not attributed: 23 sitting members share it | 5 | $50,330.00 |
| anthropic | joint: not attributed: 24 sitting members share it | 2 | $22,000.00 |
| anthropic | joint: not attributed: a participant could not be settled | 6 | $69,000.00 |
| anthropic | joint: tied to the one sitting member among its participants | 97 | $977,553.00 |
| anthropic | leadership PAC: other or unresolved sponsor | 99 | $491,000.00 |
| anthropic | leadership PAC: sitting sponsor | 24 | $120,000.00 |
| anthropic | party committee | 66 | $872,406.00 |
| anthropic | sitting member campaign | 398 | $1,391,284.00 |
| nvidia | PAC | 379 | $370,063.75 |
| nvidia | candidate not mapped to a sitting member | 395 | $278,094.00 |
| nvidia | conduit | 6243 | $747,652.72 |
| nvidia | joint: no saved statement | 5 | $9,750.00 |
| nvidia | joint: no sitting member among its participants | 91 | $141,108.00 |
| nvidia | joint: not attributed: 2 sitting members share it | 2 | $1,500.00 |
| nvidia | joint: not attributed: 4 sitting members share it | 15 | $18,200.00 |
| nvidia | joint: tied to the one sitting member among its participants | 22 | $16,531.00 |
| nvidia | leadership PAC: other or unresolved sponsor | 1 | $1,000.00 |
| nvidia | leadership PAC: sitting sponsor | 1 | $270.00 |
| nvidia | party committee | 209 | $951,723.87 |
| nvidia | sitting member campaign | 505 | $148,789.00 |

The `candidate not mapped` and unresolved-sponsor classes include unresolved identity/ownership cases, not proven non-members. The figure counts committees attributed to one sitting-cohort member: authorized/principal campaigns, sponsored leadership PACs and single-member JFCs. It excludes the conduit side, party committees, ordinary PACs, non-member candidates, shared JFCs and unresolved new JFCs. The footnote states the recipient-committee rule and conduit/shared-JFC exclusions. Some old keys are accepted from reviewed pack rows or candidate links without the full statement check now described as the rule; this is the ownership-verification gap above. The two API employer search hits outside the prefix rule are separately listed below.

**3. Employee-gift totals and each drawn member.** Latest amendments are selected once per committee and transaction ID; the same SUB_ID from multiple pulls is not counted again. There are 15,335 source copies, 11,576 distinct SUB_IDs and 11,521 latest transaction records; 55 superseded-version pairs were identified across the inventory. The raw recount under the public committee keys, before adding earlier blanked-employer originals, gives 762 Anthropic lines / $4,497,749 and 533 Nvidia lines / $172,590. The nine earlier lines add $31,500, producing the exact printed totals below. They were checked by SUB_ID against the saved original FEC JSON in the congress primary folder, and paired to the amended blank-employer lines by private identity, committee, date and amount. All nine pairs agree. Four other historical Banks receipts are memo X allocations and remain excluded; they were not silently lost.

| Company | Sitting-cohort members with a gift | Lines | Dollars | Normalized donors | Figure/table |
|---|---|---|---|---|---|
| anthropic | 151 | 771 | $4,529,249.00 | 70 | agrees under published ownership keys |
| nvidia | 65 | 533 | $172,590.00 | 83 | agrees under published ownership keys |

The figure also prints 17 of its 24 members with an Anthropic employee gift; that count agrees. All 48 company/member combinations reproduce the public dollars, line counts, normalized donor counts, first date, last date and joint-committee portion under those keys. Zero means a bounded no-match under the stated rule, not proof that no employee gave.

| Member | Employer | Lines | Dollars | People by name rule | First | Last | To JFC |
|---|---|---|---|---|---|---|---|
| warren | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| warren | nvidia | 3 | $12.00 | 1 | 2026-04-27 | 2026-06-27 | $0.00 |
| coons | anthropic | 5 | $33,000.00 | 4 | 2025-11-18 | 2026-06-25 | $15,000.00 |
| coons | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| cramer | anthropic | 7 | $57,000.00 | 6 | 2025-06-27 | 2026-06-07 | $50,000.00 |
| cramer | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| schumer | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| schumer | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| banks | anthropic | 11 | $38,500.00 | 6 | 2025-09-04 | 2026-04-17 | $0.00 |
| banks | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| blumenthal | anthropic | 13 | $88,000.00 | 9 | 2025-10-25 | 2026-09-24 | $59,000.00 |
| blumenthal | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| warner | anthropic | 21 | $107,500.00 | 14 | 2025-10-18 | 2026-06-30 | $50,000.00 |
| warner | nvidia | 5 | $2,250.00 | 1 | 2025-09-19 | 2026-03-17 | $0.00 |
| cornyn | anthropic | 3 | $10,500.00 | 1 | 2026-02-12 | 2026-04-17 | $3,500.00 |
| cornyn | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| kennedy | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| kennedy | nvidia | 2 | $74.00 | 1 | 2025-05-08 | 2025-11-26 | $0.00 |
| thune | anthropic | 4 | $108,000.00 | 3 | 2026-03-01 | 2026-09-18 | $100,000.00 |
| thune | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| wyden | anthropic | 6 | $19,000.00 | 3 | 2026-07-16 | 2026-07-23 | $0.00 |
| wyden | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| mast | anthropic | 6 | $43,000.00 | 5 | 2025-10-06 | 2026-05-04 | $17,000.00 |
| mast | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| crawford | anthropic | 4 | $42,000.00 | 2 | 2025-09-11 | 2026-10-05 | $35,000.00 |
| crawford | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| meeks | anthropic | 8 | $28,000.00 | 4 | 2025-10-10 | 2025-10-28 | $0.00 |
| meeks | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| himes | anthropic | 4 | $22,000.00 | 3 | 2025-08-28 | 2026-07-20 | $0.00 |
| himes | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| huizenga | anthropic | 7 | $30,000.00 | 4 | 2026-05-20 | 2026-06-09 | $9,000.00 |
| huizenga | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| johnson | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| johnson | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| moolenaar | anthropic | 5 | $28,000.00 | 4 | 2025-09-29 | 2026-05-20 | $0.00 |
| moolenaar | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| jeffries | anthropic | 1 | $3,500.00 | 1 | 2025-12-12 | 2025-12-12 | $0.00 |
| jeffries | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| magaziner | anthropic | 2 | $10,000.00 | 2 | 2026-09-02 | 2026-09-05 | $0.00 |
| magaziner | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| subramanyam | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| subramanyam | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| bacon | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| bacon | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| mccaul | anthropic | 0 | $0.00 | 0 | — | — | $0.00 |
| mccaul | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |
| cotton | anthropic | 16 | $99,000.00 | 14 | 2025-10-25 | 2026-09-28 | $67,500.00 |
| cotton | nvidia | 0 | $0.00 | 0 | — | — | $0.00 |

The name rule counts surname plus first given name once per member, even when the same donor has several numbered receipts. I reproduced it independently. It is a matching rule, not identity proof for every spelling; donor_identity_variants.csv records the unresolved variants without names. Both employers use the same anchored whole-word prefix regex, with case and leading whitespace ignored. The exact saved employer strings and raw/eligible counts are in final_employer_strings.csv:

| Matched company or excluded hit | Employer string as filed | Distinct raw lines |
|---|---|---|
| anthropic | ANTHROPIC | 2832 |
| anthropic | ANTHROPIC AI | 2 |
| anthropic | ANTHROPIC FELLOWS PROGRAM | 2 |
| anthropic | ANTHROPIC PBC | 562 |
| anthropic | ANTHROPIC, MACHINE LEARNING | 1 |
| anthropic | ANTHROPIC, PBC | 114 |
| anthropic | ANTHROPIC, PBC. | 2 |
| anthropic | ANTHROPIC,PBC | 1 |
| anthropic | ANTHROPIC/WORKWELL | 1 |
| not matched | ANTHROPICAI | 1 |
| not matched | ODE WITH ANTHROPIC | 1 |
| nvidia | NVIDIA | 6819 |
| nvidia | NVIDIA (CONTRACTOR) | 2 |
| nvidia | NVIDIA CO. | 1 |
| nvidia | NVIDIA COPORATION | 1 |
| nvidia | NVIDIA CORP | 280 |
| nvidia | NVIDIA CORP. | 61 |
| nvidia | NVIDIA CORPORATION | 882 |
| nvidia | NVIDIA, AV | 1 |
| nvidia | NVIDIA, INC | 6 |
| nvidia | NVIDIA, INC. | 4 |

ANTHROPICAI is a plausible concatenated employer spelling excluded by the word boundary (one $3,500 line to C00929968, not a drawn member's campaign in the requested roster). ODE WITH ANTHROPIC is an interior text match (one $50 conduit line); its wording does not establish the same employer. No excluded Nvidia employer string occurs in these saved employer-search lines. That bounded comparison has a control: the scan finds both excluded Anthropic strings and accepted Nvidia misspellings/suffixes. It says nothing about employer spellings the initial search never saved.

Amendments are counted once on the stable committee/transaction key; duplicate and replacement diagnostics are in final_amendment_pairs.csv. Eight counted Anthropic API lines replace older bulk versions. The remaining API additions are 51 Anthropic and 21 Nvidia lines, agreeing with the footnote. The historical nine are counted once instead of their blank-employer successors, not in addition to them. Two of those earlier employer fields are incorrectly shortened from ANTHROPIC PBC to ANTHROPIC in the public table; eligibility is unchanged.

Negatives are excluded on both sides, as are memo X lines. The figure should call the amounts positive receipts before chargebacks/refunds. Cornyn's $10,500 is $7,000 after the saved non-memo -$3,500 CHARGED BACK line. Across tied committees, saved non-memo negative receipts are -$4,287 Anthropic and -$200 Nvidia. Memo negatives are listed separately and must not all be subtracted as refunds. The available receipt inventory is not a complete Schedule B refund census. Bulk whole-dollar priority also loses cents that are present in matching API records: $2.55 across 7 counted Anthropic lines and $13.79 across 22 Nvidia lines. That precision limitation is disclosed in general, but not beside Kennedy's $74 rather than $74.75.

**4. October and the saved calendar.**

| Employer | Latest date read | Latest sitting campaign line | Campaign lines after Sep 30, all memo/sign classes | Conduit lines Oct 1–14 | Conduit dollars |
|---|---|---|---|---|---|
| anthropic | 2026-10-14 | 2026-09-30 | 0 | 26 | $2,740.76 |
| nvidia | 2026-10-14 | 2026-09-30 | 0 | 350 | $14,345.33 |

These agree with employee_gift_rates.csv and the rounded footnote ($2,741 and $14,345). The all-line search, not just the positive-gift selection, finds September 30 campaign controls for both employers and zero later sitting-campaign lines in the saved corpus. The conduit recipient-memo scan finds exactly two drawn-member records, both Nvidia/Warren: SUB_ID 4110920261646713992, Oct 5, $10; SUB_ID 4110920261651312562, Oct 11, $5. They are excluded from the member receipts until the campaign's own record is available, consistently with the stated rule.

The calendar's actual HTML table, not only the text extractor (which omitted the table), was opened and read. It says: Pre-General close Oct 14 / deadline Oct 22; Post-General close Nov 23 / deadline Dec 3; Year-End 2026 close Dec 31 / deadline Jan 31, 2027. Its prose limits which committees must file pre/post-general reports and describes quarterly/monthly options. Dec 3 is the correct post-general deadline, but a blanket next-deadline sentence for every committee needs qualification. Neither an absence in these saved queries nor that calendar proves no gift was made during the fifteen days.

**5. AnthroPAC.** All 117 saved e-filed Schedule B lines were read by the recount script; the file-number/transaction-ID key has no duplicates here. After excluding operating/fee lines, the 102 recipient aggregates match anthropac_by_recipient.csv in amount, line count and date span. A recipient-name join to the independent FEC campaign-owner map gives the following 24 drawn-member results. The same scan detects the 12 positive cells while supporting the other 12 bounded no-match cells.

| Drawn member | AnthroPAC net dollars | Lines | First | Last |
|---|---|---|---|---|
| warren | $0.00 | 0 | — | — |
| coons | $2,500.00 | 1 | 2026-07-07 | 2026-07-07 |
| cramer | $1,000.00 | 1 | 2026-07-07 | 2026-07-07 |
| schumer | $3,500.00 | 1 | 2026-09-25 | 2026-09-25 |
| banks | $2,500.00 | 1 | 2026-08-25 | 2026-08-25 |
| cornyn | $0.00 | 0 | — | — |
| kennedy | $0.00 | 0 | — | — |
| thune | $0.00 | 0 | — | — |
| mast | $2,500.00 | 1 | 2026-07-07 | 2026-07-07 |
| crawford | $1,000.00 | 1 | 2026-07-07 | 2026-07-07 |
| meeks | $2,500.00 | 1 | 2026-06-29 | 2026-06-29 |
| himes | $2,000.00 | 1 | 2026-09-25 | 2026-09-25 |
| huizenga | $3,500.00 | 2 | 2026-06-29 | 2026-09-30 |
| moolenaar | $0.00 | 0 | — | — |
| jeffries | $0.00 | 0 | — | — |
| magaziner | $0.00 | 0 | — | — |
| subramanyam | $0.00 | 0 | — | — |
| bacon | $0.00 | 0 | — | — |
| johnson | $0.00 | 0 | — | — |
| blumenthal | $3,500.00 | 1 | 2026-09-25 | 2026-09-25 |
| wyden | $0.00 | 0 | — | — |
| mccaul | $0.00 | 0 | — | — |
| warner | $2,500.00 | 1 | 2026-07-07 | 2026-07-07 |
| cotton | $2,500.00 | 1 | 2026-09-30 | 2026-09-30 |

The printed 12 of 24 count agrees. **Huizenga's date label does not:** $2,500 was paid Jun 29 and $1,000 Sep 30; the drawn $3,500 Jun 29 label and its panel imply a single date. The underlying recipient table already has the correct span.

**6. What is overstated, understated or asymmetric.** No definite employee-gift dollar/line/people/date discrepancy remains under the published committee assignments and positive whole-dollar rule. That is a conditional arithmetic result; the missing statements/sponsor originals prevent independent certification of every assignment. Cornyn's displayed amount overstates the saved signed non-memo receipt balance by $3,500 unless called gross positive receipts. Kennedy's displayed amount is $0.75 below the saved API precision. Huizenga's company-PAC date compresses two contributions into the first date. The table omits 54 receiving JFCs, including some already counted, so its JFC inventory is incomplete.

The extra historical depth on Anthropic's side is real: nine original-employer lines are restored, whereas no equivalent earlier Nvidia archive is supplied. The footnote explicitly discloses that asymmetry and the broader network-map asymmetry. Both current employer pulls, prefixes, positive/memo filters, source priority and conduit exclusions are otherwise the same in the records checked. I found no newly proven undisclosed Nvidia-only receipt exclusion; missing ownership originals and unsaved employer variants remain gaps, not evidence of equal completeness. The differing cents loss is quantified above.

Every difference is in money_findings.csv. Missing original records are in gaps.csv and are not graded as false ties. No claim here infers influence or motive from a gift.
