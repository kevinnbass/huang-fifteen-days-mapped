"""Rows for two figures: the run-up from January 2025 (RUNUP) and who had what at stake (STAKES).
Each `src`/`q` pair is a saved original and a passage found in it word for word (scripts/check_rows.py)."""

FEC = 'table:anthropac_by_recipient.csv#'
PK = 'pack:'

# lane: A = Anthropic's people, money and governance; B = the chip-export fight, Nvidia and Washington
RUNUP = [
 # date (YYYY-MM or YYYY-MM-DD), lane, text, src, q
 ('2025-01', 'A', 'Open Philanthropy co-founder Holden Karnofsky joins Anthropic\'s staff.',
  [PK + 'lineage/research/tenures.csv#T142'], ['joined Anthropic last month']),
 ('2025-05-28', 'A', 'Co-founder Jack Clark addresses a conference for Congress in Spain; 22 members attend.',
  ['art-aspen-report'], ['Jack Clark, Co-Founder of Anthropic, will deliver thought-provoking pre-dinner']),
 ('2025-05-30', 'A', 'Semafor: White House officials "called out" Anthropic\'s hiring of former Biden staff, naming Elizabeth Kelly and Tarun Chhabra.',
  ['semafor-0530-buchanan'], ['called out the company’s hiring of several former Biden Administration staffers, including Elizabeth Kelly and Tarun Chhabra']),
 ('2025-06-07', 'A', 'Richard Fontaine, chief executive of the think tank CNAS, is named to the trust that will elect most of Anthropic\'s board.',
  ['art-anthropic-fontaine', 'anthropic-ltbt'], ['today announced the appointment of Richard Fontaine', 'the Trust will elect a majority of the board within 4 years']),
 ('2025-06-11', 'B', 'CNAS publishes "Countering AI Chip Smuggling Has Become a National Security Priority."',
  ['art-cnas-smuggling'], ['Countering AI Chip Smuggling Has Become a National Security Priority']),
 ('2025-08-27', 'A', 'Anthropic forms a National Security and Public Sector Advisory Council.',
  ['toms-anthropic-nsc'], ['National Security and Public Sector Advisory Council']),
 ('2025-09-04', 'B', 'Bloomberg Law, citing the Financial Times: Anthropic will stop selling to groups majority-owned by Chinese entities.',
  ['bloomberglaw-ft-china'], ['Anthropic will stop selling AI services to groups majority owned by Chinese entities']),
 ('2025-11-06', 'B', 'GAIN AI Act (S. 3150) on chip exports is before the Senate; Sen. Schumer is an original cosponsor.',
  [PK + 'congress/research/timeline.csv#TL646'], ['S. 3150 GAIN AI Act of 2025 original cosponsor Charles E. Schumer']),
 ('2025-11-25', 'A', 'Two former congressmen announce plans to form Public First Action and two super PACs.',
  ['pfa-founding-release'], ['today announced plans to form a new nonpartisan 501(c)4 organization']),
 ('2026-01', 'B', 'House Foreign Affairs passes Rep. Mast\'s AI OVERWATCH Act, which would let Congress block advanced chip exports to adversaries.',
  ['art-fgs-newsletter'], ['passed through the House Foreign Affairs Committee in January']),
 ('2026-02-10', 'B', 'Sens. Warren and Banks announce plans for a Senate version; a newsletter says this came after Dario Amodei met Senate Banking members.',
  ['art-fgs-newsletter'], ['met with members of the Senate Banking Committee']),
 ('2026-02-12', 'A', 'Anthropic gives $20 million to Public First Action, citing "smart export controls on AI chips."',
  ['anthropic-pfa-1'], ['Supporting smart export controls on AI chips']),
 ('2026-02-13', 'A', 'Chris Liddell, a deputy chief of staff in Trump\'s first White House, joins Anthropic\'s board.',
  [PK + 'lineage/research/tenures.csv#T138', 'examiner-liddell'], ['Chris Liddell has been appointed to Anthropic’s Board of Directors', 'former Trump deputy chief of staff']),
 ('2026-02-27', 'B', 'Trump orders agencies to stop using Anthropic; the Pentagon designates it a supply-chain risk.',
  ['abc-anthropic-pentagon-0227'], ['President Donald Trump ordered U.S. government agencies to stop using Anthropic\'s products']),
 ('2026-04-03', 'A', 'Anthropic registers its PAC, AnthroPAC, with the FEC.',
  [PK + 'congress/research/timeline.csv#TL111'], ['files FEC Form 1 Statement of Organization']),
 ('2026-05', 'B', 'A classified U.S. intelligence memo concludes Alice Huang is a Chinese intelligence asset, per CNN.',
  ['cnn-1112-who-lied'], ['US intelligence concluded in a classified memo issued in May that Alice Huang']),
 ('2026-05', 'B', 'Huang travels to China on Air Force One with Trump.',
  ['cnbc-1111-congress-resign'], ['traveling on Air Force One to China in May']),
 ('2026-06-06', 'A', 'A forum programme lists Anthropic\'s Tarun Chhabra and Chris McGuire, both formerly of the NSC, as speakers in one session in Taipei.',
  ['art-dset-forum'], ['Chris McGuire｜Senior Fellow for China and Emerging Technologies']),
 ('2026-07-07', 'A', 'AnthroPAC gives to Coons, Cramer, Mast and Crawford, eight days after the earliest contribution in its filings.',
  [FEC + 'CHRIS COONS FOR DELAWARE', FEC + 'CRAMER FOR SENATE', FEC + 'MAST FOR CONGRESS', FEC + 'CRAWFORD FOR CONGRESS', FEC + 'FRIENDS FOR GREGORY MEEKS'],
  ['2026-07-07', '2026-07-07', '2026-07-07', '2026-07-07', '2026-06-29']),
 ('2026-07-17', 'A', 'Public First Action launches a $15 million conservative ad project; Mast and Moolenaar are among the Republicans it names.',
  ['art-pfa-conservative'], ['Public First Action today announced the Conservative Consensus Project, a $15 million effort']),
 ('2026-07-21', 'A', 'Anthropic gives Public First Action a second $20 million; it says the money is for policy and education work, not candidate elections.',
  ['anthropic-pfa-2', 'anthropic-pfa-2'], ['additional $20 million to Public First Action', 'cannot be used to influence the election of any candidate']),
 ('2026-09', 'A', 'Sihao Huang, until then a White House adviser on AI policy, joins Anthropic as head of frontier compute strategy.',
  ['cnbc-1009-poach'], ['AI lab in September as head of frontier compute strategy']),
 ('2026-10', 'B', 'Trump awards Jensen Huang the National Medal of Science.',
  ['nbc-1108-investigation'], ['In October, Trump awarded Huang the National Medal of Science']),
 ('2026-10-29', 'B', 'The New York Times reports the intelligence concerns about Alice Huang, as CNBC describes its report.',
  ['cnbc-1029-nvidia-responds'], ['a New York Times report that detailed American intelligence agencies surveilling a person close to Nvidia CEO Jensen Huang']),
 ('2026-11-10', 'A', 'Anthropic sets its IPO price range; Nvidia is one of seven companies that agree to buy $26 billion of its stock alongside.',
  ['cnbc-1110-anthropic-ipo'], ['to purchase $26 billion of the company\'s Class N common stock']),
 ('2026-11-12', 'B', 'Huang resigns as Nvidia\'s chief executive.',
  ['fortune-1111-resigns'], ['Nvidia Chief Executive Jensen Huang has resigned']),
]

