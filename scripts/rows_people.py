"""Rows for three figures: the former officials the article lists (BENCH), the documented ties drawn in the
map (TIES), and members of Congress who acted on Huang in the fortnight (ACTIONS).
Each `src`/`q` pair is a saved original and a passage found in it word for word (scripts/check_rows.py)."""

A = 'x-dream1984-article'
FEC = 'table:anthropac_by_recipient.csv#'
PK = 'pack:'

# status: confirmed = a saved document states the Anthropic role; reported = one press report, as an adviser;
#         open = no document found here for the Anthropic role
BENCH = [
 # person, article's group, government post, anthropic role, status, note, src, q
 ('Tarun Chhabra', 'Biden', 'National Security Council, 2021–2025; coordinator for technology and national security',
  'Head of national security policy', 'confirmed', 'Sampled CSET rosters from 2019 to 2021 also list him as a senior fellow.',
  ['hoover-chhabra', PK + 'toner/research/cset_people.csv#TCP234'],
  ['Tarun Chhabra is head of national security policy at Anthropic. He previously served as deputy assistant to the president and coordinator for technology and national security', 'Tarun Chhabra is listed as Senior Fellow']),
 ('Ben Buchanan', 'Biden', 'White House special adviser for AI, June 2023 to January 2025',
  'Adviser, per one May 2025 report', 'reported', 'Reported once, by Semafor; no company document saved here names him.',
  ['semafor-0530-buchanan', PK + 'lineage/research/tenures.csv#T5998'],
  ['Ben Buchanan, another Biden official, is an adviser.', 'White House special adviser for AI from June 2023 until January 2025']),
 ('Elizabeth Kelly', 'Biden', 'Founding director, U.S. AI Safety Institute, Department of Commerce',
  'Head of Beneficial Deployments', 'confirmed', '',
  ['concordia-kelly', 'concordia-kelly'],
  ['Elizabeth Kelly is Head of Beneficial Deployments at Anthropic', 'She was the founding Director of the U.S. Artificial Intelligence Safety Institute']),
 ('Joel Meyer', 'Biden', 'Deputy assistant secretary for strategic initiatives, Department of Homeland Security',
  'Head of Federal Civilian, Public Sector', 'confirmed', 'Founding member of CSET\'s advisory board, October 2025.',
  ['cset-advisory-board'],
  ['Joel Meyer is Head of Federal Civilian, Public Sector for Anthropic. Previously, he served as Deputy Assistant Secretary for Strategic Initiatives at the U.S. Department of Homeland Security']),
 ('Benjamin Della Rocca', 'Biden', 'Director for technology and national security, National Security Council (White House list, September 2024)',
  'Not confirmed here', 'open', 'The government post is documented; no document found for a role at Anthropic.',
  [A, PK + 'lineage/research/tenures.csv#T6005'],
  ['Benjamin Della Rocca and Kristine Lee', 'Benjamin Della Rocca, Director for Technology']),
 ('Kristine Lee', 'Biden', 'National Security Council staff, per the article',
  'Not confirmed here', 'open', 'No document found for either post.',
  [A], ['Benjamin Della Rocca and Kristine Lee']),
 ('Chris Liddell', 'Trump', 'Deputy White House chief of staff in Trump\'s first term',
  'Board of directors, since February 2026', 'confirmed', '',
  ['cnbc-1009-poach', PK + 'lineage/research/tenures.csv#T138'],
  ['who served as the deputy White House chief of staff during Trump\'s first term, to its board of directors in February', 'Chris Liddell has been appointed to Anthropic’s Board of Directors']),
 ('Sihao Huang', 'Trump', 'Senior policy advisor for AI, White House Office of Science and Technology Policy',
  'Head of frontier compute strategy, since September 2026', 'confirmed', '',
  ['cnbc-1009-poach'],
  ['AI lab in September as head of frontier compute strategy. He was previously a senior policy advisor for AI and emerging technology at the White House Office of Science and Technology Policy']),
 ('Sarah Heck', 'Trump', 'National Security Council, per the article only (not confirmed here)',
  'Head of Policy', 'confirmed', 'The Anthropic title is in her court declaration; her NSC service and its dates were not confirmed here.',
  ['heck-declaration', A],
  ['my role as Head of Policy', 'Sarah Heck']),
 ('Mary Croghan', 'Trump', 'Project manager, White House Office of Cabinet Affairs, March to December 2020',
  'Registered lobbyist for Anthropic', 'confirmed', '',
  [PK + 'congress/research/revolving_door.csv#RD249', 'semafor-0530-buchanan'],
  ['Office of Cabinet Affairs/White House (Mar-Dec2020)', 'lobbyist Mary Croghan']),
]

