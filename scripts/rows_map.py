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
 ('papers', 'Three newspapers', 'who their confidential intelligence sources are. Singapore\'s ministry denied the Journal\'s Oct 30 account in a statement timed the same day.', 'ST07', ''),
 ('bylines', 'Bylines with a tie on record', f'whether a tie shaped any of the {NUMBER[N_BYLINES_DRAWN]} pieces. All {N_BYLINE_NAMES} names in the bylines of the saved pages were looked up; {NUMBER[N_BYLINES_DRAWN]} have a tie on record (three of them to the Tarbell Center). A reporter or columnist without one is not drawn, however often quoted.', '', ''),
 ('analysts', 'Analysts quoted or posting', f'who, if anyone, prompted the posts or quotes. Drawn: {N_ANALYSTS_DRAWN} of the {N_ANALYSTS} analysts, experts and research groups quoted: those with a tie on record to Anthropic, Open Philanthropy or Nvidia, their own or through the organisation where they hold a post.', 'ST04', ''),
 ('senate', 'Senate', 'any contact between a senator and the reporters or their sources.', 'ST02', 'Democrats'),
 ('house', 'House', 'whether anyone outside Congress had a hand in the Nov 4 letter.', 'ST01', ''),
 ('admin', 'The administration', 'who gave the intelligence to reporters. The reports cite "people briefed on intelligence surveillance."', 'ST06', ''),
 ('nvidia', 'Nvidia', 'what the board\'s inquiry found; the saved accounts do not give its findings.', 'ST08', ''),
 ('shares', 'Share prices', 'any role for a rival chip maker: no document here connects one to the reports.', 'ST05', ''),
 ('anthropic', 'Anthropic', 'any statement by Anthropic on Huang beyond "declined to comment" (its newsroom and share-sale site, searched once on Nov 14, showed none; its share-sale filing and three more SEC documents could not be saved), or any instruction, payment or message tied to the coverage.', 'ST03', ''),
 ('labs', 'Another AI company', 'any part for OpenAI in the reports.', '', ''),
 ('voices', 'Other public voices', 'any part for them in the reports. Drawn: people outside politics and research who are quoted in three or more of the articles counted. Business with Nvidia is worded where a saved page states it; it was not looked up otherwise.', '', ''),
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
 # an expert quoted in the pages saved since the first reading, with a tie of his own on record (look-up of Nov 15, lane analysts_nv8_e, backed by the whole-name search)
 ('hodges', 'analysts', 'Joshua Hodges', 'U.S.-China Economic and Security Review Commission', None),
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
 # three members who reach three counted articles once the pages saved since the first census are counted, each article once (slice S8, Nov 15)
 ('scott', 'senate', 'Sen. Tim Scott', 'R-S.C., chairs Banking', ''),
 ('ricketts', 'senate', 'Sen. Pete Ricketts', 'R-Neb.', 'PETE RICKETTS FOR SENATE'),
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
 ('neal', 'house', 'Rep. Richard Neal', 'D-Mass., top Democrat on Ways and Means', ''),
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
 ('kress', 'nvidia', 'Colette Kress', 'chief financial officer; interim chief, announced Nov 12', None),
 ('jones', 'nvidia', 'Harvey Jones', 'director; board chair, appointed Nov 11 and announced Nov 12', None),
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
 ('rao', 'voices', 'a public voice no longer drawn', 'founder of a chip start-up', None),
 # quoted in three counted articles once the pages saved since the first reading are counted (slice S8)
 ('conway', 'voices', 'Ron Conway', 'venture capitalist', None),
 ('singapore', 'abroad', 'Singapore Ministry of Home Affairs', '', None),
 ('china', 'abroad', 'China\'s Foreign Ministry', '', None),
 ('embassy', 'abroad', 'Chinese Embassy in Washington', '', None),
 ('megaspeed', 'abroad', 'Megaspeed', 'the Singapore firm in the reports', None),
 ('taiwan', 'abroad', 'Taiwan\'s government', '', None),
 ('globaltimes', 'abroad', 'Global Times', 'newspaper in China', None),
]

# An actor who is no longer drawn. The entry stays in ACTORS_ALL and its acts keep their place in ACTS (a row id is never reused);
# the figure, the gauge and the counts read ACTORS and skip those acts. Slice S8, Nov 15, 2026 (Kevin: "count them for everyone. don't
# use duplicates. deduplicate."): the three saved pages that quote him are three copies of one article.
# Sen. Scott was withdrawn on Nov 15, 2026 (release db0261e) because the three saved articles naming him were two reports, and is
# drawn again since Nov 16: the aggregators' own list holds two more pieces of Nov 12 whose headlines name him for the same letters, which
# were not among the saved pages; one of them (the Washington Examiner's) could be saved and is a third separate report.
WITHDRAWN = {'rao': 'quoted in one article, of which three copies had been saved and counted as three pages; under the three-article line once each article is counted once'}
# How a withdrawn row of a person who holds no public office is published: by role, and without the passage that names him (the eighth
# reading, Nov 16, 2026: keeping a row id does not require publishing the name). The full row stays here.
WITHDRAWN_PUBLIC = {'rao': ('a public voice no longer drawn (the founder of a chip start-up)',
                            {'a public voice no longer drawn': 'a public voice no longer drawn', 'a chip start-up': 'a chip start-up',
                             '[address withheld: it names a person no longer drawn]': '[address withheld: it names a person no longer drawn]', '[address withheld: it names a person no longer drawn]': '[address withheld: it names a person no longer drawn]'})}
ACTORS_ALL = ACTORS
ACTORS = [a for a in ACTORS_ALL if a[0] not in WITHDRAWN]

