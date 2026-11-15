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

# the counts of the look-ups, from the table the gap gauge writes (research/nv8_lookup_counts.tsv: no names)
import csv as _csv
from pathlib import Path as _Path
LOOKUPS = {(r['register'], r['what']): int(r['count']) for r in _csv.DictReader(open(_Path(__file__).resolve().parents[1] / 'research' / 'nv8_lookup_counts.tsv', newline='', encoding='utf-8'), delimiter='\t')}
N_ANALYSTS = LOOKUPS[('analysts', 'quoted on the saved pages (a person or firm written two ways counted once)')]; N_ANALYSTS_DRAWN = LOOKUPS[('analysts', 'drawn')]
N_BYLINE_NAMES = LOOKUPS[('bylines', 'different names')]; N_BYLINES_DRAWN = LOOKUPS.get(('bylines', 'different names drawn'), LOOKUPS[('bylines', 'pairs: drawn')])
NUMBER = {3: 'three', 4: 'four', 5: 'five', 6: 'six'}

GROUPS = [
 # key, title, what no document here shows, the row of rows_context whose `before` text the header carries, words put before it
 ('papers', 'Three newspapers', 'who their confidential intelligence sources are. Singapore\'s ministry denied the Journal\'s Oct 30 account the next day.', 'ST07', ''),
 ('bylines', 'Bylines with a tie on record', f'whether a tie shaped any of the {NUMBER[N_BYLINES_DRAWN]} pieces. All {N_BYLINE_NAMES} names in the bylines of the saved pages were looked up; {NUMBER[N_BYLINES_DRAWN]} have a tie on record (three of them to the Tarbell Center). A reporter or columnist without one is not drawn, however often quoted.', '', ''),
 ('analysts', 'Analysts quoted or posting', f'who, if anyone, prompted the posts or quotes. Drawn: {N_ANALYSTS_DRAWN} of the {N_ANALYSTS} analysts, experts and research groups quoted: those with a tie on record to Anthropic, Open Philanthropy or Nvidia, their own or through the organisation where they hold a post.', 'ST04', ''),
 ('senate', 'Senate', 'any contact between a senator and the reporters or their sources.', 'ST02', 'Democrats'),
 ('house', 'House', 'whether anyone outside Congress had a hand in the Nov 4 letter.', 'ST01', ''),
 ('admin', 'The administration', 'who gave the intelligence to reporters. The reports cite "people briefed on intelligence surveillance."', 'ST06', ''),
 ('nvidia', 'Nvidia', 'what the board\'s inquiry found; the saved accounts do not give its findings.', 'ST08', ''),
 ('shares', 'Share prices', 'any role for a rival chip maker: no document here connects one to the reports.', 'ST05', ''),
 ('anthropic', 'Anthropic', 'any statement by Anthropic on Huang beyond "declined to comment" (its newsroom and share-sale site, searched once on Nov 14, showed none; its share-sale filing and three more SEC documents could not be saved), or any instruction, payment or message tied to the coverage.', 'ST03', ''),
 ('labs', 'Another AI company', 'any part for OpenAI in the reports.', '', ''),
 ('voices', 'Other public voices', 'any part for them in the reports. Drawn: people outside politics and research who are quoted on three or more saved pages. Business with Nvidia is worded where a saved page states it; it was not looked up otherwise.', '', ''),
 ('abroad', 'China and Singapore', 'whether the intelligence assessment is correct. It has not been tested in public.', 'ST09', ''),
]

