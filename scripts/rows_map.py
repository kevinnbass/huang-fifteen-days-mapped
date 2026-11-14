"""Rows for nv8, the fortnight mapped: who acted on which day (ACTS), grouped by the party they belong to (GROUPS,
ACTORS), and the ties drawn that the ties map (rows_people.TIES) does not already hold (TIES_MORE, ARCS).
Each `src`/`q` pair is a saved original and a passage found in it word for word (scripts/check_rows.py).

Which members of Congress get a row: every current member (roster of 540 from the lake's congress_members table,
research/roster_current.tsv) named on three or more of the saved story pages for something said or done about the
matter between Oct 29 and Nov 12. scripts/member_mentions.py counts the pages; the figure build checks every drawn
member against that count. Members named that often for other things (a leadership vote, an election, an older
letter) are listed in the README and not drawn.
An act is placed on the day its source gives; where the source gives none, on the day the source was published."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))   # the checker loads this file by path, in isolated mode
import rows_events, rows_people

FEC = 'table:anthropac_by_recipient.csv#'
LIN = 'pack:lineage/research/'
PK = 'pack:'

GROUPS = [
 # key, title, what no document here shows, the row of rows_context whose `before` text the header carries, words put before it
 ('papers', 'Three newspapers', 'who their confidential intelligence sources are. Singapore\'s ministry denied the Journal\'s Oct 30 account the next day.', 'ST07', ''),
 ('bylines', 'Bylines with a fellowship', 'whether the fellowship shaped either piece. Bylines at outlets not read here (Bloomberg, the Guardian and the Verge among them) were not checked.', '', ''),
 ('analysts', 'Analysts quoted or posting', 'who, if anyone, prompted the posts or quotes. Only analysts found in the funding records are drawn: a selected set, not everyone quoted.', 'ST04', ''),
 ('senate', 'Senate', 'any contact between a senator and the reporters or their sources.', 'ST02', 'Democrats'),
 ('house', 'House', 'whether anyone outside Congress had a hand in the Nov 4 letter.', 'ST01', ''),
 ('admin', 'The administration', 'who gave the intelligence to reporters. The reports cite "people briefed on intelligence surveillance."', 'ST06', ''),
 ('nvidia', 'Nvidia', 'what the board\'s inquiry found; the saved accounts do not give its findings.', 'ST08', ''),
 ('shares', 'Share prices', 'any role for a rival chip maker: no document here connects one to the reports.', 'ST05', ''),
 ('anthropic', 'Anthropic', 'any statement by Anthropic on Huang (its own channels were not searched), or any instruction, payment or message tied to the coverage.', 'ST03', ''),
 ('labs', 'Another AI company', 'any part for OpenAI in the reports.', '', ''),
 ('voices', 'Other public voices', 'any part for them in the reports. Their own business with Nvidia is not mapped here.', '', ''),
 ('abroad', 'China and Singapore', 'whether the intelligence assessment is correct. It has not been tested in public.', 'ST09', ''),
]

ACTORS = [
 # key, group, name (as in the ties), tag, committee name in the FEC table ('' = none on file, None = not a candidate)
 ('nyt', 'papers', 'The New York Times', 'what it reported, from its own pages unless a chip says otherwise', None),
 ('wsj', 'papers', 'The Wall Street Journal', 'what it reported, as others describe it', None),
 ('ft', 'papers', 'Financial Times', 'its reporter\'s post', None),
 ('kubinec', 'bylines', 'Jack Kubinec', 'reporter, The Dispatch', None),
 ('perlo', 'bylines', 'Jared Perlo', 'reporter, NBC News', None),
 ('bresnick', 'analysts', 'Sam Bresnick', 'CSET at Georgetown', None),
 ('fedasiuk', 'analysts', 'Ryan Fedasiuk', 'Foundation for American Innovation', None),
 ('mcguire', 'analysts', 'Chris McGuire', 'Council on Foreign Relations', None),
 ('grunewald', 'analysts', 'Erich Grunewald', 'Institute for AI Policy and Strategy', None),
 ('stapp', 'analysts', 'Alec Stapp', 'Institute for Progress', None),
 ('warren', 'senate', 'Sen. Elizabeth Warren', 'D-Mass.', ''),
 ('coons', 'senate', 'Sen. Chris Coons', 'D-Del.', 'CHRIS COONS FOR DELAWARE'),
 ('cramer', 'senate', 'Sen. Kevin Cramer', 'R-N.D.', 'CRAMER FOR SENATE'),
 ('schumer', 'senate', 'Sen. Chuck Schumer', 'D-N.Y., minority leader', 'FRIENDS OF SCHUMER'),
 ('banks', 'senate', 'Sen. Jim Banks', 'R-Ind.', 'BANKS FOR SENATE'),
 ('blumenthal', 'senate', 'Sen. Richard Blumenthal', 'D-Conn.', 'BLUMENTHAL FOR CONNECTICUT'),
 ('warner', 'senate', 'Sen. Mark Warner', 'D-Va., top Democrat on Intelligence', 'FRIENDS OF MARK WARNER'),
 ('cornyn', 'senate', 'Sen. John Cornyn', 'R-Texas', ''),
 ('kennedy', 'senate', 'Sen. John Kennedy', 'R-La.', ''),
 ('thune', 'senate', 'Sen. John Thune', 'R-S.D., majority leader', ''),
 ('wyden', 'senate', 'Sen. Ron Wyden', 'D-Ore.', ''),
 ('mast', 'house', 'Rep. Brian Mast', 'R-Fla., chairs Foreign Affairs', 'MAST FOR CONGRESS'),
 ('crawford', 'house', 'Rep. Rick Crawford', 'R-Ark., chairs Intelligence', 'CRAWFORD FOR CONGRESS'),
 ('meeks', 'house', 'Rep. Gregory Meeks', 'D-N.Y.', 'FRIENDS FOR GREGORY MEEKS'),
 ('himes', 'house', 'Rep. Jim Himes', 'D-Conn.', 'HIMES FOR CONGRESS'),
 ('huizenga', 'house', 'Rep. Bill Huizenga', 'R-Mich.', 'HUIZENGA FOR CONGRESS'),
 ('johnson', 'house', 'Rep. Mike Johnson', 'R-La., Speaker', ''),
 ('moolenaar', 'house', 'Rep. John Moolenaar', 'R-Mich., chairs the China committee', ''),
 ('jeffries', 'house', 'Rep. Hakeem Jeffries', 'D-N.Y., minority leader', ''),
 ('magaziner', 'house', 'Rep. Seth Magaziner', 'D-R.I.', ''),
 ('subramanyam', 'house', 'Rep. Suhas Subramanyam', 'D-Va.', ''),
 ('bacon', 'house', 'Rep. Don Bacon', 'R-Neb.', ''),
 ('mccaul', 'house', 'Rep. Michael McCaul', 'R-Texas', ''),
 ('trump', 'admin', 'President Trump', '', None),
 ('rubio', 'admin', 'Secretary of State Rubio', '', None),
 ('commerce', 'admin', 'Commerce Secretary Lutnick and his department', '', None),
 ('bessent', 'admin', 'Treasury Secretary Bessent', '', None),
 ('greer', 'admin', 'Trade Representative Greer', '', None),
 ('whitehouse', 'admin', 'White House spokespeople', '', None),
 ('justice', 'admin', 'Justice Department', '', None),
 ('nvidia', 'nvidia', 'Nvidia', 'company statements', None),
 ('huang', 'nvidia', 'Jensen Huang', 'founder and chief executive', None),
 ('board', 'nvidia', 'Nvidia board of directors', '', None),
 ('kress', 'nvidia', 'Colette Kress', 'chief financial officer; interim chief from Nov 12', None),
 ('jones', 'nvidia', 'Harvey Jones', 'director; board chair from Nov 12', None),
 ('suit', 'nvidia', 'Shareholders suing Nvidia', 'a class action', None),
 ('nvda', 'shares', 'Nvidia shares', '', None),
 ('rivals', 'shares', 'AMD and Broadcom', 'shares of two rival chip makers', None),
 ('anthropic', 'anthropic', 'Anthropic', 'the company at far left', None),
 ('openai', 'labs', 'OpenAI', '', None),
 ('musk', 'voices', 'Elon Musk', 'chief executive of Tesla', None),
 ('maguire', 'voices', 'Shaun Maguire', 'partner at Sequoia Capital', None),
 ('ackman', 'voices', 'Bill Ackman', 'founder of Pershing Square Capital Management', None),
 ('sweeney', 'voices', 'Tim Sweeney', 'chief executive of Epic Games', None),
 ('jcramer', 'voices', 'Jim Cramer', 'host of Mad Money on CNBC', None),
 ('kudlow', 'voices', 'Larry Kudlow', 'host of Kudlow on Fox Business', None),
 ('singapore', 'abroad', 'Singapore Ministry of Home Affairs', '', None),
 ('china', 'abroad', 'China\'s Foreign Ministry', '', None),
 ('embassy', 'abroad', 'Chinese Embassy in Washington', '', None),
 ('megaspeed', 'abroad', 'Megaspeed', 'the Singapore firm in the reports', None),
 ('taiwan', 'abroad', 'Taiwan\'s Interior Minister', '', None),
 ('globaltimes', 'abroad', 'Global Times', 'newspaper in China', None),
]

# An act either points at a row of rows_events (its date, source and passage are taken from there) or carries its own.
ACTS = [
 # actor, 'EVnn' or date, what, [src], [q]
 ('nyt', 'EV01', 'U.S. intelligence surveilled Alice Huang'),
 ('nyt', 'EV08', 'A memo says China\'s spy agency recruited her'),
 ('nyt', 'EV12', 'A Chinese firm was cleared to assemble Nvidia chips'),
 ('nyt', 'EV13', 'Rubio oversaw the memo'),
 ('nyt', 'EV27', 'A second relationship, with a subordinate'),
 ('wsj', 'EV03', 'Singapore officials\' concern about Alice Huang (Singapore denied the account the next day)'),
 ('wsj', '2026-11-11', 'The board plans to oust Huang',
  ['sw-dailykoscom-04'], ['The Wall Street Journal reports that Nvidia\'s board of directors plans to oust CEO Jensen Huang']),
 ('ft', 'EV09', 'Sevastopulo posts his report of a romantic relationship. 3.4M views'),
 ('kubinec', '2026-11-10', 'Publishes "Jensen Huang\'s Affair Could Reshape the Chip War"',
  ['sw-thedispatchcom-01'], ['Jensen Huang\'s Affair Could Reshape the Chip War']),
 ('perlo', '2026-11-12', 'Shares the byline on "Jensen Huang agrees to brief Congress"',
  ['sw-nbcnewscom-08', 'sw-nbcnewscom-08'], ['AUTHOR: Jared Perlo', 'Jensen Huang agrees to brief Congress on interactions with alleged spy']),
 ('bresnick', '2026-11-09', 'Tells CNBC what Democrats are likely to probe',
  ['sw-cnbccom-11'], ['said Sam Bresnick, a research fellow at the Center for Security and Emerging Technology']),
 ('fedasiuk', '', 'A podcast summary with no date is titled "Jensen Huang Must Resign"', ['biggo-fedasiuk'], ['Ryan Fedasiuk: Jensen Huang Must Resign']),
 ('fedasiuk', '2026-11-12', 'Tells Scientific American Huang is in "almost every aspect of the company"',
  ['sw-scientificamericancom-01'], ['says Ryan Fedasiuk, senior fellow at the Foundation for American Innovation']),
 ('mcguire', 'EV10', 'Recap post asks why Commerce took no action. 9.4M views'),
 ('mcguire', 'EV17', 'Post: "Jensen\'s behavior is only half the story"'),
 ('mcguire', '2026-11-10', 'Quoted by the FT, as the Bulwark relays it: "mind-boggling" that Commerce "did nothing"; guest on the ChinaTalk podcast',
  ['bulwark-chipghazi', 'bulwark-chipghazi', 'sw-chinatalkmedia-01'],
  ['The FT quotes Chris McGuire, a former senior U.S. government export controls official', 'the Financial Times reported yesterday', 'Emergency pod with Chris McGuire']),
 ('grunewald', '2026-11-10', 'Tells Al Jazeera he thinks recent events likely "add momentum" to chip bills',
  ['sw-aljazeeracom-06'], ['add momentum to bills already being discussed in Congress, like the Chip Security Act']),
 ('stapp', '2026-11-10', '"Expect it to keep getting worse"',
  ['sw-thedailyupsidecom-01', 'sw-thedailyupsidecom-01'], ['said Alec Stapp, the co-CEO of the Institute for Progress', 'Expect it to keep getting worse']),
 ('warren', '2026-11-08', '"Huang and Nvidia\'s board owe Congress answers"',
  ['sw-aljazeeracom-01'], ['NVIDIA\'s Jensen Huang and NVIDIA\'s board owe Congress answers']),
 ('warren', '2026-11-09', 'With Banks: answers, tighter export limits',
  ['sw-fortunecom-08'], ['issued a joint statement calling for answers from Nvidia and tighter restrictions on advanced AI chip exports to China']),
 ('warren', '2026-11-11', 'Letter with Coons: preserve the records',
  ['sw-nbcnewscom-09'], ['announced they had written to Commerce Secretary Howard Lutnick with a request to preserve records on the subject']),
 ('coons', 'EV11', '"Congress will investigate and get answers"'),
 ('coons', '2026-11-11', 'Letter with Warren: preserve the records',
  ['sw-nbcnewscom-09'], ['Sens. Elizabeth Warren, D-Mass., and Chris Coons, D-Del., announced they had written to Commerce Secretary Howard Lutnick']),
 ('cramer', 'EV21', '"I just think he\'s got to go"'),
 ('cramer', 'EV28', '"He should resign"'),
 ('schumer', 'EV22', 'Floor speech: pass three chip-export bills'),
 ('banks', '2026-11-09', 'With Warren: answers, tighter export limits',
  ['sw-fortunecom-08'], ['Sen. Jim Banks (R., Ind.) issued a joint statement']),
 ('blumenthal', '2026-11-09', '"We need a Senate investigation"', ['sw-semaforcom-04'], ['we need a Senate investigation']),
 ('warner', '2026-11-09', '"I want to get more facts before I weigh in"', ['sw-semaforcom-04'], ['I want to get more facts before I weigh in']),
 ('wyden', '2026-11-09', '"We don\'t know where it went"', ['sw-semaforcom-04'], ['We don\'t know where it went']),
 ('wyden', '2026-11-12', 'Letter with Rep. Neal opens a probe of chip-export approvals',
  ['sw-cnbccom-09'], ['Their letter to Commerce Secretary Howard Lutnick announcing the probe was sent by Sen. Ron Wyden']),
 ('cornyn', '2026-11-08', 'Calls a Times report "outrageous"',
  ['cnbc-1108-bipartisan'], ['Cornyn called the report "outrageous" in his post on X']),
 ('cornyn', '2026-11-09', 'Posts: "Congressional oversight investigation needed"',
  ['sw-financeyahoocom-11'], ['John Cornyn posted "Congressional oversight investigation needed."']),
 ('kennedy', '2026-11-10', '"I lost my breath"; wants investigations',
  ['sw-washingtonexaminercom-05'], ['"I lost my breath," Sen. John Kennedy (R-LA) told the Washington Examiner']),
 ('kennedy', '2026-11-11', 'Tells Politico, as the New Republic relays it, the Commerce secretary "needs to answer"',
  ['tnr-lutnick'], ['Secretary Lutnick needs to answer that in front of God and country']),
 ('thune', '2026-11-12', 'Expects "some follow-up" by Congress',
  ['sw-cnbccom-09'], ['I would expect there would be some follow-up, yeah']),
 ('mast', 'EV06', 'Letter dated Nov 4, released Nov 5, asks Huang to brief three committees'),
 ('mast', 'EV29', 'Says "yes," a subpoena is being considered'),
 ('crawford', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5'),
 ('meeks', '2026-11-10', 'Says, as MS NOW reports it, he would subpoena a Commerce appointee',
  ['sw-msnow-01'], ['said he would subpoena Jeff Kessler']),
 ('himes', '2026-11-10', '"We\'ve asked Huang to appear"',
  ['sw-msnow-01'], ['"We\'ve asked Huang to appear," Rep. Jim Himes']),
 ('himes', '2026-11-12', 'Tells NPR, as NBC reports it, Alice Huang\'s role still needs clarifying',
  ['sw-nbcnewscom-09'], ['told NPR that Alice Huang\'s role still needed to be clarified']),
 ('huizenga', '2026-11-12', 'Says the Commerce secretary should testify in public',
  ['sw-cnbccom-09'], ['said it would be "helpful" if Commerce Department Secretary Howard Lutnick testified to Congress in public']),
 ('johnson', '2026-11-09', 'Says "they\'re still gathering information"', ['sw-semaforcom-04'], ['House Speaker Mike Johnson told Semafor']),
 ('johnson', '2026-11-12', 'Calls the resignation a "big and shocking development" and the choice of successor "critically important"',
  ['globe-1112-resigns', 'cnn-1111-live'], ['critically important for right successor to be chosen to replace Huang', 'big and shocking development']),
 ('mccaul', '2026-11-09', 'Post, as quoted in Hot Air: pause advanced AI chip shipments to China',
  ['sw-hotaircom-02'], ['The U.S. should immediately pause the shipment of advanced AI chips to China']),
 ('moolenaar', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5'),
 ('moolenaar', 'EV23', 'Says Congress must "get to the bottom" of it'),
 ('moolenaar', 'EV29', 'Says Huang has not replied'),
 ('jeffries', '2026-11-09', '"We\'re going to need a full briefing"',
  ['cnbc-1110-schumer'], ['we\'re going to need a full briefing specifically as it relates to the Nvidia issue']),
 ('magaziner', '2026-11-08', 'Calls for Huang and the Commerce secretary to testify',
  ['cnbc-1108-bipartisan'], ['called on Commerce Secretary Howard Lutnick to testify before Congress along with Huang']),
 ('subramanyam', 'EV28', '"Jensen Huang should resign"'),
 ('bacon', 'EV28', 'Asked if Huang should resign: "From the little I know, yes"'),
 ('trump', 'EV16', 'Says Huang should remain chief executive: "I think he\'s an honorable guy"; asked if he wished he had acted on the intelligence: "no, I don\'t think so"',
  ['nbc-1108-investigation'], ['Asked by reporters if Trump wished that he had acted on intelligence about Alice Huang']),
 ('trump', 'EV19', 'Says Huang told him he "had absolutely no idea that the person in question was a spy"; says "the FBI is looking into it in terms of something else" and does not say what',
  ['abc-subpoena'], ['He said he had absolutely no idea that the person in question was a spy']),
 ('nvidia', 'EV02', 'Says Huang\'s interactions with Megaspeed\'s officials are not unusual and that the chip-diversion allegations about it were "debunked last year"',
  ['cnbc-1029-nvidia-responds'], ['interactions with its officials are not unusual, because he speaks with thousands of customers every year']),
 ('nvidia', 'EV07', 'Says customer meetings are "part of a CEO\'s job" and that customers get "zero information relevant to national security"',
  ['cnbc-1105-asked-to-brief'], ['zero information relevant to national security']),
 ('huang', 'EV14', 'Memo to staff: "I was unfaithful to my wife"; on the board\'s inquiry: "I support the investigation and will cooperate fully"',
  ['npr-1108-investigation'], ['I support the investigation and will cooperate fully']),
 ('huang', 'EV31', 'Resigns after 33 years as chief executive'),
 ('board', 'EV15', 'Opens an independent investigation; says it has "no reason to believe" secrets were compromised'),
 ('board', 'EV24', 'Hires outside counsel'),
 ('board', 'EV30', 'Meets to discuss removing Huang'),
 ('board', 'EV31', 'Names Kress interim chief, Jones chair; begins a search for a permanent chief',
  ['sw-tomshardwarecom-06'], ['The Board is initiating a search for a permanent Chief Executive Officer and will consider internal and external candidates']),
 ('nvda', 'EV20', 'Falls more than 4%'),
 ('nvda', 'EV25', 'Falls 5.47%'),
 ('nvda', 'EV32', 'Slides about 10% in early trading'),
 ('rivals', 'EV20', 'AMD up 13%, Broadcom up 10%'),
 ('anthropic', 'EV26', 'Sets its IPO price range; seven companies agree to buy $26B of its stock'),
 ('openai', '2026-11-04', 'Quoted by The Information, as the Daily Caller relays it: it "continues to support the strengthening of export controls"',
  ['sw-dailycallercom-07'], ['OpenAI continues to support the strengthening of export controls']),
 ('singapore', 'EV04', 'Denies the Journal\'s account of Alice Huang: "no such investigations"; says its Megaspeed inquiry continues'),
 ('china', 'EV18', 'Calls the spy allegation "unsubstantiated"'),
 # added after audit1b (its finding on the Singapore denial); kept last so earlier row ids do not move
 ('singapore', '2026-11-12', 'As NBC reports its statement: interviewed her and held her passport in 2025; "insufficient evidence" of offences; a "stern warning" for giving police inaccurate information; barred from re-entering; not investigated for espionage',
  ['sw-nbcnewscom-09'] * 5, ['authorities had interviewed Huang and impounded her passport in 2025', 'insufficient evidence to establish that Huang had committed any offences',
                             'issued her with a stern warning after finding that she had knowingly provided police with inaccurate information', 'had been barred from re-entering the country', 'was not investigated for espionage']),
 ('mast', '2026-11-12', 'Says Huang "has agreed to come" and testify; the day is being negotiated. "Jensen and I have been very at odds ... on export controls," but "he has some very serious questions to answer"',
  ['sw-cnbccom-09', 'sw-engadgetcom-0b81faf0', 'sw-engadgetcom-0b81faf0'], ['He has agreed to come', 'Jensen and I have been very at odds as some of you already know on export controls', 'but he has some very serious questions to answer']),
 # ---- S1 of the gaps spec (Nov 14): acts of speakers who had no row; appended so that earlier row ids do not move
 ('rubio', '2026-11-08', 'Says he "can\'t comment on an internal corporate matter that\'s going on with Nvidia"', ['nbc-1108-investigation'], ['comment on an internal corporate matter']),
 ('bessent', '2026-11-05', 'Axios, as the Daily Caller relays it: in a Situation Room meeting he asks Lutnick "How come Megaspeed isn\'t on the entities list?"',
  ['sw-dailycallercom-03', 'sw-dailycallercom-03'], ['pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting', 'on the entities list?']),
 ('commerce', '2026-11-11', 'Axios, as Gizmodo relays it: the president told Lutnick "let\'s get it done"; Lutnick replied "I\'ll develop some options and come back"',
  ['sw-gizmodocom-08', 'sw-gizmodocom-08'], ['develop some options and come back', 'at some point Trump told Lutnick']),
 ('commerce', '2026-11-12', 'A spokeswoman tells CNBC Bessent and Lutnick had "no such conversation"', ['sw-cnbccom-22'], ['Commerce Department spokeswoman Kristen Eichamer told CNBC that Bessent and Lutnick had "no such conversation"']),
 ('greer', '2026-11-12', 'Tells CNBC "Nvidia is a structurally important company"', ['sw-cnbccom-09'], ['Nvidia is a structurally important company']),
 ('whitehouse', '2026-11-09', 'Asked how the administration handled the information: "These sources have no idea what they\'re talking about"', ['msnow-resigns'], ['a White House spokesperson referred MS NOW to Trump']),
 ('whitehouse', '2026-11-12', 'Statement calls Lutnick "a champion of President Trump\'s America First trade and tariff policies"', ['sw-cnbccom-09'], ['Secretary Lutnick is a champion of President Trump']),
 ('justice', '2026-11-09', 'CBS, as Breitbart relays it: its National Security Division is investigating Megaspeed', ['sw-breitbartcom-04'], ['National Security Division is investigating Megaspeed']),
 ('kress', 'EV31', 'Statement: "committed to building on the extraordinary foundation Jensen created"; in an email to staff: "this has been an extraordinarily difficult period"',
  ['fortune-1111-resigns', 'sw-cnbccom-ca82d66d'], ['I am committed to building on the extraordinary foundation Jensen created', 'recognize that this has been an extraordinarily difficult period']),
 ('jones', 'EV31', 'Statement: "Colette has helped lead NVIDIA through a period of extraordinary growth"', ['fortune-1111-resigns'], ['Colette has helped lead NVIDIA through a period of extraordi']),
 ('suit', '2026-11-10', 'Complaint, as Courthouse News reports it: a company statement on Megaspeed "was materially false and misleading"', ['sw-courthousenewscom-02'], ['was materially false and misleading at the time it was made']),
 ('nvidia', '2026-11-10', 'Bloomberg, as TechCrunch relays it: Nvidia\'s head lawyer "intervened in a 2025 U.S. government probe" of Megaspeed', ['sw-techcrunchcom-08'], ['Tim Teter, intervened in a 2025 U.S. government probe']),
 ('anthropic', '2026-11-12', 'A spokesperson "declined to comment" to Quartz for a report on Huang\'s exit and Anthropic\'s share sale', ['sw-qzcom-efc3c07a'], ['An Anthropic spokesperson declined to comment']),
 ('musk', '2026-11-11', 'Posts that hiring Huang "would be an honor"', ['mj-misogyny'], ['Elon Musk wrote on Wednesday']),
 ('maguire', '2026-11-09', 'Posts: "I believe Jensen is irreplaceable for America\'s AI leadership"; Elon Musk replies "I agree"',
  ['sw-calcalistechcom-02', 'sw-calcalistechcom-02'], ['I believe Jensen is irreplaceable for America', 'Tesla CEO Elon Musk responded to Maguire']),
 ('ackman', '2026-11-09', 'Posts: "I am hoping for a simple affair, not a risk to our national security"', ['sw-gulftimescom-01'], ['I am hoping for a simple affair, not a risk to our national security']),
 ('sweeney', '2026-11-12', 'Posts: "A sad day for NVIDIA, developers, America, and all humanity"', ['sw-80lv-02'], ['A sad day for NVIDIA, developers, America, and all humanity']),
 ('jcramer', '2026-11-11', 'On his show: "A Jensen-less Nvidia is an Nvidia many will not want to own"', ['sw-financeyahoocom-b1ac141d'], ['on the November 11 episode of Mad Money']),
 ('embassy', '2026-10-29', 'Its spokesman, in the Times: a campaign of "groundless smears and slanders"', ['man-nyt-1029-01'], ['groundless smears and slanders']),
 ('megaspeed', '2026-11-12', 'Says it takes U.S. export-control compliance "extremely seriously" and has cooperated with inspections', ['huffpost-live'], ['Megaspeed said on Thursday that it takes compliance obligations under U.S. export control laws']),
 ('taiwan', '2026-11-11', 'Says security agencies are "actively investigating" the case', ['sw-taiwannewscomtw-04'], ['said outside the legislature that security agencies were']),
 ('globaltimes', '2026-11-09', 'Writes: "Whenever China-US relations begin to improve, there are often those firing shots from the shadows"', ['sw-inquirercom-01'], ['there are often those firing shots from the shadows']),
 # ---- S2 of the gaps spec (Nov 14): remarks of members already drawn that the saved pages carry and no chip did
 ('moolenaar', '2026-11-12', 'Says talks are under way "on a date to come and meet with us"; the resignation "does change the dynamic"',
  ['sw-cbsnewscom-e684eb4c', 'cnn-1111-live'], ['We are in discussions with him right now on a date to come and meet with us', 'does change the dynamic']),
 ('jeffries', '2026-11-12', 'Calls the resignation the "right thing to do"; "Now we have to get to the bottom of whether America\'s national security has been compromised"',
  ['cnn-1111-live', 'cnn-1111-live'], ['resignation Thursday was the "right thing to do,"', 'Now we have to get to the bottom of whether America']),
 ('schumer', '2026-11-12', 'Statement: "Despite Jensen Huang\'s resignation, Congress must demand answers"', ['sw-cbsnewscom-e684eb4c'], ['resignation, Congress must demand answers from Mr. Huang and others at Nvidia']),
 ('warren', '2026-11-12', 'Statement: Huang, executives and the board "still owe Congress answers"; Lutnick "must explain why they have not closed export control loopholes"',
  ['sw-cbsnewscom-09', 'sw-cnbccom-09'], ['board of directors still owe Congress answers', 'must explain why they have not closed export control loopholes']),
 ('coons', '2026-11-09', 'A post, as Australia\'s ABC reports it: "I\'m pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised"',
  ['sw-abcnetau-03'], ['pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised']),
 # the full reading of the saved pages (2026-11-14): a Times report of Nov 9 and the department's answer; one more public voice
 ('nyt', '2026-11-09', 'As CNBC relays it: Commerce investigated Megaspeed until Aug 2025, when the probe moved to the Justice Department after Nvidia\'s general counsel reached out',
  ['sw-cnbccom-02'], ['the Times reported that the Commerce Department was investigating Megaspeed until August 2025, when the probe was abruptly transferred to the Department of Justice following outreach from Nvidia\'s general counsel about the matter']),
 ('commerce', '2026-11-09', 'A spokesman for its export-control bureau tells CNBC: "BIS conducts all enforcement strictly by the book"',
  ['sw-cnbccom-02'], ['BIS conducts all enforcement strictly by the book']),
 ('kudlow', '2026-11-10', 'On his show: "Step down, Mr. Huang. Right now"', ['sw-mediaitecom-06'], ['Step down, Mr. Huang. Right now']),
 # remarks the full reading found on many pages and no chip carried (2026-11-14)
 ('trump', '2026-11-12', 'Posts: "there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!"',
  ['fox-trump-successor'], ['there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!']),
 ('nvidia', '2026-11-08', 'Tells CNBC: "Today\'s news will not slow NVIDIA. Jensen is committed to continuing to lead NVIDIA as CEO without interruption"',
  ['cnbc-1108-bipartisan'], ['Jensen is committed to continuing to lead NVIDIA as CEO without interruption']),
 ('huang', '2026-10-29', 'Tells Bloomberg: "Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual"',
  ['man-bbg-1029-01', 'sw-taiwannewscomtw-01'], ['Nvidia CEO Says Ties to Company in Spy Probe Were', 'Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual']),
 ('huang', '2026-11-11', 'Reached by phone by the Times and asked about a second relationship: "I don\'t think you should be talking to me directly"',
  ['man-e1161e38dc19'], ["I don't think you should be talking to me directly"]),
 ('commerce', '2026-11-05', 'Axios, as ZeroHedge relays it: asked by Bessent why Megaspeed is not on the entity list, Lutnick answers "I don\'t know. I\'ll look into it"',
  ['sw-zerohedgecom-10', 'sw-dailycallercom-03'], ["I don't know. I'll look into it", 'pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting']),
]

# Acts whose source gives no day for the act itself: they sit on the day the source was published and are drawn with a dashed edge.
REPORT_DAY = {('commerce', '2026-11-09'), ('bresnick', '2026-11-09'), ('fedasiuk', '2026-11-12'), ('mcguire', '2026-11-10'), ('grunewald', '2026-11-10'), ('stapp', '2026-11-10'),
              ('warren', '2026-11-08'), ('blumenthal', '2026-11-09'), ('warner', '2026-11-09'), ('wyden', '2026-11-09'), ('wyden', '2026-11-12'),
              ('cornyn', '2026-11-08'), ('cornyn', '2026-11-09'), ('thune', '2026-11-12'), ('himes', '2026-11-12'), ('johnson', '2026-11-12'),
              ('mccaul', '2026-11-09'), ('magaziner', '2026-11-08'), ('openai', '2026-11-04'),
              ('commerce', '2026-11-11'), ('justice', '2026-11-09'), ('suit', '2026-11-10'), ('nvidia', '2026-11-10'), ('maguire', '2026-11-09'), ('ackman', '2026-11-09'),
              ('taiwan', '2026-11-11'), ('globaltimes', '2026-11-09'), ('anthropic', '2026-11-12'), ('coons', '2026-11-09')}

# Ties into a row that rows_people.TIES does not hold. kind: money | act (an official act) | meet (scheduled for the same session) |
# context (a third party's statement that is worded in the row and drawn as no line: audit1b, on the newsletter about Senate Banking members)
TIES_MORE = [
 # a (a node at left), b (an actor's name), kind, wording for b's name cell, [src], [q]
 ('AnthroPAC', 'Sen. Jim Banks', 'money', '$2,500 · Aug 25', [FEC + 'BANKS FOR SENATE'], ['2500.00']),
 ('AnthroPAC', 'Rep. Gregory Meeks', 'money', '$2,500 · Jun 29', [FEC + 'FRIENDS FOR GREGORY MEEKS'], ['2500.00']),
 ('AnthroPAC', 'Rep. Jim Himes', 'money', '$2,000 · Sep 25', [FEC + 'HIMES FOR CONGRESS'], ['2000.00']),
 ('AnthroPAC', 'Sen. Richard Blumenthal', 'money', '$3,500 · Sep 25', [FEC + 'BLUMENTHAL FOR CONNECTICUT'], ['3500.00']),
 ('AnthroPAC', 'Sen. Mark Warner', 'money', '$2,500 · Jul 7', [FEC + 'FRIENDS OF MARK WARNER'], ['2500.00']),
 ('AnthroPAC', 'Rep. Bill Huizenga', 'money', '$3,500 · Jun 29 and Sep 30', [FEC + 'HUIZENGA FOR CONGRESS'], ['3500.00']),
 # The newsletter does not say Warren was at the meeting; the wording keeps to what it says.
 ('Anthropic', 'Sen. Elizabeth Warren', 'context', 'a newsletter says her Feb 2026 chip-bill announcement "came after" Anthropic\'s chief met Senate Banking Committee members; it does not name them or say she was one',
  ['art-fgs-newsletter', 'art-fgs-newsletter'], ['Warren\'s announcement came after Anthropic CEO Dario Amodei', 'met with members of the Senate Banking Committee']),
]

# Nodes at left that rows_people.TIES does not name.
NODES_MORE = ['Institute for AI Policy and Strategy', 'Institute for Progress', 'Tarbell Center for AI Journalism']
IAPS, IFP, TARBELL, OP = NODES_MORE + ['Open Philanthropy']
# nodes of the third version (the ties that reach them are built from research/member_ties.csv)
ARI = 'Americans for Responsible Innovation'; HORIZON = 'Horizon Institute for Public Service'; EMPLOYEES = 'Anthropic employees'
# Grant totals are sums of the lineage pack's yearly award rows; sums_ok() recomputes each from the pack.
GRANTS = [
 # funder, recipient, wording, yearly rows, total
 (OP, IAPS, '$34.2M in awards, 2024–26', ['FA129', 'FA130', 'FA131'], 34207471),
 (OP, IFP, '$12.0M in awards, 2021–26', ['FA132', 'FA133', 'FA134'], 11956660),
 (OP, 'CNAS', '$14.6M in awards, 2017–25', ['FA045', 'FA046', 'FA047', 'FA048', 'FA049', 'FA050'], 14626356),
 (OP, TARBELL, '$5.3M in awards, 2024–25', ['FA196', 'FA197'], 5291930),
]
TIES_MORE += [(a, b, 'grant', label, [LIN + 'flows_annual.csv#' + i for i in ids], ['Open Philanthropy / Coefficient Giving'] * len(ids)) for a, b, label, ids, _ in GRANTS]
TIES_MORE += [
 (IAPS, 'Erich Grunewald', 'role', 'senior researcher', ['sw-aljazeeracom-06'], ['Erich Grunewald, a senior researcher at the Institute for AI Policy and Strategy']),
 (IFP, 'Alec Stapp', 'role', 'co-chief executive', ['sw-thedailyupsidecom-01'], ['Alec Stapp, the co-CEO of the Institute for Progress']),
 ('CSET at Georgetown', 'Sam Bresnick', 'role', 'research fellow', ['sw-cnbccom-11'], ['Sam Bresnick, a research fellow at the Center for Security and Emerging Technology']),
 (TARBELL, 'Jack Kubinec', 'money', 'his Dispatch bio says he is "currently supported by" it',
  ['sw-thedispatchcom-01'], ['He is currently supported by the Tarbell Center for AI Journalism']),
 (TARBELL, 'Jared Perlo', 'past', 'fellow at NBC News, 2025–26; listed as a past fellow',
  [LIN + 'tenures.csv#T194', LIN + 'tenures.csv#T194'], ['tarbell_fellow', 'NBC News, 2025 – 2026']),
]


# awards the footnote states for two clients of lobbying firms (audit of Nov 14, 2026); bound as notes in rows_context.NOTES
GRANTS_NOTE = [('Open Philanthropy', 'Center for AI Safety', '$12.5M in awards, 2022–23', ['FA033', 'FA034'], 12485288),
               ('Open Philanthropy', 'Future of Life Institute', '$1.9M in awards, 2015–20', ['FA084', 'FA085', 'FA086', 'FA087', 'FA088', 'FA089'], 1912000)]
# ---- added after the audit of Nov 14, 2026 (its findings on ties left out); numbered after TIES_V3 so that earlier row ids do not move.
# Each is worded in the actor's row and drawn as no line. `a` names the other party.
TIES_V4 = [
 ('Open Philanthropy', 'Ryan Fedasiuk', 'context', 'Open Philanthropy made three awards to his institution, the Foundation for American Innovation: $976,000 for AI policy in 2023–24 (the second an exit grant) and $2.7M for energy permitting in 2026. No record here ties an award to him',
  [PK + 'congress/research/grants.csv#GR044', PK + 'congress/research/grants.csv#GR045', PK + 'congress/research/grants.csv#GR046', PK + 'congress/research/grants.csv#GR045', PK + 'congress/research/grants.csv#GR046'],
  ['552500', '423500', '2714000', 'Exit Grant', 'Energy Permitting Reforms']),
 ('Open Philanthropy', 'OpenAI', 'context', 'Open Philanthropy awarded it $30 million in 2017', [LIN + 'flows_annual.csv#FA170', LIN + 'flows_annual.csv#FA170'], ['OpenAI', '30000000']),
 ('Nvidia', 'OpenAI', 'context', 'the Daily Caller calls Nvidia its "key supplier"; CNBC reports a "backstop deal Nvidia offered OpenAI" in August, to rent a planned data center campus',
  ['sw-dailycallercom-07', 'sw-cnbccom-09'], ['stay in the good graces of its key supplier', 'backstop deal Nvidia offered OpenAI to rent SB Energy\'s planned Ohio mega data center campus in August']),
 ('Nvidia', 'President Trump', 'context', 'Al Jazeera: he "reportedly bought as much as $1.6m in Nvidia stock and sold about $1m in August"',
  ['sw-aljazeeracom-01'], ['Trump reportedly bought as much as $1.6m in Nvidia stock and sold about $1m in August']),
 ('Nvidia', 'President Trump', 'context', 'HuffPost: Rahm Emanuel "noted on social media that Trump has personally purchased more than $6 million worth of Nvidia stock this year"',
  ['huffpost-trump-china'], ['noted on social media that Trump has personally purchased more than $6 million worth of Nvidia stock this year']),
 ('CNAS', 'Erich Grunewald', 'context', 'co-author of the 2025 CNAS report on AI chip smuggling', ['art-cnas-smuggling', 'art-cnas-smuggling'], ['By: Erich Grunewald and Tim Fist', 'Countering AI Chip Smuggling Has Become a National Security Priority']),
]


def sums_ok():
    """True when every GRANTS total equals the sum of its yearly award rows (read at check time): the rows of the lineage
    pack where that pack is present, else the copy of the same rows in research/grant_rows.csv."""
    import csv
    p = Path('EVIDENCE_SETS/lineage/research/flows_annual.csv')
    if not p.exists():
        p = Path(__file__).resolve().parents[1] / 'research' / 'grant_rows.csv'
    lines = open(p, newline='', errors='replace').read().splitlines(keepends=True)
    i = 0
    while lines[i].startswith('#'):
        i += 1
    amt = {r['row_id']: float(r['amount_usd']) for r in csv.DictReader(lines[i:])}
    return all(abs(sum(amt[i] for i in ids) - total) < 1 for _, _, _, ids, total in GRANTS + GRANTS_V3 + GRANTS_NOTE)


# Ties between two actors who both have rows, drawn as arcs beside the names. `at` is the row whose name cell words it.
ARCS = [
 # a, b, kind, wording, at, [src], [q]
 ('Anthropic', 'President Trump', 'act', 'ordered agencies to stop using Anthropic, Feb 2026, with a six-month phase-out for agencies using it', 'President Trump',
  ['abc-anthropic-pentagon-0227', 'abc-anthropic-pentagon-0227'], ['President Donald Trump ordered U.S. government agencies to stop using Anthropic\'s products', 'There will be a Six Month phase out period']),
 ('President Trump', 'Jensen Huang', 'act', 'Trump gave him the National Medal of Science, Oct 2026; he flew to China on Air Force One, May 2026', 'Jensen Huang',
  ['nbc-1108-investigation', 'cnbc-1111-congress-resign'], ['In October, Trump awarded Huang the National Medal of Science', 'traveling on Air Force One to China in May']),
 ('Nvidia', 'President Trump', 'money', 'Nvidia gave $25M to his ballroom project, HuffPost reports; CNBC adds "$1 million to his 2025 inaugural fund"', 'President Trump',
  ['huffpost-trump-china', 'sw-cnbccom-02'], ['whose company donated $25 million to Trump\'s ballroom project', 'including $25 million toward his White House ballroom and $1 million to his 2025 inaugural fund']),
 ('Anthropic', 'Nvidia', 'money', 'CNBC, Nov 9: Nvidia is "an investor in the Claude creator and counts the AI lab as a significant customer"; one of seven companies that agreed to buy $26B of Anthropic stock, Nov 10', 'Nvidia',
  ['cnbc-1110-anthropic-ipo', 'sw-cnbccom-11'], ['Nvidia and Taiwan Semiconductor Manufacturing Co. to purchase $26 billion', 'an investor in the Claude creator and counts the AI lab as a significant customer']),
 ('Nvidia', 'Rep. Michael McCaul', 'past', 'Nvidia\'s in-house lobbyists include alumni of his office, CNBC reports', 'Rep. Michael McCaul',
  ['sw-cnbccom-02'], ['in-house lobbyists include alumni of congressional offices from key Republicans and Democrats, including Rep. Michael McCaul']),
 ('Anthropic', 'AMD and Broadcom', 'money', 'both among the seven that agreed to buy Anthropic stock, Nov 10', 'AMD and Broadcom',
  ['cnbc-1110-anthropic-ipo', 'cnbc-1110-anthropic-ipo'], ['Advanced Micro Devices', 'Broadcom']),
]


# ---- third version (Nov 13): nodes and node-to-node ties, numbered after the arcs so that earlier row ids do not move.
# The ties from these nodes to members are built from research/member_ties.csv (rows_ties.py).
NODES_V3 = [EMPLOYEES, ARI, HORIZON]
GRANTS_V3 = [(OP, ARI, '$3.4M in awards, 2024–25', ['FA014', 'FA015'], 3446500)]
TIES_V3 = [(a, b, 'grant', label, [LIN + 'flows_annual.csv#' + i for i in ids], ['Open Philanthropy / Coefficient Giving'] * len(ids)) for a, b, label, ids, _ in GRANTS_V3] + [
 ('Anthropic', EMPLOYEES, 'role', 'people who gave the company as their employer on an FEC line', ['table:employee_gift_rates.csv#anthropic'], ['anthropic']),
 ('Public First Action', ARI, 'role', 'ARI\'s president co-founded Public First Action',
  [PK + 'congress/research/entities.csv#EN2202', 'art-pfa-conservative'], ['Co-Founder & President, Americans for Responsible Innovation', 'Brad Carson, co-founder of Public First Action']),
 (OP, HORIZON, 'money', 'its action fund paid Horizon $100,000 in 2022',
  [PK + 'congress/research/grants.csv#GR194', PK + 'congress/research/grants.csv#GR194'], ['OPEN PHILANTHROPY ACTION FUND', '100000']),
]


def acts():
    """ACTS with date, src and q filled in from rows_events where an act points at one of its rows."""
    ev = {r['row_id']: r for r in rows_events.rows()}
    keys = {a[0] for a in ACTORS}
    out = []
    for a in ACTS:
        assert a[0] in keys, a[0]
        if a[1].startswith('EV'):
            e = ev[a[1]]
            src, q = (e['src'], e['q']) if isinstance(e['src'], list) else ([e['src']], [e['q']])
            more = (a[3], a[4]) if len(a) == 5 else ([], [])          # sources the act adds to its event row's (audit of Nov 14)
            assert len(more[0]) == len(more[1])
            out.append({'actor': a[0], 'date': e['date'], 'what': a[2], 'src': list(src) + more[0], 'q': list(q) + more[1], 'from': a[1], 'reported': (a[0], e['date']) in REPORT_DAY})
        else:
            assert len(a[3]) == len(a[4])
            out.append({'actor': a[0], 'date': a[1], 'what': a[2], 'src': a[3], 'q': a[4], 'from': '', 'reported': (a[0], a[1]) in REPORT_DAY})
    return out


def rows():
    out = []
    for i, a in enumerate(acts(), 1):
        out.append({'row_id': f'MA{i:02d}', **a})
    names = {a[2] for a in ACTORS}
    left = {t[0] for t in rows_people.TIES} | {t[1] for t in rows_people.TIES} | set(NODES_MORE)
    assert sums_ok(), 'a grant total no longer matches the lineage pack'
    for i, (a, b, kind, label, src, q) in enumerate(TIES_MORE, 1):
        assert (b in names or b in left) and a in left and kind in ('money', 'act', 'meet', 'grant', 'role', 'past', 'context') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    for i, (a, b, kind, label, at, src, q) in enumerate(ARCS, len(TIES_MORE) + 1):
        assert a in names and b in names and at in (a, b) and kind in ('money', 'act', 'meet', 'past') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'at': at, 'arc': True, 'src': src, 'q': q})
    left |= set(NODES_V3)
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V3, len(TIES_MORE) + len(ARCS) + 1):
        assert b in left and a in left and kind in ('money', 'grant', 'role') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V4, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + 1):
        assert b in names and kind == 'context' and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    return out