# An act either points at a row of rows_events (its date, source and passage are taken from there) or carries its own.
ACTS = [
 # actor, 'EVnn' or date, what, [src], [q]
 ('nyt', 'EV01', 'U.S. intelligence surveilled Alice Huang; its first report says that "Roughly a year ago, Mr. Trump was briefed about the intelligence findings" and "chose not to do anything with the information", and that the Commerce Department\'s investigation of Megaspeed "was handed over this year to the Justice Department"',
  ['man-nyt-1029-01', 'man-nyt-1029-01', 'man-nyt-1029-01'],
  ['Roughly a year ago, Mr. Trump was briefed about the intelligence findings', 'chose not to do anything with the information', 'The Commerce Department investigation into Megaspeed was handed over this year to the Justice Department, administration officials said.']),
 ('nyt', 'EV08', 'A memo says China\'s spy agency recruited her'),
 ('nyt', 'EV12', 'A Chinese firm was cleared to assemble Nvidia chips'),
 ('nyt', 'EV13', 'Rubio oversaw the memo'),
 ('nyt', 'EV27', 'A second relationship, with a subordinate'),
 ('wsj', 'EV03', 'Reports that officials in the U.S., Singapore and Taiwan "have grown concerned" that an executive close to Huang "is a Chinese intelligence source", citing people familiar with the matter (Singapore denied the account in a statement timed the same day)'),
 ('wsj', '2026-11-11', 'Reports that the board "is preparing to oust" Huang and "to meet as soon as today to determine his future", citing people familiar with the matter',
  ['sw-dailykoscom-04'], ['The Wall Street Journal reports that Nvidia\'s board of directors plans to oust CEO Jensen Huang']),
 ('ft', 'EV09', 'Reports that the U.S. government "believes" Huang "had a romantic relationship with a Chinese woman who was recruited to spy for China\'s main intelligence agency", citing people familiar with the matter. Its reporter\'s post of the report: 3.4M views'),
 ('kubinec', '2026-11-10', 'Publishes "Jensen Huang\'s Affair Could Reshape the Chip War"',
  ['sw-thedispatchcom-01'], ['Jensen Huang\'s Affair Could Reshape the Chip War']),
 ('perlo', '2026-11-12', 'Shares the byline on "Jensen Huang agrees to brief Congress"',
  ['sw-nbcnewscom-08', 'sw-nbcnewscom-08'], ['AUTHOR: Jared Perlo', 'Jensen Huang agrees to brief Congress on interactions with alleged spy']),
 ('bresnick', '2026-11-09', 'Tells CNBC what Democrats are likely to probe',
  ['sw-cnbccom-11'], ['said Sam Bresnick, a research fellow at the Center for Security and Emerging Technology']),
 # dated on Nov 15, 2026: the summary page prints no date, and the episode's record inside the saved page carries its release time
 # (a Unix time: Nov 10, 17:00 UTC). The row keeps its place and id (MA12).
 ('fedasiuk', '2026-11-10', 'A podcast episode titled "Jensen Huang Must Resign" is released. The day is the release time in the data of a summary page that prints no date; the recording was not heard. The page\'s summary has him say that whether sensitive information reached Chinese intelligence is unknown ("we really don\'t know anything about" the nature of the relationship), and of the motive he alleges: "I\'m reading between the lines"',
  ['biggo-fedasiuk', 'biggo-fedasiuk', 'biggo-fedasiuk', 'biggo-fedasiuk'],
  ['Ryan Fedasiuk: Jensen Huang Must Resign', 'published_at: 1794330018', "we really don't know anything about", "I'm reading between the lines"]),
 ('fedasiuk', '2026-11-12', 'Tells Scientific American Huang is in "almost every aspect of the company"; writes at his institute\'s site that it is "a sad day for Nvidia", that "there is reason to be optimistic" about the company and that stepping down "was dignified, and ultimately the right decision". Also to Scientific American: "The longer this drags on", "the more distracted the company will grow"; and "I don\'t think it\'s right to conceive of this as \'if Jensen goes, then there goes a huge blow to the company\'s technical capability\'". His piece ends: "gratitude does not excuse Huang\'s personal misconduct", nor should admiration for him or blame over the scandal "obscure deeper problems in his company\'s conduct"',
  ['sw-scientificamericancom-01', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'sw-scientificamericancom-01', 'sw-scientificamericancom-01', 'sw-scientificamericancom-01', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang', 'art-own-thefai-1112-nvidia-is-bigger-than-jensen-huang'],
  ['says Ryan Fedasiuk, senior fellow at the Foundation for American Innovation', 'decision to step down was dignified, and ultimately the right decision', 'It is a sad day for Nvidia', 'there is reason to be optimistic about the company', 'The longer this drags on', 'the more distracted the company will grow', "I don't think it's right to conceive of this as 'if Jensen goes, then there goes a huge blow to the company's technical capability,'", "But gratitude does not excuse Huang's personal misconduct", "obscure deeper problems in his company's conduct"]),
 ('mcguire', 'EV10', 'Recap post asks why Commerce took no action. 9.4M views'),
 ('mcguire', 'EV17', 'Post: "Jensen\'s behavior is only half the story"; "Obviously Nvidia needs to take significant steps in its operations, security, and policy advocacy to ensure it takes national security concerns more seriously"',
  ['x-mcguire-nov8'],
  ['Obviously Nvidia needs to take significant steps in its operations, security, and policy advocacy to ensure it takes national security concerns more seriously']),
 ('mcguire', '2026-11-10', 'Tells the FT it is "mind-boggling" that Commerce "did nothing"; guest on the ChinaTalk podcast',
  ['bulwark-chipghazi', 'bulwark-chipghazi', 'sw-chinatalkmedia-01'],
  ['The FT quotes Chris McGuire, a former senior U.S. government export controls official', 'the Financial Times reported yesterday', 'Emergency pod with Chris McGuire']),
 ('grunewald', '2026-11-10', 'Tells Al Jazeera he thinks recent events likely "add momentum" to chip bills',
  ['sw-aljazeeracom-06'], ['add momentum to bills already being discussed in Congress, like the Chip Security Act']),
 ('stapp', '2026-11-10', '"Expect it to keep getting worse"',
  ['sw-thedailyupsidecom-01', 'sw-thedailyupsidecom-01'], ['said Alec Stapp, the co-CEO of the Institute for Progress', 'Expect it to keep getting worse']),
 ('warren', '2026-10-29', 'Statement: "NVIDIA\'s Jensen Huang and NVIDIA\'s board owe Congress answers"; "And we need to pass bipartisan legislation we have ready to stop advanced American technology from going to China"',
  ['art-own-warren-statement-1029', 'sw-aljazeeracom-01', 'art-own-warren-statement-1029'],
  ['board owe Congress answers', "NVIDIA's Jensen Huang and NVIDIA's board owe Congress answers", 'And we need to pass bipartisan legislation we have ready to stop advanced American technology from going to China']),
 ('warren', '2026-11-09', 'Statement with Banks: Huang\'s confirmation "makes these national security concerns even more urgent"; they ask for answers and tighter export limits. The statement opens by recalling that "In March, bipartisan members of Congress urged the Department of Commerce to suspend or reconsider NVIDIA\'s export licenses to China and conduct a full national security review"',
  ['sw-fortunecom-08', 'sw-nbcnewscom-02', 'art-own-warren-banks-1109'],
  ['issued a joint statement calling for answers from Nvidia and tighter restrictions on advanced AI chip exports to China', 'makes these national security concerns even more urgent and raises important questions NVIDIA must answer', "In March, bipartisan members of Congress urged the Department of Commerce to suspend or reconsider NVIDIA's export licenses to China and conduct a full national security review"]),
 ('warren', '2026-11-11', 'Letter with Coons asks the administration to "preserve all records" and to confirm in writing by Nov 17 that preservation directives have been issued',
  ['sw-nbcnewscom-09', 'sw-financeyahoocom-23', 'art-own-warren-coons-letter-1111'],
  ['announced they had written to Commerce Secretary Howard Lutnick with a request to preserve records on the subject', 'have formally asked the Trump administration to "preserve all records"', 'confirm in writing by November 17 that preservation directives have been issued across your respective offices']),
 ('coons', 'EV11', 'Posts of "the insane relationship between the Trump Administration, Chinese spies, and AI billionaires": "Congress will investigate and get answers"'),
 ('coons', '2026-11-11', 'Letter with Warren asks the administration to "preserve all records", to confirm in writing by Nov 17 that preservation directives have been issued, and to brief members of Congress on the risks the operation may have posed',
  ['sw-nbcnewscom-09', 'sw-financeyahoocom-23', 'art-own-warren-coons-letter-1111', 'art-own-warren-coons-letter-1111'],
  ['Sens. Elizabeth Warren, D-Mass., and Chris Coons, D-Del., announced they had written to Commerce Secretary Howard Lutnick', 'have formally asked the Trump administration to "preserve all records"', 'confirm in writing by November 17 that preservation directives have been issued across your respective offices', 'brief Members of Congress regarding the risks this operation may have posed to our national security']),
 ('cramer', 'EV21', '"I just think he\'s got to go"'),
 ('cramer', 'EV28', '"He should resign"'),
 ('schumer', 'EV22', 'Floor speech: pass three chip-export bills; of the president: "He\'s supposed to protect America, not China, not his friends"',
  ['bulwark-chipghazi'], ["He's supposed to protect America, not China, not his friends"]),
 ('banks', '2026-11-09', 'Statement with Warren: Huang\'s confirmation "makes these national security concerns even more urgent"; they ask for answers and tighter export limits. The statement opens by recalling that "In March, bipartisan members of Congress urged the Department of Commerce to suspend or reconsider NVIDIA\'s export licenses to China and conduct a full national security review"',
  ['sw-fortunecom-08', 'sw-nbcnewscom-02', 'art-own-warren-banks-1109'],
  ['Sen. Jim Banks (R., Ind.) issued a joint statement', 'makes these national security concerns even more urgent and raises important questions NVIDIA must answer', "In March, bipartisan members of Congress urged the Department of Commerce to suspend or reconsider NVIDIA's export licenses to China and conduct a full national security review"]),
 ('blumenthal', '2026-11-09', '"We need a Senate investigation"', ['sw-semaforcom-04'], ['we need a Senate investigation']),
 ('warner', '2026-11-09', '"I want to get more facts before I weigh in"',
  ['sw-semaforcom-04', 'sw-semaforcom-04', 'sw-semaforcom-04'],
  ['I want to get more facts before I weigh in', "We need to hear from the FBI, and they weren't there today", 'the intelligence briefing they received in the Capitol on Monday']),
 ('wyden', '2026-11-09', '"We don\'t know where it went"',
  ['sw-semaforcom-04', 'sw-semaforcom-04'],
  ["We don't know where it went", 'the intelligence briefing they received in the Capitol on Monday']),
 ('wyden', '2026-11-12', 'Letter with Rep. Neal opens a probe of chip-export approvals; it says the administration "did not appear to acknowledge this evident national security threat"; it asks the department to preserve all records of its tariff investigation of semiconductors, of Nvidia\'s export licence applications and of its communications with and about Nvidia and Huang',
  ['sw-cnbccom-09', 'sw-cnbccom-09', 'art-own-wyden-neal-letter-1112', 'art-own-wyden-neal-letter-1112'],
  ['Their letter to Commerce Secretary Howard Lutnick announcing the probe was sent by Sen. Ron Wyden', 'did not appear to acknowledge this evident national security threat', 'we write to request that you preserve all records related to', "the Department's consideration and approval of export license applications submitted by Nvidia"]),
 ('cornyn', '2026-11-08', 'Calls a Times report of Nov 7 "outrageous" in a post that CNBC reports on Nov 8',
  ['cnbc-1108-bipartisan'], ['Cornyn called the report "outrageous" in his post on X']),
 ('cornyn', '2026-11-08', 'Posts: "Congressional oversight investigation needed"',
  ['sw-financeyahoocom-11'], ['John Cornyn posted "Congressional oversight investigation needed."']),
 ('kennedy', '2026-11-10', '"I lost my breath"; wants investigations. The Washington Sun gives his words of that Tuesday as: "They took my breath away", "And they need to be investigated by the Justice [Department], FBI, CIA, Congress"',
  ['sw-washingtonexaminercom-05', 'sw-washingtonsuncom-02', 'sw-washingtonsuncom-02', 'sw-washingtonsuncom-02'],
  ['"I lost my breath," Sen. John Kennedy (R-LA) told the Washington Examiner', 'They took my breath away', 'And they need to be investigated by the Justice [Department], FBI, CIA, Congress', 'told The Washington Sun on Tuesday']),
 ('kennedy', '2026-11-11', 'Tells Politico on Wednesday, as the New Republic relays it: "Secretary Lutnick needs to answer that in front of God and country. If I were he, I\'d call a press conference this afternoon and explain what happened and why he agreed to sell them chips, and I would stop doing it". Implicator has him say that Wednesday: "We need to know why the Commerce Department was allowing Nvidia to sell advanced chips to the company of the woman he was having an affair with"',
  ['tnr-lutnick', 'tnr-lutnick', 'sw-implicatorai-06', 'sw-implicatorai-06'],
  ['Secretary Lutnick needs to answer that in front of God and country', "If I were he, I'd call a press conference this afternoon and explain what happened and why he agreed to sell them chips, and I would stop doing it", 'We need to know why the Commerce Department was allowing Nvidia to sell advanced chips to the company of the woman he was having an affair with,', 'Sen. John Kennedy said Wednesday']),
 ('thune', '2026-11-12', 'Expects "some follow-up" by Congress, in CNBC\'s report of that day',
  ['sw-cnbccom-09', 'sw-cnbccom-09'],
  ['I would expect there would be some follow-up, yeah', "said he expects Congress to conduct oversight of the Jensen Huang affair even after the embattled tech CEO's resignation"]),
 ('mast', 'EV06', 'Letter dated Nov 4, released Nov 5, asks Huang to brief three committees on his interactions with Alice Huang, "a publicly reported People\'s Republic of China (PRC) intelligence asset", and on Nvidia\'s security protocols: "Recent reports raise significant national security concerns"; it asks him to appear on Nov 18 and to accept that date or propose another session day by Nov 11',
  ['house-hfac-letter-pr', 'house-hfac-letter-pr', 'art-own-hfac-letter-1104', 'art-own-hfac-letter-1104'],
  ['Recent reports raise significant national security concerns', "Huang's interactions with Megaspeed executive Alice Huang, a publicly reported People's Republic of China (PRC) intelligence asset", 'We formally request that you appear in room 2172 of the Rayburn House Office Building on November 18, 2026, to brief our committees', 'by November 11, 2026']),
 ('mast', 'EV29', 'Says "yes," a subpoena is being considered; TechCrunch, in a brief on a Bloomberg report that cites two House Republicans: he said that Wednesday that his committee "is preparing a subpoena for Huang to send if he doesn\'t respond". WinBuzzer: his spokesperson said on Nov 11 that he was open to issuing a subpoena if Huang did not respond',
  ['sw-techcrunchcom-90a2e604', 'sw-techcrunchcom-90a2e604', 'sw-winbuzzercom-b0d76647'],
  ['Mast, who chairs the House Foreign Affairs Committee, on Wednesday said his committee is preparing a subpoena for Huang to send if he doesn’t respond.', 'citing two House Republicans', "On November 11, Mast's spokesperson said he was open to issuing a subpoena if Huang did not respond"]),
 ('crawford', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5; it asks him to appear on Nov 18 and to accept that date or propose another session day by Nov 11',
  ['art-own-hfac-letter-1104', 'art-own-hfac-letter-1104'],
  ['We formally request that you appear in room 2172 of the Rayburn House Office Building on November 18, 2026, to brief our committees', 'by November 11, 2026']),
 ('meeks', '2026-11-10', 'Says, as MS NOW reports it, he would subpoena a Commerce appointee',
  ['sw-msnow-01'], ['said he would subpoena Jeff Kessler']),
 ('himes', '2026-11-10', '"We\'ve asked Huang to appear"',
  ['sw-msnow-01'], ['"We\'ve asked Huang to appear," Rep. Jim Himes']),
 ('himes', '2026-11-10', 'Tells NPR it is "not clear" what Alice Huang\'s relationship with the Chinese government was: "That needs to be understood". Asked whether he knew before the reports: "the Congress received no briefing on this until just yesterday", and "we have not been kept abreast of this issue"; he says he knows how long the administration knew, and that "press reports that this was sort of surfaced in the spring are more or less correct"; "why the hell didn\'t we get briefed on this earlier?"; of Nvidia\'s statement: "it may be true that they don\'t have evidence, but that\'s not in any way exculpatory prior to the completion of an investigation"; and: "it\'s the categories of information and influence that these investigations need to be looking at"',
  ['sw-nbcnewscom-09', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110', 'art-own-waer-himes-1110'],
  ["told NPR that Alice Huang's role still needed to be clarified", 'That needs to be understood', 'PUBLISHED: 2026-11-10', 'exactly what the relationship might have been between Alice Huang and the Chinese government', 'the Congress received no briefing on this until just yesterday', 'we have not been kept abreast of this issue', 'press reports that this was sort of surfaced in the spring are more or less correct', "why the hell didn't we get briefed on this earlier?", "it may be true that they don't have evidence, but that's not in any way exculpatory prior to the completion of an investigation", "it's the categories of information and influence that these investigations need to be looking at"]),
 ('huizenga', '2026-11-12', 'Says it would be "helpful" if the Commerce secretary testified in public; of the department: "They have not been as cooperative as they should be"',
  ['sw-cnbccom-09', 'sw-cnbccom-09'], ['said it would be "helpful" if Commerce Department Secretary Howard Lutnick testified to Congress in public', 'They have not been as cooperative as they should be']),
 ('johnson', '2026-11-09', 'Says "they\'re still gathering information"', ['sw-semaforcom-04'], ['House Speaker Mike Johnson told Semafor']),
 ('johnson', '2026-11-12', 'Calls the resignation a "big and shocking development" and the choice of successor "critically important"; "So I\'m reserving personal judgment on this, but it sounds like for him as an individual, he did the right thing for the company and for the country"; if questioning Huang is "the will of the body, that\'s what will happen". He told reporters that day, as Unite.AI reports it, that he supports limiting semiconductor exports to China and sees a developing consensus in Congress behind that',
  ['globe-1112-resigns', 'cnn-1111-live', 'cnn-1111-live', 'cnn-1111-live', 'cnn-1111-live', 'cnn-1111-live', 'sw-uniteai-bf709b60'],
  ['critically important for right successor to be chosen to replace Huang', 'big and shocking development', 'Johnson said he had been informed of the resignation just minutes earlier while walking to the floor', "So I'm reserving personal judgment on this, but it sounds like for him as an individual, he did the right thing for the company and for the country", 'seems to me to be a lot of facts yet to be determined', "the will of the body, that's what will happen", 'House Speaker Mike Johnson separately told reporters on November 12 that he supports limiting semiconductor exports to China and sees a developing congressional consensus behind that position. Johnson said recent developments could change some lawmakers’ minds.']),
 ('mccaul', '2026-11-08', 'A post, as the Times quotes it on Nov 8: the U.S. "should immediately pause the shipment of advanced AI chips to China until we can get to the bottom of this incident"',
  ['sw-hotaircom-02'], ['The U.S. should immediately pause the shipment of advanced AI chips to China']),
 ('moolenaar', 'EV06', 'Co-signed the letter dated Nov 4, released Nov 5; it asks him to appear on Nov 18 and to accept that date or propose another session day by Nov 11',
  ['art-own-hfac-letter-1104', 'art-own-hfac-letter-1104'],
  ['We formally request that you appear in room 2172 of the Rayburn House Office Building on November 18, 2026, to brief our committees', 'by November 11, 2026']),
 ('moolenaar', 'EV23', 'Says Congress must "get to the bottom" of it'),
 ('moolenaar', 'EV29', 'Says Huang has not replied: "We are going to continue to pursue this"; on Fox Business that Wednesday, as TechCrunch gives it in a brief on a Bloomberg report about the subpoena: Huang has until the end of the day to respond, and if he does not agree to the briefing he will likely be subpoenaed',
  ['cnbc-1111-congress-resign', 'cnbc-1111-congress-resign', 'sw-techcrunchcom-90a2e604', 'sw-techcrunchcom-90a2e604'],
  ['Mast and Moolenaar told reporters on Wednesday afternoon that they had not yet heard from Huang', 'We are going to continue to pursue this', 'House China committee Chairman Moolenaar said Wednesday on Fox Business that Huang has until the end of the day to respond to the request. If he doesn’t agree to the briefing, he’ll likely be subpoenaed, said Moolenaar.', 'citing two House Republicans']),
 ('jeffries', '2026-11-09', '"We\'re going to need a full briefing"',
  ['cnbc-1110-schumer'], ['we\'re going to need a full briefing specifically as it relates to the Nvidia issue']),
 ('magaziner', '2026-11-08', 'Calls for Huang and the Commerce secretary to testify',
  ['cnbc-1108-bipartisan'], ['called on Commerce Secretary Howard Lutnick to testify before Congress along with Huang']),
 ('subramanyam', 'EV28', '"Jensen Huang should resign"; he tells CNBC: "There\'s two parts to this investigation that [need] to happen somewhere immediately", "what was going on with Nvidia and China" and "why the administration did nothing about it even though they appeared to have known"; and: "If Nvidia finds out that he knew about what was going on and does nothing about it, then Nvidia is making a choice"',
  ['cnbc-1111-congress-resign', 'cnbc-1111-congress-resign', 'cnbc-1111-congress-resign', 'cnbc-1111-congress-resign'],
  ["There's two parts to this investigation that [need] to happen somewhere immediately", 'what was going on with Nvidia and China', 'why the administration did nothing about it even though they appeared to have known', 'If Nvidia finds out that he knew about what was going on and does nothing about it, then Nvidia is making a choice']),
 ('bacon', 'EV28', 'Asked if Huang should resign: "From the little I know, yes"'),
 ('trump', 'EV16', 'Says Huang should remain chief executive: "I think he\'s an honorable guy"; asked if he wished he had acted on the intelligence: "no, I don\'t think so"',
  ['nbc-1108-investigation'], ['Asked by reporters if Trump wished that he had acted on intelligence about Alice Huang']),
 ('trump', 'EV19', 'Says Huang told him he "had absolutely no idea that the person in question was a spy"; says "the FBI is looking into it in terms of something else" and does not say what; "I hope there\'s no problem", and "If there is a problem, we\'ll let you know about it" (NBC)',
  ['abc-subpoena', 'nbc-exprosecutor', 'nbc-exprosecutor'],
  ['He said he had absolutely no idea that the person in question was a spy', "I hope there's no problem", "If there is a problem, we'll let you know about it"]),
 ('nvidia', 'EV02', 'Says Huang\'s interactions with Megaspeed\'s officials are not unusual and that the chip-diversion allegations about it were "debunked last year"',
  ['cnbc-1029-nvidia-responds'], ['interactions with its officials are not unusual, because he speaks with thousands of customers every year']),
 ('nvidia', 'EV07', 'Says customer meetings are "part of a CEO\'s job" and that customers get "zero information relevant to national security"; a spokesman tells the Times Huang "has an outstanding security team that accompanies him where needed"; the spokesman declines to comment on whether Huang will appear before the committees',
  ['cnbc-1105-asked-to-brief', 'man-nyt-1105-01', 'cnbc-1108-bipartisan', 'man-nyt-1105-01'],
  ['zero information relevant to national security', 'Our chief executive has an outstanding security team that accompanies', 'Our chief executive has an outstanding security team that accompanies him where needed', 'declined to comment on whether Mr. Huang would appear']),
 ('huang', 'EV14', 'Memo to staff: "I owe my family and all of you an apology. I was unfaithful to my wife"; on the board\'s inquiry: "I support the investigation and will cooperate fully"; "I am fully committed to NVIDIA and will work to earn back your confidence"',
  ['npr-1108-investigation', 'sw-nvidianewsnvidiacom-03'],
  ['I support the investigation and will cooperate fully', 'I am fully committed to NVIDIA and will work to earn back your confidence']),
 ('huang', 'EV31', 'Resigns after 33 years as chief executive (announced Nov 12; the company\'s filing dates the board\'s acceptance of the resignation to Nov 11)',
  ['man-cd8c08517fc7'] * 3, ['accepted the resignation of Jen-Hsun Huang', 'Date of Report (Date of earliest event reported): November 11, 2026', 'Press Release, dated November 12, 2026']),
 ('board', 'EV15', 'Opens an independent investigation; says it has "no reason to believe" secrets were compromised and "has confidence in Jensen and his leadership team"; its inquiry "will examine all available information", and it "will provide further updates as appropriate"',
  ['sw-nvidianewsnvidiacom-01', 'man-nyt-1108-01', 'sw-runtimewirecom-02'],
  ['The Board has confidence in Jensen and his leadership team', 'the board’s inquiry will examine all available information.', 'will provide further updates as appropriate']),
 ('board', 'EV24', 'Hires outside counsel "to conduct a thorough and independent investigation"', ['nbc-exprosecutor'], ['to conduct a thorough and independent investigation as was announced on Sunday']),
 ('board', 'EV30', 'Meets to discuss removing Huang. CNBC, from a person familiar with the matter: it decided that night to oust him and made the decision official the next morning',
  ['sw-cnbccom-09'],
  ["Nvidia's board decided last night to oust longtime CEO Jensen Huang, a person familiar with the matter told CNBC.\nThe person, who spoke on the condition of anonymity, said sentiment quickly turned after the report of a second alleged affair.\nThe team worked late into the night on its communications strategy and made an official decision this morning, before naming Kress as interim CEO, the person added."]),
 ('board', 'EV31', 'Names Kress interim chief, Jones chair; begins a search for a permanent chief (announced Nov 12; the company\'s filing dates Jones\'s appointment to Nov 11 and gives no day for Kress\'s). The release says Kress keeps her duties as chief financial officer and that results will be reported on Nov 17 "as previously scheduled"; Jones is to lead the search',
  ['sw-tomshardwarecom-06', 'man-cd8c08517fc7', 'man-cd8c08517fc7', 'man-cd8c08517fc7', 'sw-gizmodocom-10', 'sw-qzcom-19', 'sw-nvidianewsnvidiacom-02'],
  ['The Board is initiating a search for a permanent Chief Executive Officer and will consider internal and external candidates', 'On November 11, 2026, the Board appointed Harvey C. Jones, age 73, as Chair of the Board', 'to serve as interim Chief Executive', 'Press Release, dated November 12, 2026', 'Colette Kress, Nvidia’s chief financial officer since 2013, will serve as interim CEO while retaining her CFO duties.', "Harvey C. Jones, who previously led Synopsys $SNPS , is Nvidia 's first board chair and will direct the search for a permanent CEO, which will consider candidates from inside and outside the company, Nvidia said.", 'NVIDIA will report its third-quarter fiscal 2027 financial results on Tuesday, November 17, at approximately 1:20 p.m. PT, as previously scheduled, followed by its earnings call at 2 p.m. PT.']),
 ('nvda', 'EV20', 'Falls more than 4%'),
 ('nvda', 'EV25', 'Falls 5.47%'),
 ('nvda', 'EV32', 'Slides about 10% in early trading, in Al Jazeera\'s account; 13% at the open, in the FT\'s'),
 ('rivals', 'EV20', 'AMD up 13%, Broadcom up 10%'),
 ('anthropic', 'EV26', 'Sets its IPO price range; seven companies agree to buy $26B of its stock'),
 ('openai', '2026-11-04', 'Quoted by The Information, as the Daily Caller relays it: it "continues to support the strengthening of export controls". The sentence is in its policy paper dated November 2026, which gives no day',
  ['sw-dailycallercom-07'], ['OpenAI continues to support the strengthening of export controls']),
 ('singapore', 'EV04', 'Denies the Journal\'s account of Alice Huang: "no such investigations"; its police say the Megaspeed inquiry continues, that they are "unable to comment further at this juncture", and: "While we do not enforce unilateral export controls imposed by other countries, we act firmly against companies and individuals who violate our laws and are engaged in fraudulent and dishonest practices"; the reply adds that Singapore "has charged four individuals and four companies in Court between Feb 2025 and Jul 2026 for committing fraud on suppliers of servers", and says Singapore "does not condone businesses deliberately using their association with Singapore to circumvent or violate other countries\' export controls" and expects companies there "to take into account other countries\' regulations, including export controls". The statement is timed Oct 30, 11:13 PM in Singapore; the ministry\'s newsroom page dates it Oct 31',
  ['mha-clarification-a', 'mha-clarification-a', 'art-fc-spf-1030', 'art-fc-spf-1030', 'mha-clarification-a', 'mha-clarification-a'],
  ['We are unable to comment further at this juncture', 'While we do not enforce unilateral export controls imposed by other countries, we act firmly against companies and individuals who violate our laws', 'we act firmly against companies and individuals who violate our laws and are engaged in fraudulent and dishonest practices', 'Singapore has charged four individuals and four companies in Court between Feb 2025 and Jul 2026 for committing fraud on suppliers of servers', "Singapore does not condone businesses deliberately using their association with Singapore to circumvent or violate other countries' export controls", "All companies operating in Singapore are expected to take into account other countries' regulations, including export controls"]),
 ('china', 'EV18', 'Calls the spy allegation "unsubstantiated"; asked that day how China would respond to tighter curbs on chips: "China\'s position on the U.S. export of chips to China is consistent. For anything specific, I\'d refer you to competent authorities"',
  ['art-own-fmprc-1109', 'art-own-fmprc-1109'],
  ['How will China respond if the U.S. pushes for tighter tech curbs, including on chips', "China's position on the U.S. export of chips to China is consistent"]),
 # added after audit1b (its finding on the Singapore denial); kept last so earlier row ids do not move
 ('singapore', '2026-11-12', 'Its statement: police interviewed her and held her passport in 2025; in Feb 2026 found "insufficient evidence" of offences over the declarations under investigation; a "stern warning" for inaccurate information; barred from re-entering; no espionage investigation. Requests to U.S. authorities over Supermicro brought "limited information or assistance"; its investigation of the company and six other individuals continues (its statement and the Journal\'s live report). The statement opens: Singapore "does not enforce unilateral export controls imposed by other countries", expects companies there "to take into account such regulations", and "does not condone companies using their association with Singapore to circumvent or violate other countries\' export controls through fraud or dishonest practices"',
  ['sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'sw-nbcnewscom-09', 'art-own-mha-1112', 'art-own-mha-1112', 'art-own-mha-1112', 'man-1fbc18e5e77d', 'art-own-mha-1112', 'art-own-mha-1112', 'art-own-mha-1112'],
  ['authorities had interviewed Huang and impounded her passport in 2025', 'insufficient evidence to establish that Huang had committed any offences', 'issued her with a stern warning after finding that she had knowingly provided police with inaccurate information', 'had been barred from re-entering the country', 'was not investigated for espionage', 'Singapore has to date received limited information or assistance in respect of the company', 'offences relating to the possible inaccurate declarations for which Megaspeed was being investigated', 'In February 2026', 'Supermicro provided limited cooperation', "Singapore's investigation into the company and six other individuals is ongoing, according to the Home Ministry", "SPF's investigations into Megaspeed and six other individuals are ongoing", 'While Singapore does not enforce unilateral export controls imposed by other countries', "Singapore does not condone companies using their association with Singapore to circumvent or violate other countries' export controls through fraud or dishonest practices"]),
 ('mast', '2026-11-12', 'Says Huang "has agreed to come" and testify; the day is being negotiated. "Jensen and I have been very at odds ... on export controls, but NVIDIA is a very important company"; "I don\'t want to see anything hurt in NVIDIA, but he has some very serious questions to answer". With Moolenaar and Crawford, sends a second request: letters ask Huang, Nvidia\'s general counsel and a Commerce under secretary to appear; the three say Congress "must immediately pass" four chip-export bills',
  ['sw-cnbccom-09', 'sw-engadgetcom-0b81faf0', 'sw-engadgetcom-0b81faf0', 'art-own-foreignaffairs-1112-chairmen-mast-moolenaar-and-crawfo', 'sw-engadgetcom-0b81faf0', 'sw-engadgetcom-0b81faf0', 'art-own-foreignaffairs-1112-chairmen-mast-moolenaar-and-crawfo'],
  ['He has agreed to come', 'Jensen and I have been very at odds as some of you already know on export controls', 'but he has some very serious questions to answer', 'requesting their appearance before Congress',
   'but NVIDIA is a very important company to the United States of America', "I don't want to see anything hurt in NVIDIA", 'Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA']),
 # ---- S1 of the gaps spec (Nov 14): acts of speakers who had no row; appended so that earlier row ids do not move
 ('rubio', '2026-11-08', 'Asked whether Huang was cut out of government meetings or briefings: "I can\'t comment on any of that. I just can\'t comment because of the nature of it"; and then: he "can\'t comment on an internal corporate matter that\'s going on with Nvidia", and: "I don\'t know anything about that part of it". NBC has him "speaking Sunday"; a republished transcript of the exchange is titled 9 November',
  ['nbc-1108-investigation', 'art-fc-rec-mirage-rubio-1109', 'art-fc-rec-mirage-rubio-1109', 'art-fc-rec-mirage-rubio-1109'],
  ['comment on an internal corporate matter', "I don't know anything about that part of it", 'if Jensen Huang was cut out of any U.S. Government meetings or any briefings', "I can't comment on any of that. I just can't comment because of the nature of it"]),
 ('bessent', '2026-11-05', 'Axios, as the Daily Caller relays it: in a Situation Room meeting he asks Lutnick "How come Megaspeed isn\'t on the entities list?" The Times reports the exchange too, as "described by people briefed on it", and prints a Commerce spokeswoman\'s denial that the conversation took place',
  ['sw-dailycallercom-03', 'sw-dailycallercom-03', 'man-nyt-1111-02', 'man-nyt-1111-02', 'man-nyt-1111-02'],
  ['pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting', 'on the entities list?', 'Treasury Secretary Scott Bessent confronted Commerce Secretary Howard Lutnick last week', 'took place at the White House on Thursday and was described by people briefed on it',
   'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place']),
 # Day moved from the report's day (Nov 11) to the act's own on 2026-11-16: a saved page (Implicator) gives it; found while drawing MA174.
 ('commerce', '2026-11-05', 'Axios, as Gizmodo relays it: the president told Lutnick "let\'s get it done"; Lutnick replied "I\'ll develop some options and come back" (Implicator, citing Axios too, dates these discussions to Nov 5). Gizmodo adds that the administration denied to Axios and the Times that the confrontation took place',
  ['sw-gizmodocom-08', 'sw-gizmodocom-08', 'sw-gizmodocom-08', 'sw-implicatorai-04', 'sw-implicatorai-04'],
  ['develop some options and come back', 'at some point Trump told Lutnick', 'denied to both Axios and the Times that any such confrontation between Bessent and Lutnick had ever taken place', 'on Nov. 5, when he told officials in the Oval Office', 'After Trump decided, he said he would "develop some options and come back."']),
 ('commerce', '2026-11-12', 'A spokeswoman tells CNBC Bessent and Lutnick had "no such conversation"', ['sw-cnbccom-22'], ['Commerce Department spokeswoman Kristen Eichamer told CNBC that Bessent and Lutnick had "no such conversation"']),
 ('greer', '2026-11-12', 'Tells CNBC "Nvidia is a structurally important company"; on exports: "we want the crown jewels to remain in U.S. hands or in the hands of our allies"; and: "The reality is the AI buildout, data centers, the next industrial revolution - that\'s happening"',
  ['sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cnbccom-09'],
  ['Nvidia is a structurally important company', 'we want the crown jewels to remain in U.S. hands or in the hands of our allies', "The reality is the AI buildout, data centers, the next industrial revolution — that's happening,"]),
 ('whitehouse', '2026-11-09', 'Asked how the administration handled the information: "These sources have no idea what they\'re talking about"', ['msnow-resigns'], ['a White House spokesperson referred MS NOW to Trump']),
 ('whitehouse', '2026-11-12', 'Statement calls Lutnick "a champion of President Trump\'s America First trade and tariff policies"', ['sw-cnbccom-09'], ['Secretary Lutnick is a champion of President Trump']),
 ('justice', '2026-11-09', 'CBS, as Breitbart relays it: its National Security Division is investigating Megaspeed', ['sw-breitbartcom-04'], ['National Security Division is investigating Megaspeed']),
 ('kress', 'EV31', 'Statement: "committed to building on the extraordinary foundation Jensen created"; in an email to staff: "this has been an extraordinarily difficult period"',
  ['fortune-1111-resigns', 'sw-cnbccom-ca82d66d'], ['I am committed to building on the extraordinary foundation Jensen created', 'recognize that this has been an extraordinarily difficult period']),
 ('jones', 'EV31', 'Statement: "Colette has helped lead NVIDIA through a period of extraordinary growth"', ['fortune-1111-resigns'], ['Colette has helped lead NVIDIA through a period of extraordi']),
 ('suit', '2026-11-09', 'Complaint filed in federal court: a company statement on Megaspeed "was materially false and misleading"; the complaint "seeks to recover compensable damages" for shareholders (Kotaku)',
  ['art-own-complaint-1109', 'art-own-complaint-1109', 'sw-courthousenewscom-02', 'sw-kotakucom-03'],
  ['Filed 11/09/26', 'was materially false and misleading at the time it was made', 'was materially false and misleading at the time it was made', 'seeks to recover compensable damages']),
 ('nvidia', '2026-11-09', 'Bloomberg reports, about an act of 2025: Nvidia\'s general counsel "intervened in a US government probe" of Megaspeed, calling a Commerce under secretary in late summer 2025 to ask about it. In Bloomberg\'s report, as the Business Times of Singapore carries it, a company spokesperson says the general counsel was unaware of the affair when he made the call',
  ['sw-techcrunchcom-08', 'sw-techcrunchcom-08', 'man-efbf718d0a5a', 'man-efbf718d0a5a', 'man-efbf718d0a5a', 'man-efbf718d0a5a', 'sw-gizmodocom-06', 'ms-deals-bloomberg-intervention-ce2630', 'ms-deals-bloomberg-intervention-ce2630'],
  ['Tim Teter, intervened in a 2025 U.S. government probe', 'November 9-10, 2026: Details emerge', 'general counsel intervened in a US government probe', 'November 9, 2026 at 3:28 PM CST', 'In late summer 2025', 'Tim Teter called Commerce Under Secretary', 'Nvidia told Bloomberg that Teter was unaware of the affair', 'An Nvidia spokesperson said that Teter was unaware of the affair at the time he called Kessler', 'Published Tue, Nov 10, 2026']),
 ('anthropic', '2026-11-12', 'Quartz reports that an Anthropic spokesperson "declined to comment", in its report on Huang\'s exit and Anthropic\'s share sale; the page does not say who asked',
  ['sw-qzcom-efc3c07a'],
  ['An Anthropic spokesperson declined to comment']),
 ('musk', '2026-11-11', 'Posts that hiring Huang "would be an honor", in reply to a ZeroHedge post: "Elon please hire Jensen". The post is stamped 8:22 PM Eastern', ['mj-misogyny', 'sw-zerohedgecom-09', 'sw-zerohedgecom-09'], ['Elon Musk wrote on Wednesday', 'Elon Musk responded to our X post', 'Elon please hire Jensen']),
 ('maguire', '2026-11-08', 'Posts that Huang "did something incredibly dumb" that was "bad for America", "but my guess is there was no bad intention", and "Two mistakes don\'t make a right, and I believe Jensen is irreplaceable for America\'s AI leadership"; Elon Musk replies "I agree"',
  ['sw-calcalistechcom-02', 'sw-calcalistechcom-02', 'sw-gulftimescom-01', 'sw-gulftimescom-01', 'semafor-1108-founder', 'semafor-1108-founder', 'sw-dailywirecom-01'],
  ['I believe Jensen is irreplaceable for America', 'Tesla CEO Elon Musk responded to Maguire', 'did something incredibly dumb', 'bad for America', 'On Sunday, Sequoia', 'PUBLISHED: 2026-11-09T02:58:19Z', 'but my guess is there was no bad intention']),
 ('ackman', '2026-11-08', 'Posts that Huang "is human. And he is an incredible human. Even incredible humans make mistakes", and adds in a reply to his own post that day: "I am not suggesting he gets a free pass. If indeed this is more than an affair", it is "a real problem"; "I am hoping for a simple affair, not a risk to our national security"',
  ['man-wapo-1112-02'] * 2 + ['art-own-x-2119560712855183434'] * 4 + ['sw-gulftimescom-01'],
  ['is human. And he is an incredible human. Even incredible humans make mistakes', 'tweeted billionaire Bill Ackman on Sunday', 'I am not suggesting he gets a free pass. If indeed this is more than an affair', 'a real problem',
   'I am hoping for a simple affair, not a risk to our national security', 'Sun Nov 08 22:40:28 +0000 2026', 'said on X the Nvidia CEO was an "incredible human"']),
 ('sweeney', '2026-11-12', 'Posts: "A sad day for NVIDIA, developers, America, and all humanity". PC Gamer: he has since called the outcome "far too much government heavy handedness" and, in another post, criticised the new interim chief for waiting a week before discussing everything at a company meeting (the article\'s paraphrase)',
  ['sw-80lv-02', 'sw-pcgamercom-eeaddc6b', 'sw-pcgamercom-eeaddc6b'],
  ['A sad day for NVIDIA, developers, America, and all humanity', 'far too much government heavy handedness', "taking a dig at Nvidia's new interim CEO for waiting a week until discussing everything in a company meeting"]),
 ('jcramer', '2026-11-11', 'On his show: "A Jensen-less Nvidia is an Nvidia many will not want to own"', ['sw-financeyahoocom-b1ac141d'], ['on the November 11 episode of Mad Money']),
 ('embassy', '2026-10-29', 'Its spokesman, in the Times: a campaign of "groundless smears and slanders"', ['man-nyt-1029-01'], ['groundless smears and slanders']),
 ('megaspeed', '2026-11-12', 'Says it takes U.S. export-control compliance "extremely seriously" and has cooperated with inspections', ['huffpost-live'], ['Megaspeed said on Thursday that it takes compliance obligations under U.S. export control laws']),
 ('taiwan', '2026-11-11', 'Its interior minister says, in the Journal\'s account of her words on Wednesday, that Alice Huang will be barred from returning to Taiwan and that security agencies are "continuing to investigate"',
  ['art-fc-mint-wsj-taiwan', 'art-fc-mint-wsj-taiwan'],
  ['Taiwan Interior Minister Liu Shyh-fang said Wednesday that Alice Huang would be barred from returning to Taiwan', 'national security agencies were continuing to investigate the case, Liu said']),
 ('globaltimes', '2026-11-09', 'Writes: "Whenever China-US relations begin to improve, there are often those firing shots from the shadows". ZeroHedge, relaying the commentary: "All it took were a few photographs showing Asian faces and Nvidia\'s previous efforts to push for relaxing trade curbs on China"; in its account the paper denies any government connection to the affair, says U.S. media are "going crazy", and warns that an "anti-China script" could disrupt technology and trade ties',
  ['sw-inquirercom-01', 'sw-zerohedgecom-06', 'sw-zerohedgecom-06'],
  ['there are often those firing shots from the shadows', 'All it took were a few photographs showing Asian faces', 'could disrupt technology and trade ties']),
 # ---- S2 of the gaps spec (Nov 14): remarks of members already drawn that the saved pages carry and no chip did
 ('moolenaar', '2026-11-12', 'Says talks are under way "on a date to come and meet with us", and: "If for some reason that were not to happen ... all three chairs have said we will use our subpoena power"; the resignation "does change the dynamic". Statement: the departure is "an unfortunate end that could have been avoided"; "It is in our national interest for NVIDIA and our other AI champions to succeed", but Nvidia "must now change its corporate practices and appoint leadership that makes national security its top priority", and "In Congress we must act quickly to pass bipartisan export control legislation in the year-end national defense bill" (Unite.AI relays this statement). With Mast and Crawford, sends a second request to appear; the three say Congress "must immediately pass" four chip-export bills',
  ['sw-cbsnewscom-e684eb4c', 'sw-cbsnewscom-e684eb4c', 'cnn-1111-live', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'art-own-chinaselectcommittee-1112-chairmen-moolenaar-mast-and-cr', 'art-own-chinaselectcommittee-1112-moolenaar-statement-on-jensen', 'sw-uniteai-bf709b60'],
  ['We are in discussions with him right now on a date to come and meet with us', 'If for some reason that were not to happen, all three committees, all three chairs have said we will use our subpoena power', 'does change the dynamic', 'Nvidia must now change its corporate practices and appoint leadership that makes national security its top priority', 'requesting their appearance before Congress', 'is an unfortunate end that could have been avoided', 'It is in our national interest for NVIDIA and our other AI champions to succeed', 'Congress must immediately pass the AI OVERWATCH Act, Chip Security Act, MATCH Act, and Remote Access Security Act in the NDAA', 'In Congress we must act quickly to pass bipartisan export control legislation in the year-end national defense bill', 'Moolenaar took a more specific legislative position in a November 12 statement']),
 ('jeffries', '2026-11-12', 'Calls the resignation the "right thing to do"; "Now we have to get to the bottom of whether America\'s national security has been compromised"',
  ['cnn-1111-live', 'cnn-1111-live'], ['resignation Thursday was the "right thing to do,"', 'Now we have to get to the bottom of whether America']),
 ('schumer', '2026-11-12', 'Posts: "Despite Jensen Huang\'s resignation, Congress must demand answers"', ['sw-cbsnewscom-e684eb4c'], ['resignation, Congress must demand answers from Mr. Huang and others at Nvidia']),
 ('warren', '2026-11-12', 'Statement: Huang, executives and the board "still owe Congress answers"; Lutnick "must explain why they have not closed export control loopholes"; the resignation "does not absolve him, other executives or the company as a whole of responsibility for putting our national security at risk or for any potential violations of our laws" (the Times); she calls on Congress to pass the AI Overwatch Act (CNBC); and says the two Commerce officials must "act today to ensure our advanced technology is not fueling China\'s military" (The National)',
  ['sw-cbsnewscom-09', 'sw-cnbccom-09', 'man-5db1c88adc15', 'sw-cnbccom-09', 'sw-thenationalnewscom-04'],
  ['board of directors still owe Congress answers', 'must explain why they have not closed export control loopholes', 'Senator Elizabeth Warren of Massachusetts, the top Democrat on the banking committee, said that Mr. Huang’s resignation “does not absolve him, other executives or the company as a whole of responsibility for putting our national security at risk or for any potential violations of our laws.”', 'Warren also called on Congress to pass the AI Overwatch act , giving Congress oversight over advanced AI chip exports.', '" Secretary Howard Lutnick and Under Secretary Jeffrey Kessler must explain why they have not closed export control loopholes and act today to ensure our advanced technology is not fueling China’s military," she said, referring to reports of Nvidia\'s dealings with China.']),
 ('coons', '2026-11-09', 'Posts: "I\'m pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised"',
  ['sw-abcnetau-03'], ['pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised']),
 # the full reading of the saved pages (2026-11-14): a Times report of Nov 9 and the department's answer; one more public voice
 ('nyt', '2026-11-09', 'Reports that a Commerce Department investigation of Megaspeed "came to a sudden halt late last year" and was "transferred to the Justice Department", after Nvidia\'s general counsel emailed the investigators in August 2025. It says the transfer was "to avoid any potential compromise" of the investigation, that Justice "is conducting a criminal inquiry into Megaspeed", and that "it is not clear if other factors contributed". Of the email it reports, from people familiar with the incident and a Commerce official: he told the agents the under secretary had given him permission to reach out about the case; Nvidia had asked them directly for a meeting with one of them, and when they turned it down he replied that he was unsure what the issue was, because the under secretary had said Nvidia could communicate with the bureau\'s employees. It adds that the investigators forwarded the email chain to the under secretary, and that since the president\'s return to office he and other leaders of the department "had mandated that any investigations into Nvidia and other outreach to the company first receive their approval"',
  ['sw-cnbccom-02', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03'],
  ["the Times reported that the Commerce Department was investigating Megaspeed until August 2025, when the probe was abruptly transferred to the Department of Justice following outreach from Nvidia's general counsel about the matter", 'their work came to a sudden halt late last year', 'the case was abruptly transferred to the Justice Department last year', 'In August 2025, officials at the Commerce Department', 'received an email from Mr. Teter, the general counsel of Nvidia', "in an effort to avoid any potential compromise of the government's investigation of Megaspeed", 'The Justice Department is conducting a criminal inquiry into Megaspeed', "It is not clear if other factors contributed to the decision to suspend the Commerce Department's work", 'had given him permission to reach out about the case', 'had contacted the employees directly to request a meeting with one of them', 'he was unsure what the issue was because', 'The employees forwarded the email chain to', 'had mandated that any investigations into Nvidia and other outreach to the company first receive their approval']),
 ('commerce', '2026-11-09', 'A spokesman for its export-control bureau tells CNBC: "BIS conducts all enforcement strictly by the book", and: "BIS enforces aggressively across the board, including with respect to chip smuggling, and enforcement is at an all-time high". A department spokesman tells the Times it "had been aggressively enforcing its rules"; an official tells the paper the under secretary told the agents to "continue to handle the case strictly by the book" and did not order them to give Nvidia information',
  ['sw-cnbccom-02', 'sw-cnbccom-02', 'sw-cnbccom-02', 'man-nyt-1109-03', 'man-nyt-1109-03', 'man-nyt-1109-03'],
  ['BIS conducts all enforcement strictly by the book', 'Later Monday morning, the Times reported that the Commerce Department was investigating Megaspeed until August 2025', 'BIS enforces aggressively across the board, including with respect to chip smuggling, and enforcement is at an all-time high.', 'A Commerce Department spokesman said that department had been aggressively enforcing its rules and had conducted this and other actions strictly by the book.', 'they should continue to handle the case strictly by the book', 'did not order his employees to divulge information to Nvidia']),
 ('kudlow', '2026-11-10', 'On his show: "Step down, Mr. Huang. Right now"', ['sw-mediaitecom-06'], ['Step down, Mr. Huang. Right now']),
 # remarks the full reading found on many pages and no chip carried (2026-11-14)
 ('trump', '2026-11-12', 'Posts: "there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!"',
  ['fox-trump-successor'], ['there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!']),
 ('nvidia', '2026-11-08', 'Tells CNBC: "Today\'s news will not slow NVIDIA. Jensen is committed to continuing to lead NVIDIA as CEO without interruption". Tells CBS: "We trust that if we were the target of a genuine threat, the U.S. government would have notified us". A spokesman tells the Times that Huang will not take part in choosing the outside counsel',
  ['cnbc-1108-bipartisan', 'sw-cbsnewscom-01', 'sw-cbsnewscom-01', 'man-nyt-1108-01'],
  ['Jensen is committed to continuing to lead NVIDIA as CEO without interruption', 'We trust that if we were the target of a genuine threat, the U.S. government would have notified us', 'told CBS News on Sunday', "said Mr. Huang wouldn't be part of the selection process"]),
 ('huang', '2026-10-29', 'Tells Bloomberg, as Taiwan News relays the interview (Bloomberg\'s saved page shows its opening only): "Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual"; as Data Center Knowledge relays it, "We\'ve studied all their deployments of our GPUs and counted every one". Data Center Dynamics has him calling the story "groundless speculation". Quartz relays more of it: "And I think the U.S. government also has as well"; and he said the U.S. government had not told him of its suspicions about her',
  ['man-bbg-1029-01', 'sw-taiwannewscomtw-01', 'sw-datacenterknowledgecom-01', 'sw-datacenterknowledgecom-01', 'sw-datacenterdynamicscom-03', 'sw-datacenterdynamicscom-03', 'sw-qzcom-01', 'sw-qzcom-01'],
  ['Nvidia CEO Says Ties to Company in Spy Probe Were', 'Our relationship, our interactions, have been related to Megaspeed, and it was all completely normal and not unusual', 'studied all their deployments of our GPUs and counted every one', 'in an October 29 Bloomberg interview', 'Huang called the story', 'groundless speculation', 'And I think the U.S. government also has as well', 'He said the U.S. government has not told him of its suspicions about her']),
 ('huang', '2026-11-11', 'Reached by phone by the Times and asked about a second relationship: "I don\'t think you should be talking to me directly"',
  ['man-e1161e38dc19'], ["I don't think you should be talking to me directly"]),
 ('commerce', '2026-11-05', 'Axios, as ZeroHedge relays it: asked by Bessent why Megaspeed is not on the entity list, Lutnick answers "I don\'t know. I\'ll look into it". In a second report of Axios, of an Oval Office meeting with the president that day, he warns that the controls "will start a trade war with China". In the Times\'s account of the first exchange he answers that Commerce "could now move quickly to put restrictions on Megaspeed in place". A Commerce spokeswoman: "This is false. Secretary Bessent and Secretary Lutnick had no such conversation". Implicator\'s account of the Axios report has him appear to agree at the first exchange and then mutter "I need to check with the president"',
  ['sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'sw-dailycallercom-03', 'sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'sw-zerohedgecom-10', 'man-nyt-1111-02', 'man-nyt-1111-02', 'sw-implicatorai-04'],
  ['again in the Oval Office on Nov. 5', "I don't know. I'll look into it", 'pressed Commerce Secretary Howard Lutnick in a Thursday White House Situation Room meeting', 'This is false. Secretary Bessent and Secretary Lutnick had no such conversation', 'while Lutnick warned that the controls', 'will start a trade war with China', 'Commerce Department could now move quickly to put restrictions on Megaspeed in place', 'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place', 'Lutnick appeared to agree, then muttered under his breath']),
 # every analyst and byline on the saved pages was looked up in the funding records (2026-11-14): two more analysts and one more byline have a record and a remark of these days
 ('king', '2026-11-12', 'Quartz reports her saying that export controls cover the physical transfer of chips but not remote access to them',
  ['sw-qzcom-13'], ['U.S. export controls cover the physical transfer of chips but not remote access to them, said Cassia King']),
 ('nie', '2026-11-12', 'Quartz reports her saying the remote-access bill alone would fall short: it would give the legal authority, but "a separate rulemaking process would be required" before it could be used on advanced chips',
  ['sw-qzcom-13', 'sw-qzcom-13'], ['RASA alone would fall short of closing the loophole, said Michelle Nie', 'a separate rulemaking process would be required before that authority could be used on advanced chips']),
 ('hashim', '2026-11-09', 'Publishes "Jensen Huang should resign": "In the worst case, Nvidia may have fundamentally undermined American national security and AI leadership"; "An investigation is necessary to see just how bad the incident was"; "we do not know if the affair was disclosed to Nvidia\'s board or if Huang removed himself from decision-making involving Megaspeed"; it does not know whether the company\'s spokesman knew his statements were false; "Nvidia\'s board may keep him around"',
  ['sw-transformernewsai-01', 'sw-transformernewsai-01', 'sw-transformernewsai-01', 'sw-transformernewsai-01', 'sw-transformernewsai-01', 'sw-transformernewsai-01', 'sw-transformernewsai-01'],
  ['AUTHOR: Shakeel Hashim', 'Jensen Huang should resign', 'In the worst case, Nvidia may have fundamentally undermined American national security and AI leadership', 'An investigation is necessary to see just how bad the incident was', "we do not know if the affair was disclosed to Nvidia's board or if Huang removed himself from decision-making involving Megaspeed", 'We do not know if Rizzo knew they were false too; if not, Huang appears to have misled his own executives as well.', "Nvidia's board may keep him around"]),
 # a member named on five saved pages for an act on the matter a year before these days: no day on the calendar (drawn in his row, like any act with no day)
 ('cotton', '', 'Before these days: in Oct 2025 he wrote to the Commerce secretary about Megaspeed\'s "suspicious ownership, affiliations"; pages of these days cite the letter',
  ['sw-thefederalistcom-01', 'sw-thefederalistcom-01', 'sw-spectatorcom-01'],
  ['In October 2025, Sen. Tom Cotton, R-Ark., wrote to Commerce Secretary Howard Lutnick to raise concerns about Megaspeed', 'suspicious ownership, affiliations', 'the Arkansas Republican who chairs the Senate Intelligence Committee, asked the Commerce Department to investigate Megaspeed in October last year']),
 # ---- S6 of the gaps spec (Nov 14): remarks and acts found on the actors' own channels (ministry transcripts, members' releases, an institute's site) that no chip carried
 ('china', '2026-10-30', 'Its spokesman on the Times report: "unsubstantiated. It is nothing but smears against China"',
  ['art-own-fmprc-1030-t20261030-12050434'], ['Relevant report is unsubstantiated. It is nothing but smears against China']),
 ('china', '2026-11-11', 'Asked about calls for tighter chip limits: "Our position on U.S. chip exports to China is consistent"',
  ['art-own-fmprc-1111-t20261111-12057544'], ['Our position on U.S. chip exports to China is consistent']),
 ('china', '2026-11-12', 'Its spokeswoman: the U.S. should "stop fabricating" spy "narratives as a pretext for imposing technology restrictions"; asked that Thursday about a report that she had returned to China: "I do not have information on what you mentioned" (CBS). Asked at that briefing whether the scandal will affect relations before the two presidents\' likely summit, she says the two countries "maintain close communication on heads-of-state interactions"',
  ['art-own-fmprc-1112-t20261112-12058413', 'art-own-fmprc-1112-t20261112-12058413', 'sw-cbsnewscom-08', 'sw-cbsnewscom-08', 'art-own-fmprc-1112-t20261112-12058413', 'art-own-fmprc-1112-t20261112-12058413'],
  ['The U.S. should stop fabricating the', 'narratives as a pretext for imposing technology restrictions', 'I do not have information on what you mentioned.', 'Asked Thursday about the report that Alice Huang had returned', 'Is China concerned that the NVIDIA spy scandal will affect U.S.-China relations ahead of the likely summit', 'China and the U.S. maintain close communication on heads-of-state interactions']),
 ('meeks', '2026-11-09', 'Letter with two colleagues asks the Commerce secretary to "immediately halt exports of advanced artificial intelligence chips" to China; it says "the American people must have transparency into what your Department knew, when it knew it, and why it continued to permit these exports"',
  ['art-own-democrats-foreignaffairs-1109-meeks-amo-kamlager-dove-de', 'ms-gap-suits-amo-8d5790'],
  ['We call on the Department of Commerce to immediately halt exports of advanced artificial intelligence chips', 'Considering these alarming reports, the American people must have transparency into what your Department knew, when it knew it, and why it continued to permit these exports. We hope that the Department did not ignore warnings about a suspected PRC intelligence operation while allowing advanced American technology to flow through companies under scrutiny. If Commerce was not briefed, we need to know why. If it was briefed, we need to know how it responded. And if the Department knowingly permitted these exports despite credible national-security concerns, the American people deserve an explanation.”']),
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
 ('trump', '2026-10-31', 'At his Halloween party, asked if he still has confidence in Huang as an adviser: "I would like to say yes. I mean, unless we find out something to the contrary"; says the matter is "very complex" and will be looked at "very closely"; asked about the intelligence concerns, in the pool report of that evening: "I didn\'t know about the specific thing, but I hope he\'s going to be okay"',
  ['sw-aninewsin-01', 'sw-aninewsin-01', 'sw-irishtimescom-01', 'sw-irishtimescom-01', 'ms-admin-app-trump-1031-1ea74d', 'ms-admin-app-trump-1031-1ea74d'],
  ['I would like to say yes. I mean, unless we find out something to the contrary', 'going to check it out very closely', 'Trump told reporters on October 31st', 'calling the situation', "I didn't know about the specific thing, but I hope he's going to be okay", 'Asked about U.S. intelligence concerns around Jensen Huang']),
 # B04: Mast's interview of Tuesday, Nov 10, with what he says in Nvidia's favour
 ('mast', '2026-11-10', 'Tells ABC he is prepared to subpoena Huang if no reply comes by Wednesday. Of Nvidia: "we thank God that Jensen is an American entrepreneur ... they\'re the best chips anywhere in the globe. But that being said, we don\'t want China to access them"',
  ['abc-subpoena'] * 4, ['told ABC News on Tuesday that he', 'So we thank God that Jensen is an American entrepreneur', 'the best chips anywhere in the globe', 'want China to access them, to use them, to produce them like that']),
 # quoted analysts with a tie on record, by the one rule (see ACTORS)
 ('chan', '2026-11-12', 'Tells CNBC the president\'s weakened grip on congressional Republicans after the midterm defeat makes it harder for the administration to hold back chip-export measures',
  ['sw-cnbccom-08', 'sw-cnbccom-08'], ['said Kyle Chan, a China fellow at the Brookings Institution', 'PUBLISHED: 2026-11-12']),
 ('ohanlon', '2026-11-10', 'Tells Newsweek: "Huang\'s motives must now be suspect. That is the key point. But he did not make the actual decisions on export control policy so the damage may be limited"',
  ['sw-newsweekcom-01'] * 3, ['a senior fellow at the Brookings Institution who studies defense and foreign policy, told Newsweek', 'But he did not make the actual decisions on export control policy so the damage may be limited', 'PUBLISHED: 2026-11-10']),
 ('wiblin', '2026-11-08', 'Posts that Huang "Lied to the board. Lied to journalists. Meanwhile pushing to sell maximum of cutting edge AI chips to China against advice of ~entire natsec community". Zvi Mowshowitz\'s newsletter of Nov 10 carries the post',
  ['sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01'],
  ['Rob Wiblin', 'Meanwhile pushing to sell maximum of cutting edge AI chips to China against advice of ~entire natsec community', 'PUBLISHED: 2026-11-10', 'Lied to the board. Lied to journalists.']),
 ('moorhead', '2026-11-10', 'Tells CNBC: "In 35 years, I haven\'t seen a chip CEO with this much direct influence on export policy"; he expects more export-control legislation to pass as a result of the turmoil',
  ['sw-cnbccom-04', 'sw-cnbccom-04', 'sw-cnbccom-04', 'sw-cnbccom-04'],
  ['seen a chip CEO with this much direct influence on export policy', 'said Patrick Moorhead, CEO at Moor Insights', 'PUBLISHED: 2026-11-10', 'Moorhead expects more export control legislation to pass as a result of the latest turmoil.']),
 ('newman', '2026-11-09', 'Tells CBS by email: "There is no known succession plan, and there is no leader in the company who would be the clear next step if he had to step down"; "That does not mean they cannot find a Tim Cook in the future, but it would be a massive changing of the guard"',
  ['sw-cbsnewscom-03', 'sw-cbsnewscom-03', 'sw-cbsnewscom-03', 'sw-cbsnewscom-03', 'sw-cbsnewscom-03'],
  ['There is no known succession plan, and there is no leader in the company who would be the clear next step if he had to step down', 'said Daniel Newman, CEO of tech consulting firm Futurum, in an email', 'PUBLISHED: 2026-11-09', 'That does not mean they cannot find a Tim Cook in the future, but it would be a massive changing of the guard', 'tech analysts said on Monday']),
 ('boloor', '2026-11-12', 'Tells Fortune the selloff is overdone: he does not see "12 to 18 months of revenue suddenly disappearing if Jensen were to leave" (the San Francisco Standard had printed the sentence the evening before as told to Yahoo Finance: his chip of Nov 11). Quoted the same day: "My bigger concern is next decade", because Huang "has consistently identified where computing is going". Reuters, as TrendForce relays it that day, has him say that demand and the product roadmap "were firmly established well before the controversy" and could sustain revenue for 12 to 18 months even if Huang leaves; the pages do not say whether these are one comment sent to several outlets',
  ['sw-fortunecom-11', 'sw-fortunecom-11', 'sw-fortunecom-11', 'sw-rteie-05', 'sw-rteie-05', 'sw-trendforcecom-637e84ec', 'sw-trendforcecom-637e84ec'],
  ['12 to 18 months of revenue suddenly disappearing if Jensen were to leave', 'Shay Boloor, chief market strategist at The Futurum Group', 'PUBLISHED: 2026-11-12', 'My bigger concern is next decade', 'the person who has consistently identified where computing is going', 'Citing Shay Boloor, chief market strategist at Futurum Equities, Reuters highlights', 'could help sustain revenue momentum over the next 12 to 18 months even if Huang departs']),
 ('yoo', '2026-11-12', 'Tells the Korea JoongAng Daily that Nvidia\'s people "have a high level of expertise and autonomy", so its culture will hold',
  ['sw-koreajoongangdailycom-06'] * 3, ['Because its people have a high level of expertise and autonomy, the culture won', 'Yoo Eung-joon, CEO of JOON AI Consulting and a former head of Nvidia Korea', 'PUBLISHED: 2026-11-12']),
 ('mowshowitz', '2026-11-10', 'Publishes "Nvidia CEO Jensen Huang Had an Affair With a Chinese Spy": "National security has been compromised. He must resign"; "I would be very surprised if Jensen Huang knew he was being compromised by a Chinese agent"; he accepts as "a mitigating factor" that Huang "was up against actual professional spies and an active operation to compromise him"; "If he will not resign, the board must remove him. If the board will not remove him, the United States Government should force him to step down"; and anyone in the government "who knowingly let this go on for a year should be offering their resignation as well". He also writes that the affair "is not necessary to explain" Huang\'s conduct on chip sales to China: "He might or might not have done that anyway, or done that to the same extent"',
  ['sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01'],
  ['AUTHOR: Zvi Mowshowitz', 'National security has been compromised. He must resign', 'PUBLISHED: 2026-11-10', 'I would be very surprised if Jensen Huang knew he was being compromised by a Chinese agent', 'he was up against actual professional spies and an active operation to compromise him', 'as a mitigating factor', 'If he will not resign, the board must remove him. If the board will not remove him, the United States Government should force him to step down', 'who knowingly let this go on for a year should be offering their resignation as well', 'Sleeping with a Chinese spy is not necessary to explain Jensen Huang treating America like an adversary', 'He might or might not have done that anyway, or done that to the same extent']),
 ('schneider', '2026-11-10', 'Publishes "The Spy Who Leased Me", the newsletter page of his podcast with Chris McGuire on the affair, which his feed dates the day before',
  ['sw-chinatalkmedia-01'] * 3, ['AUTHOR: Jordan Schneider', 'Emergency pod with Chris McGuire', 'PUBLISHED: 2026-11-10']),
 ('newman', '2026-11-12', 'Tells NPR: "They\'ve always had Jensen as this sort of visionary at the front. I don\'t think that\'s replaceable"',
  ['sw-nprorg-01', 'sw-nprorg-01', 'sw-nprorg-01', 'sw-nprorg-01'],
  ['always had Jensen as this sort of visionary at the front', 'Daniel Newman, CEO of the Futurum Group, a tech research firm', 'PUBLISHED: 2026-11-12', 'said the company will inevitably be different without Huang']),
 # three more public voices on three or more saved pages
 ('delangue', '2026-11-12', 'Posts: "This whole thing sucks, and I wish none of it had happened"; calls it "a really sad day" and adds: "we\'ll keep fighting for open-source AI, harder than ever"',
  ['cnn-1111-live', 'sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cnbccom-09'], ['This whole thing sucks, and I wish none of it had happened', 'lamented Huang', 'PUBLISHED: 2026-11-12', 'keep fighting for open-source AI, harder than ever']),
 ('zhao', '2026-11-12', 'Posts that it is "a mistake for Nvidia to let Jensen resign"',
  ['sw-cnbccom-09', 'cnn-1111-live'], ['a mistake for Nvidia to let Jensen resign', 'departure Thursday morning, Binance co-founder and former CEO Changpeng Zhao']),
 ('rao', '2026-11-12', 'Tells Yahoo Finance the search for a new chief "needs to be closed probably in the next three or four months"',
  ['sw-financeyahoocom-23'] * 3, ['it needs to be closed probably in the next three or four months', 'a chip start-up founder and CEO a public voice no longer drawn', 'PUBLISHED: 2026-11-12']),
 # ---- added after the release of Nov 15 (commit 2b7a13d), at the END so that no published id moves
 # two reports of the Times that its row lacked (hand-saved on Nov 12 and never drawn; found when the hand-saved pages were listed on Nov 15)
 ('nyt', '2026-11-10', 'Reports that the president was told aboard Air Force One in May, by Rubio, of the intelligence on Huang, which "contradicts the president\'s assertion" that he had not known then; the White House "disputed the reporting", it says, "without elaborating"',
  ['man-nyt-1110-02'] * 5, ['President Trump was told aboard Air Force One in May en route to China', 'The message was delivered by Marco Rubio', 'assertion on Monday that he had not known at the time of the trip', 'The email disputed the reporting for this article, without elaborating', 'PUBLISHED: 2026-11-10']),
 ('nyt', '2026-11-11', 'Reports that Bessent "confronted" Lutnick at the White House over Megaspeed, as "described by people briefed on it"; a Commerce spokeswoman denies the conversation took place; it adds that the move to blacklist Megaspeed had earlier come before a meeting of cabinet deputies, where a Commerce under secretary "deferred on taking action, saying that the decision was up to Mr. Lutnick"',
  ['man-nyt-1111-02', 'man-nyt-1111-02', 'man-nyt-1111-02', 'man-nyt-1111-02', 'man-nyt-1111-02'],
  ['Treasury Secretary Scott Bessent confronted Commerce Secretary Howard Lutnick last week', 'took place at the White House on Thursday and was described by people briefed on it', 'A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place', 'PUBLISHED: 2026-11-11', 'The move to blacklist Megaspeed had earlier been discussed at a meeting of the deputies of cabinet officials, where Jeffrey Kessler, an under secretary in the Commerce Department, deferred on taking action, saying that the decision was up to Mr. Lutnick.']),
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
 # ---- slice S8 (Nov 15, 2026): three members named in three or more counted articles once the pages saved since are counted
 ('scott', '2026-11-12', 'Letters to Huang and to Lutnick ask each to testify before the Senate Banking Committee; he asks Huang to appear on Dec. 3. In a post: "Recent reports raise serious concerns about our national security and the protection of sensitive U.S. technology". The Washington Examiner reports that the letters ask them to appear or be subject to "all tools at our disposal, including subpoenas"',
  ['man-5db1c88adc15', 'man-5db1c88adc15', 'man-5db1c88adc15', 'man-9de9f2a5db75', 'man-9de9f2a5db75', 'man-nyt-1112-09', 'art-line-wex-scott-1112'],
  ['on Thursday evening sent letters to Mr. Huang and Mr. Lutnick requesting their testimony in front of the Senate Banking Committee', 'Recent reports raise serious concerns about our national security and the protection of sensitive U.S. technology', 'Mr. Scott asked Mr. Huang to appear on Dec. 3', 'sent letters late Thursday requesting that Jensen Huang and Lutnick testify before his panel early next month', 'Scott said he will hold the hearing Dec. 3', 'on Thursday evening sent letters to Mr. Huang and Mr. Lutnick requesting their testimony in front of the Senate Banking Committee', 'all tools at our disposal, including subpoenas.']),
 ('neal', '2026-11-12', 'Letter with Sen. Wyden opens a probe of chip-export approvals; it says the administration "did not appear to acknowledge this evident national security threat"; it asks the department to preserve all records of its tariff investigation of semiconductors, of Nvidia\'s export licence applications and of its communications with and about Nvidia and Huang',
  ['sw-cnbccom-09', 'art-own-wyden-neal-letter-1112', 'art-own-wyden-neal-letter-1112', 'man-a45550a35921', 'art-own-wyden-neal-letter-1112', 'art-own-wyden-neal-letter-1112'],
  ['Their letter to Commerce Secretary Howard Lutnick announcing the probe was sent by Sen. Ron Wyden, D-Ore., and Rep. Richard Neal, D-Mass.', 'the Administration did not appear to acknowledge this evident national security threat', 'November 12, 2026 The Honorable Howard Lutnick', 'In a letter addressed to Lutnick on Thursday, Senator Ron Wyden and Congressman Richard Neal requested', 'we write to request that you preserve all records related to', "the Department's consideration and approval of export license applications submitted by Nvidia"]),
 ('ricketts', '2026-11-10', 'Says of the allegations: "this needs to be investigated to find out if indeed the allegations are true"; "We cannot allow our chief adversary in the world [to] have access to our high-end technology"',
  ['sw-washingtonsuncom-02', 'sw-washingtonsuncom-02', 'sw-washingtonsuncom-02', 'sw-washingtonsuncom-02'],
  ['this needs to be investigated to find out if indeed the allegations are true', 'We cannot allow our chief adversary in the world [to] have access to our high-end technology', 'PUBLISHED: 2026-11-10', 'Several Republicans told The Washington Sun on Tuesday']),
 ('ricketts', '2026-11-12', 'Says, in the FT\'s account, that Congress needs to hear from Commerce officials on why actions on Megaspeed were "delayed". A Fox Business caption has him on "Varney & Co." on the resignation and "the need for an investigations"; the recording was not heard',
  ['man-a45550a35921', 'fox-trump-successor', 'fox-trump-successor', 'man-a45550a35921'],
  ['said Congress needed to hear from commerce department officials over why actions on Megaspeed were "delayed"', 'discusses the resignation of Jensen Huang as CEO of Nvidia, the need for an investigations and the national security implications', 'PUBLISHED: 2026-11-12', 'Outraged Republican legislators on Thursday called for Lutnick']),
 # ---- slice S8: remarks of actors already drawn that two or more counted articles carry and no chip did (the reading of the pages saved since)
 ('nvidia', '2026-11-09', 'A spokesman tells the Times the company consults with officials "to answer their questions, provide information we have gathered from the field, request their guidance and instructions", and works "to help government and our partners halt any would-be smugglers"',
  ['man-nyt-1109-03'] * 2, ['to answer their questions, provide information we have gathered from the field, request their guidance and instructions and ask whether they have any follow-ups', 'to help government and our partners halt any would-be smugglers while serving the critical market of lawful customers']),
 ('cornyn', '2026-11-12', 'Tells the FT: "There needs to be a thorough investigation and accountability for the outrageous circumvention of national security export controls ... Heads should roll"',
  ['man-a45550a35921', 'man-a45550a35921', 'man-a45550a35921'],
  ['There needs to be a thorough investigation and accountability for the outrageous circumvention of national security export controls', 'Republican senator John Cornyn told the FT. "Heads should roll."', 'Outraged Republican legislators on Thursday called for Lutnick']),
 ('megaspeed', '2026-11-09', 'Posts a statement on LinkedIn, in a Dow Jones report of that day: investigations by U.S. authorities and others found "no evidence of any violations concerning the illicit transfer of chips or any illegal activities"; it maintains "the highest standards of legal and ethical conduct". The words are those of its statement dated Dec 23, 2025, which another page of that day says it is standing by. The statement also says: "we do not rule out pursuing legal action to protect our reputation and to hold Bloomberg accountable for the misleading nature of the article"; and that "over the past six months, our company has undergone multiple on-site inspections and reviews by key institutions, including the Bureau of Industry and Security of the US Commerce Department, the Ministry of Investment, Trade and Industry of Malaysia, and Nvidia" (PC Gamer quotes that sentence the same day)',
  ['art-fc-itiger-2682389645', 'art-fc-itiger-2682389645', 'art-fc-itiger-2682389645', 'art-fc-itiger-2682389645', 'sw-chinamoneynetworkcom-01', 'sw-chinamoneynetworkcom-01', 'sw-chinamoneynetworkcom-01', 'sw-pcgamercom-02'],
  ['In a statement posted on LinkedIn on Monday, Megaspeed said', 'no evidence of any violations concerning the illicit transfer of chips or any illegal activities', 'Dow Jones Nov 09', 'the highest standards of legal and ethical conduct', 'The company is standing by a statement dated December 23, 2025', 'there has been no evidence of any violations concerning the illicit transfer of chips or any illegal activities', 'we do not rule out pursuing legal action to protect our reputation and to hold Bloomberg accountable for the misleading nature of the article', 'over the past six months, our company has undergone multiple on-site inspections and reviews by key institutions']),
 ('moorhead', '2026-11-11', 'Quoted in a Times article of Nov 11: "Jensen is very much the command and control ... nobody can replace Jensen. There has to be a different operating system"',
  ['sw-bostonglobecom-01'] * 4 + ['man-nyt-1112-07'], ['Jensen is very much the command and control', 'nobody can replace Jensen. There has to be a different operating system', 'This article originally appeared in The New York Times',
   'bostonglobe.com/2026/11/11/business/nvidia-board-meeting-jensen-huang-future', 'Jensen is very much the command and control']),
 ('thune', '2026-11-12', 'Tells reporters "it would make sense" for Huang to testify "because of the nature of the association and the governments and the national security interests"',
  ['man-ft-1112-05', 'man-575551038d4a'], ['told reporters on Capitol Hill on Thursday that "it would make sense [for Huang to testify] because of the nature of the association and the governments and the national security interests"',
   'on Thursday said "it would make sense [for Huang to testify] because of the nature of the association and the governments and the national security interests"']),
 ('himes', '2026-11-11', 'Tells Politico after a classified briefing: "What\'s the relationship with Alice Huang and the Chinese, and what do we know about what influence or information was traded? Because today, at least, I don\'t know"; and: "I would hope that the FBI would launch a major counterintelligence investigation. I haven\'t heard that they did"; he tells Politico that Wednesday that the FBI should have begun investigating earlier this year after a memo circulated, and that he has not seen the memo',
  ['art-fc-yahoo-politico-himes', 'art-fc-yahoo-politico-himes', 'art-fc-yahoo-politico-himes', 'art-fc-yahoo-politico-himes', 'art-fc-yahoo-politico-himes'],
  ["what do we know about what influence or information was traded? Because today, at least, I don't know", "I would hope that the FBI would launch a major counterintelligence investigation. I haven't heard that they did", 'PUBLISHED: 2026-11-11T23:30:07Z', 'In a wide-ranging interview on Wednesday, Himes told POLITICO', 'Himes told POLITICO the FBI should have begun investigating Alice Huang earlier this year after a "memo circulated" around government offices raising concerns about her links to the Chinese government, though he clarified that he had not seen the memo. "I would hope that the FBI would launch a major counterintelligence investigation. I haven\'t heard that they did," he said, adding that when he asked Director of National Intelligence Jay Clayton and CIA Director John Ratcliffe, "they didn\'t know" whether the FBI had opened an investigation.']),
 # ---- slice S8: an item found on a new member's own channel (lane s6_channels_4), and the people drawn from the pages saved since
 ('ricketts', '2026-11-09', 'Statement: "We need to know if Chinese spies received sensitive information and if Nvidia chips were illegally smuggled through Megaspeed ... To start we must pass my MATCH Act and the Safe Chips Act"',
  ['art-own-ricketts-statement-1109'] * 3, ['We need to know if Chinese spies received sensitive information and if Nvidia chips were illegally smuggled through Megaspeed', 'To start we must pass my MATCH Act and the Safe Chips Act', 'PUBLISHED: 2026-11-09T23:17:00+00:00']),
 ('hodges', '2026-11-12', 'Tells CNN: "we\'ve seen repeatedly the Chinese are incredibly adept at using people both wittingly and unwittingly"',
  ['art-fc-cnn-1112'] * 3, ["Joshua Hodges, a commissioner on the US-China Economic and Security Review Commission", "we've seen repeatedly the Chinese are incredibly adept at using people both wittingly and unwittingly", 'PUBLISHED: 2026-11-12']),
 ('conway', '2026-11-11', 'Posts: "As the swirl continues (which I believe should be taken seriously), let\'s pause for a moment and remember what Jensen has contributed to our industry ... Now we should be patient and wait for investigations by the board of directors and any government authorities to conclude"',
  ['art-own-x-2120633328441479589'] * 3 + ['sw-sfstandardcom-09', 'man-wapo-1112-02'],
  ["As the swirl continues (which I believe should be taken seriously), let's pause for a moment and remember what Jensen has contributed to our industry", 'Now we should be patient and wait for investigations by the board of directors and any government authorities to conclude',
   'Wed Nov 11 21:42:39 +0000 2026', 'At 1:42 pm on Wednesday, just minutes before the Times broke its story, venture capitalist Ron Conway called for patience while investigations concluded',
   'wrote venture capitalist Ron Conway, adding that the public should wait for various investigations by the government and the company to conclude']),
 # ---- Nov 16, 2026: two remarks that the reading of the recovered pages (lane remarks_nv8_f) found on two counted articles and on no chip
 ('megaspeed', '2026-10-29', 'In a statement to the Times, in its first report: "outside counsel has been retained to conduct a thorough internal investigation and has notified the U.S. government that we are fully committed to cooperating"',
  ['man-nyt-1029-01', 'man-nyt-1029-01'],
  ['In a statement to The New York Times, Megaspeed said that its “current leadership” takes the matter “extremely seriously', 'outside counsel has been retained to conduct a thorough internal investigation and has notified the U.S. government that we are fully committed to cooperating']),
 ('warner', '2026-11-09', 'In Bloomberg\'s report of the closed briefing of that day, carried by the Straits Times: "We all obviously have questions, but I\'m not going to weigh in on any substance"; "we need to hear from the Federal Bureau of Investigation"',
  ['art-line-straitstimes-bloomberg-1110'] * 3,
  ["We all obviously have questions, but I'm not going to weigh in on any substance", 'we need to hear from the Federal Bureau of Investigation', 'met on Nov 9 behind closed doors for a security briefing']),
 # ---- the 54 pages saved by hand on Nov 16: a remark of an actor already drawn that two counted articles carry and no chip did
 ('stapp', '2026-11-11', 'Tells the FT: "People in San Francisco are thinking ... \'we know that he had an affair, and he apologised, now it\'s time to move on\'"; "DC is not going to let it move on"',
  ['man-ft-1112-03'] * 3, ['said Alec Stapp, co-founder of the Institute for Progress, a Washington tech policy think-tank', 'DC is not going to let it move on', 'Published NOV 11 2026']),
 # ---- added after the fourteenth reading (Nov 16, 2026). It found two acts in the census reading of the recovered live pages that no chip carried; the register of
 # remarks only lists a QUOTED remark that two pages give in the same words, so an act that two articles report in different words was not in it. A second
 # gauge (scripts/nv8_actor_days.py: a drawn actor, a day, dated lines of the census in two or more counted articles, no chip that day) found these eight.
 ('meeks', '2026-11-12', 'Tells reporters there is "no question" that Democrats should investigate Huang; asked whether Commerce officials should testify: "If it\'s up to me, I\'m going to at least have some questions or some hearings"; Cointelegraph: he "was considering forming a subcommittee to investigate the matter when the new Congress convenes in January"',
  ['huffpost-live', 'sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cointelegraphcom-04'],
  ['told reporters Thursday there’s “no question” that Democrats should investigate Huang', "If it's up to me, I'm going to at least have some questions or some hearings", 'When asked if Commerce Secretary Howard Lutnick or Under Secretary Jeffrey Kessler should be called to testify', 'Rep. Gregory Meeks, the top Democrat on the House Foreign Affairs Committee, said he was considering forming a subcommittee to investigate the matter when the new Congress convenes in January.']),
 ('justice', '2026-11-12', 'Attorney General Blanche tells reporters, of the woman in the reports, that there are "no conclusions reached by the Department of Justice, or by me, or by [FBI] Director Patel around who she is or is not"; that she is a spy is "something I have never said and that I don\'t know to be true"; says "of course" the FBI is investigating the reports',
  ['art-fc-cnn-1112', 'man-ft-1112-05', 'man-e8a4f78b0d7e', 'man-e8a4f78b0d7e'],
  ['no conclusions reached by the Department of Justice, or by me, or by [FBI] Director Patel around who she is or is not', 'something I have never said and that I don’t know to be true',
   '"of course" the FBI was investigating reports', 'Todd Blanche said on Thursday that the Justice Department has not yet reached a conclusion']),
 ('justice', '2026-11-12', 'Bloomberg, as Quartz relays it: the department "is examining whether entities tied to Alice Huang ... had a hand in attempts to smuggle Super Micro Computer\'s products into China"; the U.S. attorney\'s office in Manhattan leads; the department and that office had no comment. Quartz adds that Jensen Huang "is not a target of U.S. law enforcement probes", and that it "remains uncertain" whether the inquiry connects to any smuggling prosecution and what part Alice Huang or her entities had. Reuters, as the Star-Advertiser carries it: a spokesperson for that office "declined to comment on the Bloomberg report"',
  ['sw-qzcom-3e59440e', 'sw-qzcom-3e59440e', 'sw-qzcom-3e59440e', 'sw-qzcom-3e59440e', 'sw-ensedailycom-9e6f248e', 'sw-qzcom-3e59440e', 'sw-qzcom-3e59440e', 'sw-staradvertisercom-efab8d8f'],
  ['The Justice Department is examining whether entities tied to Alice Huang', "had a hand in attempts to smuggle Super Micro Computer's products into China, according to Bloomberg", "The U.S. attorney's office in Manhattan is leading the scrutiny, according to Bloomberg", "Representatives for the Justice Department and the U.S. attorney's office in Manhattan likewise had no comment", 'Bloomberg reported on Nov. 12 local time', 'Jensen Huang is not a target of U.S. law enforcement probes', 'It remains uncertain whether the inquiry connects to any of the chip smuggling prosecutions launched in the U.S. or Asia, and what part Alice Huang or her entities might have had in the alleged smuggling', "A spokesperson for the Manhattan U.S. Attorney's office declined to comment on the Bloomberg report"]),
 ('huang', '2026-11-09', 'Pulls out of speaking engagements at the ElevenLabs Summit and the Anthropic CEO Forum, in TechCrunch\'s timeline; Business Insider, as The Coin Republic relays it, dates the withdrawal to Nov 9',
  ['sw-techcrunchcom-08', 'sw-techcrunchcom-08', 'sw-thecoinrepubliccom-01'],
  ['The Nvidia CEO pulled out of upcoming speaking engagements at the ElevenLabs Summit and Anthropic CEO Forum', 'November 9, 2026: Huang pulls out of various speaking engagements',
   'Business Insider reported that he withdrew from Anthropic’s executive forum and the ElevenLabs New York summit on November 9']),
 ('musk', '2026-11-08', 'Replies "I agree" to Shaun Maguire\'s post that Huang is "irreplaceable for America\'s AI leadership"; the FT: he "backed Huang"',
  ['man-wapo-1112-02', 'man-wapo-1112-02', 'man-ft-1109-04'],
  ['“I agree,” replied Elon Musk', 'I believe Jensen is irreplaceable for America’s AI leadership', 'Elon Musk on Sunday backed Huang, saying he was irreplaceable for US AI leadership']),
 ('jcramer', '2026-11-12', 'On CNBC after the announcement: "It had to happen. There\'s way too much evidence"; of the interim chief: "I think she\'s going to be terrific in trying to figure out where the pieces are"; he rejects the idea that the company\'s other employees have no bearing on its future: "I think that\'s just not true"; CNBC\'s report adds his investing club\'s guidance, "We don\'t want to step in to buy the stock into this scandal-driven sell-off, but we\'re not giving up on the company either", and that he suggested the company preannounce its results',
  ['sw-cnbccom-23', 'sw-cnbccom-23', 'sw-cnbccom-23', 'sw-cnbccom-23', 'sw-cnbccom-23', 'sw-cnbccom-23'],
  ['"It had to happen. There\'s way too much evidence," Jim said', "I think she's going to be terrific in trying to figure out where the pieces are", 'Jim Cramer said Thursday', "there's 42,000 other people there who have no baring whatsoever because of the way the company was set up by Jensen. I think that's just not true,", "We don't want to step in to buy the stock into this scandal-driven sell-off, but we're not giving up on the company either", 'Jim suggested the company should preannounce its results']),
 ('warren', '2026-11-08', 'On CBS, as Yahoo Finance quotes her: "on the chipmaker specifically, this is an issue where we have substantial bipartisan support in the Banking Committee ... I\'m on bipartisan bills in order to put more restraints on the ability to export our chips to China"',
  ['sw-financeyahoocom-11', 'sw-financeyahoocom-11', 'man-politico-1109-01'],
  ['said Sunday on CBS that "on the chipmaker specifically, this is an issue where we have substantial bipartisan support in the Banking Committee', "I'm on bipartisan bills in order to put more restraints on the ability to export our chips to China", 'said Sunday on CBS that there is “substantial bipartisan support” on the committee']),
 ('trump', '2026-11-05', 'Axios, as CNBC relays it: at the meeting where Bessent pressed Lutnick, with Cabinet officials backing the export controls, he says "Let\'s get it done"; Implicator, citing Axios too: he had signed off on such curbs three times. A Commerce spokeswoman tells CNBC Bessent and Lutnick had "no such conversation"; Implicator notes that the denial "did not address the three approvals or the Oval Office meeting"',
  ['sw-cnbccom-22', 'sw-cnbccom-22', 'sw-implicatorai-04', 'sw-cnbccom-22', 'sw-implicatorai-04'],
  ['Trump said, "Let\'s get it done," but Lutnick has continued to delay, Axios reported', 'in the White House Situation Room last Thursday',
   'Trump signed off three times on curbs against suspected Nvidia chip diversion to China, most recently in the Oval Office on Nov. 5',
   'Commerce Department spokeswoman Kristen Eichamer told CNBC that Bessent and Lutnick had "no such conversation"', 'The denial did not address the three approvals or the Oval Office meeting']),

 # Added 2026-11-16 after reading the 31 actor-days that one counted article carries and the quoted remarks in two or more articles that no chip carried
 # (scripts/nv8_actor_days.py, scripts/nv8_remarks_no_chip.py). MA175 to MA187.
 ('trump', '2026-11-12', 'In a podcast interview released that day, asked whether Huang should have resigned: "The big thing is, was the woman a spy? And I don\'t know if that\'s been determined yet. But if the woman was a spy, yes. If the woman was not a spy, perhaps it would be different"; says he spoke to Huang on Wednesday',
  ['man-e8a4f78b0d7e', 'man-e8a4f78b0d7e', 'man-e8a4f78b0d7e', 'art-fc-cnn-1112'],
  ['asked in an interview released later on Thursday whether Huang should have resigned', 'The big thing is, was the woman a spy? And I don\'t know if that\'s been determined yet. But if the woman was a spy, yes. If the woman was not a spy, perhaps it would be different',
   'adding that he spoke to Jensen Huang on Wednesday', 'President Donald Trump also hedged Thursday on whether the US had determined she was a spy']),
 ('musk', '2026-11-05', 'Axios, as Implicator relays it from unnamed sources: the president called him from the Oval Office before deciding, and he "supported imposing the controls"',
  ['sw-implicatorai-04', 'sw-implicatorai-04', 'sw-implicatorai-04', 'sw-gizmodocom-08'],
  ['Trump called tech adviser Elon Musk, who supported imposing the controls', 'At the Nov. 5 Situation Room meeting', 'The meeting account rests on six anonymous high-level sources', 'even called up Elon Musk before making a decision']),
 ('greer', '2026-11-05', 'Axios, as CNBC relays it: was in the Situation Room when Bessent pressed Lutnick and, with other Cabinet officials, "supported the controls". A Commerce spokeswoman tells CNBC Bessent and Lutnick had "no such conversation"',
  ['sw-cnbccom-22', 'sw-cnbccom-22', 'sw-cnbccom-22'],
  ['Axios reported that Greer was present in the White House Situation Room last Thursday', 'Greer and other Cabinet officials supported the controls', 'Commerce Department spokeswoman Kristen Eichamer told CNBC that Bessent and Lutnick had "no such conversation"']),
 ('rubio', '2026-11-05', 'Axios, as Gizmodo relays it: was at the Situation Room meeting and "on Bessent\'s side for a more strict approach to exports". Gizmodo adds that the administration denied to Axios and the Times that the confrontation took place',
  ['sw-gizmodocom-08', 'sw-gizmodocom-08', 'sw-gizmodocom-08', 'sw-implicatorai-04'],
  ['U.S. Trade Representative Jamieson Greer, and Secretary of State Marco Rubio', 'all of whom were on Bessent\'s side for a more strict approach to exports', 'denied to both Axios and the Times that any such confrontation between Bessent and Lutnick had ever taken place', 'At the Nov. 5 Situation Room meeting']),
 ('nvidia', '2026-11-06', 'A spokesman tells the Times the company does not share classified information with its customers, and that customers do not ask it to press the government to change its policies on chip sales to China; China has "consistently promoted its own domestic alternatives in China, including Huawei, and strictly limited imports of our data center products". To the FT, for its report of that day, the company "declined to comment on the government memo and the assertions that its chief executive had an intimate relationship with Alice Huang". The FT adds that the company "has previously said" he meets "thousands of customer executives every year"; NBC\'s account of Nov 8 gives those words as part of its response to the FT',
  ['man-nyt-1106-01', 'man-nyt-1106-01', 'man-nyt-1106-01', 'man-ft-1107-01', 'nbc-1108-investigation'],
  ['said that the company does not share classified information with its customers', 'customers do not ask Nvidia to press the U.S. government to change its policies on chip sales to China', 'consistently promoted its own domestic alternatives in China, including Huawei, and strictly limited imports of our data center products', 'Nvidia declined to comment on the government memo and the assertions that its chief executive had an intimate relationship with Alice Huang', 'Nvidia declined to comment and said Jensen Huang meets "thousands of customer executives every year,"']),
 ('embassy', '2026-11-06', 'Its spokesman tells the Times its reporting is "unsubstantiated" and "nothing but smears against China"',
  ['man-nyt-1106-01', 'man-nyt-1106-01'], ['a spokesman for the Chinese embassy, said The Times reporting was "unsubstantiated"', 'nothing but smears against China']),
 ('cramer', '2026-11-12', 'CBS reports that he said on CNBC, moments before the resignation was announced, that he would happily support subpoenaing Huang, and that his spokesperson said afterwards he still would',
  ['sw-cbsnewscom-e684eb4c', 'sw-cbsnewscom-e684eb4c'],
  ['said on CNBC on Thursday that he would happily support subpoenaing Huang moments before Nvidia announced his resignation', 'A Cramer spokesperson said he would still support subpoenaing the tech founder']),
 ('banks', '2026-11-11', 'Posts, as Yahoo Finance quotes it: "President Trump has been clear: he wants to prohibit advanced Nvidia Blackwell chips from going to China. Allowing Chinese companies to use these chips through the cloud undermines the President\'s policy"',
  ['sw-financeyahoocom-d2842b9f', 'sw-financeyahoocom-d2842b9f', 'sw-financeyahoocom-d2842b9f'],
  ['President Trump has been clear: he wants to prohibit advanced Nvidia Blackwell chips from going to China', "Allowing Chinese companies to use these chips through the cloud undermines the President's policy", 'posted to X on Wednesday']),
 ('cornyn', '2026-11-09', 'A post dated Nov 9 where a blog embeds it: "Did FBI do defensive briefing?"',
  ['sw-joemygodcom-01', 'sw-joemygodcom-01'], ['Did FBI do defensive briefing?', 'Senator John Cornyn (@JohnCornyn) November 9, 2026']),
 ('cornyn', '2026-11-10', 'Tells the Washington Sun that Congress "absolutely" has a role in investigating the matter: "What I would be interested in is whether the FBI gave him a defensive briefing"',
  ['sw-washingtonsuncom-02', 'sw-washingtonsuncom-02', 'sw-washingtonsuncom-02'],
  ['has a role in investigating the matter, pointing to the Senate Intelligence Committee', 'What I would be interested in is whether the FBI gave him a defensive briefing', 'Several Republicans told The Washington Sun on Tuesday']),
 ('globaltimes', '2026-11-10', 'A commentary of Nov 10, "Jensen Huang Probe: Counterintelligence or Political Witch Hunt?", as the Seoul Economic Daily relays it: the reporting rests on anonymous sources and unverified material; "You cannot build next-generation graphics processing units on suspicion alone"',
  ['sw-ensedailycom-13', 'sw-ensedailycom-13', 'sw-ensedailycom-13'],
  ['In a commentary on the 10th headlined "Jensen Huang Probe: Counterintelligence or Political Witch Hunt?"', 'saying it rested on anonymous sources and material that the media themselves had been unable to verify', 'You cannot build next-generation graphics processing units on suspicion alone']),
 ('himes', '2026-11-09', 'Statement after the classified briefing of that day, in CNN\'s report: "We are aggressively pursuing more information to understand what happened and whether the decision-making process to export chips was improperly influenced or compromised"',
  ['ms-gap-whitehouse-cnn-trip-20261109-92bd36', 'ms-gap-whitehouse-cnn-trip-20261109-92bd36', 'sw-madrobotblog-01', 'ms-gap-whitehouse-cnn-trip-20261109-92bd36'],
  ['We are aggressively pursuing more information to understand what happened and whether the decision-making process to export chips was improperly influenced or compromised', 'said in a statement', 'whether the decision-making process to export chips was improperly influenced or compromised', 'lawmakers indicated afterward they still had more questions than answers']),
 ('warren', '2026-11-09', 'Posts: "NVIDIA\'s CEO just confirmed a relationship with a suspected Chinese spy. Congress is back today. We have legislation ready to go to stop advanced AI chips from fueling China\'s military"',
  ['sw-cnbccom-02', 'sw-cnbccom-02', 'sw-cnbccom-02'],
  ['NVIDIA\'s CEO just confirmed a relationship with a suspected Chinese spy', 'posted on X Monday morning', 'Congress is back today. We have legislation ready to go to stop advanced AI chips from fueling China\'s military']),
 # Added 2026-11-16 in answer to the fifteenth reading (lane audit_nv8_s8i) and under one rule for refusals to comment. MA188 to MA196.
 ('china', '2026-11-10', 'At the ministry\'s press conference, asked whether the two presidents will discuss the allegations: "the two sides are in communication regarding interactions between the two heads of state within the year", and "we\'ve stated China\'s position on multiple occasions"; asked about Alice Huang\'s citizenship and whereabouts: "We responded to that yesterday", and the allegation "is purely unsubstantiated and directed at smearing China"',
  ['art-fc-rec-fmprc-1110', 'art-fc-rec-fmprc-1110', 'art-fc-rec-fmprc-1110', 'art-fc-rec-fmprc-1110'],
  ["we've stated China's position on multiple occasions", 'We responded to that yesterday. The "Chinese spy" allegation is purely unsubstantiated and directed at smearing China', 'Regular Press Conference on November 10, 2026', 'the two sides are in communication regarding interactions between the two heads of state within the year']),
 ('rubio', '2026-11-09', 'Asked again about Huang and how important a thorough investigation is: "I\'m not going to comment on an internal corporate matter for them"; asked whether he sees a national security concern: "I\'m just not going to comment on it"; of the travel to China: "you\'ll have to ask the White House", "I don\'t handle the - that part of our operation". The republished transcript is titled 10 November and stamped the evening of Nov 9, Eastern time',
  ['art-fc-rec-mirage-rubio-1110', 'art-fc-rec-mirage-rubio-1110', 'art-fc-rec-mirage-rubio-1110', 'art-fc-rec-mirage-rubio-1110', 'art-fc-rec-mirage-rubio-1110', 'art-fc-rec-mirage-rubio-1110'],
  ["I'm not going to comment on an internal corporate matter for them, so I'm just not going to comment on that topic", "I'm just not going to comment on it", '10 Nov 2026 10:48 am AEDT', 'Rubio Speaks to Press as Secretary of State 10 November', "you'll have to ask the White House", "I don't handle the - that part of our operation"]),
 ('nvidia', '2026-11-12', "A spokesperson clarifies, in NBC's report of the resignation, that Huang will not be working with Nvidia in any capacity going forward",
  ['sw-nbcnewscom-03'],
  ['A company spokesperson clarified that Huang will not be working with Nvidia in any capacity going forward']),
 ('musk', '2026-11-12', 'CNBC reports that, before the resignation, he agreed with an investment manager\'s post that "Nvidia\'s board should wait for the results of the investigation before ousting Jensen"',
  ['sw-cnbccom-09', 'sw-cnbccom-09'],
  ['Before Jensen Huang resigned from Nvidia, SpaceX and Tesla CEO Elon Musk said', 'who wrote in a post on X that "Nvidia\'s board should wait for the results of the investigation before ousting Jensen."']),
 ('coons', '2026-11-12', 'As Yahoo Finance quotes him: Huang "has spent years lobbying Trump to allow advanced AI chip sales to China ... Now, serious questions are emerging about his ties to an alleged Chinese spy and what Trump knew. Congress needs answers, and Americans deserve better national security protections"',
  ['sw-financeyahoocom-d2842b9f', 'sw-financeyahoocom-d2842b9f', 'sw-financeyahoocom-d2842b9f'],
  ['NVIDIA CEO Jensen Huang has spent years lobbying Trump to allow advanced AI chip sales to China', 'Now, serious questions are emerging about his ties to an alleged Chinese spy and what Trump knew. Congress needs answers, and Americans deserve better national security protections', 'said on Thursday']),
 ('whitehouse', '2026-10-29', 'With the CIA and the National Security Agency, declines to comment to the Times for its first report',
  ['man-nyt-1029-01'],
  ['The White House, the C.I.A. and the National Security Agency all declined to comment']),
 ('whitehouse', '2026-11-06', 'With the CIA, declines to comment to the Times and to the FT for their reports of the memo',
  ['man-nyt-1106-01', 'man-ft-1107-01'],
  ['Spokeswomen for the White House and C.I.A. declined to comment', 'The White House and CIA declined to comment']),
 ('nvidia', '2026-11-11', 'Declines to give the Times a statement for its report of a second relationship; declines to comment for another Times article and for an FT report of that day',
  ['man-e1161e38dc19', 'man-441e3f343197', 'man-ft-1112-03'],
  ['Nvidia declined to provide a statement', 'Nvidia declined to comment and Ms. Huang did not respond to a request for comment', 'Nvidia declined to comment']),
 ('commerce', '2026-11-10', 'Tells the FT it does not comment on internal discussions about the entity list; the department says it has "enforced aggressively across the board, including on smuggling advanced chips" and cites six investigations with "criminal charges against 17 defendants"',
  ['man-ft-1110-02', 'man-ft-1110-02', 'man-ft-1110-02'],
  ['which said it did not comment on internal discussions about the entity list', 'it said it had "enforced aggressively across the board, including on smuggling advanced chips"', 'criminal charges against 17 defendants involving billions of dollars of smuggled chips']),
 # Added 2026-11-16 in answer to the sixteenth reading (lane audit_nv8_s8j): refusals to comment under one rule for every actor (MA197 to MA208) and eight acts (MA209 to MA216).
 ('nvidia', '2026-11-09', 'At its event in Seoul that day, asked about the investigation and Korea\'s chip purchases, declines to comment: "Those questions don\'t seem to be related to today\'s event" (Asia Economy). A spokesman declines to comment to the Times, which asked on Monday for its report on succession and the board. To the FT it declines to comment on remarks the paper attributes to its general counsel',
  ['sw-asiaecokr-04', 'sw-qzcom-04', 'man-ft-1109-04', 'man-nyt-1110-06'],
  ['NVIDIA declined to comment, saying, "Those questions don\'t seem to be related to today\'s event."', 'held an AI partnership event in Seoul on Monday', 'Nvidia declined to comment on the remarks', "None of Nvidia's board members responded to requests for comment on Monday, and a company spokesman declined to comment"]),
 ('nvidia', '2026-11-10', 'Declines to comment to the Times for its profile of Alice Huang',
  ['art-fc-bs-nyt-1110-woman'],
  ['Nvidia and Megaspeed declined to comment']),
 ('nvidia', '2026-11-12', 'Has declined to say how Megaspeed\'s sales were classified after it changed how it reports revenue by country, in the Journal\'s account; Implicator adds that the filings "do not establish a connection between the reporting change and the block". Declines to comment to the FT, the Journal and Reuters for other reports of that day',
  ['man-wsj-1112-02', 'sw-implicatorai-06', 'sw-implicatorai-06', 'man-50c4c8f67531', 'art-fc-tovima-wsj-1112-kangwei', 'man-08b0429539bf'],
  ["Nvidia has declined to say how Megaspeed's sales were classified or whether the two moves were related", 'A spokesman declined to say where Megaspeed sales were classified under either method', 'The filings do not establish a connection between the reporting change and the block', 'Nvidia declined to comment', 'Nvidia declined to comment', 'Nvidia declined to comment']),
 ('whitehouse', '2026-11-08', "A spokeswoman declines to comment to the Times for its report on the secretary of state's memo",
  ['man-nyt-1108-02'],
  ['A State Department spokesman and a White House spokeswoman declined to comment']),
 ('rubio', '2026-11-08', 'A State Department spokesman declines to comment to the Times for its report on his memo',
  ['man-nyt-1108-02'],
  ['A State Department spokesman and a White House spokeswoman declined to comment']),
 ('whitehouse', '2026-11-10', 'Declines to comment to the FT for its report on the entity list. For the Times\'s report that the president was told of the concerns on his trip to China, its press office declines to comment on the record and emails a statement on background that points to the president\'s remarks of Monday and disputes the reporting, "without elaborating". Asked by Newsweek whether the president would expand on his remarks, the press office refers it to his comments at Monday\'s briefing',
  ['man-ft-1110-02', 'man-nyt-1110-02', 'man-nyt-1110-02', 'man-nyt-1110-02', 'sw-newsweekcom-01'],
  ['The energy department referred questions to the White House, which declined to comment', 'Asked to comment, the White House press office declined to do so on the record', "Instead, the office emailed a statement on background that pointed to Mr. Trump's remarks from Monday", 'The email disputed the reporting for this article, without elaborating', "The press office referred Newsweek to his comments at Monday's briefing"]),
 ('rubio', '2026-11-10', 'The State Department declines to comment to the Times for its report that the president was told of the concerns on his trip to China',
  ['man-nyt-1110-02'],
  ['The State Department declined to comment']),
 ('bessent', '2026-11-10', 'The Treasury Department declines to comment to the FT for its report on the entity list',
  ['man-ft-1110-02'],
  ['The Treasury department declined to comment']),
 ('justice', '2026-11-09', "A spokeswoman tells the Times the department does not comment on continuing investigations; it declines to comment to NBC, and the FBI declines to comment to AFP and to Semafor on the president's remark that it is looking into the matter",
  ['man-nyt-1109-03', 'sw-nbcnewscom-02', 'sw-thejournalie-03', 'sw-semaforcom-04'],
  ['A Justice Department spokeswoman said the agency does not comment on continuing investigations', 'The Justice Department also declined to comment on the matter', 'the FBI declined comment Monday', 'An FBI spokesperson declined to comment']),
 ('justice', '2026-11-10', 'The FBI declines to comment when the BBC asks, as a Ukrainian outlet relays it; Yahoo Finance also reports an FBI refusal, without saying who asked',
  ['sw-hromadskeua-02', 'sw-financeyahoocom-18'],
  ['The FBI declined to comment when contacted by the BBC', 'He gave no detail, and the FBI declined to comment']),
 ('commerce', '2026-11-11', 'Axios, as Implicator and CryptoNews relay it: beside her denial of the confrontation, the department\'s spokeswoman "would not immediately comment on the other allegations". The allegation, as Implicator gives Axios\'s report: the secretary "has held up chip export curbs President Trump approved three times this year"; Implicator adds that Commerce "says it uses the blacklist every day against bad actors"',
  ['sw-implicatorai-04', 'art-cryptonews-axios-crackdown', 'sw-implicatorai-04', 'sw-implicatorai-04'],
  ['The department would not immediately comment on the other allegations', 'Axios said she would not immediately comment on the other allegations', 'Commerce Secretary Howard Lutnick has held up chip export curbs President Trump approved three times this year, Axios reported Wednesday from six high-level sources.', 'Commerce says it uses the blacklist every day against bad actors.']),
 ('megaspeed', '2026-11-10', 'Declines to comment to the Times for its profile of Alice Huang',
  ['art-fc-bs-nyt-1110-woman'],
  ['Nvidia and Megaspeed declined to comment']),
 ('jones', '2026-11-12', 'In a note to employees: "The Board takes seriously our duty as stewards of this great company"; "I am confident that under Colette\'s leadership, with the full support of the Board, we will continue to grow our business"',
  ['sw-cnbccom-ca82d66d', 'sw-cnbccom-ca82d66d', 'sw-nbcnewscom-03'],
  ['The Board takes seriously our duty as stewards of this great company', "I am confident that under Colette's leadership, with the full support of the Board, we will continue to grow our business", "In a separate note to the company's workforce, Jones, the new chairman, wrote"]),
 ('mcguire', '2026-11-10', 'In a piece of the Council on Foreign Relations, where he is a fellow: Southeast Asia has become "a major hub for chip smuggling and export control circumvention"; of rules that would require licences, "the Department of Commerce is refusing to enforce them"; it should "impose new controls that ban Chinese companies from renting remote access to the AI chips that they are currently prohibited from purchasing"',
  ['sw-cfrorg-01', 'sw-cfrorg-01', 'sw-cfrorg-01'],
  ['a major hub for chip smuggling and export control circumvention', 'the Department of Commerce is refusing to enforce them', 'impose new controls that ban Chinese companies from renting remote access to the AI chips that they are currently prohibited from purchasing']),
 ('huang', '2026-11-09', 'Wired reports, as TechCrunch and SiliconANGLE relay it that day, that he hired a crisis-communications firm "at least a year before he publicly acknowledged" the relationship; CNBC, Nov 11: the firm he "reportedly hired as early as last year"',
  ['sw-techcrunchcom-06', 'sw-siliconanglecom-03', 'sw-cnbccom-06'],
  ['at least a year before he publicly acknowledged an extramarital affair', 'A report in Wired said today that the Nvidia boss has hired the services of a public relations firm called Heller that specializes in handling public scandals', 'the crisis PR firm Huang reportedly hired as early as last year']),
 ('huang', '2026-11-12', 'CNBC confirms a Times report that he has hired the law firm Paul Weiss: "It\'s not immediately clear what he will use its services for"',
  ['sw-cnbccom-09', 'sw-cnbccom-09', 'sw-staradvertisercom-efab8d8f'],
  ['Huang has hired the law firm Paul Weiss, CNBC confirmed', "It's not immediately clear what he will use its services for", 'It was not clear what the firm had been retained to do, the report said']),
 ('commerce', '2026-11-12', 'The Information, as CNBC relays it: the department "is finalizing a rule aimed at preventing Chinese AI firms from remotely accessing advanced chips through data centers in other countries"; Semafor, on Nov 10, links a report of The Information that the department "has reportedly begun readying a new set of semiconductor export controls"',
  ['sw-cnbccom-08', 'sw-qzcom-13', 'sw-semaforcom-05'],
  ['The Commerce Department is finalizing a rule aimed at preventing Chinese AI firms from remotely accessing advanced chips through data centers in other countries, according to The Information', 'The Commerce Department is finalizing a rule meant to stop Chinese AI firms from getting at advanced chips via overseas data centers', 'and the US Commerce Department has reportedly begun readying a new set of semiconductor export controls .']),
 ('commerce', '2026-11-10', 'Extends to Jan. 10 its pause on a rule that would stretch entity-list limits to companies majority-owned by listed firms. Yahoo Finance, on Nov 10, says it did so "On Monday" (Nov 9); Implicator dates it Nov 5',
  ['sw-financeyahoocom-16', 'sw-implicatorai-04'],
  ['On Monday, Commerce extended its pause on a rule that would stretch those limits to companies majority-owned by listed firms', 'Commerce pushed back to Jan. 10, 2027 a frozen rule that would have extended Entity List restrictions to any company at least 50% owned by a listed firm']),
 ('kress', '2026-11-12', 'CNBC, from a person familiar with the matter: she "will gather the company\'s executive team today" at headquarters to "discuss leadership and continuity plans"',
  ['sw-cnbccom-09', 'sw-cnbccom-09', 'sw-staradvertisercom-efab8d8f'],
  ["Interim CEO Colette Kress will gather the company's executive team today at the chipmaker's headquarters", 'Kress will discuss leadership and continuity plans with the group of high-level executives', "Kress was gathering Nvidia's executive team at its headquarters today, CNBC reported"]),
 ('blumenthal', '2026-11-05', 'CNBC reports that he "re-upped his warning" that Thursday, in its account of his questions to Huang about Nvidia\'s donation to the White House ballroom and its White House contacts; it gives no words of the warning',
  ['sw-cnbccom-02', 'sw-cnbccom-02'],
  ['Blumenthal re-upped his warning on Thursday', "who pressed Huang in November 2025 about Nvidia's ballroom donation and White House contacts"]),
 # answer to the sixteenth reading, second part (Nov 16): the refusal rule applied by the builder to the parties the reading did not list (Taiwan, the president; Singapore is on its own row above),
 # and Taiwan's other statements, which the gauges had not seen because the census names each official
 ('taiwan', '2026-10-30', 'Its representative office in Washington tells the Journal it "doesn\'t comment on specific intelligence or security matters"',
  ['art-fc-itiger-wsj-1030-v1', 'man-923fe8754943'],
  ["Taiwan's representative office in Washington said it doesn't comment on specific intelligence or security matters", "Taiwan's representative office in Washington said it doesn't comment on specific intelligence or security matters"]),
 ('taiwan', '2026-11-10', 'At the legislature its interior minister says "The national security authorities are actively investigating, and the Ministry of the Interior is cooperating" (Asia Economy, from a Taiwanese daily). Its premier declines to answer a question about Taiwan\'s part in the U.S. investigation; he says the government has records of her entries and exits and "would not say how many times she had visited" (Taiwan News)',
  ['sw-asiaecokr-07', 'sw-asiaecokr-07', 'sw-taiwannewscomtw-04', 'sw-taiwannewscomtw-04', 'sw-taiwannewscomtw-04', 'sw-taiwannewscomtw-04'],
  ['on November 10, Interior Minister Liu Shih-fang told reporters at the Legislative Yuan that day', 'The national security authorities are actively investigating, and the Ministry of the Interior is cooperating', 'said outside the legislature that security agencies were', 'On Tuesday, Premier Cho Jung-tai', 'declined to answer a question from KMT Legislator Lai Shyh-bao', 'Cho said the government had records of her entry and exit but would not say how many times she had visited Taiwan']),
 ('taiwan', '2026-11-10', "Its deputy foreign minister says she complied with entry rules and that the government is taking the necessary precautions, in Asia Economy's account of Nov 10; he declines to tell reporters under what status she entered, and adds that travellers who comply with the rules and have no criminal record in Taiwan would not face unnecessary restrictions (Taiwan News)",
  ['sw-asiaecokr-07', 'sw-asiaecokr-07', 'sw-taiwannewscomtw-04', 'sw-taiwannewscomtw-04'],
  ['said Alice Huang had complied with entry regulations but did not disclose the capacity in which she entered Taiwan', 'Chen said the Taiwanese government was taking the necessary precautionary measures', 'declined to tell reporters under what status Alice Huang entered Taiwan', 'He added that travelers who comply with regulations and have no criminal record in Taiwan would not face unnecessary restrictions']),
 ('taiwan', '2026-11-11', 'Its interior minister says she entered Taiwan several times on a Hong Kong passport, is not in Taiwan now, and that her entry permit has been revoked; that had the authorities known she was a spy they would not have let her in; and, as the Central News Agency quotes her, "the police administration will provide full assistance" under the security laws (NTD)',
  ['sw-ntdcom-2bcf3b6d', 'sw-ntdcom-2bcf3b6d', 'sw-ntdcom-2bcf3b6d', 'sw-ntdcom-2bcf3b6d'],
  ['Liu Shyh-fang stated on Wednesday that Alice Huang had entered Taiwan multiple times using a Hong Kong passport', 'Liu confirmed that Huang is not currently in Taiwan and that her entry permit has been revoked', 'the police administration will provide full assistance', 'they certainly would not have allowed her to enter']),
 ('taiwan', '2026-11-12', 'Its China-policy agency\'s spokesman, of a U.S. recommendation in 2024 to monitor her visits that the Times reported: "MAC has indeed never received such information"; the agency is not an intelligence agency, and "We are not sure whether other agencies received it"; without a lead, visitors get routine screening; it can neither confirm nor deny the allegations. The cabinet\'s spokesperson calls the case a cross-border cooperative investigation and declines to give details, citing the confidentiality of ongoing investigations; the immigration agency says it worked with security authorities to monitor her visits (Focus Taiwan)',
  ['art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112'],
  ['said Thursday it had received no information about a reported U.S. recommendation to monitor', 'MAC has indeed never received such information', 'We are not sure whether other agencies received it', 'the case involved a cross-border cooperative investigation, but declined to disclose details, citing the confidentiality of ongoing investigations', "the agency had worked with national security authorities to monitor Alice Huang's visits to Taiwan", 'Liang said MAC was not an intelligence agency', 'Without such information, applicants generally undergo routine screening', 'MAC could neither confirm nor deny the espionage allegations against Alice Huang']),
 ('trump', '2026-11-09', 'Asked whether he knew of the concerns when Huang flew with him to China in May: "No, I didn\'t hear about it then"; pressed on whether he had been briefed a year earlier: "I\'d certainly check with the intelligence people. They could have been mentioned. Certainly, it didn\'t make much of an impact on me" (the Times). The Journal: he "declined to provide a detailed explanation of when he learned about the federal government\'s concerns"',
  ['man-nyt-1109-01', 'man-nyt-1109-01', 'man-nyt-1109-01', 'man-wsj-1109-09', 'man-wsj-1110-04'],
  ['On Monday, Mr. Trump said that he did not recall receiving the information', "No, I didn't hear about it then", "Certainly, it didn't make much of an impact on me", "declined to provide a detailed explanation of when he learned about the federal government's concerns", "declined to provide a detailed explanation of when he learned about the federal government's concerns"]),
 # found when the gauges were given the speaker labels their list lacked (Nov 16)
 ('openai', '2026-11-09', 'Its board chairman, who also runs an AI startup, on CNBC, as Yahoo Finance quotes him: "AI is not particularly popular right now in this country"; "So I think this just introduces even more risk"',
  ['sw-financeyahoocom-16', 'sw-financeyahoocom-16', 'sw-financeyahoocom-16'],
  ["Bret Taylor, OpenAI's chairman and CEO of AI startup Sierra, told Bosa on the same show", 'So I think this just introduces even more risk', 'told Deirdre Bosa on Monday']),
 # from reading the quoted remarks that the register had set aside (Nov 16): parts of statements already drawn that no chip carried
 ('trump', '2026-11-08', 'Also that Sunday: "I have not spoken to him about it. I just know he\'s a fine person, but you never know what is going on" (FT); asked whether Huang would take part in the coming summit in China: "I don\'t know, but I\'d certainly take him" (Al Jazeera); "I haven\'t heard he\'s done anything wrong. He dealt with somebody, but you know, so does everybody else" (the Times)',
  ['man-ft-1109-05', 'man-ft-1109-05', 'aljazeera-1112-board', 'aljazeera-1112-board', 'man-nyt-1108-01', 'man-nyt-1108-01', 'man-nyt-1108-01'],
  ['Asked about Huang on Sunday', "I have not spoken to him about it. I just know he's a fine person, but you never know what is going on", 'Asked on Sunday whether Huang would take part in the summit', "I don't know, but I'd certainly take him", "I haven't heard he's done anything wrong", 'so does everybody else', 'In a brief comment to reporters on Sunday evening']),
 ('trump', '2026-11-09', 'Says Huang will not accompany him to China the next week and that he does not plan to raise the matter with Xi (the Times); of Huang\'s denial: "I really believe him" (FT); of when he learned of the concerns: "Not too long ago" (the Journal)',
  ['man-nyt-1110-02', 'man-nyt-1110-02', 'man-ft-1109-04', 'man-wsj-1109-09'],
  ['on Monday he said the Nvidia executive will not accompany him on the trip', 'The president said he did not plan to raise the matter with Mr. Xi', 'I really believe him', 'Not too long ago']),
 ('nvidia', '2026-10-29', 'In its statement to several outlets that day: "We\'re confident that if the U.S. government believes that any person is a threat to American industry, it would let us know"; "We often receive updates from the U.S. government regarding parties and entities of concern and always act accordingly" (Tom\'s Hardware); the spokesperson adds, in CNBC\'s account, that customers do not get access to its trade secrets or to relevant national security information',
  ['sw-tomshardwarecom-09', 'sw-tomshardwarecom-09', 'cnbc-1029-nvidia-responds', 'cnbc-1029-nvidia-responds'],
  ["We're confident that if the U.S. government believes that any person is a threat to American industry, it would let us know", 'We often receive updates from the U.S. government regarding parties and entities of concern and always act accordingly', 'confident that if the U.S. government believes', "The spokesperson added that customers don't get access to Nvidia trade secrets or relevant national security information"]),
 ('huang', '2026-11-08', 'In the same memo: "I am committed to protecting Nvidia and supporting America\'s national security"; and, as the Times quotes its end: "My family bears no responsibility for my choices. I do"',
  ['sw-foxbusinesscom-01', 'sw-euronewscom-01', 'man-441e3f343197'],
  ["I am committed to protecting Nvidia and supporting America's national security", "I am committed to protecting Nvidia and supporting America's national security", 'My family bears no responsibility for my choices. I do']),
 ('board', '2026-11-12', 'In the release on the resignation: "Jensen\'s contributions to NVIDIA are profound"; "The Board and the company thank Jensen for his immeasurable contributions to the company and the industry"',
  ['sw-cnbccom-09', 'sw-deadlinecom-02'],
  ['The Board and the company thank Jensen for his immeasurable contributions to the company and the industry', 'The Board and the company thank Jensen for his immeasurable contributions to the company and the industry']),
 ('megaspeed', '2026-11-12', 'In a statement on its site: it "has retained a leading U.S. law firm to lead a comprehensive census of its graphics processing units (GPUs) and independently verify its export control compliance practices", and "welcomes appropriate government scrutiny"; it says it "stands ready to cooperate fully with any other relevant U.S. government authority" and "is committed to working constructively and transparently with the U.S. government"',
  ['art-fc-rec-megaspeed-home', 'art-fc-rec-megaspeed-home', 'sw-qzcom-13', 'art-fc-rec-megaspeed-home', 'art-fc-rec-megaspeed-home'],
  ['Megaspeed has retained a leading U.S. law firm to lead a comprehensive census of its graphics processing units (GPUs) and independently verify its export control compliance practices', 'Megaspeed welcomes appropriate government scrutiny', 'The company said Thursday that it had assisted inspectors', 'stands ready to cooperate fully with any other relevant U.S. government authority', 'Megaspeed is committed to working constructively and transparently with the U.S. government']),
 ('mcguire', '2026-11-08', 'In the same post: "The biggest problem remains unaddressed"; "it is even more important that the Department of Commerce tighten up export controls to prevent things like this from ever happening again"',
  ['x-mcguire-nov8', 'x-mcguire-nov8'],
  ['The biggest problem remains unaddressed', 'it is even more important that the Department of Commerce tighten up export controls to prevent things like this from ever happening again']),
 ('schumer', '2026-11-12', 'In the same post: "The Trump administration must also answer for what it did once it learned about Mr. Huang\'s relationship with a suspected Chinese intelligence asset"; "What did Trump know when he personally invited Mr. Huang aboard Air Force One?"',
  ['cnn-1111-live', 'cnn-1111-live'],
  ["The Trump administration must also answer for what it did once it learned about Mr. Huang's relationship with a suspected Chinese intelligence asset", 'What did Trump know when he personally invited Mr. Huang aboard Air Force One?']),
 ('jeffries', '2026-11-09', 'To reporters that Monday, in Semafor\'s account: he "strongly supports" the Senate\'s provisions for stricter chip export controls in the defense bill, and "We\'re going to work hard to make sure that those provisions make it into the final version"',
  ['sw-semaforcom-04', 'sw-semaforcom-04', 'art-line-straitstimes-bloomberg-1110'],
  ['the stricter chip export control provisions that the Senate has already advanced in its annual defense policy bill', "We're going to work hard to make sure that those provisions make it into the final version", 'make sure that those provisions make it into the final version of the National Defense Authorization Act']),
 ('whitehouse', '2026-11-12', 'A White House official tells CNN that the president "maintains complete confidence in the secretary and his ability to carry out the position"',
  ['cnn-1111-live', 'cnn-1111-live'],
  ['a White House official told CNN on Thursday', 'President Trump maintains complete confidence in the secretary and his ability to carry out the position']),
 ('warren', '2026-11-11', 'The letter with Coons says reports suggest that officials at the White House, the State Department and Commerce "were aware of concerns about NVIDIA" and "did not move to block the continued flow of advanced AI chips"; it asks that Congress be briefed on the risks',
  ['cnn-1111-live', 'cnn-1111-live', 'cnn-1111-live'],
  ['were aware of concerns about NVIDIA, its relationship with', 'yet did not move to block the continued flow of advanced AI chips', 'They also asked the officials to brief Congress on what risks']),
 ('moolenaar', '2026-11-11', 'Tells CNBC, in a broadcaster\'s report of Nov 11, that he has three main questions (what was shared with the suspected spy, whether Huang was influenced by her, whether Chinese buyers were favoured); the access Huang allowed "could have been leveraged at any point by the CCP"',
  ['sw-cbsaustincom-04', 'sw-cbsaustincom-04'],
  ['said he has three main questions', 'could have been leveraged at any point by the CCP']),
 # answer to the seventeenth reading (Nov 16): acts and parts of statements it found on no chip
 ('taiwan', '2026-11-12', 'The head of its China-policy agency tells lawmakers she entered Taiwan three times in 2024 and five times in 2025, with no recorded visit this year, as a Hong Kong resident on business, and was not specially flagged during those visits (Focus Taiwan)',
  ['art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112', 'art-fc-rec-focustaiwan-1112'],
  ['told lawmakers that Alice Huang had entered Taiwan three times in 2024 and five times in 2025, with no recorded visits this year', 'had not been specially flagged during those visits', 'Earlier Thursday']),
 ('taiwan', '2026-11-12', 'Its science minister, in Taiwan News: "an isolated incident" should have no real impact on Taiwan\'s AI development',
  ['sw-taiwannewscomtw-06', 'sw-taiwannewscomtw-06'],
  ["shouldn't have any real impact on Taiwan's AI development", 'of the National Science and Technology Council echoed the sentiment']),
 ('megaspeed', '2026-11-09', 'A representative tells the Times, for its report of an inquiry, that the company is conducting an internal investigation into allegations of chip diversion and has repeatedly offered to cooperate with the U.S. government, and that those offers have gone unanswered',
  ['man-nyt-1109-03'],
  ['A representative for Megaspeed said the company was conducting an internal investigation into allegations of chip diversion and had repeatedly offered to cooperate with the U.S. government but that those offers had gone unanswered']),
 ('commerce', '2026-11-07', 'A spokesman for its export bureau tells the Times, for its report on licences for chip sales to Chinese firms, that it carefully reviews all applications for national security risks; the agency says it imposed $324 million of penalties for export violations in 2025 and hired more than 90 officers this year',
  ['man-nyt-1107-01', 'man-nyt-1107-01'],
  ['said it carefully reviews all applications for national security risks', 'it had imposed $324 million of penalties on companies for export violations in 2025 and hired more than 90 officers this year']),
 ('nvidia', '2026-11-07', 'A spokesman tells the Times, for its report on licences for chip sales to Chinese firms: "it makes no sense for the Chinese military to depend on American technology"; Nvidia sells "the first, best and most of our technology in America"; and China has strictly limited imports of the chip',
  ['man-nyt-1107-01', 'man-nyt-1107-01', 'man-nyt-1107-01'],
  ['it makes no sense for the Chinese military to depend on American technology', 'the first, best and most of our technology in America', 'the Chinese government has strictly limited imports of the H200']),
 ('nvidia', '2026-11-05', 'In the same statement, to CNBC: "We\'re confident that if the U.S. government believes that any person is a threat to American industry, it would let us know"',
  ['cnbc-1105-asked-to-brief', 'cnbc-1105-asked-to-brief'],
  ["We're confident that if the U.S. government believes that any person is a threat to American industry, it would let us know", 'Nvidia instead provided a statement that largely mirrored the one it previously sent the Times']),
 ('huang', '2026-11-09', 'By the president\'s account that Monday, tells him by phone that he "had absolutely no idea that the person in question was a spy"',
  ['abc-subpoena', 'man-nyt-1109-01'],
  ['he had absolutely no idea that the person in question was a spy', 'I did speak to him today']),
 ('jones', '2026-11-12', 'In the release on the appointment: "The Board has full confidence in Colette and the leadership team, and we expect the company\'s operations, customer commitments and product roadmap to continue without interruption"',
  ['sw-cnbccom-09', 'man-ft-1112-05', 'sw-nvidianewsnvidiacom-02'],
  ['The Board has full confidence in Colette and the leadership team', 'The Board has full confidence in Colette and the leadership team', "The Board has full confidence in Colette and the leadership team, and we expect the company's operations, customer commitments and product roadmap to continue without interruption"]),
 ('board', '2026-11-08', 'In the same statement: "A committee of independent directors, assisted by outside independent counsel, will oversee the investigation. The Board prioritizes U.S. national and economic security, which is paramount to the interests of NVIDIA and its shareholders"',
  ['nbc-1108-investigation', 'nbc-1108-investigation'],
  ['The Board prioritizes U.S. national and economic security, which is paramount to the interests of NVIDIA and its shareholders', 'A committee of independent directors, assisted by outside independent counsel, will oversee the investigation']),
 ('kress', '2026-11-12', 'In the same email to staff: "I believe deeply in this company and in its future"; "we will host a company meeting on November 18"',
  ['cnn-1111-live', 'cnn-1111-live', 'cnn-1111-live'],
  ['I believe deeply in this company and in its future', 'we will host a company meeting on November 18', 'sent the following email to staff Thursday morning']),
 ('mast', '2026-11-12', 'Says Congress is not ruling out "public hearings for other people or other things down road" (CNBC)',
  ['sw-cnbccom-09', 'sw-cnbccom-09'],
  ['public hearings for other people or other things down road', 'told reporters on Thursday that former Nvidia CEO Jensen Huang will testify before Congress']),
 ('jeffries', '2026-11-09', 'On CBS that morning, as HuffPost reports it: "I haven\'t been fully briefed on that issue"; he expects a classified briefing "later on today" to take it up, and says he has not reviewed the secretary of state\'s memo',
  ['huffpost-live', 'huffpost-live', 'huffpost-live'],
  ["I haven't been fully briefed on that issue", 'on Monday, House Minority Leader Hakeem Jeffries', 'Jeffries added that he has not reviewed the classified memo']),
 ('jeffries', '2026-11-12', 'At a news conference: "We need a classified briefing made available to members of Congress as it relates to the Nvidia situation"; the incoming chairs of two House committees "are leading the effort to get to the bottom of what has happened" (CNBC)',
  ['sw-cnbccom-09', 'sw-cnbccom-09'],
  ['We need a classified briefing made available to members of Congress as it relates to the Nvidia situation', 'are leading the effort to get to the bottom of what has happened']),
 ('schumer', '2026-11-10', 'In the same speech: "We also need answers on Nvidia\'s influence campaign and how [it] affected the Trump administration\'s national security decisions"; "We need a full accounting for Trump\'s failure to address foreign espionage in the American tech industry"; "And I call on the Trump administration to brief the Senate and House intelligence committees immediately on the PRC\'s efforts to spy on Nvidia and other US AI companies"',
  ['cnbc-1110-schumer', 'cnbc-1110-schumer', 'art-own-schumer-floor-1110'],
  ["We also need answers on Nvidia's influence campaign and how [it] affected the Trump administration's national security decisions", "We need a full accounting for Trump's failure to address foreign espionage in the American tech industry", "And I call on the Trump administration to brief the Senate and House intelligence committees immediately on the PRC's efforts to spy on Nvidia and other US AI companies"]),
 ('newman', '2026-11-12', 'Tells CNBC: "AMD is clearly the immediate beneficiary. But people need to realize AMD can\'t just instantly ramp up massive additional volume even if customers look to move its way"; "If everyone turned tomorrow and went to AMD, AMD couldn\'t supply"',
  ['sw-cnbccom-09', 'sw-cnbccom-09'],
  ["AMD is clearly the immediate beneficiary. But people need to realize AMD can't just instantly ramp up massive additional volume even if customers look to move its way", "If everyone turned tomorrow and went to AMD, AMD couldn't supply"]),
 # answer to the eighteenth reading and to three reading lanes (Nov 16): occasions and parts of statements they found on no chip
 ('nvidia', '2026-10-29', 'A spokesperson tells Tom\'s Guide: "Building American AI infrastructure worldwide has been a core U.S. policy goal of every Administration. Attacking American industry for honoring longstanding U.S. law and policy undercuts national security"; "The PRC government is not seeking NVIDIA products from regional clouds"; its regional cloud customers receive "ordinary business information" and "zero information relevant to national security"',
  ['sw-tomsguidecom-01', 'sw-tomsguidecom-01', 'sw-tomsguidecom-01'],
  ['Building American AI infrastructure worldwide has been a core U.S. policy goal of every Administration. Attacking American industry for honoring longstanding U.S. law and policy undercuts national security,', 'The PRC government is not seeking NVIDIA products from regional clouds. Instead, the PRC government blocked U.S. AI chips, protecting its own industry and resulting in the largest write-offs in U.S. tech history,', 'Our regional cloud customers receive ordinary business information — not sensitive NVIDIA trade secrets—and zero information relevant to national security,']),
 ('nvidia', '2026-10-31', "A spokesman tells the Journal that the photographs of Huang with Alice Huang were taken at meetings that included other Nvidia cloud partners in Asia (the sentence is not in an earlier version of the article, timed Oct 30 in a licensed copy; it is in the version the Journal's page dates Oct 31)",
  ['man-923fe8754943', 'art-fc-itiger-wsj-1030-v1', 'man-923fe8754943'],
  ['The photos were taken at meetings that included other Nvidia cloud partners in Asia', 'was photographed in public with Jensen Huang in Taipei in 2024 and 2025.', 'Updated Oct. 31, 2026']),
 ('nvidia', '2026-11-06', 'Bloomberg reports, as Tom\'s Hardware relays it, that computing providers in Southeast Asia must now register with Nvidia\'s Fleet Intelligence tracking system to become official Nvidia Cloud Partners; Nvidia "was not immediately available for comment"',
  ['sw-tomshardwarecom-12', 'sw-tomshardwarecom-12'],
  ["Southeast Asia computing providers are now reportedly required to register with Nvidia's Fleet Intelligence tracking system if they want to become official Nvidia Cloud Partners (NCPs).", 'Nvidia was not immediately available for comment']),
 ('nvidia', '2026-11-09', 'The FT reports, from people familiar with the situation, that its general counsel insisted inside the company the week before that claims of an affair were inaccurate, saying the sources had "an axe to grind with Jensen" and "They are laundering salacious gossip"; what the company told the FT about them is on its other act of that day',
  ['man-ft-1109-04', 'man-ft-1109-04', 'man-ft-1109-04'],
  ['insisted inside the company that claims of an affair were inaccurate', 'an axe to grind with Jensen', 'They are laundering salacious gossip']),
 ('nvidia', '2026-11-10', 'A spokesperson tells the FT, for its report on the delayed listing of Megaspeed: "we placed Megaspeed on our block list in June 2025, prohibiting any further sales or shipments"; "That voluntary block remains in place"',
  ['man-ft-1110-02', 'man-ft-1110-02'],
  ['Despite Megaspeed not being on the entity list or subject of an ‘is informed’ letter, we placed Megaspeed on our block list in June 2025, prohibiting any further sales or shipments,', 'That voluntary block remains in place']),
 ('nvidia', '2026-11-10', 'A spokesman tells the Journal, of its general counsel\'s call to the export bureau: "we have an obligation to resolve any potential \'red flags\' before proceeding"; that the ban on sales to Megaspeed is still in place, that Commerce has not blacklisted the company, and that Nvidia got the bureau\'s permission for parts and replacement components sent since; and that U.S. intelligence officials never gave Huang a warning that he might be a target',
  ['art-fc-tovima-wsj-1110', 'art-fc-tovima-wsj-1110', 'art-fc-tovima-wsj-1110', 'man-bb944902439c'],
  ['When we have requests from customers for new shipments, service, or support, we have an obligation to resolve any potential ‘red flags’ before proceeding. That process can include asking [government agencies] whether they require any further information from us,', 'Nvidia got permission from the Commerce Department unit overseeing export controls for parts and replacement components sent to the company since then, he said.', 'U.S. intelligence officials never gave Huang a warning that he might be a target of foreign intelligence efforts, often referred to as a defensive briefing, the spokesman said.', 'adding that the Commerce Department still has yet to blacklist the company or take other action requiring the company to stop doing business with it.']),
 ('nvidia', '2026-11-11', 'A spokesperson tells the Daily Caller News Foundation: "We sell our data-center GPUs primarily to well-known partners", "who work with us to ensure that all sales comply with U.S. export control rules"; "Our due diligence has helped identify suspected attempts to circumvent U.S. export controls, leading to federal prosecutions"',
  ['sw-dailycallercom-03', 'sw-dailycallercom-03'],
  ['Our due diligence has helped identify suspected attempts to circumvent U.S. export controls, leading to federal prosecutions. Our work with law enforcement has led to prosecutions,', 'We sell our data-center GPUs primarily to well-known partners, including original equipment manufacturers, system builders, integrators, and original design manufacturers, who work with us to ensure that all sales comply with U.S. export control rules,']),
 ('nvidia', '2026-11-12', 'Tells a nonprofit that found accounts on X defending Huang in what the Washington Post calls an apparent effort that it was aware of the accounts and was trying to identify the source; it did not respond to the Post',
  ['man-wapo-1112-02', 'man-wapo-1112-02'],
  ['Nvidia told the nonprofit that it was aware of the accounts and was trying to identify the source (Nvidia did not respond to a request for comment from the Post).', "It's not clear who orchestrated the apparent effort"]),
 ('megaspeed', '2026-10-29', 'Later adds, in a further statement the Times prints, that it "cannot respond to a media trial and welcomes formal, evidence-based investigation"',
  ['man-nyt-1029-01', 'man-nyt-1029-01'],
  ['cannot respond to a media trial and welcomes formal, evidence-based investigation.', 'Megaspeed later added in a statement']),
 ('board', '2026-11-11', "Bloomberg reports, as Semafor and Daring Fireball relay it, that Nvidia has hired an outside search firm to find its next chief and that the board is weighing a temporary one. Semafor adds, from people familiar with the matter and an administration official: some directors favour naming Kress interim chief if Huang is removed, it briefed the White House on its planned meeting, and Apple's hardware chief is among those being considered",
  ['sw-semaforcom-11', 'sw-daringfireballnet-05', 'sw-semaforcom-11', 'sw-semaforcom-11', 'sw-semaforcom-11', 'sw-semaforcom-15', 'sw-semaforcom-15', 'sw-semaforcom-15'],
  ['Nvidia has tapped an outside search firm to find the company’s next CEO, Bloomberg reported.', 'The board is weighing the idea of naming a temporary chief while searching for a permanent one, the person said, asking not to be identified because the information isn’t public.', 'Some members of Nvidia’s board favor appointing Chief Financial Officer Colette Kress as interim CEO at the beleaguered chipmaker if CEO and founder Jensen Huang is ousted, according to people familiar with the matter.', 'The Nvidia board briefed the White House on its planned meeting, according to a senior administration official.', 'One person being considered for the top job is Apple hardware chief', "Some members of Nvidia's board favor appointing Chief Financial Officer Colette Kress as interim CEO", 'The Nvidia board briefed the White House on its planned meeting', 'One person being considered for the top job is Apple hardware chief']),
 ('meeks', '2026-11-12', 'Tells the FT: "The administration suspected Alice Huang for a year and didn\'t put Megaspeed on the entity list or warn Nvidia. Why not?"; "Did the push to approve high-end chip licences for China shape the administration\'s response? We should get answers in this Congress. If we don\'t, Democrats will get them next year"',
  ['man-a45550a35921', 'man-a45550a35921'],
  ['The administration suspected Alice Huang for a year and didn’t put Megaspeed on the entity list or warn Nvidia. Why not? Was our national security or Nvidia’s technology compromised?', 'Did the push to approve high-end chip licences for China shape the administration’s response? We should get answers in this Congress. If we don’t, Democrats will get them next year.']),
 ('mast', '2026-11-10', 'Tells reporters at the Capitol he does not know whether Huang has answered the letter: "I can\'t say that I\'ve heard an answer back yet"; what he wants answered: "questions relating to his relationship and what information was or was not passed about anything"; he "can\'t say it would hurt" to hear from the Commerce Department as well. Politico, as WinBuzzer relays it: he told reporters he already has the authority to compel Huang\'s attendance if needed',
  ['cnbc-1110-schumer', 'cnbc-1110-schumer', 'cnbc-1110-schumer', 'cnbc-1110-schumer', 'sw-winbuzzercom-01'],
  ["I can't say that I've heard an answer back yet that,", 'Obviously questions relating to his relationship and what information was or was not passed about anything,', "can't say it would hurt", 'Mast said Tuesday he did not know whether Huang had responded to the letter', 'The request is not a subpoena, but Mast told reporters he already has the authority to compel Huang’s attendance if needed, according to Politico.']),
 ('mast', '2026-11-11', 'In an interview with the Journal, says there have been longstanding concerns about Nvidia\'s sales relationships with China and other countries: "Nvidia is often a huge part of this conversation"',
  ['man-wsj-1112-05', 'man-wsj-1112-05'],
  ['Nvidia is often a huge part of this conversation,', 'said in an interview with the Journal that there have been longstanding concerns about Nvidia']),
 ('mast', '2026-11-12', 'In the same exchange with reporters: "We want to see him basically in a week"; "If negotiations shut off and we don\'t think they\'re in good faith - okay, fine, do that. I\'ll just subpoena you for the next day"; he has not spoken to the Commerce secretary or the export bureau\'s head since the revelations, and wants Congress to investigate the bureau\'s role (CNBC). In the Gazette\'s live report: "we said, like in any negotiation, \'no, this is what we\'ll accept or your subpoena comes for the day after\'". CNBC also has him tell reporters that Thursday that he still has confidence in the Commerce secretary',
  ['sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cnbccom-09', 'sw-cnbccom-09', 'sw-gazettecom-5cfc7b8d', 'sw-cnbccom-09'],
  ['We want to see him basically in a week,', "If negotiations shut off and we don't think they're in good faith — okay, fine, do that. I'll just subpoena you for the next day,", "Mast said he hadn't spoken to Lutnick or Kessler since the revelations.", 'Mast also said he wanted Congress to investigate the role of the Bureau of Industry and Security, a subagency of the Commerce Department that manages and enforces export controls, in the Huang scandal.', 'They made their offer for what they would like to do, and we said, like in any negotiation, ‘no, this is what we’ll accept or your subpoena comes for the day after,’', 'told reporters on Thursday that he still has confidence in Commerce Secretary Howard Lutnick']),
 ('mast', '2026-11-12', 'His spokesperson tells the FT: "We are in ongoing negotiations", and "we cannot confirm it will happen before Thanksgiving". He tells MS NOW the testimony is "likely going to be an under oath transcribed video recorded between several committees". His committee tells the Daily Caller News Foundation that it is in "ongoing negotiations" with Nvidia and Huang; the outlet says no date has been set for the testimony',
  ['man-ft-1112-05', 'man-ft-1112-05', 'man-ft-1112-05', 'msnow-resigns', 'msnow-resigns', 'sw-dailycallercom-9316aa01', 'sw-dailycallercom-9316aa01'],
  ['We are in ongoing negotiations', 'how much time needs to be given to notify, we cannot', 'it will happen before Thanksgiving', 'likely going to be an under oath transcribed video recorded between several committees,', 'told MS NOW on Thursday', 'The Foreign Affairs Committee told the Daily Caller News Foundation that they were in', 'A date has not yet been scheduled for the testimony']),
 ('moolenaar', '2026-11-09', 'Tells the FT it is "vital" that Huang "address our national security concerns in Congress related to China\'s access to sensitive technology and information"',
  ['man-ft-1109-05', 'man-ft-1109-05'],
  ['It is vital that Jensen', "Huang address our national security concerns in Congress related to China's access to sensitive technology and information"]),
 ('thune', '2026-11-09', 'After the intelligence briefing that Monday: "We want to be responding in a serious way to anything that threatens America\'s national security interests or our values" (Semafor); "Clearly in this environment with all the cyber threats and all the world of superintelligence, these types of things take on an added significance" (the Journal); Congress is trying to get more information about the nature of the relationship "and the connections that come with it" (Bloomberg, as the Straits Times carries it)',
  ['sw-semaforcom-04', 'sw-semaforcom-04', 'art-fc-tovima-wsj-1110', 'art-line-straitstimes-bloomberg-1110'],
  ['We want to be responding in a serious way to anything that threatens America’s national security interests or our values,', 'following the intelligence briefing they received in the Capitol on Monday', 'Clearly in this environment with all the cyber threats and all the world of superintelligence, these types of things take on an added significance,', 'Congress, he said, is trying to get more information about the nature of Huang’s relationship “and the connections that come with it”.']),
 ('johnson', '2026-11-12', 'CNN reports that he told it earlier he was not concerned Huang had compromised the president, and that he learned of the allegations "when everyone else did in the media"',
  ['cnn-1111-live', 'cnn-1111-live'],
  ['told CNN earlier he was not concerned Huang compromised the president', 'when everyone else did in the media.']),
 ('jeffries', '2026-11-12', 'Of the president\'s call for a named successor: "This is just another example of Donald Trump weighing in on behalf of his views connected to corporate America, as opposed to focusing on working class America"; "this administration has repeatedly undermined the free market economy"',
  ['sw-gazettecom-5cfc7b8d', 'sw-gazettecom-5cfc7b8d'],
  ['This is just another example of Donald Trump weighing in on behalf of his views connected to corporate America, as opposed to focusing on working class America,', 'this administration has repeatedly undermined the free market economy,']),
 ('coons', '2026-11-09', 'Tells the National News Desk: "I\'m concerned about our national security and the very real possibility that laws have been broken and the American people have been lied to"',
  ['sw-cbsaustincom-03'],
  ['I’m concerned about our national security and the very real possibility that laws have been broken and the American people have been lied to,']),
 ('huizenga', '2026-11-12', 'Calls on the Commerce secretary to testify, in the New Republic\'s relay of Politico: "I don\'t think he\'s been very responsive"; the export bureau has "been less responsive than they should be"',
  ['tnr-lutnick', 'tnr-lutnick'],
  ['I don’t think he’s been very responsive.', 'been less responsive than they should be']),
 ('bresnick', '2026-11-09', 'Tells NPR, of Huang\'s case for selling chips to China: "It calls into question, you know, was he acting in the best interests of the United States to a certain degree, right? Has he compromised U.S. national security because of this relationship?"',
  ['sw-nprorg-02'],
  ['It calls into question the - that entire approach. It calls into question, you know, was he acting in the best interests of the United States to a certain degree, right? Has he compromised U.S. national security because of this relationship?']),
 ('fedasiuk', '2026-11-09', 'Tells the Journal: "It was this unparalleled access to politicos and other industry titans that made him such an attractive target for Chinese intelligence to begin with"',
  ['man-wsj-1109-08'],
  ['It was this unparalleled access to politicos and other industry titans that made him such an attractive target for Chinese intelligence to begin with.']),
 ('fedasiuk', '2026-11-12', 'Tells the Washington Post, of accounts defending Huang: "There are many actors in the American economy who believe that Mr. Huang\'s personal status as CEO of the company is an essential part of American economic growth"',
  ['man-wapo-1112-02'],
  ['There are many actors in the American economy who believe that Mr. Huang’s personal status as CEO of the company is an essential part of American economic growth,']),
 ('mcguire', '2026-11-09', 'Tells Bloomberg, as The National relays it: "You have the CEO of one of the biggest companies in America, that is potentially compromised by the Chinese and they have some information on him - it really needs to be looked into"',
  ['sw-thenationalnewscom-02'],
  ['You have the CEO of one of the biggest companies in America, that is potentially compromised by the Chinese and they have some information on him – it really needs to be looked into,']),
 ('mcguire', '2026-11-10', 'Tells the Journal, of the chip-export bills: "They should just be pushed now and voted on, up or down, as a way to signal Congress\'s concern about this issue and how it\'s being handled"',
  ['man-bb944902439c'],
  ['They should just be pushed now and voted on, up or down, as a way to signal Congress’s concern about this issue and how it’s being handled,']),
 ('mcguire', '2026-11-10', 'In a post that a newsletter of Nov 10 quotes: "Nvidia\'s most advanced chips remain available to Megaspeed"; "And for some reason, @BISgov refuses to cut them off"; "the best evidence is the fact that the MSS is actively trying to convince us to loosen them!"',
  ['sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01'],
  ['Also, Nvidia’s most advanced chips remain available to Megaspeed, the Singapore-based company that Alice Huang led and that is known to be a Chinese cutout. And for some reason, @BISgov refuses to cut them off.', 'For anyone who still needs convincing that export controls support US leadership in AI, the best evidence is the fact that the MSS is actively trying to convince us to loosen them!']),
 ('stapp', '2026-11-10', 'In a post that a newsletter of Nov 10 quotes: "So, the current position of the NVIDIA board is that there\'s \'no reason to believe that national security was compromised\' by Jensen Huang having an affair with a Chinese spy. wtf?"',
  ['sw-thezvisubstackcom-01'],
  ['So, the current position of the NVIDIA board is that there’s “no reason to believe that national security was compromised” by Jensen Huang having an affair with a Chinese spy. wtf?']),
 ('hashim', '2026-11-10', 'In a post that a newsletter of Nov 10 quotes: the company\'s spokesman "has put out multiple statements in recent weeks that we now know are false. Unclear, of course, if he believed them to be true at the time"; "Jensen himself directly lied to Bloomberg\'s" reporters',
  ['sw-thezvisubstackcom-01', 'sw-thezvisubstackcom-01'],
  ['Note that Nvidia’s spokesman John Rizzo has put out multiple statements in recent weeks that we now know are false. Unclear, of course, if he believed them to be true at the time.', 'Jensen himself directly lied to Bloomberg']),
 ('moorhead', '2026-11-09', 'Tells CNBC by email: "Jensen holding so much power is why Nvidia moves faster than anyone"',
  ['sw-cnbccom-11'],
  ['Jensen holding so much power is why Nvidia moves faster than anyone.']),
 ('moorhead', '2026-11-09', 'Tells TheWrap: "Near term, this is a governance and political-risk story, not a demand story"; "Jensen is the product strategist, the closer with the big cloud companies and the face of the company in Washington and Beijing, and there\'s no named successor"',
  ['sw-thewrapcom-01', 'sw-thewrapcom-01'],
  ['Near term, this is a governance and political-risk story, not a demand story,', 'Jensen is the product strategist, the closer with the big cloud companies and the face of the company in Washington and Beijing, and there’s no named successor,']),
 ('moorhead', '2026-11-11', 'Posts, on the report of a second relationship: "This one will be hard, if not impossible, to recover from"',
  ['sw-gamesbeatcom-01', 'sw-gamesbeatcom-01'],
  ['This one will be hard, if not impossible, to recover from.', 'November 11, 2026']),
 ('moorhead', '2026-11-12', 'Implicator quotes him on the interim chief: "In my conversations with her, she goes deep on the product roadmap, from rack-scale systems to networking and software"; "She has credibility with investors because she answers hard questions directly"; it says he called her "the logical choice", with a link to WIRED',
  ['sw-implicatorai-06', 'sw-implicatorai-06', 'sw-implicatorai-06', 'sw-implicatorai-06'],
  ['In my conversations with her, she goes deep on the product roadmap, from rack-scale systems to networking and software,', 'She has credibility with investors because she answers hard questions directly,', 'the logical choice', 'chief analyst at Moor Insights & Strategy, called her']),
 ('newman', '2026-11-12', 'Tells CNBC, for its profile of the interim chief, that she "deeply understands the business and has shown fierce loyalty to the company"',
  ['sw-cnbccom-21'],
  ['deeply understands the business and has shown fierce loyalty to the company,']),
 ('jcramer', '2026-11-12', 'In a post that PC Gamer quotes: "Jensen we hardly knew yah. Just plain awful...."',
  ['sw-pcgamercom-569569dc'],
  ['Jensen we hardly knew yah. Just plain awful....']),
 ('maguire', '2026-11-09', 'The FT quotes him: "Yes he should have known better"; "But let\'s also not nuke our AI industry because China ran a successful intel op"',
  ['man-ft-1110-01', 'man-ft-1110-01'],
  ['Yes he should have known better', "But let's also not nuke our AI industry because China ran a successful intel op"]),
 ('maguire', '2026-11-09', 'A blog of that day quotes him on such approaches: "you\'re drunk and make a mistake and then you\'re owned"',
  ['sw-emptywheelnet-01'],
  ['you’re drunk and make a mistake and then you’re owned.']),
 ('maguire', '2026-11-12', 'In a post that a Journal column quotes: "This has nothing to do with money. This is about America winning in AI"',
  ['man-f2f8fbf1fc93'],
  ['This has nothing to do with money. This is about America winning in AI.']),
 ('boloor', '2026-11-10', 'Tells Reuters, as the International Business Times carries it: "The key-person risk is massive since Jensen co-founded Nvidia, built the CUDA ecosystem that underpins its competitive advantage and personally anchors relationships with the largest AI customers and governments"',
  ['sw-ibtimescom-05'],
  ['The key-person risk is massive since Jensen co-founded Nvidia, built the CUDA ecosystem that underpins its competitive advantage and personally anchors relationships with the largest AI customers and governments,']),
 ('boloor', '2026-11-12', 'On the day of the resignation ("today with Jensen\'s resignation"), as the International Business Times quotes him: replacing Huang\'s "strategic vision at a company built around ~60 direct reports and no obvious second-in-command is an enormous challenge"; but Meta, Amazon, Google, SpaceX and Microsoft "aren\'t suddenly going to stop building capacity"',
  ['sw-ibtimescom-5f024890', 'sw-ibtimescom-5f024890', 'sw-ibtimescom-5f024890'],
  ['strategic vision at a company built around ~60 direct reports and no obvious second-in-command is an enormous challenge', "aren't suddenly going to stop building capacity", "today with Jensen's resignation"]),
 ('sweeney', '2026-11-12', 'Before the resignation, in a comment PC Gamer quotes that day: "This would be an Apple firing Steve Jobs level of idiocy from Nvidia\'s board if they did that, and a grievous harm to the United States of America"',
  ['sw-pcgamercom-eeaddc6b'],
  ['This would be an Apple firing Steve Jobs level of idiocy from Nvidia’s board if they did that, and a grievous harm to the United States of America.']),
 # what six more reading lanes found (Nov 16): reported acts, occasions and parts of statements on no chip
 ('nyt', '2026-11-08', 'Reports that Nvidia opened its inquiry after Huang "acknowledged to the company\'s board that he had been intimate with a business executive who U.S. intelligence determined to be a Chinese spy" (as Boston.com carries the article)',
  ['sw-bostoncom-01'],
  ['SAN FRANCISCO — Nvidia said on Sunday that it was opening an investigation into Jensen Huang, its chief executive and co-founder, after he acknowledged to the company’s board that he had been intimate with a business executive who U.S. intelligence determined to be a Chinese spy.']),
 ('nyt', '2026-11-10', 'Reports, in a profile of Alice Huang, that in 2024 "Taiwanese authorities began to monitor Ms. Huang\'s trips to the island at the suggestion of the U.S. government", citing a person familiar with the matter (as Business Standard carries the article). The profile also reports that Megaspeed "was named a Nvidia cloud partner" four days after a change of its ownership, and that in late 2024 the Commerce Department "sent an official to inspect a Megaspeed data center", where "Some Nvidia equipment was still packed in boxes"',
  ['art-fc-bs-nyt-1110-woman', 'art-fc-bs-nyt-1110-woman', 'art-fc-bs-nyt-1110-woman', 'art-fc-bs-nyt-1110-woman'],
  ["Taiwanese authorities began to monitor Ms. Huang's trips to the island at the suggestion of the U.S. government", 'Four days after the ownership change Megaspeed was named a Nvidia cloud partner', 'In late 2024, the U.S. Commerce Department sent an official to inspect a Megaspeed data center', 'Some Nvidia equipment was still packed in boxes']),
 ('ft', '2026-11-06', "Reports that before the president's trip to China in May, when he learnt that Huang was not in the group, he called him, and Huang flew to Alaska, where he boarded the presidential jet during a stopover",
  ['man-ft-1107-01'],
  ['After Trump learnt that he was not included in the group, he called the Nvidia CEO, who ﬂew to Alaska where he boarded the presidential jet during a stopover.']),
 ('ft', '2026-11-10', 'Reports, from people familiar with the matter, that the Commerce Department "sought over the past two months to delay new inclusions" on the entity list, saying it needed more information about some companies, and that the state, energy and Treasury departments and the Pentagon "were among the agencies that were pushing for Megaspeed\'s inclusion on the list"',
  ['man-ft-1110-02', 'man-ft-1110-02'],
  ['But the commerce department, which chairs the panel overseeing the list, sought over the past two months to delay new inclusions, one of the people said. Department oﬃcials had liaised with their counterparts and had stressed that they needed more information about some companies in the package, the person said.', 'The state, energy and Treasury departments, along with the Pentagon, were among the agencies that were pushing for Megaspeed’s inclusion on the list, the people familiar with the matter said.']),
 ('huang', '2026-11-09', 'Apologises to his staff at headquarters that Monday and then runs his meetings "as if it were business as usual", in Fortune\'s account, which cites CNBC',
  ['sw-fortunecom-09', 'sw-fortunecom-09'],
  ['apologized to his staff, and then ran his meetings as CEO as if it were business as usual', "On Monday, Jensen Huang walked into Nvidia's HQ in Santa Clara, California"]),
 ('huang', '2026-11-11', "By Rep. Mast's account to reporters, tentatively agrees that Wednesday night to testify before Congress (CNN)",
  ['cnn-1111-live'],
  ['Huang tentatively agreed to testify on Wednesday night']),
 ('trump', '2026-11-10', 'The Times reports, from two people briefed on the call, that he called Huang that Tuesday "and urged him to keep fighting for his job" (as Business Standard carries the article)',
  ['art-fc-bs-nyt-1112-trump', 'art-fc-bs-nyt-1112-trump'],
  ['President Trump called Jensen Huang on Tuesday', 'and urged him to keep fighting for his job, according to two people briefed on the conversation']),
 ('embassy', '2026-10-30', 'In the Journal\'s report, as a licensed copy timed that day carries it: rejects the allegations, saying China opposes the peddling of a "Chinese spy narrative" and that its technological development is grounded in "independent innovation"',
  ['art-fc-itiger-wsj-1030-v1', 'art-fc-itiger-wsj-1030-v1', 'man-923fe8754943', 'man-923fe8754943'],
  ['The Chinese Embassy in Washington rejected the allegations', 'independent innovation', 'The Chinese Embassy in Washington rejected the allegations', 'independent innovation']),
 ('commerce', '2026-11-11', 'Tells the Times, beside its denial of the confrontation, that the decision whether to add companies to the entity list "was an administration-wide one"',
  ['man-nyt-1111-02'],
  ['A spokeswoman for the Commerce Department denied that the conversation between Mr. Bessent and Mr. Lutnick had taken place. She said that the decision about whether to add companies to the entity list was an administration-wide one.']),
 ('commerce', '2026-11-11', 'Politico reports, as The Bulwark relays it, that officials of its export bureau "had warned in dozens of reports of the risk of Nvidia\'s advanced chips being diverted to China". CNN, as a local station carries it: senior officials, the secretary among them, "were briefed months ago about Huang\'s relationship with Alice Huang"',
  ['bulwark-chipghazi', 'sw-ktvzcom-01'],
  ['Politico reports that officials in the Bureau of Industry and Security, the office that oversees tech exports, had warned in dozens of reports of the risk of Nvidia’s advanced chips being diverted to China.', 'Senior Trump officials, including Lutnick, also were briefed months ago about Huang’s relationship with Alice Huang, a Megaspeed executive who the intelligence community suspected of being a Chinese spy, people familiar with the matter said.']),
 ('justice', '2026-11-10', 'CNN reports, as a local station carries it, that the FBI "first raised concerns to lawmakers that Alice Huang might be feeding information to China nearly a year ago", from two people familiar with the matter',
  ['sw-localnews8com-03'],
  ['The FBI first raised concerns to lawmakers that Alice Huang might be feeding information to China nearly a year ago , two people familiar with the matter told CNN.']),
 ('moolenaar', '2026-11-09', 'His committee posts on X that Monday, "In case you missed it", with a copy of the letter (The National)',
  ['sw-thenationalnewscom-02'],
  ['On Monday, the US select committee on the CCP posted on X: "In case you missed it," along with a copy of the letter in which Mr Huang\'s appearance was requested last week.']),
 ('moolenaar', '2026-11-10', 'Says in a statement that restrictions on chip exports should be included in the annual military spending bill (Reuters, as the Globe and Mail carries it)',
  ['sw-theglobeandmailcom-01', 'sw-theglobeandmailcom-01'],
  ['House China Committee Chairman John Moolenaar, a Republican, said in a statement that restrictions on chip exports should be included in the U.S.’s annual military spending bill.', 'U.S. lawmakers on Tuesday renewed calls for tighter restrictions']),
 ('moolenaar', '2026-11-12', 'In a statement of Nov 12, as Unite.AI reports it: urges Congress to pass export-control legislation in the year-end defence bill, and calls on Nvidia to change its corporate practices and appoint leadership that prioritises national security',
  ['sw-uniteai-bf709b60'],
  ['Moolenaar took a more specific legislative position in a November 12 statement , urging Congress to pass bipartisan export-control legislation in the year-end national defense bill. He also called on NVIDIA to change its corporate practices and appoint leadership that prioritizes national security. American AI companies, he said, should not jeopardize national security by giving Chinese companies access to their most advanced chips.']),
 ('moolenaar', '2026-11-12', 'Tells Politico, as the New Republic relays it: "I\'d say we want to get to the bottom of the matter and to really have transparency on this"; he wants the Commerce secretary and others in the administration to brief Congress',
  ['tnr-lutnick'],
  ['“I’d say we want to get to the bottom of the matter and to really have transparency on this,” said Republican Representative John Moolenar, who chairs the House Select Committee on the Chinese Communist Party. Moolenar told Politico that he wants Lutnick and others in the administration to brief Congress on the Chinese government’s influence on Nvidia, and how that in turn influenced U.S. security policy.']),
 ('banks', '2026-11-12', 'The Journal reports that he told Fox News the Commerce secretary appeared to be "defying President Trump\'s orders" by not imposing chip-export restrictions',
  ['man-9de9f2a5db75'],
  ['“defying President Trump’s orders” by declining to impose chip-export restrictions.']),
 ('coons', '2026-11-10', 'Tells NPR, as The Daily Upside reports it, that investigating Huang is one of his top priorities',
  ['sw-thedailyupsidecom-01'],
  ['Chris Coons, the Democratic Senator for Delaware set to chair the upper chamber’s Foreign Relations Committee told NPR investigating Huang is one of his top priorities.']),
 ('kennedy', '2026-11-12', 'The Journal reports that he said he was prepared to bring the Commerce secretary to testify before Congress',
  ['man-9de9f2a5db75'],
  ['Sen. John Kennedy (R., La.) said he was prepared to bring Lutnick to testify in front of Congress.']),
 ('mcguire', '2026-11-12', 'Tells the Washington Post by email that he had "definitely" noticed the accounts that targeted his posts, and had assumed they were Chinese bot accounts',
  ['man-wapo-1112-02'],
  ['Chris McGuire, a senior fellow at the Council on Foreign Relations, was another frequent target of the posts. He said in an email that he had “definitely” noticed them, and had assumed that they were from Chinese bot accounts, which he said regularly attacked his posts']),
 ('musk', '2026-11-12', 'Replies "True words" to a post that a founder is not simply replaced, in a Journal column of that day',
  ['man-f2f8fbf1fc93'],
  ['To which Musk replied: “True words.”']),
 # answer to the nineteenth reading (Nov 16): occasions it found on no chip
 ('nvidia', '2026-11-06', 'A representative tells The National, for its report of that day on the committees\' letter, that the company has a robust security team that travels with its chief executive "when needed" and always acts accordingly when the government tells it of entities of concern; the paper says the representative "did not say whether Mr Huang would agree to attend". It prints beside this two sentences of the company\'s statement of the day before; whether its answers to the paper were a separate exchange the page does not say',
  ['sw-thenationalnewscom-01', 'sw-thenationalnewscom-01'],
  ['The Nvidia representative told The National that the company has a robust security team that travels with its chief executive', 'did not say whether Mr Huang would agree to attend the meeting']),
 ('nvidia', '2026-11-09', 'In a statement to The National, for its report of that day: "Jensen is committed to continuing to lead", and his tenure would continue "without interruption" (the words of its statement to CNBC the day before)',
  ['sw-thenationalnewscom-02'],
  ['"Jensen is committed to continuing to lead," Nvidia said in a statement to The National']),
 ('nvidia', '2026-11-12', 'TechCrunch\'s timeline of that day recounts its statements of October 2025, when the investigations of Megaspeed were confirmed: it did not have "any reason to believe products had been diverted", and "NVIDIA visited multiple Megaspeed sites yet again earlier this week and confirmed what we previously observed - Megaspeed is running a small commercial cloud, like many other companies throughout the world, as allowed by U.S. export control rules"',
  ['sw-techcrunchcom-08', 'sw-techcrunchcom-08', 'sw-techcrunchcom-08'],
  ['At the time, an Nvidia spokesperson told press that the company did not have', 'NVIDIA visited multiple Megaspeed sites yet again earlier this week and confirmed what we previously observed', 'October 2025: U.S. and Singapore each investigate Megaspeed']),
 ('wsj', '2026-11-09', 'Reports, in an article on who could succeed Huang, that Nvidia\'s latest proxy statement warns it is "highly dependent on the services of our longstanding executive team" and that a failure to ensure effective succession planning could "hinder our strategic planning, execution, and long-term success"',
  ['man-wsj-1109-08', 'man-wsj-1109-08'],
  ["Nvidia's latest proxy statement warns that it is", 'hinder our strategic planning, execution, and long-term success']),
 ('board', '2026-11-12', 'Electronics Weekly, a British trade paper, reports that Thursday that the board "is meeting today to decide if CEO Jensen Huang should be replaced and, if so, by who"; the page does not say whether that is the session of Wednesday night, U.S. time. Semafor\'s report of the night before, in a version changed that morning, adds that the board "has debated whether, as part of its potential replacement of Huang, to introduce a chief operating officer to serve alongside the interim chief executive"',
  ['sw-electronicsweeklycom-01', 'sw-semaforcom-11'],
  ['The Nvidia board is meeting today to decide if CEO Jensen Huang should be replaced and, if so, by who', "Nvidia's board has debated whether, as part of its potential replacement of Huang, to introduce a chief operating officer to serve alongside the interim chief executive"]),
 # found by the screen of earlier pages and versions (Nov 16): a remark another outlet reported a day earlier
 ('boloor', '2026-11-11', 'Tells Yahoo Finance, as the San Francisco Standard reports it that evening: "I don\'t see the next 12 to 18 months of revenue suddenly disappearing if Jensen were to leave". Fortune prints the sentence the next morning as told to it; whether he said it twice or sent one comment to both, the pages do not say',
  ['sw-sfstandardcom-05', 'sw-sfstandardcom-05'],
  ['Shay Boloor, chief market strategist at The Futurum Group, told Yahoo Finance', "I don't see the next 12 to 18 months of revenue suddenly disappearing if Jensen were to leave"]),
 # answer to the twentieth reading (Nov 16): reports of earlier acts and further responses it found on no chip
 ('nvidia', '2026-11-09', 'Bloomberg reports, as the Business Times of Singapore carries it, an earlier call: about three months before, its general counsel told a White House official, according to a person familiar with the call, that Alice Huang "is not as important in Megaspeed as she makes herself out to be", and that Nvidia had stopped doing business with Megaspeed because of the bad publicity around her',
  ['ms-deals-bloomberg-intervention-ce2630', 'ms-deals-bloomberg-intervention-ce2630', 'ms-deals-bloomberg-intervention-ce2630'],
  ['Around three months ago', 'is not as important in Megaspeed as she makes herself out to be', 'Nvidia had stopped doing business with Megaspeed']),
 ('whitehouse', '2026-11-12', 'The Spectator recalls that the president disclosed the month before that he had bought and sold Nvidia stock, and that the White House said independent managers had made the trades and there were "no conflicts of interest"; the page gives the reply no day',
  ['sw-spectatorcom-01', 'sw-spectatorcom-01'],
  ['Trump disclosed that he had bought and sold Nvidia stock two months earlier', 'The White House said independent managers had made the trades']),
 ('taiwan', '2026-11-12', 'The Journal reports, as To Vima carries the article, that Taiwanese authorities say they have revoked Alice Huang\'s entry permit and barred her from returning, and that officials say they "are now investigating whether her visits involved intelligence gathering or violated the island\'s anti-infiltration act"',
  ['art-fc-tovima-wsj-1112-kangwei', 'art-fc-tovima-wsj-1112-kangwei'],
  ["Taiwanese authorities said they had revoked Alice Huang's entry permit", 'Taiwanese officials said they are now investigating whether her visits involved intelligence gathering']),
 ('moolenaar', '2026-11-05', 'Implicator recounts, in its report on the chairmen\'s letter, that his committee "opened an investigation into Nvidia\'s sale of chips in Asia" in April 2025',
  ['sw-implicatorai-01'],
  ["In April 2025, Moolenaar's committee opened an investigation into Nvidia's sale of chips in Asia"]),
 ('commerce', '2026-11-11', 'The Seoul Economic Daily reports, in an article it marks as translated by machine from Korean, that on May 14 the department "approved purchases of Nvidia H200 chips by about 10 Chinese companies", after, by Axios\'s account, its secretary had received a document warning of the relationship',
  ['sw-ensedailycom-14', 'sw-ensedailycom-14', 'sw-ensedailycom-14'],
  ['the Commerce Department on May 14 approved purchases of Nvidia H200 chips by about 10 Chinese companies', 'Lutnick received a document warning about the relationship', 'AI-translated from Korean']),
 ('commerce', '2026-11-12', 'The Internet Governance Project\'s timeline says that in its investigation of Megaspeed, from late 2024 to mid 2025, its export bureau "conducted on-site inspections and supply chain audits across Southeast Asian data centers to verify serial numbers and end-user declarations"',
  ['sw-internetgovernanceorg-593ba1ee', 'sw-internetgovernanceorg-593ba1ee'],
  ['BIS conducted on-site inspections and supply chain audits across Southeast Asian data centers to verify serial numbers and end-user declarations', 'Late 2024 - mid 2025']),
 ('commerce', '2026-11-12', 'MS NOW recalls, in its report of that day, that the department "greenlit" Megaspeed "as a buyer of Nvidia\'s advanced chips earlier this year"; the page gives no detail of the approval',
  ['msnow-resigns'],
  ["which the Commerce Department greenlit as a buyer of Nvidia's advanced chips earlier this year"]),
 ('ft', '2026-11-10', 'Reports, in its piece "Too big to fire", that Megaspeed, according to that company\'s documents, "has been the recipient of loans from the US chip group in 2024"',
  ['man-211030e54eba', 'man-211030e54eba'],
  ['has been the recipient of loans from the US chip group in 2024', "according to Megaspeed's company"]),
 ('mcguire', '2026-11-08', 'Posts that Sunday: "So Rubio himself is worried about Jensen\'s romantic relationship with the Chinese spy and Megaspeed executive, meaning the intel was validated at the highest levels of government. But still, Commerce has done nothing to limit AI chip shipments to Megaspeed or Southeast Asia. Why?" (The National embeds the post in its report of Nov 9)',
  ['art-own-x-2119511177600422146', 'art-own-x-2119511177600422146', 'sw-thenationalnewscom-02'],
  ['But still, Commerce has done nothing to limit AI chip shipments to Megaspeed or Southeast Asia. Why?', 'Sun Nov 08 19:23:38 +0000 2026', 'Earlier on X, Mr McGuire said some members of the administration']),
 ('nyt', '2026-11-05', 'Reports, in its article on the chairmen\'s letter, that Sen. Warren "renewed her call for testimony" the week before, after its first report; Huang had turned down her request in June to appear before the Senate',
  ['man-nyt-1105-01', 'man-nyt-1105-01'],
  ['Ms. Warren renewed her call for testimony after The Times reported', 'a request to appear before the Senate from Senator Elizabeth Warren']),
 ('huang', '2026-11-11', 'ANI reports, giving no day, that he "addressed the matter during a closed-door staff meeting, expressed regret and did not take questions before moving on to regular business discussions"; Fortune describes an apology to his staff on Monday, Nov 9 (his chip of that day), and the pages do not say whether this is that meeting',
  ['sw-aninewsin-07'],
  ['He reportedly addressed the matter during a closed-door staff meeting, expressed regret and did not take questions']),
 ('huang', '2026-11-12', 'The Spectator recounts an earlier bargain: in August 2025, when the president wanted 20 percent of the revenue from sales of the H20 chip to China, "Huang talked him down to 15"; it quotes the president: "So we negotiated a little deal"',
  ['sw-spectatorcom-01', 'sw-spectatorcom-01', 'sw-spectatorcom-01'],
  ['In August last year, Trump said he wanted 20 percent', 'Huang talked him down to 15', 'So we negotiated a little deal']),
 ('trump', '2026-11-12', 'The Spectator recounts that in December 2025 he "announced conditional permission for sales of H200, a different chip, to approved Chinese customers, with a proposed 25 percent government share"; it sets this after the briefing the Times reported',
  ['sw-spectatorcom-01', 'sw-spectatorcom-01'],
  ['In December he announced conditional permission for sales of H200', 'Two months later, Trump was briefed that Alice Huang was presumed to be a spy, according to the Times']),
]

# Acts whose source gives no day for the act itself: they sit on the day the source was published and are drawn with a dashed edge.
# (rewritten in date order on 2026-11-16: eleven marks removed where the source's context fixes the day, five added with MA191 and MA193 to MA196)
REPORT_DAY = {('megaspeed', '2026-10-29'), ('nvidia', '2026-10-29'), ('whitehouse', '2026-10-29'), ('embassy', '2026-10-30'), ('taiwan', '2026-10-30'), ('nvidia', '2026-10-31'),
              ('openai', '2026-11-04'), ('moolenaar', '2026-11-05'), ('embassy', '2026-11-06'), ('nvidia', '2026-11-06'), ('whitehouse', '2026-11-06'), ('commerce', '2026-11-07'),
              ('nvidia', '2026-11-07'), ('cornyn', '2026-11-08'), ('magaziner', '2026-11-08'), ('mccaul', '2026-11-08'), ('rubio', '2026-11-08'), ('whitehouse', '2026-11-08'),
              ('blumenthal', '2026-11-09'), ('bresnick', '2026-11-09'), ('coons', '2026-11-09'), ('fedasiuk', '2026-11-09'), ('huang', '2026-11-09'), ('justice', '2026-11-09'),
              ('maguire', '2026-11-09'), ('mcguire', '2026-11-09'), ('megaspeed', '2026-11-09'), ('moolenaar', '2026-11-09'), ('moorhead', '2026-11-09'), ('nvidia', '2026-11-09'),
              ('bessent', '2026-11-10'), ('boloor', '2026-11-10'), ('bresnick', '2026-11-10'), ('commerce', '2026-11-10'), ('coons', '2026-11-10'), ('grunewald', '2026-11-10'),
              ('hashim', '2026-11-10'), ('justice', '2026-11-10'), ('mcguire', '2026-11-10'), ('megaspeed', '2026-11-10'), ('moorhead', '2026-11-10'), ('nvidia', '2026-11-10'),
              ('ohanlon', '2026-11-10'), ('rubio', '2026-11-10'), ('stapp', '2026-11-10'), ('taiwan', '2026-11-10'), ('whitehouse', '2026-11-10'), ('board', '2026-11-11'),
              ('boloor', '2026-11-11'), ('bresnick', '2026-11-11'), ('commerce', '2026-11-11'), ('huang', '2026-11-11'), ('mast', '2026-11-11'), ('moolenaar', '2026-11-11'),
              ('moorhead', '2026-11-11'), ('nvidia', '2026-11-11'), ('stapp', '2026-11-11'), ('anthropic', '2026-11-12'), ('banks', '2026-11-12'), ('board', '2026-11-12'),
              ('boloor', '2026-11-12'), ('chan', '2026-11-12'), ('commerce', '2026-11-12'), ('cornyn', '2026-11-12'), ('fedasiuk', '2026-11-12'), ('hodges', '2026-11-12'),
              ('huang', '2026-11-12'), ('huizenga', '2026-11-12'), ('jcramer', '2026-11-12'), ('johnson', '2026-11-12'), ('justice', '2026-11-12'), ('kennedy', '2026-11-12'),
              ('king', '2026-11-12'), ('maguire', '2026-11-12'), ('mcguire', '2026-11-12'), ('meeks', '2026-11-12'), ('moolenaar', '2026-11-12'), ('moorhead', '2026-11-12'),
              ('musk', '2026-11-12'), ('newman', '2026-11-12'), ('nie', '2026-11-12'), ('nvidia', '2026-11-12'), ('sweeney', '2026-11-12'), ('taiwan', '2026-11-12'),
              ('trump', '2026-11-12'), ('whitehouse', '2026-11-12'), ('yoo', '2026-11-12')}        # added 2026-11-16 with MA179, MA180, MA184, MA186
# Row ids whose source gives the act's own day although another act of the same actor on that day is known only by its report's day
# (slice S8, 2026-11-15: the Journal has Cornyn's post "on X Sunday"; his remark on the Times report that day is dated by CNBC's page).
OWN_DAY = {'MA33', 'MA156', 'MA59', 'MA74', 'MA77', 'MA170', 'MA190', 'MA197', 'MA205', 'MA218', 'MA49', 'MA47', 'MA80', 'MA104', 'MA107', 'MA175', 'MA233', 'MA297',  'MA63', 'MA228', 'MA296', 'MA303', 'MA305', 'MA96', 'MA290', 'MA282', 'MA38', 'MA43', 'MA45', 'MA56', 'MA62', 'MA90', 'MA100', 'MA141', 'MA144', 'MA167', 'MA172', 'MA226', 'MA236', 'MA242', 'MA134', 'MA157', 'MA221',        # the last six: acts with their own day on a day that also holds a refusal or report dated by its report (sixteenth reading)
                  # MA156: the FT dates the legislators' calls to Thursday; Cornyn's other act of Nov 12 (MA147) is dated by a newsletter
          
           'MA142',        # Moorhead's broadcast of Nov 11 is dated by his firm's own summary; the Times article that quotes him that day gives no day for the remark (MA158)
           'MA159',
           'MA168'}        # the attorney general "said on Thursday" (Reuters); the other act of the department that day (MA169) is dated by Bloomberg's report        # Thune "told reporters on Capitol Hill on Thursday" (the FT); his "some follow-up" (MA36) is dated by CNBC's report

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
 # Kevin, 2026-11-15: an earlier exclusive from Anthropic counts as a tie ("yes include it as a tie"), for Anthropic only ("we are not including nvidia
 # exclusives. we are only doing anthropic"). The record is the relay held here; the FT's own article of that day and its byline are not held.
 ('Anthropic', 'Financial Times', 'context', 'its report of Sep 4, 2025 that Anthropic would stop selling AI services to groups majority-owned by Chinese entities cited "an Anthropic executive familiar with the matter", as Bloomberg Law relays it. No record here shows who the sources of its Nov 6 report were',
  ['art-lead-bloomberglaw-20250904-anthropic-china-ft'] * 3, ['the Financial Times reports', 'citing an Anthropic executive familiar with the matter', 'PUBLISHED: 2025-09-04']),
]
# ---- slice S8 (Nov 15, 2026): ties of the members drawn since that day; numbered after TIES_V7
TIES_V8 = [
 ('AnthroPAC', 'Sen. Pete Ricketts', 'money', '$2,000 · Sep 25', [FEC + 'PETE RICKETTS FOR SENATE'], ['2000.00']),
 # the look-up of the names the pages saved since added (lane analysts_nv8_e, Nov 15). Identity: the commission's own page and Anthropic's
 # announcement both give his earlier post as national security adviser to the Speaker.
 ('Anthropic', 'Joshua Hodges', 'named', 'named by Anthropic on Aug 27, 2025 as a member of its National Security and Public Sector Advisory Council; whether he sits on it now was not checked',
  [PK + 'congress/research/revolving_door.csv#RD038', 'art-tie-anthropic-advisory-council-20250827', 'art-tie-anthropic-advisory-council-20250827', 'art-tie-uscc-commission-members'],
  ['Anthropic National Security and Public Sector Advisory Council', 'Mr. Hodges was formerly the National Security Advisor to Speaker of the House Mike Johnson', 'National Security and Public Sector Advisory Council', 'Previously he was National Security Advisor to Speaker']),
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


# An act withdrawn by itself while its actor stays drawn (the twentieth independent reading, Nov 16, 2026). The row keeps its id and is
# published with the reason; it is not drawn and not counted.
WITHDRAWN_ACTS = {'MA305': 'the same statement as act MA96: the outlet that relays it links the chairman\'s statement of Nov 12, which MA96 already carried; '
                           'its one further clause, on legislation, was added to MA96 (found by the twentieth independent reading)'}


def acts():
    """ACTS with date, src and q filled in from rows_events where an act points at one of its rows."""
    ev = {r['row_id']: r for r in rows_events.rows()}
    keys = {a[0] for a in ACTORS_ALL}
    out = []
    for i, a in enumerate(ACTS, 1):
        assert a[0] in keys, a[0]
        own = f'MA{i:02d}' in OWN_DAY
        if a[1].startswith('EV'):
            e = ev[a[1]]
            src, q = (e['src'], e['q']) if isinstance(e['src'], list) else ([e['src']], [e['q']])
            more = (a[3], a[4]) if len(a) == 5 else ([], [])          # sources the act adds to its event row's (audit of Nov 14)
            assert len(more[0]) == len(more[1])
            out.append({'actor': a[0], 'date': e['date'], 'what': a[2], 'src': list(src) + more[0], 'q': list(q) + more[1], 'from': a[1], 'reported': (a[0], e['date']) in REPORT_DAY and not own, 'withdrawn': WITHDRAWN.get(a[0], '')})
        else:
            assert len(a[3]) == len(a[4])
            out.append({'actor': a[0], 'date': a[1], 'what': a[2], 'src': a[3], 'q': a[4], 'from': '', 'reported': (a[0], a[1]) in REPORT_DAY and not own, 'withdrawn': WITHDRAWN.get(a[0], '')})
    for rid, why in WITHDRAWN_ACTS.items():
        out[int(rid[2:]) - 1]['withdrawn'] = why
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


# Slice S8 (2026-11-15). The posts themselves, saved by post id (no handle is sent), and the papers' own pages saved since the
# first census, added to the chips they stand behind. A post's time is the stamp in its saved record (UTC); the figure's days are
# U.S. Eastern days. Keyed by row id, so no act moves.
def _also(rid, src, q):
    assert len(src) == len(q), rid
    s0, q0 = ORIGINALS.get(rid, ([], []))
    ORIGINALS[rid] = (list(s0) + src, list(q0) + q)


_X = 'art-own-x-'
_also('MA16', ['man-ft-1110-02'], ['It is mind-boggling that commerce knew months ago that Megaspeed is being run by a Chinese spy but did nothing to stop them from buying $4.8bn worth of Nvidia chips'])
_also('MA22', ['man-ft-1107-01'] * 2, ['"Congress will investigate and get answers," Coons wrote on X.', 'insane relationship between the Trump Administration, Chinese spies, and AI billionaires'])
_also('MA58', ['art-fc-tovima-ft-1109-admits'], ['"I owe my family and all of you an apology," Huang said in the message. "I was unfaithful to my wife.'])
_also('MA33', ['art-fc-tovima-wsj-1108-board'], ['Sen. John Cornyn (R., Texas) said on X Sunday, "Congressional oversight investigation needed."'])
_also('MA46', ['man-nyt-1108-01'] * 2 + ['man-politico-1109-01'],
      ['Representative Michael McCaul, a Republican of Texas who is the vice chair of the House Committee on Homeland Security, wrote on social media', 'PUBLISHED: 2026-11-08',
       'Michael McCaul (R-Texas), the former chair of the House Foreign Affairs Committee, said on X'])
_also('MA54', ['man-nyt-1108-02'] * 2, ["I think he's an honorable guy. I think he probably has an excuse for it", '"No, I don\'t think so," the president said'])
_also('MA55', ['man-nyt-1109-01'], ['I know the F.B.I. is looking into it in terms of something else'])
_also('MA62', ['man-nyt-1112-07'], ['board met for several hours Wednesday evening'])
_also('MA64', ['man-ft-1109-05'], ['before paring losses to close 4.3 per cent lower'])
_also('MA66', ['man-ft-1112-05'], ['Nvidia shares have slumped 13 per cent at the open'])
_also('MA68', ['man-9e4f3db24cad'], ['$26 billion in a private placement to companies'])
_also('MA74', ['nbc-1108-investigation'] + ['art-fc-rec-mirage-rubio-1109'] * 2,
      ["Speaking Sunday to reporters in Florida shortly after Nvidia's announcement", "And I also can't comment on an internal corporate matter that's going on with Nvidia", 'Rubio Speaks to Press as Secretary of State 9 November'])
_also('MA87', [_X + '2120688743111971293'] * 2 + ['man-f2f8fbf1fc93'], ['That would be an honor', 'Thu Nov 12 01:22:51 +0000 2026', 'on Wednesday said it "would be an honor" to hire Huang'])
_also('MA88', ['man-wapo-1112-02'], ["Two mistakes don't make a right, and I believe Jensen is irreplaceable for America's AI leadership"])
_also('MA90', [_X + '2120887322312921465'] * 2, ['A sad day for NVIDIA, developers, America, and all humanity', 'Thu Nov 12 14:31:56 +0000 2026'])
_also('MA98', [_X + '2120921049097187618'] * 2, ["Despite Jensen Huang's resignation, Congress must demand answers from Mr. Huang and others at Nvidia", 'Thu Nov 12 16:45:57 +0000 2026'])
_also('MA99', ['man-nyt-1112-09'], ['must explain why they have not closed export control loopholes'])
_also('MA100', [_X + '2119855894318252137'] * 2 + ['man-politico-1110-02'],
      ["I'm pushing to investigate Jensen Huang and Nvidia to determine whether our national security was compromised", 'Mon Nov 09 18:13:24 +0000 2026', 'wrote on X Monday that he is'])
_also('MA102', ['art-fc-tovima-wsj-1110'], ['"BIS conducts all enforcement strictly by the book," a spokesman said'])
_also('MA104', ['man-ft-1112-05'], ['there is only one man to take his place - TIM COOK of Apple. A Legend replaces a Legend!'])
_also('MA105', ['art-fc-tovima-wsj-1108-board'], ["Today's news will not slow NVIDIA. Jensen is committed to continuing to lead NVIDIA as CEO without interruption"])
_also('MA127', [_X + '2119543114222522593'] * 2, ['Meanwhile pushing to sell maximum of cutting edge AI chips to China against advice of ~entire natsec community', 'Sun Nov 08 21:30:32 +0000 2026'])
_also('MA135', [_X + '2120883918119592037'] * 3, ['This whole thing sucks, and I wish none of it had happened', "we'll keep fighting for open-source AI, harder than ever", 'Thu Nov 12 14:18:24 +0000 2026'])
_also('MA136', [_X + '2120888881717612576'] * 2, ["It's a mistake for Nvidia to let Jensen resign", 'Thu Nov 12 14:38:08 +0000 2026'])
# the letter carries its own day, and the FT gives it too: Wyden's chip no longer sits on a report's day
_also('MA152', ['art-own-waysandmeans-wyden-neal-letter-1112'] * 2, ['November 12, 2026 The Honorable Howard Lutnick', 'the Administration did not appear to acknowledge this evident national security threat'])
_also('MA31', ['art-own-wyden-neal-letter-1112', 'man-a45550a35921'], ['November 12, 2026 The Honorable Howard Lutnick', 'In a letter addressed to Lutnick on Thursday, Senator Ron Wyden and Congressman Richard Neal requested'])



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
    for i, (a, b, kind, label, src, q) in enumerate(TIES_V8, len(TIES_MORE) + len(ARCS) + len(TIES_V3) + len(TIES_V4) + len(TIES_V5) + len(TIES_V6) + len(ARCS_V6) + len(TIES_V7) + 1):
        assert b in names and (kind == 'context' or (a in left and kind in ('role', 'money', 'past', 'named'))) and len(src) == len(q), (a, b)
        out.append({'row_id': f'MT{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    return out