ACTORS = [
 # key, group, name (as in the ties), tag, committee name in the FEC table ('' = none on file, None = not a candidate)
 ('nyt', 'papers', 'The New York Times', 'what it reported, from its own pages unless a chip says otherwise', None),
 ('wsj', 'papers', 'The Wall Street Journal', 'what it reported, from its own page saved by hand and from copies its licensed partners carry', None),
 ('ft', 'papers', 'Financial Times', 'what it reported, from its own page', None),
 ('kubinec', 'bylines', 'Jack Kubinec', 'reporter, The Dispatch', None),
 ('perlo', 'bylines', 'Jared Perlo', 'reporter, NBC News', None),
 ('hashim', 'bylines', 'Shakeel Hashim', 'editor, Transformer', None),
 # found by the third lane of the second audit (Nov 15, 2026): the earlier look-up had called him "none found", while the evidence sets hold a gift to him by name
 ('mowshowitz', 'bylines', 'Zvi Mowshowitz', 'author of a newsletter on AI', None),
 ('schneider', 'bylines', 'Jordan Schneider', 'founder of ChinaTalk', None),
 ('bresnick', 'analysts', 'Sam Bresnick', 'CSET at Georgetown', None),
 ('fedasiuk', 'analysts', 'Ryan Fedasiuk', 'Foundation for American Innovation', None),
 ('mcguire', 'analysts', 'Chris McGuire', 'Council on Foreign Relations', None),
 ('grunewald', 'analysts', 'Erich Grunewald', 'Institute for AI Policy and Strategy', None),
 ('stapp', 'analysts', 'Alec Stapp', 'Institute for Progress', None),
 ('king', 'analysts', 'Cassia King', 'Institute for AI Policy and Strategy', None),
 ('nie', 'analysts', 'Michelle Nie', 'Center for a New American Security', None),
 ('barez', 'analysts', 'Fazl Barez', 'University of Oxford', None),
 # added after the third lane of the second audit (Nov 15, 2026): one rule for both sides. A quoted analyst is drawn when a record ties the person,
 # or the organisation where they hold a post, to Anthropic, Open Philanthropy or Nvidia
 ('chan', 'analysts', 'Kyle Chan', 'Brookings Institution', None),
 ('ohanlon', 'analysts', "Michael O'Hanlon", 'Brookings Institution', None),
 ('wiblin', 'analysts', 'Rob Wiblin', '80,000 Hours', None),
 ('moorhead', 'analysts', 'Patrick Moorhead', 'Moor Insights & Strategy', None),
 ('newman', 'analysts', 'Daniel Newman', 'The Futurum Group', None),
 ('boloor', 'analysts', 'Shay Boloor', 'Futurum Equities', None),
 ('yoo', 'analysts', 'Yoo Eung-joon', 'JOON AI Consulting', None),
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
 ('cotton', 'senate', 'Sen. Tom Cotton', 'R-Ark., chairs Intelligence', 'COTTON FOR SENATE, INC.'),
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
 ('justice', 'admin', 'Justice Department and the FBI', '', None),
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
 # three more voices quoted on three or more saved pages; the reading had split two of them under spellings of their names (second audit, lane c)
 ('delangue', 'voices', 'Clément Delangue', 'chief executive of Hugging Face', None),
 ('zhao', 'voices', 'Changpeng Zhao', 'co-founder of Binance', None),
 ('rao', 'voices', 'Naveen Rao', 'founder of Unconventional AI', None),
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
 ('wsj', 'EV03', 'Reports that officials in the U.S., Singapore and Taiwan "have grown concerned" that an executive close to Huang "is a Chinese intelligence source", citing people familiar with the matter (Singapore denied the account the next day)'),
 ('wsj', '2026-11-11', 'Reports that the board "is preparing to oust" Huang and "to meet as soon as today to determine his future", citing people familiar with the matter',
  ['sw-dailykoscom-04'], ['The Wall Street Journal reports that Nvidia\'s board of directors plans to oust CEO Jensen Huang']),
 ('ft', 'EV09', 'Reports that the U.S. government "believes" Huang "had a romantic relationship with a Chinese woman who was recruited to spy for China\'s main intelligence agency", citing people familiar with the matter. Its reporter\'s post of the report: 3.4M views'),
 ('kubinec', '2026-11-10', 'Publishes "Jensen Huang\'s Affair Could Reshape the Chip War"',
  ['sw-thedispatchcom-01'], ['Jensen Huang\'s Affair Could Reshape the Chip War']),
 ('perlo', '2026-11-12', 'Shares the byline on "Jensen Huang agrees to brief Congress"',
  ['sw-nbcnewscom-08', 'sw-nbcnewscom-08'], ['AUTHOR: Jared Perlo', 'Jensen Huang agrees to brief Congress on interactions with alleged spy']),
 ('bresnick', '2026-11-09', 'Tells CNBC what Democrats are likely to probe',
  ['sw-cnbccom-11'], ['said Sam Bresnick, a research fellow at the Center for Security and Emerging Technology']),
 ('fedasiuk', '', 'A podcast summary with no date is titled "Jensen Huang Must Resign"', ['biggo-fedasiuk'], ['Ryan Fedasiuk: Jensen Huang Must Resign']),
 ('fedasiuk', '2026-11-12', 'Tells Scientific American Huang is in "almost every aspect of the company"; writes at his institute\'s site that it is "a sad day for Nvidia", that "there is reason to be optimistic" about the company and that stepping down "was dignified, and ultimately the right decision"',
  ['sw-scientificamericancom-01', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang'],
  ['says Ryan Fedasiuk, senior fellow at the Foundation for American Innovation', 'decision to step down was dignified, and ultimately the right decision', 'It is a sad day for Nvidia', 'there is reason to be optimistic about the company']),
 ('mcguire', 'EV10', 'Recap post asks why Commerce took no action. 9.4M views'),
 ('mcguire', 'EV17', 'Post: "Jensen\'s behavior is only half the story"'),
 ('mcguire', '2026-11-10', 'Quoted by the FT, as the Bulwark relays it: "mind-boggling" that Commerce "did nothing"; guest on the ChinaTalk podcast',
  ['bulwark-chipghazi', 'bulwark-chipghazi', 'sw-chinatalkmedia-01'],
  ['The FT quotes Chris McGuire, a former senior U.S. government export controls official', 'the Financial Times reported yesterday', 'Emergency pod with Chris McGuire']),
 ('grunewald', '2026-11-10', 'Tells Al Jazeera he thinks recent events likely "add momentum" to chip bills',
  ['sw-aljazeeracom-06'], ['add momentum to bills already being discussed in Congress, like the Chip Security Act']),
 ('stapp', '2026-11-10', '"Expect it to keep getting worse"',
  ['sw-thedailyupsidecom-01', 'sw-thedailyupsidecom-01'], ['said Alec Stapp, the co-CEO of the Institute for Progress', 'Expect it to keep getting worse']),
 ('warren', '2026-10-29', 'Statement: "NVIDIA\'s Jensen Huang and NVIDIA\'s board owe Congress answers"',       # her own statement is dated Oct 29 (found Nov 14); the chip sat on Nov 8, the day of a page that quoted it
  ['art-own-warren-statement-1029'] + ['sw-aljazeeracom-01'], ['board owe Congress answers'] + ['NVIDIA\'s Jensen Huang and NVIDIA\'s board owe Congress answers']),
 ('warren', '2026-11-09', 'Statement with Banks: Huang\'s confirmation "makes these national security concerns even more urgent"; they ask for answers and tighter export limits',
  ['sw-fortunecom-08', 'sw-nbcnewscom-02'], ['issued a joint statement calling for answers from Nvidia and tighter restrictions on advanced AI chip exports to China', 'makes these national security concerns even more urgent and raises important questions NVIDIA must answer']),
 ('warren', '2026-11-11', 'Letter with Coons asks the administration to "preserve all records"',
  ['sw-nbcnewscom-09', 'sw-financeyahoocom-23'], ['announced they had written to Commerce Secretary Howard Lutnick with a request to preserve records on the subject', 'have formally asked the Trump administration to "preserve all records"']),
 ('coons', 'EV11', '"Congress will investigate and get answers"'),
 ('coons', '2026-11-11', 'Letter with Warren asks the administration to "preserve all records"',
  ['sw-nbcnewscom-09', 'sw-financeyahoocom-23'], ['Sens. Elizabeth Warren, D-Mass., and Chris Coons, D-Del., announced they had written to Commerce Secretary Howard Lutnick', 'have formally asked the Trump administration to "preserve all records"']),
 ('cramer', 'EV21', '"I just think he\'s got to go"'),
 ('cramer', 'EV28', '"He should resign"'),
 ('schumer', 'EV22', 'Floor speech: pass three chip-export bills; of the president: "He\'s supposed to protect America, not China, not his friends"',
  ['bulwark-chipghazi'], ["He's supposed to protect America, not China, not his friends"]),
 ('banks', '2026-11-09', 'Statement with Warren: Huang\'s confirmation "makes these national security concerns even more urgent"; they ask for answers and tighter export limits',
  ['sw-fortunecom-08', 'sw-nbcnewscom-02'], ['Sen. Jim Banks (R., Ind.) issued a joint statement', 'makes these national security concerns even more urgent and raises important questions NVIDIA must answer']),
 ('blumenthal', '2026-11-09', '"We need a Senate investigation"', ['sw-semaforcom-04'], ['we need a Senate investigation']),
 ('warner', '2026-11-09', '"I want to get more facts before I weigh in"', ['sw-semaforcom-04'], ['I want to get more facts before I weigh in']),
 ('wyden', '2026-11-09', '"We don\'t know where it went"', ['sw-semaforcom-04'], ['We don\'t know where it went']),
 ('wyden', '2026-11-12', 'Letter with Rep. Neal opens a probe of chip-export approvals; it says the administration "did not appear to acknowledge this evident national security threat"',
  ['sw-cnbccom-09', 'sw-cnbccom-09'], ['Their letter to Commerce Secretary Howard Lutnick announcing the probe was sent by Sen. Ron Wyden', 'did not appear to acknowledge this evident national security threat']),
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
 ('mast', 'EV06', 'Letter dated Nov 4, released Nov 5, asks Huang to brief three committees: "Recent reports raise significant national security concerns"',
  ['house-hfac-letter-pr'], ['Recent reports raise significant national security concerns']),
 ('mast', 'EV29', 'Says "yes," a subpoena is being considered'),
 ('crawford', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5'),
 ('meeks', '2026-11-10', 'Says, as MS NOW reports it, he would subpoena a Commerce appointee',
  ['sw-msnow-01'], ['said he would subpoena Jeff Kessler']),
 ('himes', '2026-11-10', '"We\'ve asked Huang to appear"',
  ['sw-msnow-01'], ['"We\'ve asked Huang to appear," Rep. Jim Himes']),
 ('himes', '2026-11-10', 'Tells NPR it is "not clear" what Alice Huang\'s relationship with the Chinese government was: "That needs to be understood"',
  ['sw-nbcnewscom-09'] + ['art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110'],
  ['told NPR that Alice Huang\'s role still needed to be clarified'] + ['That needs to be understood', 'PUBLISHED: 2026-11-10', 'exactly what the relationship might have been between Alice Huang and the Chinese government']),
 ('huizenga', '2026-11-12', 'Says it would be "helpful" if the Commerce secretary testified in public; of the department: "They have not been as cooperative as they should be"',
  ['sw-cnbccom-09', 'sw-cnbccom-09'], ['said it would be "helpful" if Commerce Department Secretary Howard Lutnick testified to Congress in public', 'They have not been as cooperative as they should be']),
 ('johnson', '2026-11-09', 'Says "they\'re still gathering information"', ['sw-semaforcom-04'], ['House Speaker Mike Johnson told Semafor']),
 ('johnson', '2026-11-12', 'Calls the resignation a "big and shocking development" and the choice of successor "critically important"',
  ['globe-1112-resigns', 'cnn-1111-live'], ['critically important for right successor to be chosen to replace Huang', 'big and shocking development']),
 ('mccaul', '2026-11-09', 'Post, as quoted in Hot Air: pause advanced AI chip shipments to China',
  ['sw-hotaircom-02'], ['The U.S. should immediately pause the shipment of advanced AI chips to China']),
 ('moolenaar', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5'),
 ('moolenaar', 'EV23', 'Says Congress must "get to the bottom" of it'),
 ('moolenaar', 'EV29', 'Says Huang has not replied: "We are going to continue to pursue this"',
  ['cnbc-1111-congress-resign', 'cnbc-1111-congress-resign'], ['Mast and Moolenaar told reporters on Wednesday afternoon that they had not yet heard from Huang', 'We are going to continue to pursue this']),
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
 ('nvidia', 'EV07', 'Says customer meetings are "part of a CEO\'s job" and that customers get "zero information relevant to national security"; a spokesman tells the Times Huang "has an outstanding security team that accompanies him where needed"',
  ['cnbc-1105-asked-to-brief', 'man-nyt-1105-01', 'cnbc-1108-bipartisan'], ['zero information relevant to national security', 'Our chief executive has an outstanding security team that accompanies', 'Our chief executive has an outstanding security team that accompanies him where needed']),
 ('huang', 'EV14', 'Memo to staff: "I was unfaithful to my wife"; on the board\'s inquiry: "I support the investigation and will cooperate fully"',
  ['npr-1108-investigation'], ['I support the investigation and will cooperate fully']),
 ('huang', 'EV31', 'Resigns after 33 years as chief executive'),
 ('board', 'EV15', 'Opens an independent investigation; says it has "no reason to believe" secrets were compromised and "has confidence in Jensen and his leadership team"',
  ['sw-nvidianewsnvidiacom-01'], ['The Board has confidence in Jensen and his leadership team']),
 ('board', 'EV24', 'Hires outside counsel "to conduct a thorough and independent investigation"', ['nbc-exprosecutor'], ['to conduct a thorough and independent investigation as was announced on Sunday']),
 ('board', 'EV30', 'Meets to discuss removing Huang'),
 ('board', 'EV31', 'Names Kress interim chief, Jones chair; begins a search for a permanent chief',
  ['sw-tomshardwarecom-06'], ['The Board is initiating a search for a permanent Chief Executive Officer and will consider internal and external candidates']),
 ('nvda', 'EV20', 'Falls more than 4%'),
 ('nvda', 'EV25', 'Falls 5.47%'),
 ('nvda', 'EV32', 'Slides about 10% in early trading'),
 ('rivals', 'EV20', 'AMD up 13%, Broadcom up 10%'),
 ('anthropic', 'EV26', 'Sets its IPO price range; seven companies agree to buy $26B of its stock'),
 ('openai', '2026-11-04', 'Quoted by The Information, as the Daily Caller relays it: it "continues to support the strengthening of export controls". The sentence is in its policy paper dated November 2026, which gives no day',
  ['sw-dailycallercom-07'], ['OpenAI continues to support the strengthening of export controls']),
 ('singapore', 'EV04', 'Denies the Journal\'s account of Alice Huang: "no such investigations"; says its Megaspeed inquiry continues'),
 ('china', 'EV18', 'Calls the spy allegation "unsubstantiated"'),
 # added after audit1b (its finding on the Singapore denial); kept last so earlier row ids do not move
 ('singapore', '2026-11-12', 'Its statement: police interviewed her and held her passport in 2025; in Feb 2026 found "insufficient evidence" of offences over the declarations under investigation; a "stern warning" for inaccurate information; barred from re-entering; no espionage investigation. Requests to U.S. authorities over Supermicro brought "limited information or assistance"',
  ['sw-nbcnewscom-09'] * 6 + ['art-own-mha-1112'] * 3,
  ['authorities had interviewed Huang and impounded her passport in 2025', 'insufficient evidence to establish that Huang had committed any offences',
   'issued her with a stern warning after finding that she had knowingly provided police with inaccurate information', 'had been barred from re-entering the country', 'was not investigated for espionage',
   'Singapore has to date received limited information or assistance in respect of the company',
   'offences relating to the possible inaccurate declarations for which Megaspeed was being investigated', 'In February 2026', 'Supermicro provided limited cooperation']),
 ('mast', '2026-11-12', 'Says Huang "has agreed to come" and testify; the day is being negotiated. "Jensen and I have been very at odds ... on export controls, but NVIDIA is a very important company"; "I don\'t want to see anything hurt in NVIDIA, but he has some very serious questions to answer". With Moolenaar and Crawford, sends a second request: letters ask Huang, Nvidia\'s general counsel and a Commerce under secretary to appear; the three say Congress "must immediately pass" four chip-export bills',
  ['sw-cnbccom-09', 'sw-engadgetcom-0b81faf0', 'sw-engadgetcom-0b81faf0', 'art-own-foreignaffairs-1112-chairmen-mast-moolenaar-and-crawfo', 'sw-engadgetcom-0b81faf0', 'sw-engadgetcom-0b81faf0', 'art-own-foreignaffairs-1112-chairmen-mast-moolenaar-and-crawfo'],
  ['He has agreed to come', 'Jensen and I have been very at odds as some of you already know on export controls', 'but he has some very serious questions to answer', 'requesting their appearance before Congress',
   'but NVIDIA is a very important company to the United States of America', "I don't want to see anything hurt in NVIDIA", 'Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA']),
 # ---- S1 of the gaps spec (Nov 14): acts of speakers who had no row; appended so that earlier row ids do not move
 ('rubio', '2026-11-08', 'Says he "can\'t comment on an internal corporate matter that\'s going on with Nvidia"', ['nbc-1108-investigation'], ['comment on an internal corporate matter']),
 ('bessent', '2026-11-05', 'Axios, as the Daily Caller relays it: in a Situation Room meeting he asks Lutnick "How come Megaspeed isn\'t on the entities list?" The Times reports the exchange too, as "described by people briefed on it", and prints a Commerce spokeswoman\'s denial that the conversation took place',
  ['sw-dailycallercom-03', 'sw-dailycallercom-03', 'man-nyt-1111-02', 'man-nyt-1111-02', 'man-nyt-1111-02'],
  ['pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting', 'on the entities list?', 'Treasury Secretary Scott Bessent confronted Commerce Secretary Howard Lutnick last week', 'took place at the White House on Thursday and was described by people briefed on it',
   'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place']),
 ('commerce', '2026-11-11', 'Axios, as Gizmodo relays it: the president told Lutnick "let\'s get it done"; Lutnick replied "I\'ll develop some options and come back". Gizmodo adds that the administration denied to Axios and the Times that the confrontation took place',
  ['sw-gizmodocom-08', 'sw-gizmodocom-08', 'sw-gizmodocom-08'], ['develop some options and come back', 'at some point Trump told Lutnick', 'denied to both Axios and the Times that any such confrontation between Bessent and Lutnick had ever taken place']),
 ('commerce', '2026-11-12', 'A spokeswoman tells CNBC Bessent and Lutnick had "no such conversation"', ['sw-cnbccom-22'], ['Commerce Department spokeswoman Kristen Eichamer told CNBC that Bessent and Lutnick had "no such conversation"']),
 ('greer', '2026-11-12', 'Tells CNBC "Nvidia is a structurally important company"', ['sw-cnbccom-09'], ['Nvidia is a structurally important company']),
 ('whitehouse', '2026-11-09', 'Asked how the administration handled the information: "These sources have no idea what they\'re talking about"', ['msnow-resigns'], ['a White House spokesperson referred MS NOW to Trump']),
 ('whitehouse', '2026-11-12', 'Statement calls Lutnick "a champion of President Trump\'s America First trade and tariff policies"', ['sw-cnbccom-09'], ['Secretary Lutnick is a champion of President Trump']),
 ('justice', '2026-11-09', 'CBS, as Breitbart relays it: its National Security Division is investigating Megaspeed', ['sw-breitbartcom-04'], ['National Security Division is investigating Megaspeed']),
 ('kress', 'EV31', 'Statement: "committed to building on the extraordinary foundation Jensen created"; in an email to staff: "this has been an extraordinarily difficult period"',
  ['fortune-1111-resigns', 'sw-cnbccom-ca82d66d'], ['I am committed to building on the extraordinary foundation Jensen created', 'recognize that this has been an extraordinarily difficult period']),
 ('jones', 'EV31', 'Statement: "Colette has helped lead NVIDIA through a period of extraordinary growth"', ['fortune-1111-resigns'], ['Colette has helped lead NVIDIA through a period of extraordi']),
 ('suit', '2026-11-09', 'Complaint filed in federal court: a company statement on Megaspeed "was materially false and misleading"',      # the complaint itself is stamped filed Nov 9 (found Nov 14); the chip sat on Nov 10
  ['art-own-complaint-1109', 'art-own-complaint-1109', 'sw-courthousenewscom-02'], ['Filed 11/09/26', 'was materially false and misleading at the time it was made', 'was materially false and misleading at the time it was made']),
 ('nvidia', '2026-11-09', 'Bloomberg reports, about an act of 2025: Nvidia\'s general counsel "intervened in a US government probe" of Megaspeed, calling a Commerce under secretary in late summer 2025 to ask about it',
  ['sw-techcrunchcom-08', 'sw-techcrunchcom-08', 'man-efbf718d0a5a', 'man-efbf718d0a5a', 'man-efbf718d0a5a', 'man-efbf718d0a5a'],
  ['Tim Teter, intervened in a 2025 U.S. government probe', 'November 9-10, 2026: Details emerge', 'general counsel intervened in a US government probe', 'November 9, 2026 at 3:28 PM CST', 'In late summer 2025', 'Tim Teter called Commerce Under Secretary']),
 ('anthropic', '2026-11-12', 'A spokesperson "declined to comment" to Quartz for a report on Huang\'s exit and Anthropic\'s share sale', ['sw-qzcom-efc3c07a'], ['An Anthropic spokesperson declined to comment']),
 ('musk', '2026-11-11', 'Posts that hiring Huang "would be an honor", in reply to a ZeroHedge post: "Elon please hire Jensen"', ['mj-misogyny', 'sw-zerohedgecom-09', 'sw-zerohedgecom-09'], ['Elon Musk wrote on Wednesday', 'Elon Musk responded to our X post', 'Elon please hire Jensen']),
 ('maguire', '2026-11-08', 'Posts that Huang "did something incredibly dumb" that was "bad for America", but "Two mistakes don\'t make a right, and I believe Jensen is irreplaceable for America\'s AI leadership"; Elon Musk replies "I agree"',
  ['sw-calcalistechcom-02', 'sw-calcalistechcom-02', 'sw-gulftimescom-01', 'sw-gulftimescom-01', 'semafor-1108-founder', 'semafor-1108-founder'],
  ['I believe Jensen is irreplaceable for America', 'Tesla CEO Elon Musk responded to Maguire', 'did something incredibly dumb', 'bad for America', 'On Sunday, Sequoia', 'PUBLISHED: 2026-11-09T02:58:19Z']),
 ('ackman', '2026-11-09', 'Posts that Huang is an "incredible human", but if "indeed this is more than an affair, then it is obviously a real problem": "I am hoping for a simple affair, not a risk to our national security"',
  ['sw-gulftimescom-01'] * 3, ['I am hoping for a simple affair, not a risk to our national security', 'indeed this is more than an affair, then it is obviously a real problem', 'said on X the Nvidia CEO was an "incredible human"']),
 ('sweeney', '2026-11-12', 'Posts: "A sad day for NVIDIA, developers, America, and all humanity"', ['sw-80lv-02'], ['A sad day for NVIDIA, developers, America, and all humanity']),
 ('jcramer', '2026-11-11', 'On his show: "A Jensen-less Nvidia is an Nvidia many will not want to own"', ['sw-financeyahoocom-b1ac141d'], ['on the November 11 episode of Mad Money']),
 ('embassy', '2026-10-29', 'Its spokesman, in the Times: a campaign of "groundless smears and slanders"', ['man-nyt-1029-01'], ['groundless smears and slanders']),
 ('megaspeed', '2026-11-12', 'Says it takes U.S. export-control compliance "extremely seriously" and has cooperated with inspections', ['huffpost-live'], ['Megaspeed said on Thursday that it takes compliance obligations under U.S. export control laws']),
 ('taiwan', '2026-11-11', 'Says security agencies are "actively investigating" the case', ['sw-taiwannewscomtw-04'], ['said outside the legislature that security agencies were']),
 ('globaltimes', '2026-11-09', 'Writes: "Whenever China-US relations begin to improve, there are often those firing shots from the shadows"', ['sw-inquirercom-01'], ['there are often those firing shots from the shadows']),
 # ---- S2 of the gaps spec (Nov 14): remarks of members already drawn that the saved pages carry and no chip did
 ('moolenaar', '2026-11-12', 'Says talks are under way "on a date to come and meet with us"; the resignation "does change the dynamic". Statement: the departure is "an unfortunate end that could have been avoided"; "It is in our national interest for NVIDIA and our other AI champions to succeed", but Nvidia "must now change its corporate practices". With Mast and Crawford, sends a second request to appear; the three say Congress "must immediately pass" four chip-export bills',
  ['sw-cbsnewscom-e684eb4c', 'cnn-1111-live', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr',
   'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr'],
  ['We are in discussions with him right now on a date to come and meet with us', 'does change the dynamic', 'Nvidia must now change its corporate practices and appoint leadership that makes national security its top priority', 'requesting their appearance before Congress',
   'is an unfortunate end that could have been avoided', 'It is in our national interest for NVIDIA and our other AI champions to succeed', 'Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA']),
 ('jeffries', '2026-11-12', 'Calls the resignation the "right thing to do"; "Now we have to get to the bottom of whether America\'s national security has been compromised"',
  ['cnn-1111-live', 'cnn-1111-live'], ['resignation Thursday was the "right thing to do,"', 'Now we have to get to the bottom of whether America']),
 ('schumer', '2026-11-12', 'Statement: "Despite Jensen Huang\'s resignation, Congress must demand answers"', ['sw-cbsnewscom-e684eb4c'], ['resignation, Congress must demand answers from Mr. Huang and others at Nvidia']),
 ('warren', '2026-11-12', 'Statement: Huang, executives and the board "still owe Congress answers"; Lutnick "must explain why they have not closed export control loopholes"',
  ['sw-cbsnewscom-09', 'sw-cnbccom-09'], ['board of directors still owe Congress answers', 'must explain why they have not closed export control loopholes']),
 ('coons', '2026-11-09', 'A post, as Australia\'s ABC reports it: "I\'m pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised"',
  ['sw-abcnetau-03'], ['pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised']),
 # the full reading of the saved pages (2026-11-14): a Times report of Nov 9 and the department's answer; one more public voice
 ('nyt', '2026-11-09', 'Reports that a Commerce Department investigation of Megaspeed "came to a sudden halt late last year" and was "transferred to the Justice Department", after Nvidia\'s general counsel emailed the investigators in August 2025. It says the transfer was "to avoid any potential compromise" of the investigation, that Justice "is conducting a criminal inquiry into Megaspeed", and that "it is not clear if other factors contributed"',
  ['sw-cnbccom-02', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03'],
  ['the Times reported that the Commerce Department was investigating Megaspeed until August 2025, when the probe was abruptly transferred to the Department of Justice following outreach from Nvidia\'s general counsel about the matter',
   'their work came to a sudden halt late last year', 'the case was abruptly transferred to the Justice Department last year', 'In August 2025, officials at the Commerce Department', 'received an email from Mr. Teter, the general counsel of Nvidia',
   "in an effort to avoid any potential compromise of the government's investigation of Megaspeed", 'The Justice Department is conducting a criminal inquiry into Megaspeed',
   "It is not clear if other factors contributed to the decision to suspend the Commerce Department's work"]),
 ('commerce', '2026-11-09', 'A spokesman for its export-control bureau tells CNBC: "BIS conducts all enforcement strictly by the book"',
  ['sw-cnbccom-02'], ['BIS conducts all enforcement strictly by the book']),
 ('kudlow', '2026-11-10', 'On his show: "Step down, Mr. Huang. Right now"', ['sw-mediaitecom-06'], ['Step down, Mr. Huang. Right now']),
 # remarks the full reading found on many pages and no chip carried (2026-11-14)
 ('trump', '2026-11-12', 'Posts: "there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!"',
  ['fox-trump-successor'], ['there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!']),
 ('nvidia', '2026-11-08', 'Tells CNBC: "Today\'s news will not slow NVIDIA. Jensen is committed to continuing to lead NVIDIA as CEO without interruption". Tells CBS: "We trust that if we were the target of a genuine threat, the U.S. government would have notified us"',
  ['cnbc-1108-bipartisan', 'sw-cbsnewscom-01', 'sw-cbsnewscom-01'], ['Jensen is committed to continuing to lead NVIDIA as CEO without interruption', 'We trust that if we were the target of a genuine threat, the U.S. government would have notified us', 'told CBS News on Sunday']),
 ('huang', '2026-10-29', 'Tells Bloomberg, as Taiwan News relays the interview (Bloomberg\'s saved page shows its opening only): "Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual"; as Data Center Knowledge relays it, "We\'ve studied all their deployments of our GPUs and counted every one". Data Center Dynamics has him calling the story "groundless speculation"',
  ['man-bbg-1029-01', 'sw-taiwannewscomtw-01', 'sw-datacenterknowledgecom-01', 'sw-datacenterknowledgecom-01', 'sw-datacenterdynamicscom-03', 'sw-datacenterdynamicscom-03'],
  ['Nvidia CEO Says Ties to Company in Spy Probe Were', 'Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual',
   'studied all their deployments of our GPUs and counted every one', 'in an October 29 Bloomberg interview', 'Huang called the story', 'groundless speculation']),
 ('huang', '2026-11-11', 'Reached by phone by the Times and asked about a second relationship: "I don\'t think you should be talking to me directly"',
  ['man-e1161e38dc19'], ["I don't think you should be talking to me directly"]),
 ('commerce', '2026-11-05', 'Axios, as ZeroHedge relays it: asked by Bessent why Megaspeed is not on the entity list, Lutnick answers "I don\'t know. I\'ll look into it". In a second report of Axios, of an Oval Office meeting with the president that day, he warns that the controls "will start a trade war with China". In the Times\'s account of the first exchange he answers that Commerce "could now move quickly to put restrictions on Megaspeed in place". A Commerce spokeswoman: "This is false. Secretary Bessent and Secretary Lutnick had no such conversation"',
  ['sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'sw-dailycallercom-03', 'sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'man-nyt-1111-02', 'man-nyt-1111-02'],
  ['again in the Oval Office on Nov. 5', "I don't know. I'll look into it", 'pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting', 'This is false. Secretary Bessent and Secretary Lutnick had no such conversation', 'while Lutnick warned that the controls', 'will start a trade war with China',
   'Commerce Department could now move quickly to put restrictions on Megaspeed in place', 'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place']),
 # every analyst and byline on the saved pages was looked up in the funding records (2026-11-14): two more analysts and one more byline have a record and a remark of these days
 ('king', '2026-11-12', 'Quartz reports her saying that export controls cover the physical transfer of chips but not remote access to them',
  ['sw-qzcom-13'], ['U.S. export controls cover the physical transfer of chips but not remote access to them, said Cassia King']),
 ('nie', '2026-11-12', 'Quartz reports her saying the remote-access bill alone would fall short: it would give the legal authority, but "a separate rulemaking process would be required" before it could be used on advanced chips',
  ['sw-qzcom-13', 'sw-qzcom-13'], ['RASA alone would fall short of closing the loophole, said Michelle Nie', 'a separate rulemaking process would be required before that authority could be used on advanced chips']),
 ('hashim', '2026-11-09', 'Publishes "Jensen Huang should resign"', ['sw-transformernewsai-01', 'sw-transformernewsai-01'], ['AUTHOR: Shakeel Hashim', 'Jensen Huang should resign']),
 # a member named on five saved pages for an act on the matter a year before these days: no day on the calendar (drawn in his row, like any act with no day)
 ('cotton', '', 'Before these days: in Oct 2025 he wrote to the Commerce secretary about Megaspeed\'s "suspicious ownership, affiliations"; pages of these days cite the letter',
  ['sw-thefederalistcom-01', 'sw-thefederalistcom-01', 'sw-spectatorcom-01'],
  ['In October 2025, Sen. Tom Cotton, R-Ark., wrote to Commerce Secretary Howard Lutnick to raise concerns about Megaspeed', 'suspicious ownership, affiliations', 'the Arkansas Republican who chairs the Senate Intelligence Committee, asked the Commerce Department to investigate Megaspeed in October last year']),
 # ---- S6 of the gaps spec (Nov 14): remarks and acts found on the actors' own channels (ministry transcripts, members' releases, an institute's site) that no chip carried
 ('china', '2026-10-30', 'Its spokesman on the Times report: "unsubstantiated. It is nothing but smears against China"',
  ['art-own-fmprc-1030-t20261030-12050434'], ['Relevant report is unsubstantiated. It is nothing but smears against China']),
 ('china', '2026-11-11', 'Asked about calls for tighter chip limits: "Our position on U.S. chip exports to China is consistent"',
  ['art-own-fmprc-1111-t20261111-12057544'], ['Our position on U.S. chip exports to China is consistent']),
 ('china', '2026-11-12', 'Its spokeswoman: the U.S. should "stop fabricating" spy "narratives as a pretext for imposing technology restrictions"',
  ['art-own-fmprc-1112-t20261112-12058413', 'art-own-fmprc-1112-t20261112-12058413'], ['The U.S. should stop fabricating the', 'narratives as a pretext for imposing technology restrictions']),
 ('meeks', '2026-11-09', 'Letter with two colleagues asks the Commerce secretary to "immediately halt exports of advanced artificial intelligence chips" to China',
  ['art-own-democrats-foreignaffairs-1109-meeks-amo-kamlager-dove-de'], ['We call on the Department of Commerce to immediately halt exports of advanced artificial intelligence chips']),
 ('jeffries', '2026-11-10', 'On PBS, after a classified briefing: nothing disclosed yet "to be able to draw any conclusions with respect to the timeline"; "clearly there\'s a need for Members of Congress to be briefed moving forward"',
  ['art-own-democraticleader-1110-leader-jeffries-pbs-we-will-visit'] * 2, ["clearly there's a need for Members of Congress to be briefed moving forward", 'to be able to draw any conclusions with respect to the timeline']),
 ('crawford', '2026-11-12', 'With Moolenaar and Mast, sends a second request: letters ask Huang, Nvidia\'s general counsel and a Commerce under secretary to appear before Congress. Their joint statement: "Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA"',
  ['art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr', 'art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr'], ['requesting their appearance before Congress', 'Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA']),
 ('globaltimes', '2026-11-12', 'Writes of "Washington\'s increasingly hysterical anti-China climate"',
  ['art-own-globaltimes-1112-1374159', 'art-own-globaltimes-1112-1374159'], ["Washington's increasingly hysterical anti-China climate", 'Published: Nov 12, 2026']),
 ('bresnick', '2026-11-10', 'In a Washington Post article, as his centre quotes it: "There\'s a sex scandal, an espionage issue, and then there is the issue of selling advanced computer chips to a company that seemingly does not exist"',
  ['art-own-georgetown-1110-the-phantom-life-of-alice-huang-al'] * 2, ['Sam Bresnick shared his expert insight in an article published by The Washington Post', 'and then there is the issue of selling advanced computer chips to a company that seemingly does not exist']),
 ('bresnick', '2026-11-11', 'In a second Washington Post article, as his centre quotes it, on the president\'s response: "Either Trump doesn\'t necessarily care about this very much or still trusts Huang to a degree"',
  ['art-own-georgetown-1111-spy-scandal-highlights-contradicti'] * 2, ['Sam Bresnick shared his expert insight in an article published by The Washington Post', "necessarily care about this very much or still trusts Huang to a degree"]),
 # found on Nov 15, 2026 by the search of the records held for Nvidia's side: his college's page says Anthropic, among others, supports his research.
 # The look-up of Nov 14 had read another row (a 2020 grant to another Oxford institute) and called it none.
 ('barez', '2026-11-09', 'Tells Al Jazeera that as AI shapes national economies "safeguarding becomes even more serious", for "confidential secrets" and "advancements" alike',
  ['sw-aljazeeracom-03', 'sw-aljazeeracom-03', 'sw-aljazeeracom-03'], ['safeguarding becomes even more serious', 'Fazl Barez, a senior researcher at the University of Oxford specialising in AI safety and governance, told Al Jazeera', 'PUBLISHED: 2026-11-09']),
 # ---- added after the third lane of the second audit (Nov 15, 2026)
 # B11: the president's first remarks, which the reading had set against his chips of Nov 8 and 9
 ('trump', '2026-10-31', 'At his Halloween party, asked if he still has confidence in Huang as an adviser: "I would like to say yes. I mean, unless we find out something to the contrary"; says the matter is "very complex" and will be looked at "very closely"',
  ['sw-aninewsin-01', 'sw-aninewsin-01', 'sw-irishtimescom-01', 'sw-irishtimescom-01'],
  ['I would like to say yes. I mean, unless we find out something to the contrary', 'going to check it out very closely', 'Trump told reporters on October 31st', 'calling the situation']),
 # B04: Mast's interview of Tuesday, Nov 10, with what he says in Nvidia's favour
 ('mast', '2026-11-10', 'Tells ABC he is prepared to subpoena Huang if no reply comes by Wednesday. Of Nvidia: "we thank God that Jensen is an American entrepreneur ... they\'re the best chips anywhere in the globe. But that being said, we don\'t want China to access them"',
  ['abc-subpoena'] * 4, ['told ABC News on Tuesday that he', 'So we thank God that Jensen is an American entrepreneur', 'the best chips anywhere in the globe', 'want China to access them, to use them, to produce them like that']),
 # quoted analysts with a tie on record, by the one rule (see ACTORS)
 ('chan', '2026-11-12', 'Tells CNBC the president\'s weakened grip on congressional Republicans after the midterm defeat makes it harder for the administration to hold back chip-export measures',
  ['sw-cnbccom-08', 'sw-cnbccom-08'], ['said Kyle Chan, a China fellow at the Brookings Institution', 'PUBLISHED: 2026-11-12']),
 ('ohanlon', '2026-11-10', 'Tells Newsweek: "Huang\'s motives must now be suspect. That is the key point. But he did not make the actual decisions on export control policy so the damage may be limited"',
  ['sw-newsweekcom-01'] * 3, ['a senior fellow at the Brookings Institution who studies defense and foreign policy, told Newsweek', 'But he did not make the actual decisions on export control policy so the damage may be limited', 'PUBLISHED: 2026-11-10']),
 ('wiblin', '2026-11-10', 'A post of his, as Zvi Mowshowitz\'s newsletter carries it: Huang was "pushing to sell maximum of cutting edge AI chips to China against advice of ~entire natsec community"',
  ['sw-thezvisubstackcom-01'] * 3, ['Rob Wiblin', 'Meanwhile pushing to sell maximum of cutting edge AI chips to China against advice of ~entire natsec community', 'PUBLISHED: 2026-11-10']),
 ('moorhead', '2026-11-10', 'Tells CNBC: "In 35 years, I haven\'t seen a chip CEO with this much direct influence on export policy"',
  ['sw-cnbccom-04'] * 3, ['seen a chip CEO with this much direct influence on export policy', 'said Patrick Moorhead, CEO at Moor Insights', 'PUBLISHED: 2026-11-10']),
 ('newman', '2026-11-09', 'Tells CBS by email: "There is no known succession plan, and there is no leader in the company who would be the clear next step if he had to step down"; "That does not mean they cannot find a Tim Cook in the future, but it would be a massive changing of the guard"',
  ['sw-cbsnewscom-03'] * 4, ['There is no known succession plan, and there is no leader in the company who would be the clear next step if he had to step down', 'said Daniel Newman, CEO of tech consulting firm Futurum, in an email', 'PUBLISHED: 2026-11-09',
   'That does not mean they cannot find a Tim Cook in the future, but it would be a massive changing of the guard']),
 ('boloor', '2026-11-12', 'Tells Fortune the selloff is overdone: he does not see "12 to 18 months of revenue suddenly disappearing if Jensen were to leave". Quoted the same day: "My bigger concern is next decade", because Huang "has consistently identified where computing is going"',
  ['sw-fortunecom-11', 'sw-fortunecom-11', 'sw-fortunecom-11', 'sw-rteie-05', 'sw-rteie-05'], ['12 to 18 months of revenue suddenly disappearing if Jensen were to leave', 'Shay Boloor, chief market strategist at The Futurum Group', 'PUBLISHED: 2026-11-12',
   'My bigger concern is next decade', 'the person who has consistently identified where computing is going']),
 ('yoo', '2026-11-12', 'Tells the Korea JoongAng Daily that Nvidia\'s people "have a high level of expertise and autonomy", so its culture will hold',
  ['sw-koreajoongangdailycom-06'] * 3, ['Because its people have a high level of expertise and autonomy, the culture won', 'Yoo Eung-joon, CEO of JOON AI Consulting and a former head of Nvidia Korea', 'PUBLISHED: 2026-11-12']),
 ('mowshowitz', '2026-11-10', 'Publishes "Nvidia CEO Jensen Huang Had an Affair With a Chinese Spy": "National security has been compromised. He must resign"',
  ['sw-thezvisubstackcom-01'] * 3, ['AUTHOR: Zvi Mowshowitz', 'National security has been compromised. He must resign', 'PUBLISHED: 2026-11-10']),
 ('schneider', '2026-11-10', 'Publishes "The Spy Who Leased Me", the newsletter page of his podcast with Chris McGuire on the affair, which his feed dates the day before',
  ['sw-chinatalkmedia-01'] * 3, ['AUTHOR: Jordan Schneider', 'Emergency pod with Chris McGuire', 'PUBLISHED: 2026-11-10']),
 ('newman', '2026-11-12', 'Tells NPR: "They\'ve always had Jensen as this sort of visionary at the front. I don\'t think that\'s replaceable"',
  ['sw-nprorg-01'] * 3, ['always had Jensen as this sort of visionary at the front', 'Daniel Newman, CEO of the Futurum Group, a tech research firm', 'PUBLISHED: 2026-11-12']),
 # three more public voices on three or more saved pages
 ('delangue', '2026-11-12', 'Posts: "This whole thing sucks, and I wish none of it had happened"; calls it "a really sad day" and adds: "we\'ll keep fighting for open-source AI, harder than ever"',
  ['cnn-1111-live', 'sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cnbccom-09'], ['This whole thing sucks, and I wish none of it had happened', 'lamented Huang', 'PUBLISHED: 2026-11-12', 'keep fighting for open-source AI, harder than ever']),
 ('zhao', '2026-11-12', 'Posts that it is "a mistake for Nvidia to let Jensen resign"',
  ['sw-cnbccom-09', 'cnn-1111-live'], ['a mistake for Nvidia to let Jensen resign', 'departure Thursday morning, Binance co-founder and former CEO Changpeng Zhao']),
 ('rao', '2026-11-12', 'Tells Yahoo Finance the search for a new chief "needs to be closed probably in the next three or four months"',
  ['sw-financeyahoocom-23'] * 3, ['it needs to be closed probably in the next three or four months', 'Unconventional AI founder and CEO Naveen Rao', 'PUBLISHED: 2026-11-12']),
 # ---- added after the release of Nov 15 (commit 2b7a13d), at the END so that no published id moves
 # two reports of the Times that its row lacked (hand-saved on Nov 12 and never drawn; found when the hand-saved pages were listed on Nov 15)
 ('nyt', '2026-11-10', 'Reports that the president was told aboard Air Force One in May, by Rubio, of the intelligence on Huang, which "contradicts the president\'s assertion" that he had not known then; the White House "disputed the reporting", it says, "without elaborating"',
  ['man-nyt-1110-02'] * 5, ['President Trump was told aboard Air Force One in May en route to China', 'The message was delivered by Marco Rubio', 'assertion on Monday that he had not known at the time of the trip', 'The email disputed the reporting for this article, without elaborating', 'PUBLISHED: 2026-11-10']),
 ('nyt', '2026-11-11', 'Reports that Bessent "confronted" Lutnick at the White House over Megaspeed, as "described by people briefed on it"; a Commerce spokeswoman denies the conversation took place',
  ['man-nyt-1111-02'] * 4, ['Treasury Secretary Scott Bessent confronted Commerce Secretary Howard Lutnick last week', 'took place at the White House on Thursday and was described by people briefed on it',
                            'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place', 'PUBLISHED: 2026-11-11']),
 # items on the actors' own channels found by the second own-channel search (lane s6_channels_3, Nov 15), each saved and read first
 ('moorhead', '2026-11-08', 'On BBC News. His firm\'s own summary of the broadcast: the short-term operational impact on Nvidia "will be negligible", but "any findings implicating U.S. national security could force Huang\'s departure"',
  ['art-own-moorinsights-1109-bbc-1108'] * 5, ['Yesterday (U.S. Central time) I appeared on BBC News Business Today', 'the short-term operational impact on Nvidia will be negligible',
                                               "any findings implicating U.S. national security could force Huang's departure", 'an AI-generated, human-edited overview and summary', 'PUBLISHED: 2026-11-09']),
 ('moorhead', '2026-11-09', 'On ABC7 Bay Area. His firm\'s summary: "even if Huang stepped down, qualified internal candidates exist among dozens of direct reports". His weekly note that day: "I\'ve given about 20 press interviews in the span of a day since the news broke"',
  ['art-own-moorinsights-1110-abc7-1109'] * 3 + ['art-own-moorinsights-1109-weekly-1106'] * 2,
  ['Yesterday I appeared on ABC7 Bay Area to discuss the unfolding saga of NVIDIA CEO Jensen Huang', 'even if Huang stepped down, qualified internal candidates exist among dozens of direct reports', 'PUBLISHED: 2026-11-10',
   "I've given about 20 press interviews in the span of a day since the news broke", 'Week Ending November 6, 2026 November 9, 2026']),
 ('moorhead', '2026-11-11', 'On ABC7 Bay Area again. His firm\'s summary: the two matters together make it "very difficult for Huang to remain CEO if the allegations are proven true"; the cloud companies\' plans "should not miss a beat"',
  ['art-own-moorinsights-1112-abc7-1111'] * 4, ['Yesterday I appeared again on ABC7 Bay Area', 'makes it very difficult for Huang to remain CEO if the allegations are proven true',
                                                'day-to-day operations and datacenter plans for the cloud giants should not miss a beat', 'PUBLISHED: 2026-11-12']),
 ('newman', '2026-11-10', 'Hosts his firm\'s show with Shay Boloor on "what Nvidia\'s board investigation means for the AI trade"; the firm\'s page says "both hosts call it key-man risk". The recording was not heard',
  ['art-own-futurumequities-daily-shay'] * 4, ['Jensen Huang under review. What it means for Nvidia and the AI trade | Ep 64.', 'Futurum Equities November 10, 2026 8:05 am',
                                               "to break down what Nvidia's board investigation means for the AI trade", 'why both hosts call it key-man risk']),
 ('boloor', '2026-11-10', 'Hosts his firm\'s show with Daniel Newman on Nvidia\'s board investigation. A later post of the firm about that show quotes him: "Nothing about the technology or roadmap has changed on NVIDIA. This is just purely a key man risk issue". The recording was not heard',
  ['art-own-futurumequities-daily-shay'] * 3, ['Nothing about the technology or roadmap has changed on NVIDIA. This is just purely a key man risk issue.', '-@StockSavvyShay', 'Futurum Equities November 10, 2026 8:05 am']),
 ('mowshowitz', '2026-10-29', 'In his weekly newsletter, on the Times report: "you should be entirely unshocked that such a spy is out there"; "this is me not updating"',
  ['art-own-thezvi-1029-ai-192'] * 5, ['We all know that Jensen Huang is at minimum the target of Chinese spy plots', 'you should be entirely unshocked that such a spy is out there', 'Yeah, this is me not updating',
                                       'AUTHOR: Zvi Mowshowitz', 'PUBLISHED: 2026-10-29']),
 ('mowshowitz', '2026-11-12', 'In his weekly newsletter, "Spy Versus Guy": removing Huang "will be tricky because Jensen Huang deliberately tried to make himself unfireable, with over 50 direct reports and no succession plan"',
  ['art-own-thezvi-1112-ai-194'] * 4, ["Nvidia's board of directors is preparing to remove Jensen Huang and is searching for an interim CEO",
                                       'This will be tricky because Jensen Huang deliberately tried to make himself unfireable, with over 50 direct reports and no succession plan', 'TITLE: AI #194: Spy Versus Guy', 'PUBLISHED: 2026-11-12']),
 ('cornyn', '2026-11-12', 'A post of his, as Zvi Mowshowitz\'s newsletter of Nov 12 carries it, gives the title of Mowshowitz\'s piece of Nov 10 and its author\'s handle. The post itself could not be opened, so its day is not known',
  ['art-own-thezvi-1112-ai-194'] * 3, ['Senator John Cornyn (R-Texas): Nvidia CEO Jensen Huang Had an Affair With a Chinese Spy', 'You never know who is listening, Senatorial edition', 'PUBLISHED: 2026-11-12']),
 ('schneider', '2026-11-09', 'His podcast releases two episodes: an "emergency pod", "Jensen and His Spy", with Chris McGuire, and one recorded, it says, "Friday afternoon, before the FT reported", with a part on "the alleged spy in Jensen Huang\'s orbit". The recordings were not heard',
  ['art-own-applepodcasts-chinatalk-emergency-pod'] * 2 + ['art-own-applepodcasts-chinatalk-are-we-cooking'] * 3,
  ['November 9 EMERGENCY POD: Jensen and His Spy', 'To make sense of it we have Chris McGuire',
   "November 9 Are We Cooking!? What Should Dems Do Next + Jensen's Affair", 'we recorded this Friday afternoon, before the FT reported', "The alleged spy in Jensen Huang's orbit"]),
 ('schneider', '2026-10-31', 'An episode of his podcast, with him among the speakers, lists a part titled "Jensen, spies, and the J-5 firing". The recording was not heard',
  ['art-own-applepodcasts-chinatalk-episodes'] * 3, ['Oct 31 WarTalk: Pressing the War Button: Iran, Cuba, and Rubio 2028', 'WarTalk regulars Jordan Schneider', '00:24:37 Jensen, spies, and the J-5 firing']),
 # the reading of the corrections (lane audit_nv8_s7d, Nov 15): a saved page reports what the FBI's inquiry is about, as one does for Justice; the bureau is part of that department
 ('justice', '2026-11-10', 'Mother Jones reports that the FBI, "along with the Justice Department\'s national security division", is investigating Megaspeed over chip shipments to China and "looking into whether China recruited Alice Huang to spy"',
  ['mj-trump-corner'] * 4, ['I know the FBI is looking into it', "The agency, along with the Justice Department's national security division",
                            'is investigating Megaspeed for allegedly shipping Nvidia AI chips to customers in China and looking into whether China recruited Alice Huang to spy', 'PUBLISHED: 2026-11-10']),
]

# Acts whose source gives no day for the act itself: they sit on the day the source was published and are drawn with a dashed edge.
REPORT_DAY = {('justice', '2026-11-10'), ('cornyn', '2026-11-12'), ('chan', '2026-11-12'), ('ohanlon', '2026-11-10'), ('wiblin', '2026-11-10'), ('moorhead', '2026-11-10'), ('newman', '2026-11-09'), ('newman', '2026-11-12'), ('boloor', '2026-11-12'), ('yoo', '2026-11-12'), ('commerce', '2026-11-09'), ('bresnick', '2026-11-10'), ('bresnick', '2026-11-11'), ('king', '2026-11-12'), ('nie', '2026-11-12'), ('bresnick', '2026-11-09'), ('fedasiuk', '2026-11-12'), ('mcguire', '2026-11-10'), ('grunewald', '2026-11-10'), ('stapp', '2026-11-10'),
              ('blumenthal', '2026-11-09'), ('warner', '2026-11-09'), ('wyden', '2026-11-09'), ('wyden', '2026-11-12'),
              ('cornyn', '2026-11-08'), ('cornyn', '2026-11-09'), ('thune', '2026-11-12'), ('johnson', '2026-11-12'),
              ('mccaul', '2026-11-09'), ('magaziner', '2026-11-08'), ('openai', '2026-11-04'),
              ('commerce', '2026-11-11'), ('justice', '2026-11-09'), ('nvidia', '2026-11-09'), ('ackman', '2026-11-09'),
              ('taiwan', '2026-11-11'), ('anthropic', '2026-11-12'), ('coons', '2026-11-09')}

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
# ---- added on Nov 14, 2026 with the look-up of every analyst and byline; numbered after TIES_V4 so that earlier row ids do not move. Drawn as lines.
TIES_V5 = [
 (IAPS, 'Cassia King', 'role', 'senior researcher', ['sw-qzcom-13'], ['Cassia King, a senior researcher in the Compute Policy group at the Institute for AI Policy and Strategy']),
 ('CNAS', 'Michelle Nie', 'role', 'visiting fellow', ['sw-qzcom-13'], ['Michelle Nie, a visiting fellow in technology and national security at the Center for a New American Security']),
 (TARBELL, 'Shakeel Hashim', 'role', 'listed on its team page as editor of Transformer', [LIN + 'people.csv#P124', LIN + 'people.csv#P124'], ['Editor, Transformer', 'https://www.tarbellcenter.org/team/shakeel-hashim']),
 (HORIZON, 'Michelle Nie', 'role', 'AI fellow on its think-tank track, 2025–26, placed at CNAS',
  [PK + 'congress/research/revolving_door.csv#RD1262'] * 3, ['AI Fellow, Think Tank Track', 'Horizon Institute for Public Service', 'placement=Center for a New American Security']),
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
# ---- added after the second audit (Nov 15, 2026): a tie it found recorded in the tables and not drawn; numbered after TIES_V5.
TIES_V6 = [
 ('AnthroPAC', 'Sen. Tom Cotton', 'money', '$2,500 · Sep 30', [FEC + 'COTTON FOR SENATE, INC.'], ['2500.00']),
 # found by the search of the records held for Nvidia's side (Nov 15, 2026), which ran the same search for Anthropic
 ('Anthropic', 'Fazl Barez', 'money', 'supports his research, as do OpenAI, Schmidt Sciences and Nvidia, his college\'s page says; no amount or date is given',
  ['art-f1-reuben-barez', PK + 'evaluators-deep/research/people_edges.csv#WPE6739'], ['His research is supported by OpenAI, Anthropic, Schmidt Sciences and NVIDIA, among others', 'research support from OpenAI, Anthropic and NVIDIA']),
 ('Anthropic', 'Sen. John Thune', 'past', 'a lobbyist registered for Anthropic at Fierce Government Relations (2026) lists a past post as his senior policy adviser',
  ['lda-gov-anthropic-2026', 'lda-gov-anthropic-2026'], ['Sen. Thune: Sr Policy/Tax/Trade Policy Adv', '9389667a-a5ea-4572-bf77-a71207627990']),
]

# the same record for Nvidia: past posts with a drawn member that its lobbyists declare on its lobbying filings (drawn like the McCaul arc above)
ARCS_V6 = [
 ('Nvidia', 'Sen. Jim Banks', 'past', 'a lobbyist registered for Nvidia at Brownstein Hyatt Farber Schreck (2025) lists a past post as his legislative director', 'Sen. Jim Banks',
  ['lda-gov-nvidia-2025', 'lda-gov-nvidia-2025'], ['Legislative Director, Rep Jim Banks', '838b7711-7926-4a1d-87b4-cc6b85a39a47']),
 ('Nvidia', 'Sen. John Kennedy', 'past', 'a lobbyist registered for Nvidia at Brownstein Hyatt Farber Schreck (2025) lists a past post as his national security adviser', 'Sen. John Kennedy',
  ['lda-gov-nvidia-2025', 'lda-gov-nvidia-2025'], ['Sen John Kennedy, Nat Security Adv', 'ce2780f8-a08d-4881-883a-5c26b8db6ed8']),
]

# Nvidia's own support of institutions whose people are drawn, from each institution's own published list (pages saved Nov 15, 2026 after the
# web leads of slice F1): worded in the person's row beside the Open Philanthropy record for the same institution; no line is drawn
TIES_V7 = [
 ('Nvidia', 'Sam Bresnick', 'context', 'CSET\'s 2025 annual report lists Nvidia among its donors, in the $1,000 to $14,999 band',
  ['art-f1-cset-annual-report-2025'] * 3, ['Thank you to our donors', 'NVIDIA', '$1,000 – $14,999']),
 ('Nvidia', 'Michelle Nie', 'context', 'CNAS\'s supporters list for Oct 2024 to Sep 2025 names Nvidia in its $50,000 to $99,999 band, and Coefficient Giving (Open Philanthropy\'s new name) at $500,000 and above',
  ['art-f1-cnas-supporters'] * 5, ['Contributions from October 1, 2024 to September 30, 2025', 'NVIDIA Corporation', '$50,000 to $99,999', 'Coefficient Giving', '$500,000 and above']),
 ('Nvidia', 'Erich Grunewald', 'context', 'CNAS, which published that report, lists Nvidia among its supporters for Oct 2024 to Sep 2025, in its $50,000 to $99,999 band',
  ['art-f1-cnas-supporters'] * 3, ['Contributions from October 1, 2024 to September 30, 2025', 'NVIDIA Corporation', '$50,000 to $99,999']),
 ('Nvidia', 'Chris McGuire', 'context', 'the Council on Foreign Relations lists Nvidia among its corporate members, in its Bronze tier, as of Sep 3, 2026',
  ['art-f1-cfr-corporate-members'] * 3, ['NVIDIA', 'Bronze', 'as of September 3, 2026']),
 # ---- added after the third lane of the second audit (Nov 15, 2026); numbered after the rows above
 ('Open Philanthropy', 'Kyle Chan', 'context', 'Open Philanthropy made two awards to Brookings: $100,000 in 2015 for work on China and India and $200,000 in May 2026 for policy briefs on foreign assistance. No record here ties either to him. Brookings\'s donor list for the year to June 2026 names it (as Coefficient Giving) and does not name Nvidia',
  [PK + 'congress/research/grants.csv#GR024', PK + 'congress/research/grants.csv#GR024', PK + 'congress/research/grants.csv#GR025', PK + 'congress/research/grants.csv#GR025', 'art-f1-brookings-honor-roll-2026', 'art-f1-brookings-honor-roll-2026', 'art-f1-brookings-honor-roll-2026'],
  ['Work on China and India', '100000', 'Policy Briefs on U.S. Foreign Assistance', '200000', 'Coefficient Giving', 'July 1, 2025 – June 30, 2026', 'Microsoft Corporation']),
 ('Open Philanthropy', "Michael O'Hanlon", 'context', 'Open Philanthropy made two awards to Brookings: $100,000 in 2015 for work on China and India and $200,000 in May 2026 for policy briefs on foreign assistance. No record here ties either to him. Brookings\'s donor list for the year to June 2026 names it (as Coefficient Giving) and does not name Nvidia',
  [PK + 'congress/research/grants.csv#GR024', PK + 'congress/research/grants.csv#GR024', PK + 'congress/research/grants.csv#GR025', PK + 'congress/research/grants.csv#GR025', 'art-f1-brookings-honor-roll-2026', 'art-f1-brookings-honor-roll-2026', 'art-f1-brookings-honor-roll-2026'],
  ['Work on China and India', '100000', 'Policy Briefs on U.S. Foreign Assistance', '200000', 'Coefficient Giving', 'July 1, 2025 – June 30, 2026', 'Microsoft Corporation']),
 ('Open Philanthropy', 'Rob Wiblin', 'context', 'founder and host of the 80,000 Hours podcast. Open Philanthropy awarded 80,000 Hours $7.7M in general support in Sep 2025, and the group calls it "our largest donor". No record here ties an award to him',
  ['art-f1-80k-team', 'art-f1-80k-team', PK + 'lineage/research/flows_named.csv#FN210', PK + 'lineage/research/flows_named.csv#FN210', 'art-f1-80k-donors'],
  ['Rob Wiblin', 'Founder and Host of the 80,000 Hours Podcast', '7700000', 'General Support', 'Our largest donor is Coefficient Giving']),
 ('Nvidia', 'Patrick Moorhead', 'context', 'his firm lists Nvidia among the companies with which it "has had, or currently has, paid business relationships"; he wrote in Sep 2024 that "Nvidia is a client of my firm, as are many of its competitors and customers"',
  ['art-f1-moor-disclosures', 'art-f1-moor-disclosures', 'art-f1-moor-antitrust-2024', 'art-f1-moor-antitrust-2024'],
  ['The company has had, or currently has, paid business relationships with', 'NVIDIA', 'Nvidia is a client of my firm, as are many of its competitors and customers', 'September 27, 2024']),
 ('Nvidia', 'Daniel Newman', 'context', 'a 2026 market brief he signs as chief executive says it "was produced by The Futurum Group and commissioned by NVIDIA"',
  ['art-f1-futurum-brief-2026'] * 2, ['This market brief was produced by The Futurum Group and commissioned by NVIDIA', 'Daniel Newman']),
 ('Nvidia', 'Shay Boloor', 'context', 'Futurum Equities is the stock-research arm of The Futurum Group, which produced a 2026 brief "commissioned by NVIDIA"; the group says the arm is "strictly separated" from its advisory practice',
  ['art-f1-futurum-equities-own', 'art-f1-futurum-brief-2026', 'art-f1-futurum-equities-own'], ['Chief Market Strategist, Shay Boloor', 'This market brief was produced by The Futurum Group and commissioned by NVIDIA', 'Strictly separated from Futurum']),
 ('Nvidia', 'Yoo Eung-joon', 'context', 'the Korea JoongAng Daily describes him as "a former head of Nvidia Korea"', ['sw-koreajoongangdailycom-06'], ['a former head of Nvidia Korea']),
 # business with Nvidia that a saved page states for a public voice who is drawn
 ('Nvidia', 'Elon Musk', 'context', 'CNBC: "SpaceX is one of Nvidia\'s largest customers, and Nvidia invested in SpaceX via an equity investment in Musk\'s xAI"',
  ['sw-cnbccom-09'], ['largest customers, and Nvidia invested in SpaceX via an equity investment in Musk']),
 ('Nvidia', 'Clément Delangue', 'context', 'Nvidia agreed in 2026 to acquire his company for about $12.9 billion, CNBC reports; the deal has not closed',
  ['sw-cnbccom-09'] * 3, ['agreed to acquire Hugging Face', 'in a deal worth about $12.9 billion', 'expects the deal to close in the first half of 2027']),
 # a gift on record to a byline, from the investor who led Anthropic's first funding round (not from Anthropic or Open Philanthropy); identity rests on his
 # own post in the same newsletter, which says he served as a recommender for the fund that lists the gift
 ('Jaan Tallinn', 'Zvi Mowshowitz', 'context', 'the Survival and Flourishing Fund lists a $200,000 "unconditional gift" to him in 2024 from Jaan Tallinn, who led Anthropic\'s first funding round in 2021; he has written of serving as a recommender for that fund. No record here ties the gift to this piece',
  ['art-f1-sff-initiative-committee', 'art-f1-sff-initiative-committee', PK + 'congress/research/grants.csv#GR1940', PK + 'lineage/research/equity.csv#EQ010', 'art-f1-zvi-sff-2024', 'art-f1-zvi-sff-2024'],
  ['Zvi Mowshowitz', 'Unconditional gift', '200000', 'Series A lead (named participant)', 'be a recommender in the Survival and Flourishing Fund for the second time', 'AUTHOR: Zvi Mowshowitz']),
 ('CNAS', 'Jordan Schneider', 'context', 'CNAS lists the founder of ChinaTalk as an adjunct fellow of its technology programme; its supporters list for Oct 2024 to Sep 2025 names Coefficient Giving (Open Philanthropy) at $500,000 and above and Nvidia at $50,000 to $99,999',
  ['art-f1-cnas-schneider', 'art-f1-cnas-schneider', PK + 'lineage/research/tenures.csv#T3683', 'art-f1-cnas-supporters', 'art-f1-cnas-supporters', 'art-f1-cnas-supporters', 'art-f1-cnas-supporters'],
  ['Adjunct Fellow, Technology and National Security Program', 'founder of the ChinaTalk Podcast and Newsletter', 'Adjunct Fellow, Technology and National Security Program', 'Coefficient Giving', '$500,000 and above', 'NVIDIA Corporation', '$50,000 to $99,999']),
 # E02: the strength of Anthropic's earlier stance on chip sales to China, in its chief executive's words (background, not an act of these days)
 ('Anthropic', 'Anthropic', 'context', 'at Davos in January its chief executive likened selling advanced chips to China to "selling nuclear weapons to North Korea", TechCrunch recalls',
  ['sw-techcrunchcom-04', 'sw-techcrunchcom-04'], ['selling nuclear weapons to North Korea', 'had a lot to say about selling chips to China at Davos back in January']),
 # E04: an earlier fellowship his Tarbell page states
 ('Open Philanthropy', 'Jared Perlo', 'context', 'his Tarbell page says he was earlier "a Winter Fellow with the Centre for the Governance of AI (GovAI)", to which Open Philanthropy made three general-support awards in 2024 ($3.5M in all); the page gives no year for the fellowship',
  ['art-f1-tarbell-perlo', PK + 'lineage/research/flows_named.csv#FN181', PK + 'lineage/research/flows_named.csv#FN173', PK + 'lineage/research/flows_named.csv#FN174'],
  ['He was a Winter Fellow with the Centre for the Governance of AI (GovAI)', '2500000', '600000', '400000']),
]

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


# Originals found by the search of the actors' own channels (slice S6 of the gaps spec, Nov 14, 2026) and saved here: added to
# the sources of the act they are the original of. Keyed by row id, so no act above moves.
ORIGINALS = {
 'MA37': (['art-own-hfac-letter-1104'], ['We are writing to request that you appear before our committees for a joint, closed-door briefing']),
 'MA39': (['art-own-hfac-letter-1104'], ['We are writing to request that you appear before our committees for a joint, closed-door briefing']),
 'MA47': (['art-own-hfac-letter-1104'], ['We are writing to request that you appear before our committees for a joint, closed-door briefing']),
 'MA21': (['art-own-warren-coons-letter-1111'], ['preserve all records and materials specifically related to this reported intelligence operation']),
 'MA23': (['art-own-warren-coons-letter-1111'], ['preserve all records and materials specifically related to this reported intelligence operation']),
 'MA26': (['art-own-schumer-floor-1110'], ['supposed to protect America, not China, not his friends']),
 'MA31': (['art-own-wyden-neal-letter-1112'], ['the Administration did not appear to acknowledge this evident national security threat']),
 'MA20': (['art-own-warren-banks-1109'], ['makes these national security concerns even more urgent']),
 'MA27': (['art-own-warren-banks-1109'], ['makes these national security concerns even more urgent']),
 'MA58': (['sw-nvidianewsnvidiacom-03'], ['I was unfaithful to my wife']),
 'MA06': (['art-fc-itiger-wsj-1030', 'art-fc-itiger-wsj-1030'], ['have grown concerned that a data-center industry executive with close ties to Nvidia Chief Executive Jensen Huang is a Chinese intelligence source', 'according to people familiar with the matter']),
 'MA07': (['art-fc-tovima-wsj-1111-oust', 'art-fc-tovima-wsj-1111-oust', 'art-fc-tovima-wsj-1111-oust'], ['board is preparing to oust CEO Jensen Huang', 'The board is preparing to meet as soon as today to determine his future', 'PUBLISHED: 2026-11-11T23:26:36+00:00']),
 'MA08': (['man-ft-1107-01', 'man-ft-1107-01', 'man-ft-1107-01'], ['had a romantic relationship with a Chinese woman who was recruited to spy for China', 'according to people familiar with the matter', 'Published NOV 6 2026']),
 'MA60': (['sw-nvidianewsnvidiacom-01'], ['has no reason to believe that either national security or NVIDIA secrets were compromised']),
 'MA69': (['art-own-openai-compute-campus-policy-blueprint', 'art-own-openai-compute-campus-policy-blueprint'], ['OpenAI continues to support the strengthening of export controls', 'November 2026']),
 'MA61': (['sw-nvidianewsnvidiacom-04'], ['to conduct a thorough and independent investigation']),
 'MA59': (['sw-nvidianewsnvidiacom-02'], ['has resigned as President, Chief Executive Officer, and a member of the Board, effective immediately']),
 'MA63': (['sw-nvidianewsnvidiacom-02'], ['has agreed to serve as Interim Chief Executive Officer']),
 'MA82': (['sw-nvidianewsnvidiacom-02'], ['extraordinary foundation Jensen created']),
 'MA83': (['sw-nvidianewsnvidiacom-02'], ['period of extraordinary growth']),
 'MA71': (['art-own-fmprc-1109'], ['allegation is purely unsubstantiated and directed at smearing China']),
 'MA72': (['art-own-mha-1112', 'art-own-mha-1112', 'art-own-mha-1112'], ['there was insufficient evidence to establish that Huang had committed any offences', 'She was issued a stern warning and barred from re-entering the country', 'was not investigated for espionage']),
 'MA93': (['art-own-megaspeed-site'], ['Megaspeed takes its compliance obligations under U.S. export control laws extremely seriously']),
 'MA95': (['art-own-globaltimes-1109', 'art-own-globaltimes-1109'], ['there are often those firing shots from the shadows', 'Published: Nov 09, 2026']),
 # second own-channel search (Nov 15): the White House's own page for the exchange with the press (its video could not be read as text), and the podcast feed's page for the episode
 'MA123': (['art-own-whitehouse-1031-gaggle-halloween-party'], ['President Trump Gaggles with Press at a Halloween Party at Mar-a-Lago, Oct. 31, 2026']),
 'MA133': (['art-own-applepodcasts-chinatalk-emergency-pod'], ['November 9 EMERGENCY POD: Jensen and His Spy']),
}
# the Journal's own page of Oct 30, saved by hand on Nov 15 (two passages, on either side of a stock ticker that the PDF's text layer wove into the sentence)
ORIGINALS['MA06'] = (ORIGINALS['MA06'][0] + ['man-923fe8754943'] * 2, ORIGINALS['MA06'][1] + ['have grown concerned that a data-center industry executive with close ties to Nvidia', 'Chief Executive Jensen Huang is a Chinese intelligence source, according to people familiar with the matter'])



def rows():
    out = []
    for i, a in enumerate(acts(), 1):
        rid = f'MA{i:02d}'
        if rid in ORIGINALS:
            a = dict(a, src=list(a['src']) + ORIGINALS[rid][0], q=list(a['q']) + ORIGINALS[rid][1])
        out.append({'row_id': rid, **a})
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
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V5, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + len(TIES_V4) + 1):
        assert b in names and a in left and kind in ('role', 'money', 'past') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V6, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + len(TIES_V4) + len(TIES_V5) + 1):
        assert b in names and a in left and kind in ('role', 'money', 'past') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    for i, (a, b, kind, label, at, src, q) in enumerate(ARCS_V6, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + len(TIES_V4) + len(TIES_V5) + len(TIES_V6) + 1):
        assert a in names and b in names and at in (a, b) and kind in ('money', 'act', 'meet', 'past') and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'at': at, 'arc': True, 'src': src, 'q': q})
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V7, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + len(TIES_V4) + len(TIES_V5) + len(TIES_V6) + len(ARCS_V6) + 1):
        assert b in names and kind == 'context' and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    return out