# kind: money | role (current post) | past (former post) | seat (governance seat) | grant | panel (appeared together)
TIES = [
 # a, b, kind, label, src, q
 ('Anthropic', 'AnthroPAC', 'role', 'its connected PAC, registered April 3, 2026',
  [PK + 'congress/research/timeline.csv#TL111'], ['naming Anthropic PBC as the connected organization']),
 ('Jack Clark', 'AnthroPAC', 'money', '$5,000 · Jul 31, 2026',
  [PK + 'congress/research/hard_money.csv#HM109'], ['"contribution_receipt_amount":5000.0']),
 ('AnthroPAC', 'Sen. Chuck Schumer', 'money', '$3,500 · Sep 25', [FEC + 'FRIENDS OF SCHUMER'], ['3500.00']),
 ('AnthroPAC', 'Sen. Chris Coons', 'money', '$2,500 · Jul 7', [FEC + 'CHRIS COONS FOR DELAWARE'], ['2500.00']),
 ('AnthroPAC', 'Sen. Kevin Cramer', 'money', '$1,000 · Jul 7', [FEC + 'CRAMER FOR SENATE'], ['1000.00']),
 ('AnthroPAC', 'Rep. Brian Mast', 'money', '$2,500 · Jul 7', [FEC + 'MAST FOR CONGRESS'], ['2500.00']),
 ('AnthroPAC', 'Rep. Rick Crawford', 'money', '$1,000 · Jul 7', [FEC + 'CRAWFORD FOR CONGRESS'], ['1000.00']),
 ('Anthropic', 'Public First Action', 'money', '$40 million · Feb and Jul 2026 · for policy and education work, it says',
  ['anthropic-pfa-2', 'anthropic-pfa-2'], ['bringing our total support to $40 million', 'cannot be used to influence the election of any candidate']),
 ('Public First Action', 'Rep. Brian Mast', 'ad', 'ads naming him announced · Jul 2026', ['art-pfa-conservative'], ['Rep. Brian Mast']),
 ('Public First Action', 'Rep. John Moolenaar', 'ad', 'ads naming him announced · Jul 2026', ['art-pfa-conservative'], ['Rep. John Moolenaar']),
 ('Anthropic', 'Jack Clark', 'role', 'co-founder', [PK + 'lineage/research/tenures.csv#T130'], ['Jack Clark co-founded Anthropic']),
 ('Anthropic', 'Tarun Chhabra', 'role', 'head of national security policy', ['hoover-chhabra'], ['Tarun Chhabra is head of national security policy at Anthropic']),
 ('Anthropic', 'Holden Karnofsky', 'role', 'joined the staff, Jan 2025', [PK + 'lineage/research/tenures.csv#T142'], ['joined Anthropic last month']),
 ('Anthropic', 'Richard Fontaine', 'seat', 'trustee of the body that will elect most of its board',
  ['art-anthropic-fontaine', 'anthropic-ltbt'], ['appointment of Richard Fontaine, CEO of the Center for a New American Security, as a new member of the Trust', 'the Trust will elect a majority of the board within 4 years']),
 ('Richard Fontaine', 'CNAS', 'role', 'chief executive', ['art-anthropic-fontaine'], ['Richard Fontaine, CEO of the Center for a New American Security']),
 ('Holden Karnofsky', 'Open Philanthropy', 'past', 'led it until 2023', [PK + 'lineage/research/tenures.csv#T022'], ['He served as Open Philanthropy’s CEO and then co-CEO until 2023']),
 ('Open Philanthropy', 'CSET at Georgetown', 'grant', '$55M in Jan 2019; $107.75M in five awards',
  [PK + 'toner/research/cset_money.csv#TCS232'], ['$55M (2019-01-25)']),
 ('Jack Clark', 'CSET at Georgetown', 'past', 'listed as non-resident fellow, Jan 2020–Jan 2022 rosters', [PK + 'toner/research/cset_people.csv#TCP119'], ['Research Fellow (non-resident)']),
 ('Tarun Chhabra', 'CSET at Georgetown', 'past', 'listed as senior fellow, 2019–21 rosters', [PK + 'toner/research/cset_people.csv#TCP234'], ['Tarun Chhabra is listed as Senior Fellow']),
 ('CSET at Georgetown', 'Ryan Fedasiuk', 'past', 'listed as research analyst, 2019–22 rosters', [PK + 'toner/research/cset_people.csv#TCP215'], ['Ryan Fedasiuk is listed as Research Analyst']),
 ('Tarun Chhabra', 'NSC technology office', 'past', 'led it, 2021–25', ['hoover-chhabra'], ['From 2021 to 2025, Chhabra coordinated US strategies for technology competition']),
 ('NSC technology office', 'Chris McGuire', 'past', 'deputy senior director, 2022–24', ['cfr-mcguire'], ['deputy senior director for technology and national security at the National Security Council (NSC), where he served from 2022 to 2024']),
 ('Tarun Chhabra', 'Chris McGuire', 'panel', 'scheduled for the same session, Taipei, Jun 6, 2026', ['art-dset-forum', 'art-dset-forum'],
  ['Head of National Security Policy, Anthropic', 'Chris McGuire｜Senior Fellow for China and Emerging Technologies']),
]