# One row per group with something at stake. `before` and `during` are documented; `gap` says what is not.
STAKES = [
 # group, before Oct 29 (on the record), in the fortnight (on the record), what no document shows, src, q
 ('House backers of tighter chip-export controls',
  'Rep. Mast\'s AI OVERWATCH Act, which would let Congress block advanced chip exports, passed his committee in January.',
  'The chairs of three committees wrote to Huang on Nov 4, then raised a subpoena. A set of chip-export bills is in play for the annual defense bill.',
  'Whether anyone outside Congress had a hand in the letter. Two of its three signers had received AnthroPAC contributions in July.',
  ['art-fgs-newsletter', 'house-hfac-letter-pr', 'cnbc-1111-congress-resign', FEC + 'MAST FOR CONGRESS', FEC + 'CRAWFORD FOR CONGRESS'],
  ['would allow Congress to block advanced AI chip exports to U.S. foreign adversaries', 'requesting that he appear before their committees for a joint, closed-door briefing', 'a suite of bills in this year\'s National Defense Authorization Act', '2026-07-07', '2026-07-07']),
 ('Democrats in Congress',
  'Sen. Schumer was an original cosponsor of the GAIN AI Act on chip exports.',
  'Won both chambers on Nov 3 and take control in January. Coons, Schumer and others framed the affair as a failure by the Trump administration and promised investigations.',
  'Any contact with the reporters or their sources.',
  ['cnbc-1110-schumer', PK + 'congress/research/timeline.csv#TL646', 'cnbc-1111-congress-resign'],
  ['the party will have the ability to launch investigations into Nvidia and Huang', 'original cosponsor Charles E. Schumer', 'Democrats are widely expected to launch myriad investigations']),
 ('Anthropic',
  'Backs "smart export controls on AI chips"; gave $40 million to Public First Action, for policy and education work, it says, not candidate elections; its PAC gave to candidates of both parties; has hired former administration officials.',
  'Set its IPO price range on Nov 10. Nvidia is one of seven companies that agreed to buy $26 billion of its stock alongside the offering.',
  'Any statement by Anthropic on Huang beyond a spokesperson\'s "declined to comment" to Quartz (none in what could be read on Nov 14: its newsroom and share-sale site; its share-sale filing and three more SEC documents could not be saved). Any instruction, payment or message tied to the coverage.',
  ['anthropic-pfa-1', 'anthropic-pfa-2', 'cnbc-1110-anthropic-ipo', 'anthropic-pfa-2', 'cnbc-1009-poach', FEC + 'FRIENDS OF SCHUMER', FEC + 'MAST FOR CONGRESS'],
  ['Supporting smart export controls on AI chips', 'bringing our total support to $40 million', 'Nvidia and Taiwan Semiconductor Manufacturing Co. to purchase $26 billion',
   'cannot be used to influence the election of any candidate', 'AI lab in September as head of frontier compute strategy', '3500.00', '2500.00']),
 ('Export-control analysts outside government',
  'Chris McGuire, now at the Council on Foreign Relations, "crafted and implemented" the Biden administration\'s chip export controls at the NSC, his biography says. CNAS published on chip smuggling in 2025.',
  'McGuire\'s Nov 6 recap reached 9.4 million views. A saved summary of a podcast has Ryan Fedasiuk arguing that Huang "must resign."',
  'Who, if anyone, prompted the posts.',
  ['cfr-mcguire', 'art-cnas-smuggling', 'x-mcguire-nov6', 'biggo-fedasiuk'],
  ['including all semiconductor and dual-use technology export controls', 'Countering AI Chip Smuggling Has Become a National Security Priority', 'The story keeps getting crazier', 'Jensen Huang Must Resign']),
 ('Rival chip makers',
  'AMD and Broadcom compete with Nvidia for AI chip sales.',
  'On Nov 9, AMD rose 13% and Broadcom just over 10% as Nvidia fell. A consultant told Fortune the exit "could turn what has effectively been a monopoly into a horse race again."',
  'Any role at all: no document here connects a rival to the reports.',
  ['cnbc-1110-selloff', 'fortune-1111-resigns'],
  ['AMD gained 13% on Monday, while Broadcom added just over 10%', 'This could turn what has effectively been a monopoly into a horse race again']),
 ('Inside the administration',
  'The government cleared Nvidia\'s H200 chip for sale to China this year. As CNBC relays the Times\'s reporting, policymakers received the intelligence memo last spring and Trump, once briefed, "chose not to do anything."',
  'The Times reported, as CNBC relays it, that Secretary of State Rubio oversaw the memo. Trump defended Huang and said the FBI was looking into it.',
  'Who gave the intelligence to reporters. The reports cite "people briefed on intelligence surveillance."',
  ['cnbc-1029-nvidia-responds', 'cnbc-1105-asked-to-brief', 'cnbc-1108-bipartisan', 'cnbc-1029-nvidia-responds'],
  ['Earlier this year the U.S. government cleared Nvidia\'s H200 chip to be shipped to China', 'chose not to do anything with the information', "Secretary of State Marco Rubio oversaw the memo's creation", 'which cited people briefed on intelligence surveillance']),
 ('Three newspapers',
  'The New York Times, the Wall Street Journal and the Financial Times cover chips and China.',
  'Other outlets\' saved accounts credit each new element to one of them: surveillance (Oct 29), Singapore (Oct 30), the memo and the relationship (Nov 6), Rubio (Nov 8), a second relationship (Nov 11).',
  'Who their confidential intelligence sources are. Singapore\'s ministry denied the Journal\'s account of it in a statement timed the same day.',
  ['cnbc-1029-nvidia-responds', 'mha-clarification-a', 'cnbc-1108-bipartisan', 'aljazeera-1112-resigns'],
  ['pushed back on a New York Times report', 'neither the Singapore Government nor its officials said this', 'the Times first reported on Friday', 'The New York Times reported that Huang also had an extramarital relationship']),
 ('Nvidia\'s board and shareholders',
  'The board had no chair, and the company had "not set out a clear succession plan," Fortune reported; Huang held about 3.6% of the stock.',
  'The board opened an inquiry on Nov 8, saying it had "no reason to believe" national security or company secrets were compromised; it hired outside counsel on Nov 10 and met on Nov 11. A shareholder class action was filed.',
  'What the inquiry found: no saved account gives its findings.',
  ['fortune-1111-resigns', 'aljazeera-1112-resigns', 'cnbc-1110-selloff', 'cnbc-1108-bipartisan', 'art-roic-cramer'],
  ['the company has not set out a clear succession plan', 'Nvidia’s board met on Wednesday night to discuss ousting Huang', 'a class-action shareholder lawsuit filed against Nvidia and Huang',
   'While the Board has no reason to believe that either national security or NVIDIA secrets were compromised', 'On November 10, independent directors retained former acting U.S. Attorney Joon H. Kim']),
 ('China and Singapore',
  'Megaspeed, the Singapore firm Alice Huang is linked to, bought Nvidia chips and was under investigation there.',
  'China\'s foreign ministry called the spy allegation unsubstantiated. Singapore\'s ministry, in a statement timed Oct 30 (its newsroom page is dated Oct 31), said of the Journal\'s account that there were "no such investigations" of Alice Huang; on Nov 12 NBC reported its statement that police interviewed her and held her passport in 2025, found in Feb 2026 "insufficient evidence" of offences relating to the declarations under investigation, gave her a "stern warning" for inaccurate information and barred her from re-entering; the statement adds that repeated requests to U.S. authorities brought "limited information or assistance".',
  'Whether the intelligence assessment is correct. It has not been tested in public, and NBC reported on Nov 12 that her "precise role and relationship with China\'s spy service remain unclear."',
  ['mha-clarification-a', 'nbc-1108-investigation', 'mha-clarification-a', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'art-own-mha-1112', 'art-own-mha-1112', 'sw-nbcnewscom-09'],
  ['Investigations into Megaspeed are ongoing', 'the so-called Chinese spy allegation is unsubstantiated', 'there were no such investigations conducted in respect of Alice Huang',
   'authorities had interviewed Huang and impounded her passport in 2025', 'insufficient evidence to establish that Huang had committed any offences', 'precise role and relationship with China\'s spy service remain unclear',
   'issued her with a stern warning after finding that she had knowingly provided police with inaccurate information', 'had been barred from re-entering the country',
   'offences relating to the possible inaccurate declarations for which Megaspeed was being investigated', 'In February 2026', 'Singapore has to date received limited information or assistance in respect of the company']),
]


# Limits and context that a figure's footnote states; each is bound to a saved passage like any drawn row.
NOTES = [
 ('openai_hires', 'cnbc-1009-poach', 'OpenAI has hired at least three from the president\'s administrations'),
 ('board_statement', 'cnbc-1108-bipartisan', 'While the Board has no reason to believe that either national security or NVIDIA secrets were compromised'),
 ('role_unclear', 'sw-nbcnewscom-09', 'precise role and relationship with China\'s spy service remain unclear'),
 ('pac_next_report', 'sw-cnbccom-02', 'Its next disclosure is due Dec. 3'),
 # limits the saved reports themselves state, added to the footnote after the audit of Nov 14
 ('no_briefing', 'man-nyt-1029-01', 'Mr. Huang has not received a defensive briefing'),
 ('did_not_know', 'man-nyt-1029-01', 'U.S. officials did not believe the Nvidia executive knew that Ms. Huang was gathering information for the Chinese'),
 ('nvidia_denial', 'cnbc-1105-asked-to-brief', 'zero information relevant to national security'),
 ('no_press', 'man-nyt-1106-01', 'customers do not ask Nvidia to press the U.S. government to change its policies on chip sales to China'),
 ('cais_2022', 'pack:lineage/research/flows_annual.csv#FA033', '5160000'), ('cais_2023', 'pack:lineage/research/flows_annual.csv#FA034', '7325288'),
 ('fli_2015', 'pack:lineage/research/flows_annual.csv#FA084', '1186000'), ('fli_2016', 'pack:lineage/research/flows_annual.csv#FA085', '100000'),
 ('fli_2017', 'pack:lineage/research/flows_annual.csv#FA086', '100000'), ('fli_2018', 'pack:lineage/research/flows_annual.csv#FA087', '250000'),
 ('fli_2019', 'pack:lineage/research/flows_annual.csv#FA088', '100000'), ('fli_2020', 'pack:lineage/research/flows_annual.csv#FA089', '176000'),
 # the FEC's own calendar: the post-general report closes its books on Nov 23 and is due Dec 3, 2026 (bound for the footnote's sentence on gifts after Oct 14)
 ('fec_post_general_due', 'fec-reporting-dates-2026-20261114', '12/03/2026'),
 # limits the saved reports state that the footnote still lacked (second audit, Nov 15, 2026)
 ('agencies_unknown', 'man-nyt-1029-01', 'It could not be determined which intelligence agency or agencies have been involved in monitoring Ms. Huang'),
 ('information_unknown', 'man-nyt-1029-01', 'what information she passed along or its value to China'),
 ('trump_when_told', 'nbc-exprosecutor', 'They could have been mentioned'),
 ('trump_not_then', 'nbc-exprosecutor', 'hear about it then'),
 ('nvpac_registered', 'fec-committee-c00960070-20261114', '2026-08-27'),
 ('nvpac_one_report', 'fec-filings-c00960070-20261114', 'OCTOBER QUARTERLY'),
 # why each lobbying client is on the map: the grant rows behind the footnote's sentence (second audit: the chain was left to the reader)
 ('ifp_action_2022', 'pack:congress/research/grants.csv#GR195', '500000'), ('ifp_action_2023', 'pack:congress/research/grants.csv#GR155', '1200000'),
 ('ifp_action_2023_ai', 'pack:congress/research/grants.csv#GR156', '341660'), ('encode_no_op_award', 'pack:congress/research/grants.csv#GR071', 'exact_n=0'),
 ('encode_fli_2024', 'pack:congress/research/grants.csv#GR250', '250000'), ('encode_tallinn_2025', 'pack:congress/research/grants.csv#GR207', 'Jaan Tallinn'),
 ('cais_af_tallinn', 'pack:congress/research/grants.csv#GR206', 'Jaan Tallinn'),
 ('nvpac_disbursements', 'fec-schedule_b-c00960070-20261114', 'CREDIT CARD PROCESSING'),
 # second audit, lane c (Nov 15, 2026): the records behind the footnote's sentences on banks, on the donor lists read for Nvidia, and on the own-channel recount
 ('banks_lenders', 'pack:evaluators-deep/research/equity_edges.csv#WEQ733', '17 named banks'), ('banks_lead_sale', 'pack:evaluators-deep/research/equity_edges.csv#WEQ733', 'the four also lead the IPO'),
 ('brookings_list_period', 'art-f1-brookings-honor-roll-2026', 'July 1, 2025 – June 30, 2026'), ('brookings_list_control', 'art-f1-brookings-honor-roll-2026', 'Microsoft Corporation'),
 ('eighty_k_largest_donor', 'art-f1-80k-donors', 'Our largest donor is Coefficient Giving'),
 # reading of the corrections (Nov 15, 2026): the report of the banks' facility is provisional, and the FBI's reported inquiry
 ('banks_facility_nearing', 'pack:evaluators-deep/research/equity_edges.csv#WEQ733', 'is nearing a $15 billion revolving credit facility'),
 ('banks_details_could_change', 'pack:evaluators-deep/research/equity_edges.csv#WEQ733', 'Details of the loan could still change'),
]


def rows():
    out = [{'row_id': f'NT{i:02d}', 'note': key, 'src': src, 'q': q} for i, (key, src, q) in enumerate(NOTES, 1)]
    for i, (date, lane, text, src, q) in enumerate(RUNUP, 1):
        assert lane in 'AB' and len(src) == len(q)
        out.append({'row_id': f'RU{i:02d}', 'date': date, 'lane': lane, 'text': text, 'src': src, 'q': q})
    for i, (group, before, during, gap, src, q) in enumerate(STAKES, 1):
        assert len(src) == len(q)
        out.append({'row_id': f'ST{i:02d}', 'group': group, 'before': before, 'during': during, 'gap': gap, 'src': src, 'q': q})
    return out