# What each person on the right-hand side of the map did between Oct 29 and Nov 12, 2026.
ACTIONS = [
 # person, fec committee name or '', what, date, src, q
 ('Rep. Brian Mast', 'MAST FOR CONGRESS', 'Signed the Nov 4 letter; on Nov 11 said "yes" to a subpoena', '2026-11-04',
  ['house-hfac-letter-pr', 'cnbc-1111-congress-resign'], ['House Foreign Affairs Committee Chairman Brian Mast', 'Mast said "yes."']),
 ('Rep. Rick Crawford', 'CRAWFORD FOR CONGRESS', 'Signed the Nov 4 letter', '2026-11-04',
  ['house-hfac-letter-pr', 'cnbc-1111-congress-resign'], ['House Permanent Select Committee on Intelligence Chairman Rick Crawford', 'called for Huang to appear in a Nov. 4 letter']),
 ('Rep. John Moolenaar', '', 'Signed the Nov 4 letter; on Nov 10 said Congress should "get to the bottom" of it', '2026-11-04',
  ['house-hfac-letter-pr', 'cnbc-1110-schumer'], ['Select Committee on China Chairman John Moolenaar', 'get to the bottom']),
 ('Sen. Chris Coons', 'CHRIS COONS FOR DELAWARE', 'Posted "Congress will investigate"', '2026-11-07',
  ['cnbc-1108-bipartisan'], ['Congress will investigate and get answers.']),
 ('Sen. Chuck Schumer', 'FRIENDS OF SCHUMER', 'Floor speech; urged passing three chip-export bills', '2026-11-10',
  ['cnbc-1110-schumer'], ['We also need answers on Nvidia\'s influence campaign']),
 ('Sen. Kevin Cramer', 'CRAMER FOR SENATE', 'Said Huang should resign', '2026-11-09',
  ['art-roic-cramer', 'cnbc-1111-congress-resign'], ["I just think he's got to go", 'As a matter of his own conscience, he should resign']),
 ('Rep. Seth Magaziner', '', 'Called for Huang and the Commerce secretary to testify (reported Nov 8)', '2026-11-08',
  ['cnbc-1108-bipartisan'], ['called on Commerce Secretary Howard Lutnick to testify before Congress along with Huang']),
 ('Rep. Suhas Subramanyam', '', 'Said Huang should resign', '2026-11-11',
  ['cnbc-1111-congress-resign'], ['"Jensen Huang should resign from Nvidia," Rep. Suhas Subramanyam']),
 ('Rep. Don Bacon', '', 'Asked if Huang should resign: "From the little I know, yes"', '2026-11-11',
  ['cnbc-1111-congress-resign'], ['Bacon told CNBC in response to whether Huang should resign']),
 ('Chris McGuire', '', 'Post recapping the reports, 9.4 million views', '2026-11-06',
  ['x-mcguire-nov6'], ['The story keeps getting crazier']),
 ('Ryan Fedasiuk', '', 'Podcast "Jensen Huang Must Resign" (an undated summary, saved Nov 12)', '2026-11-12',
  ['biggo-fedasiuk'], ['Ryan Fedasiuk: Jensen Huang Must Resign']),
]


def rows():
    out = []
    for i, (person, group, gov, role, status, note, src, q) in enumerate(BENCH, 1):
        assert status in ('confirmed', 'reported', 'open') and len(src) == len(q)
        out.append({'row_id': f'BN{i:02d}', 'person': person, 'group': group, 'gov': gov, 'role': role, 'status': status, 'note': note, 'src': src, 'q': q})
    for i, (a, b, kind, label, src, q) in enumerate(TIES, 1):
        assert len(src) == len(q)
        out.append({'row_id': f'TI{i:02d}', 'a': a, 'b': b, 'kind': kind, 'label': label, 'src': src, 'q': q})
    for i, (person, fec, what, date, src, q) in enumerate(ACTIONS, 1):
        assert len(src) == len(q)
        out.append({'row_id': f'AC{i:02d}', 'person': person, 'fec': fec, 'what': what, 'date': date, 'src': src, 'q': q})
    return out
