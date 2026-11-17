"""Run: python3 -I scripts/nv8_reading_lanes.py      (written Nov 16, 2026, with the answer to the eighteenth reading)
What the gauges do not see, read by independent readers (another company's model, one lane each, files in research/reading_lanes/):
  single_nv8_a  every direct quotation of a drawn actor on a counted page that no chip carried by its words and that only ONE counted article
                gives (the third gauge lists such a remark only from two articles up): 294 groups and 7 planted controls;
  para_nv8_a    every census line by Nvidia that is not a direct quotation of seven words or more and that no chip of the company carried by
                its words (1,162 lines; two acts held out as controls), sorted by the reader into the acts they describe;
  para_nv8_b    the same for the board, its chairman and the interim chief (865 lines; two acts held out).
  para_nv8_c to para_nv8_h (added later on Nov 16)   the same for every other drawn actor, in six lanes (2,949 lines; two acts held out in each): Huang; the president and the White House;
                China's ministry and embassy, the Global Times, Taiwan and Singapore; the three House chairmen; Megaspeed and four departments; and the 62 other actors.
The controls: acts taken out of the table of chips the reader was given, so that the lines only they carried stood among the lines. A reader
that does not call them missing is not relied on. The reader gave each group or act one verdict; the builder then checked every CANDIDATE
against its saved page and wrote one disposition for each below (an act it is drawn on, or the reason it is not drawn). The other verdicts
(carried, reason, not on the matter, outside the days, not the actor's) are the reader's and were not read again by the builder.
  earlier_nv8_a (added after the twentieth reading)   a second reading, by a further reader, of the 67 groups and acts that the readers above had set aside as
                'outside the days' (things said or done before Oct 29 that a page of these days reports); four acts held out as controls, three of which had an item.
  recall_nv8_01 to recall_nv8_12 (Nov 17)   twelve further readers who together read every counted article once (1,154 articles, one page each) for reports of
                earlier acts; two acts that are such reports were held out of each reader's table of chips. Their lines are pooled in research/reading_lanes/recall_nv8.pool.tsv
                (scripts/nv8_recall_pool.py), which holds words of the pages and is not published; the published table gives each line without them.
Writes research/nv8_single_article_remarks.tsv, research/nv8_paraphrased_acts.tsv, research/nv8_earlier_acts.tsv and research/nv8_recalls.tsv. Stops on a candidate with no disposition.
Limits: these are the lines of the census readings, so a remark no census reader recorded is not here; the first two paraphrase readers were told
to set aside what was said before Oct 29, so they did not look for reports of these days about an earlier act (the six later lanes were told to);
and four of the six later lanes closed 'reading: incomplete', leaving acts with no verdict where the saved context did not settle which occasion a
line belongs to (the script prints how many acts and lines). Where a paper that has its own row reports an earlier act of someone else, the report is drawn
on the paper's row, and a reader's candidate for it on the other actor's row is answered 'carried on the paper's row'."""
import csv, re, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; L = R / 'reading_lanes'; sys.path.insert(0, str(ROOT / 'scripts'))
import rows_map
OLD = ('not drawn: the page gives it as background, the company\'s answer "at the time" to a different claim (that a Chinese model was trained on smuggled chips); it answers nothing about this affair. '
       'That it is earlier is not the reason: a report of these days about an earlier act on the matter is drawn (reason corrected after the nineteenth reading)')
SUMMARY = 'not an act of these days: the page sums up the company\'s standing position ("says", "has said") and names no occasion'
D = lambda *ids: 'drawn: ' + ', '.join(ids)
# single_nv8_a: the reader's candidates, each with the builder's disposition
ONE = {
 'G002': D('MA261'), 'G022': D('MA261'), 'G008-b': D('MA12'), 'G008-c': D('MA12'), 'G013': D('MA272'), 'G181': D('MA272'), 'G208': D('MA272'), 'G014': D('MA13'), 'G271': D('MA13'),
 'G016': D('MA264'), 'G250': D('MA264'), 'G199': D('MA264'), 'G282-b': D('MA264'), 'G282-c': D('MA264'), 'G017': D('MA42'), 'G123': D('MA42'), 'G213': D('MA42'), 'G219': D('MA42'), 'G244': D('MA42'), 'G297': D('MA42'),
 'G025': D('MA243'), 'G029': D('MA275'), 'G033': D('MA63'), 'G035': D('MA278'), 'G047': D('MA262'), 'G130': D('MA262'),
 'G285': 'drawn with the sentence the page prints just before it, that it would not hurt to hear from the Commerce Department (MA262)',
 'G051': D('MA132'), 'G156': D('MA132'), 'G276': D('MA132'), 'G299': D('MA132'),
 'G107': D('MA132') + ' (first set aside as a step in the argument; the nineteenth reading judged it a hedge on what the affair explains)',
 'G053': D('MA255'), 'G057': D('MA266'), 'G060': D('MA280'), 'G067': D('MA276'), 'G068': D('MA172'), 'G068-b': D('MA172'), 'G069': D('MA277'), 'G141': D('MA277'), 'G070': D('MA282'), 'G071': D('MA284'),
 'G072': D('MA265'), 'G255': D('MA265'), 'G079': D('MA285'), 'G088': D('MA281'), 'G287': D('MA281'), 'G089': D('MA287'), 'G090': D('MA286'), 'G092': D('MA283'), 'G280': D('MA283'), 'G093': D('MA267'), 'G117': D('MA267'),
 'G094': D('MA279'), 'G102': D('MA279'), 'G097': D('MA19'), 'G104': D('MA45'), 'G104-b': D('MA268'), 'G111': D('MA270'), 'G113': D('MA269'), 'G291': D('MA269'),
 'G121-b': D('MA111'), 'G136': D('MA111'), 'G186': D('MA111'), 'G248': D('MA111'), 'G249': D('MA111'), 'G128': D('MA289'), 'G135': D('MA151'), 'G137': D('MA106'), 'G137-b': D('MA106'), 'G142': D('MA274'),
 'G157': 'not drawn: a staff meeting about a product keynote; that it answered the scandal is the paper\'s characterisation, which the figure does not draw (the reader called it borderline)',
 'G159': D('MA273'), 'G218': D('MA273'), 'G171': D('MA210'), 'G173': D('MA263'), 'G193': D('MA288'), 'G194': D('MA256'), 'G196': D('MA259'), 'G203': OLD, 'G229': OLD,
 'G214': D('MA52'), 'G223': D('MA52'), 'G275': D('MA52'), 'G215': 'drawn on his chip of Oct 31 (MA123): the pool report of that evening prints the answer, so it is part of that exchange and not of the later page\'s day',
 'G220': D('MA115'), 'G221': D('MA115') + ' (first set aside; the nineteenth reading judged it a direct answer to the question about the summit)',
 'G224': D('MA251'), 'G224-b': D('MA251'), 'G224-c': D('MA251'), 'G232': D('MA35'), 'G266': D('MA78'), 'G269': D('MA290'), 'G269-b': D('MA290'), 'G273': D('MA291'), 'G288': D('MA157'), 'G292': D('MA271'),
 'G294': 'not drawn: a translated account of the Times\'s report; the board\'s own statement does not hold the clause, and what the company said of his staying is on its chip of that day (MA105)',
 'G296': D('MA257'), 'G296-b': D('MA257'), 'G298': D('MA70'),
}
CTL = lambda i: f"carried by {i}, which was held out of the reader's table as a control"
NOOCC = "not drawn: a later page's summary that he denied compromising security, naming no occasion; his denials that have an occasion are on his chips (the interview of Oct 29, the call the president relates)"
T101 = "carried on the Times's row: a detail of its report of Nov 9 (MA101)"
MARCH = 'not drawn: it recalls a call the two senators made in March'
PARA = {
 # the six later lanes
 ('c', 'A004'): NOOCC, ('c', 'A016'): NOOCC, ('c', 'A033'): NOOCC, ('c', 'A034'): NOOCC, ('c', 'A035'): NOOCC, ('c', 'A036'): NOOCC, ('c', 'A037'): NOOCC, ('c', 'A005'): D('MA292'), ('c', 'A006'): CTL('MA170'), ('c', 'A007'): D('MA296'),
 ('c', 'A008'): CTL('MA211'), ('c', 'A009'): D('MA297'), ('c', 'A017'): 'not drawn: a summary that names no occasion; his memo of that day holds no such sentence', ('c', 'A021'): "not drawn: the memo names no one; the page's own gloss",
 ('c', 'A031'): "not drawn: the page runs his pledge to cooperate with the board's inquiry together with the FBI's; the pledge is on his chip of Nov 8 (MA58)", ('c', 'A039'): D('MA296'),
 ('d', 'A007'): CTL('MA54'), ('d', 'A009'): CTL('MA54'), ('d', 'A016'): D('MA55'), ('d', 'A017'): CTL('MA54') + '; this page gives Monday for a remark the Times and NBC give for Sunday',
 ('d', 'A020'): D('MA01') + " (on the Times's row)", ('d', 'A021'): D('MA294') + " (on the FT's row)", ('d', 'A026'): "not drawn: a page's own summary of his remarks of that week", ('d', 'A027'): "not drawn: the reader's words are not in the page as saved",
 ('d', 'A028'): D('MA298'), ('d', 'A032'): CTL('MA202'), ('d', 'A036'): "not drawn: an account of what was not done a year earlier; the first report's finding is on the Times's chip of Oct 29 (MA01)",
 ('d', 'A038'): 'carried: the same referral as to Newsweek that day (MA202)', ('d', 'A041'): D('MA202'), ('d', 'A045'): 'not drawn: a reply about his share trades for which the page gives no day',
 ('d', 'A058'): 'carried: a relay of his remark of Sunday that he would take Huang along (MA224)',
 ('e', 'A004'): 'not drawn: the ministry on relations between the two countries, in the same answer; read the same way as its sibling sentence in the third gauge', ('e', 'A011'): CTL('MA92'), ('e', 'A015'): D('MA299'),
 ('e', 'A017'): "not drawn: the reader's words are not in the page as saved; the paper's commentary is on its chip (MA95)", ('e', 'A018'): CTL('MA70'), ('e', 'A019'): CTL('MA70'), ('e', 'A020'): D('MA72'), ('e', 'A028'): D('MA293') + " (on the Times's row)",
 ('e', 'A030'): "carried on the Journal's row: a relay of its report of Oct 30 (MA06)", ('e', 'A031'): 'carried: its officials\' statements that they are investigating are on its chips of Nov 10 and 11 (MA218, MA94)',
 ('e', 'A037'): "not drawn: a one-line paraphrase that names no piece and no day, on a page changed after Nov 8; the paper's commentary of Nov 9 is on its chip (MA95)",
 ('f', 'A004'): CTL('MA124'), ('f', 'A006'): D('MA38'), ('f', 'A007'): 'carried: the same position that day (MA38)', ('f', 'A008'): D('MA264', 'MA265'), ('f', 'A010'): 'carried: the same statement as to the FT that day (MA265)', ('f', 'A011'): D('MA262'),
 ('f', 'A013'): D('MA303'), ('f', 'A015'): D('MA49'), ('f', 'A016'): CTL('MA96'), ('f', 'A017'): D('MA305'), ('f', 'A018'): "not drawn: background on his committee's inquiries of 2025", ('f', 'A019'): "not drawn: background on his committee's inquiries of 2025",
 ('f', 'A020'): D('MA306'), ('f', 'A021'): 'not drawn: a relay that names no occasion; his interviews of that week are on his chips', ('f', 'A022'): D('MA304'),
 ('g', 'A003'): "not drawn: a page's summary that names no occasion", ('g', 'A008'): "carried on the Times's row: a relay of its report of Nov 7 (MA03)", ('g', 'A012'): D('MA301'), ('g', 'A013'): D('MA295') + " (on the FT's row)", ('g', 'A015'): D('MA301'),
 ('g', 'A016'): D('MA01') + " (on the Times's row)", ('g', 'A020'): T101, ('g', 'A028'): T101, ('g', 'A029'): T101, ('g', 'A030'): T101, ('g', 'A021'): "not drawn: a blog's relay of a Journal account of earlier years",
 ('g', 'A022'): D('MA102'), ('g', 'A023'): D('MA102'), ('g', 'A032'): D('MA207'), ('g', 'A033'): 'carried: the exchange at the meeting of Nov 5 (MA76, MA108)', ('g', 'A034'): D('MA207'), ('g', 'A035'): D('MA300'), ('g', 'A036'): D('MA139') + " (on the Times's row)",
 ('g', 'A037'): D('MA213'), ('g', 'A038'): "drawn in part (MA301): the finding Politico reports is drawn; the relaying outlet's own characterisation of the department's leaders is left out", ('g', 'A039'): D('MA102'),
 ('g', 'A040'): 'not drawn: background on inspections before these days', ('g', 'A043'): "carried on the Times's row: a relay of its report of Nov 7 (MA03)", ('g', 'A044'): 'not drawn: a one-line recall of an approval earlier in the year, naming no report',
 ('g', 'A052'): D('MA01') + " (on the Times's row)", ('g', 'A058'): D('MA302'), ('g', 'A065'): "not drawn here: the reader's words are not in the page as saved; its statement of Nov 12 is on its chips (MA93, MA229)", ('g', 'A090'): "not drawn: an editorial's summary of its earlier denials",
 ('g', 'A091'): "not drawn: the reader's words are not in the page as saved; a paper's finding in company documents about 2024", ('g', 'A092'): CTL('MA157'), ('g', 'A137'): "carried on the Times's row: its report of the memo (MA04)",
 ('g', 'A138'): "carried on the Times's row (MA138)", ('g', 'A142'): CTL('MA178'), ('g', 'A143'): D('MA295') + " (on the FT's row)", ('g', 'A146'): "not drawn: a blog's garbled relay of the Times's report (MA138)",
 ('g', 'A147'): "not drawn: a detail of the Times's first report, whose chip gives its main findings (MA01)",
 ('h', 'A006'): MARCH, ('h', 'A091'): MARCH, ('h', 'A008'): MARCH, ('h', 'A098'): MARCH, ('h', 'A010'): D('MA307'), ('h', 'A015'): 'carried: his point to Fortune that day (MA130)', ('h', 'A019'): CTL('MA22'), ('h', 'A021'): D('MA308'), ('h', 'A037'): D('MA160'),
 ('h', 'A047'): D('MA45'), ('h', 'A048'): D('MA45'), ('h', 'A051'): D('MA34') + ' (the same remarks as his chip of that day, in another outlet\'s words)', ('h', 'A052'): D('MA309'), ('h', 'A058'): 'not drawn: an earlier post the page sums up without a day; his posts of Nov 6 and Nov 8 are on his chips',
 ('h', 'A059'): D('MA310'), ('h', 'A060'): D('MA116'), ('h', 'A062'): D('MA167'), ('h', 'A066'): D('MA128'), ('h', 'A067'): D('MA283'), ('h', 'A068'): 'carried: his point on the BBC (MA140)', ('h', 'A070'): CTL('MA87'), ('h', 'A073'): D('MA311'),
 ('h', 'A075'): D('MA152'), ('h', 'A084'): 'not drawn: what a complaint asks for; the chip says a suit was filed (MA84)', ('h', 'A086'): D('MA90'), ('h', 'A087'): D('MA267'), ('h', 'A093'): D('MA99'), ('h', 'A095'): D('MA99'), ('h', 'A096'): D('MA99'),
 ('h', 'A100'): 'carried: her statement of Oct 29 (MA19)',
 # the first two lanes
 ('a', 'A002'): D('MA226'), ('a', 'A008'): 'carried by MA57, which was held out of the reader\'s table as a control', ('a', 'A009'): 'carried by MA57, which was held out of the reader\'s table as a control',
 ('a', 'A011'): D('MA60'), ('a', 'A012'): D('MA105'), ('a', 'A023'): D('MA63'), ('a', 'A024'): D('MA63'), ('a', 'A025'): D('MA243'), ('a', 'A027'): D('MA60'), ('a', 'A037'): D('MA179'), ('a', 'A039'): D('MA260'),
 ('a', 'A044'): SUMMARY, ('a', 'A046'): D('MA253'), ('a', 'A056'): D('MA257'), ('a', 'A057'): SUMMARY, ('a', 'A058'): SUMMARY, ('a', 'A061'): D('MA252'), ('a', 'A063'): D('MA256'), ('a', 'A066'): SUMMARY,
 ('a', 'A071'): D('MA85'), ('a', 'A085'): D('MA63'), ('a', 'A095'): SUMMARY, ('a', 'A099'): SUMMARY, ('a', 'A104'): 'carried: a relay of its reply of Nov 6 that it does not share classified information with customers (MA179)',
 ('a', 'A106'): D('MA256'), ('a', 'A107'): D('MA256'), ('a', 'A111'): D('MA256'), ('a', 'A112'): D('MA254'), ('a', 'A116'): D('MA258'), ('a', 'A119'): D('MA255'),
 ('a', 'A120'): 'carried: a relay of its statements of that day that the block on sales stands (MA255, MA256)',
 ('a', 'A121'): D('MA312') + ' (first read as the statement of the day before given to another outlet; the nineteenth reading: one repeated sentence does not prove that)',
 ('b', 'A002'): D('MA60'), ('b', 'A003'): 'carried by MA61, which was held out of the reader\'s table as a control', ('b', 'A005'): D('MA260'), ('b', 'A006'): D('MA260'), ('b', 'A007'): D('MA62'), ('b', 'A011'): D('MA243'),
 ('b', 'A012'): D('MA260'), ('b', 'A013'): D('MA260'), ('b', 'A014'): D('MA260'), ('b', 'A023'): 'carried by MA215, which was held out of the reader\'s table as a control',
 ('b', 'A025'): 'not drawn: her signature on the company\'s filing; the filing is on the board\'s chip of that day (MA63)', ('b', 'A032'): D('MA316') + ' (first read as a relay of the Wednesday-night meeting; the nineteenth reading: the page dates its own report, and the chip says the identity is open)', ('b', 'A033'): D('MA260'),
}


# People who are not drawn and hold no public office are named by role, in the lines' first words and in the readers' own words too.
# The names and their roles are in a file that is not published (research/reading_lanes/roles.private.tsv: pattern, role, one per line).
SCRUB = [tuple(x.split('\t')) for x in (L / 'roles.private.tsv').read_text().split('\n') if x.strip() and not x.startswith('#')]

# Dispositions changed in answer to the twentieth reading (Nov 16, 2026). It read all 53 candidates of lanes c to h that the builder had not
# drawn and found that the builder had set aside reports of earlier acts for their date, and four candidates on the false ground that the
# reader's words were not in the page (the builder's check compared several passages as one string). The earlier dispositions stand above.
W = lambda i, why: D(i) + f' (first set aside: {why}; drawn after the twentieth reading)'
PARA.update({
 ('f', 'A017'): D('MA96') + ' (first drawn as its own act, MA305, withdrawn since: the relay links the statement MA96 already carried)',
 ('c', 'A039'): D('MA328') + ' (first joined to MA296; the pages do not prove it is that meeting, so it has its own act on its report\'s day)',
 ('d', 'A045'): W('MA319', 'the page gives the reply no day'), ('e', 'A017'): W('MA95', 'the builder\'s check wrongly said the words were not in the page'),
 ('e', 'A031'): W('MA320', 'read as the minister\'s statements of Nov 10 and 11'), ('f', 'A007'): W('MA38', 'read as the same position that day'), ('f', 'A010'): W('MA265', 'read as the statement to the FT'),
 ('f', 'A019'): W('MA321', 'called background of 2025'), ('g', 'A008'): W('MA322', 'read as a relay of the Times\'s report of one assembly approval'), ('g', 'A029'): W('MA101', 'called a detail of the report'),
 ('g', 'A030'): W('MA101', 'called a detail of the report'), ('g', 'A033'): W('MA108', 'read as carried by the exchange'), ('g', 'A040'): W('MA323', 'called background before these days'),
 ('g', 'A044'): W('MA324', 'a one-line recall naming no report'), ('g', 'A065'): W('MA229', 'the builder\'s check wrongly said the words were not in the page'),
 ('g', 'A091'): W('MA325', 'the builder\'s check wrongly said the words were not in the page'), ('h', 'A006'): W('MA27', 'it recalls a call of March'), ('h', 'A008'): W('MA27', 'it recalls a call of March'),
 ('h', 'A091'): W('MA20', 'it recalls a call of March'), ('h', 'A098'): W('MA20', 'it recalls a call of March'), ('h', 'A015'): W('MA130', 'read as his point to another outlet'),
 ('h', 'A058'): W('MA326', 'an earlier post the page sums up; the post itself is embedded in the saved page and is saved now'), ('h', 'A084'): W('MA84', 'what a complaint asks for'),
 ('h', 'A100'): W('MA327', 'read as her statement of Oct 29'),
 ('d', 'A027'): 'not drawn: a reason given for a position already drawn (his proposal of a successor, MA104), with no new occasion named (the first reason, that the words were not in the page, was wrong: corrected after the twentieth reading)',
 ('d', 'A038'): 'not drawn: an unlocated referral; the page names no asking outlet, so it may be the reply to Newsweek of that day (MA202) but that is not established (reason corrected after the twentieth reading)',
 ('d', 'A058'): 'not drawn: the page places his interest in taking Huang to Asia at Monday\'s briefing, where the Times has him say it on Sunday (MA224); the pages do not settle which, and the remark is on his Sunday chip (reason corrected after the twentieth reading)',
 ('g', 'A147'): 'not drawn: an uncorroborated order of events in a relay (it puts the removal of her name after the inquiry began; the Times\'s first report describes a change of paperwork in 2023, before it) (reason corrected after the twentieth reading)',
 ('h', 'A068'): 'not drawn: an unlocated recap; the page speaks of "financial coverage" and names no outlet, so it may be his remarks on the BBC (MA140) but that is not established (reason corrected after the twentieth reading)',
})

# ---- earlier_nv8_a: the second reading of what the readers above set aside as 'outside the days' (Nov 16, after the twentieth reading) ----
# One disposition for each candidate of that reader, and for each item where the builder did not follow the reader's verdict. A report of these days about an
# earlier act on the matter is drawn on the day of the first saved page that carries it, dashed, in words that say whose report it is and that the act is earlier.
SUCC = (' (the reader called it not on the matter, under a brief whose definition of the matter left succession out; the figure draws acts on succession, '
        'so the builder drew his earlier remarks on it, on the day of the first saved page that recalls them)')
JRNL = (' on the Journal\'s row (its column of the evening of Nov 11); the refusal the column reports is now on the company\'s act of that day (MA195), and its act of Nov 12 (MA199) says so')
TIE = 'carried: it is a tie line of the figure ({}), which the table of chips the reader was given did not show'
EARLIER = {
 'single:G003': D('MA331'), 'a:A059': D('MA331') + ' (the same assurance as G003)', 'single:G108': D('MA332'), 'single:G184': D('MA332'), 'single:G055': D('MA336'),
 'a:A047': D('MA365') + ' (the reader\'s page is a copy of the news agency\'s dispatch; the disclosure it recalls is drawn on the Times\'s row at Nov 7, the first saved page that carries it; the chip first drawn for it, MA333, was withdrawn as its duplicate after the twenty-second reading)',
 'a:A054': D('MA334') + ' (one rule for every actor: a search of every counted page for a sum of money beside the word lobbying found CNBC\'s two reports of Nvidia\'s spending and no report of another actor\'s)',
 'a:A062': D('MA337'),
 'a:A076': D('MA338') + ' and, for the chief executive\'s remark in the same sentence, MA339; both on Nov 10, the day of the page that first relays the Axios report (the reader cited a page of Nov 11)',
 'single:G190': D('MA340') + JRNL, 'single:G238': D('MA340') + JRNL, 'single:G253': D('MA340') + JRNL, 'a:A041': D('MA340') + JRNL,
 'a:A053': TIE.format('Nvidia to President Trump, money: the gift to the ballroom project'),
 'a:A001': D('MA335'),
 'a:A082': D('MA335') + ' (the same response of Dec 10, 2025: the page links the report of that date; drawn on the day of the earlier page, which sets it against the reports of diversion)',
 'single:G116': D('MA341'), 'single:G279': D('MA341'), 'c:A028': D('MA342'), 'c:A048': D('MA342'), 'c:A044': D('MA343'), 'single:G217': D('MA344'), 'single:G082': D('MA346'),
 'single:G150': D('MA347') + ' (on Oct 29: a page of that day recalls the same statement of May 2025 in other words; the reader\'s page, of Nov 12, gives the words)',
 'single:G201': D('MA348'), 'd:A001': D('MA348'), 'single:G174': D('MA349'), 'd:A046': D('MA349'), 'single:G182': D('MA350'), 'g:A048': D('MA351'),
 'd:A057': 'carried: MA329 quotes it (an act held out of the reader\'s table as a control)',
 'g:A049': D('MA169') + ' (the translated account is on the department\'s act of Nov 12, which already cited the page; since the twenty-first reading the indictment itself is drawn on the first saved page that recalls it, of Oct 29: MA362)',
 'h:A009': D('MA352'), 'h:A101': D('MA353'),
 'h:A025': D('MA112') + ' (the act had no day; it sits now on Oct 29, the day of the first saved page of these days that reports the letter, and carries the request for an investigation)',
 'h:A026': D('MA354'), 'h:A103': D('MA355'), 'h:A064': D('MA356'),
 'h:A102': D('MA357') + ' (on her row, on Oct 29, the day of the page; the reader proposed a part of the Times\'s act MA327 of Nov 5)',
 'h:A003': TIE.format('Anthropic, context: the remark at Davos'),
 # items where the builder did not follow the reader
 'single:G222': D('MA345') + SUCC, 'single:G228': D('MA345') + SUCC,
 'single:G301': D('MA345') + ' (another line of the same interview; the chip names the interview and the page, and does not quote this line)' + SUCC,
 'single:G122': D('MA345') + ' (another line of the same interview; the chip names the interview and the page, and does not quote this line)' + SUCC,
}
SAME_INTERVIEW = 'not drawn: another answer of the interview whose remarks on succession are drawn (MA345); this one is on his management and the pressure of the post, as the reader said'
EARLIER.update({'single:G065': SAME_INTERVIEW, 'single:G066': SAME_INTERVIEW, 'single:G087': SAME_INTERVIEW})
# three items on which the second reader's verdict stood until the twenty-first reading (Nov 17), which would draw the first two and place the third's indictment on its first report
EARLIER.update({'a:A103': D('MA363') + ' (the second reader called the company\'s answer on financing not on the matter; the twenty-first reading would draw it, since the page ties it to what the resignation means for that financing)',
                'b:A028': D('MA364') + ' (the second reader called the finance chief\'s statement of 2023 not on the matter; the twenty-first reading would draw it, since the Times\'s profile of the interim chief gives it under her views on export policy; on the Times\'s row)',
                'single:G178': 'carried: the indictment of March is on the department\'s chip of Oct 29 (MA362), the first saved page that recalls it, and on the Journal\'s first report (MA06); this page, of Nov 9, recalls it later'})
E_CONTROL = {'a:A043': 'MA85', 'a:A078': 'MA85', 'c:A022': 'MA329', 'd:A022': 'MA330'}      # the items that only a held-out act carried
# the first reader's two candidates for the response of Dec 10, 2025: drawn now, from another page
NOW = (' (first set aside as the company\'s answer to a different claim in the page that carried it; another page of these days, of Nov 9, sets the same response of Dec 10, 2025 against the reports '
       'of diversion through Southeast Asia, so it is drawn on that page\'s day and this page gives its words; changed after the second reading of the set-aside items)')
ONE.update({'G203': D('MA335') + NOW, 'G229': D('MA335') + NOW})

# ---- recall_nv8_01 to _12: every counted article read for reports of earlier acts (Nov 17) ----
# Lines the builder has acted on, by page, actor and a few words of the passage; every other candidate line is open (not yet grouped or drawn).
R_DONE = [
 ('man-nyt-1110-01', 'huang', 'Lunacy', 'drawn: on the tie line MT57, beside the remark it answers'),
 ('sw-techcrunchcom-baccdaa9', 'anthropic', 'appealed directly to Washington', 'drawn: tie line MT62 (background on the row)'),
 ('sw-techcrunchcom-baccdaa9', 'openai', 'appealed directly to Washington', 'drawn: tie line MT64 (background on the row)'),
 ('sw-decryptco-31a5e63b', 'anthropic', 'spent millions lobbying', 'drawn: tie line MT63 (background on the row), with the page\'s caution and the denial it prints'),
 ('sw-decryptco-31a5e63b', 'anthropic', 'never advocated such a ban', 'drawn: tie line MT63 (background on the row)'),
 ('sw-decryptco-31a5e63b', 'openai', 'spent millions lobbying', 'drawn: tie line MT64 (background on the row)'),
 ('sw-decryptco-31a5e63b', 'openai', 'signed the pro-open-weight letter', 'drawn: tie line MT64 (background on the row)'),
 ('x-dream1984-article', 'anthropic', 'Coons received', 'carried: the member\'s line for this gift (research/member_ties.csv, TY003), a table the reader was not given'),
 ('x-dream1984-article', 'coons', 'Coons received', 'carried: the member\'s line for this gift (research/member_ties.csv, TY003), a table the reader was not given'),
 ('x-dream1984-article', 'anthropic', 'took $1,000 from AnthroPAC', 'carried: the member\'s line for this gift (TY007), a table the reader was not given'),
 ('x-dream1984-article', 'cramer', 'took $1,000 from AnthroPAC', 'carried: the member\'s line for this gift (TY007), a table the reader was not given'),
 ('x-dream1984-article', 'anthropic', 'also received $2,500 from AnthroPAC', 'carried: the member\'s line for this gift (TY051), a table the reader was not given'),
 ('x-dream1984-article', 'mast', 'also received $2,500 from AnthroPAC', 'carried: the member\'s line for this gift (TY051), a table the reader was not given'),
 ('x-dream1984-article', 'anthropic', '$40 million to Public First Action', 'carried: the figure\'s box for that group states the gifts, a part of the figure the reader was not given'),
 ('x-dream1984-article', 'anthropic', 'shared a stage at the DSET forum', 'carried: the figure draws the shared panel between the analyst and the Anthropic executive (rows of people), a table the reader was not given'),
 ('x-dream1984-article', 'mcguire', 'shared a stage at the DSET forum', 'carried: the figure draws the shared panel between the analyst and the Anthropic executive (rows of people), a table the reader was not given'),
 ('x-dream1984-article', 'anthropic', 'pushing for tighter curbs on AI chips to China', 'carried: tie line MT07 (the meeting of February and the announcement that followed)'),
 ('sw-cnncom-02', 'huang', 'die at his desk', 'drawn: MA359 (the remark to a podcaster, on the day of this page; the chip of Nov 11 keeps the later interview)'),
 # candidate lines that chips added or amended on Nov 17 carry (the day corrections and the answer to the twenty-first reading), on the pages those chips cite
 ('man-923fe8754943', 'nvidia', 'compliance with export restrictions is a top priority', 'drawn: on the Journal\'s first report (MA06), beside the arrest of March it answers'),
 ('man-923fe8754943', 'singapore', 'physical surveillance teams', 'drawn: on the Journal\'s first report (MA06), with the investigations in Singapore and Taiwan'),
 ('man-923fe8754943', 'taiwan', 'physical surveillance teams', 'drawn: on the Journal\'s first report (MA06), with the investigations in Singapore and Taiwan'),
 ('sw-sfexaminercom-02', 'kress', 'In 2023, she said on a call', 'drawn: MA364 (on the Times\'s row, from its profile of the interim chief)'),
 ('man-nyt-1029-01', 'huang', 'He also negotiated a deal with Mr. Trump', 'drawn: MA330 (the permission and the government\'s share, on the day of this page; the chip quotes this sentence)'),
 ('man-nyt-1029-01', 'trump', 'He also negotiated a deal with Mr. Trump', 'drawn: MA330 (the permission and the government\'s share, on the day of this page; the chip quotes this sentence)'),
 ('sw-techcrunchcom-04', 'nvidia', 'Nvidia has invested in OpenAI, Anthropic, xAI, CoreWeave, and Nebius', 'carried in part: the tie line MT20 carries the investment in Anthropic and MT53 the one in xAI; the investments in OpenAI, CoreWeave and Nebius are on no chip or tie line and are open in the register (earlier acts B.05, B.02 and B.03, added by the builder after the twenty-second reading)'),
 ('sw-hntrbrkcom-01', 'nvidia', 'funded investments in OpenAI and Anthropic', 'carried in part: the tie line MT20 carries the investment in Anthropic; the investment in OpenAI is on no chip or tie line and is open in the register (earlier act B.05), which this line now counts toward'),
 ('sw-semaforcom-19', 'huang', 'largely neutral tenor', 'drawn: on MA344 (the review\'s finding for the years before 2025, with the words that it scored the interviews with AI models of Anthropic and OpenAI)'),
]
# chips the readers named as carrying a line from a page EARLIER than the chip's day, and what the builder did
R_EARLY = {
 'MA330': 'moved: the chip now sits on Oct 29, the day of the first pages that recall the permission',
 'MA329': 'moved: the chip now sits on Nov 8, the day of the first page that recalls the bargain',
 'MA301': 'moved: the chip now sits on Nov 10, the day of the first saved relay of the report',
 'MA322': 'moved: the chip now sits on Nov 7, the day of the first page that recalls the approvals',
 'MA345': 'split: the remark to a podcaster has its own chip on Nov 9 (MA359); this chip keeps the interview first recalled on Nov 11',
 'MA319': 'not moved: the earlier page recalls the president\'s share trades, which are tie lines; the White House\'s reply drawn here is in the page of Nov 12',
 'MA323': 'not moved: the earlier pages speak of the inquiry in general or give Megaspeed\'s own statement (its chip); the audits as this chip words them are in the page of Nov 12',
 'MA353': 'not moved: the earlier pages carry Huang\'s refusal of June, which is on the Times\'s chip of Nov 5 and on her chip of Oct 29; the letter of July 2025 is first in the page of Nov 10',
 'MA355': 'not moved: the earlier pages carry Huang\'s refusal of June, which is on the Times\'s chip of Nov 5 and on her chip of Oct 29; her joining the bill is first in the page of Nov 12',
 'MA169': 'carried earlier: the indictment of March is now worded on the first saved pages that recall it, the department\'s chip of Oct 29 (MA362) and the Journal\'s first report (MA06, Oct 30); the chip of Nov 12 keeps the report that the department is examining a link to Megaspeed',
}
# a chip the readers named that was withdrawn since as a duplicate: where its act is carried now, by (chip, page); None stands for any other page
R_WD = {
 ('MA333', 'sw-jpostcom-01'): 'drawn: MA365 (on the Times\'s row at Nov 7; this page is the relay of that day which the chip cites for the Times\'s sentences on the small shipments of the quarter that ended in July). The chip the reader named, of Nov 8, was withdrawn as its duplicate (the twenty-second reading)',
 ('MA333', 'sw-uniteai-01'): 'carried: MA365 names this page, an article of Nov 5 that does not mention the affair, for its account of the same quarterly report; the chip the reader named was withdrawn as a duplicate of MA365 (the twenty-second reading)',
 ('MA333', 'sw-newsweekcom-01'): 'carried: the licences of February are on MA338; the small shipments are on the Times\'s row at Nov 7 (MA365), the other chip the reader named having been withdrawn as its duplicate (the twenty-second reading)',
 ('MA333', None): 'carried earlier: the same disclosure is on the Times\'s row at Nov 7 (MA365), the first saved page that recalls it, which also quotes the wire sentence; the chip the reader named, of Nov 8, was withdrawn as its duplicate (the twenty-second reading)',
}
R_OPEN = 'open: not yet grouped or drawn'
NOT_VALID_CTL = {'MA327'}        # its earlier part (a refusal of June) is carried by two other chips, as its reader said: not a test of that reader
G_OPEN = 'open: on no chip; not drawn until the owner decides what the image should carry'
# groups of the six grouping lanes that the builder reads otherwise than their reader did: chips drawn or amended on Nov 17, after the lanes' tables were frozen
G_BUILDER = {
 '6.NV6-002': 'carried since Nov 17: MA01, MA06 (the Times\'s and the Journal\'s first reports now word the start of the inquiry in late 2024)',
 '4.NV4-006': 'carried since Nov 17: MA06 (the Journal\'s first report, beside the arrest of March)',
 '4.NV4-096': 'carried since Nov 17: MA364 (on the Times\'s row)',
 '4.NV4-101': 'carried since Nov 17: MA364 (on the Times\'s row; this is the page the chip cites)',
 '6.NV6-007': 'carried since Nov 17: MA06 (the Journal\'s first report; Singapore\'s denial is on its chip of Oct 30)',
 '6.NV6-008': 'carried since Nov 17: MA06 (the Journal\'s first report)',
 '2.NV2-227': 'carried since Nov 17: MA344 (the chip that relays the review now gives its finding for the years before 2025, and says the review scored the interviews with AI models of Anthropic and OpenAI)',
 '4.NV4-115': 'carried since Nov 17: MT20 (the tie line between Anthropic and Nvidia now gives the page\'s sentence on the interim chief\'s part in financing deals)',
}
# chips that also carry a group since Nov 17, added to what its reader named
G_BUILDER['4.NV4-017'] = ('carried since Nov 17: MA365 (the Times\'s report of Nov 7, which its relay of that day repeats, gives the forecast of August that assumed no sales to China; the builder quoted the sentence on the chip and left this group open, which the twenty-third reading found)')
G_BUILDER['6.NV6-049'] = ('carried since Nov 17: MA72 (Singapore\'s chip of Nov 12 gives, since the nine pages were added, its ministry\'s own sentence that the inquiry began in February 2025; this group\'s one line is the Journal\'s account of that statement. The builder found this by its own search of the open groups before the release)')
# the twenty-fifth reading compared the open groups of Huang, the president and the White House with the chips: nine groups are worded in full by the Times's first report, three in part (G_PART below)
PHOTOS = ('carried since Nov 17: MA01 (the Times\'s first report gives the photographed occasions this group recalls, at a bar in Taipei in June 2024 and leaving a restaurant there in May 2025; '
          'the twenty-fifth reading found the group worded in full by that chip)')
G_BUILDER.update({k: PHOTOS for k in ('1.U002', '1.U005', '1.U006', '1.U007', '1.U008', '1.U021', '1.U030', '1.U031', '2.NV2-195')})
# Nvidia's investment in OpenAI and the delivery of 2016 are on the tie line between the two since the answer to the twenty-fifth reading, which noted that the investment in Anthropic was drawn and these were not
G_BUILDER['B.05'] = ('carried since Nov 17: MT29 (the tie line between Nvidia and OpenAI now gives the investment, from TechCrunch and Hunterbrook; registered by the builder after the twenty-second reading and drawn after the twenty-fifth, '
                     'which noted that the investment in Anthropic was drawn and this one was not)')
G_BUILDER['B.08'] = 'carried since Nov 17: MT29 (the tie line between Nvidia and OpenAI now gives the delivery of 2016, from Yahoo Finance and CNN; registered by the builder after the twenty-fourth reading and drawn after the twenty-fifth)'
# groups that stay open and that a chip words in part (the twenty-fourth reading): what the chip words, and what stays on no chip
APPROVALS = ('MA31, MA152 (the letter of Nov 12 by Sen. Wyden and Rep. Neal, whose footnote cites the Times\'s report of Nov 7, attacks the department\'s approvals of sales to Chinese companies "with government and military ties", and the two chips quote it; the approvals themselves, the buyers and what the pages say of each are on no chip)')
G_PART = dict({k: APPROVALS for k in ('6.NV6-013', '6.NV6-083', '6.NV6-084', '6.NV6-085', '6.NV6-086', '6.NV6-087', '6.NV6-088', '6.NV6-089', '6.NV6-090')},
              **{'6.NV6-019': 'MA101 (the Times\'s chip of Nov 9 quotes that officials "rapidly disclosed it to partner law enforcement agencies"; the meetings the group also recalls are on no chip)'})
G_ALSO = {'4.NV4-012': 'MA365', '6.NV6-063': 'MA362', '3.MS44': 'MA360', '4.NV4-111': 'MA360', '1.G001': 'MA01', '1.G002': 'MA01'}
G_PART.update({'1.U033': 'MA01 (the Times\'s first report gives the photograph at a bar in Taipei in June 2024; the second photograph this page recalls, of the following May, is not identified with the restaurant the chip gives)',
               '1.U048': 'MA01 (the Times\'s first report gives the restaurant in Taipei in May 2025, which this page\'s caption names; the photograph of 2024 it also recalls is not identified)',
               '2.NV2-197': 'MT57 (the tie line gives his answer on a podcast to the nuclear analogy, "Lunacy"; the five-layer explanation the page also recalls is on no chip)'})        # the twenty-fifth reading
# batch s9o, the take-in of the other session's pages (Nov 17): open groups that a chip of the batch now words, by the builder's search of the open groups against every amended and new chip
for _k in ('6.NV6-013', '6.NV6-083', '6.NV6-084', '6.NV6-085', '6.NV6-086', '6.NV6-087', '6.NV6-088', '6.NV6-089', '6.NV6-090'): G_PART.pop(_k)        # the nine groups on the approvals of H200 buyers: worded in full now
G_BUILDER.update({k: "carried since Nov 17: MA03 (the Times's chip of Nov 7 now gives the report's findings from the paper's own page: dozens of Chinese companies approved to handle the chips, roughly two dozen to buy or handle them, ties to blacklisted firms and military contractors, a listed address that stands empty; until the take-in of Nov 17 the chip gave one firm, and this group was worded only in part, through a letter that cites the report)" for k in ('6.NV6-013', '6.NV6-083', '6.NV6-084', '6.NV6-085', '6.NV6-086', '6.NV6-087', '6.NV6-088', '6.NV6-089', '6.NV6-090')})
G_BUILDER.update({'1.U046': "carried since Nov 17: MA199 (the company's refusal to Reuters now comes with the report it answers: an intimate relationship with a second employee, by two people's account; the page gives the relationship no dates)", '4.NV4-007': "carried since Nov 17: MA388 (the FT's report of Nov 2 on the rule, with the company's reply, is on the company's row; an earlier reading of the builder had set that day aside as not on the matter)", '3.MS18': "carried since Nov 17: MA395 (the FT's report of Nov 9, on the paper's row, gives the pitch to investors)"})
G_BUILDER.update({k: "carried since Nov 17: MA390 (The Information's report of Nov 10 is worded, as Gizmodo relays it, on the company's row with the company's statement; MA257 gives the Daily Caller's account of it the next day)" for k in ('1.G009', '2.NV2-216')})
G_PART.update({'3.MS41': "MA390 (the chip gives the report's total, at least $7.5 billion of chips to Chinese companies since 2023, and the company's statement; the network the pages describe and the number of chips are on no chip)", '3.MS19': "MA395 (the FT's chip of Nov 9 gives the loan of June 2024 from a subsidiary of Alibaba; the pledge of the business as collateral is on no chip)", '2.NV2-242': 'MA162 (the analyst\'s chip of Nov 12 says that Huang spoke against "China hawks" and gives the analyst\'s words about it; Huang\'s own words are on no chip)'})
# the twenty-sixth reading: five open groups that a chip words in part (its P08 to P12), and two groups on the finance chief's objections to financing OpenAI, worded by the tie line since the batch that answers it (P07)
G_PART.update({'3.MS01': 'MA01 (the Times\'s first report dates the photographs of June 2024 to "just weeks before Megaspeed began its purchases", which gives the start of the purchases; who bought, the total of at least $4.8 billion and the period to February 2026 are on no chip)', '4.NV4-075': 'MA365 (the Times\'s chip of Nov 7 quotes that the company "said in August that it was not assuming any sales to China in its estimate for data center revenue for the current quarter"; the forecasts since August 2025 that the group recalls, and the reason the page gives for them, are on no chip)', '4.NV4-077': "MA365 (the Times's chip of Nov 7 quotes the forecast of August that assumed no sales to China for the current quarter; the sum of $108 billion that this page gives for it is on no chip)", '4.NV4-090': 'MA376 (the White House\'s chip of Nov 9 quotes a relay\'s sentence that Nvidia "has lobbied against closing the remote-access gap"; when it did so, and for how long, is on no chip)', '4.NV4-095': 'MA376 (the White House\'s chip of Nov 9 quotes a relay\'s sentence that Nvidia "has lobbied against closing the remote-access gap"; the argument this page reports, that a restriction would push China to build its own chip industry, is on no chip)'})
G_BUILDER.update({'4.NV4-087': "carried since Nov 17: MT29 (the tie line between Nvidia and OpenAI now gives the FT's account, from two people, that the finance chief challenged Huang over a $250 billion deal to support data centres for OpenAI, and what Nvidia then agreed to; drawn after the twenty-sixth reading, which found the group open although records about OpenAI and Anthropic are drawn when found)", '4.NV4-091': "carried since Nov 17: MT29 (the tie line between Nvidia and OpenAI now gives CNBC's relay of The Information's report that the finance chief was against the $105 billion deal with OpenAI; the line says that this account and the FT's give different sums and are not shown to be one occasion; drawn after the twenty-sixth reading)"})
# the builder's own search of the open groups after that answer: one more group that the same chip words in part
G_PART.update({'4.NV4-008': 'MA365 (the Times\'s chip of Nov 7 quotes that the company "said in August that it was not assuming any sales to China in its estimate for data center revenue for the current quarter"; that the finance chief said it on the earnings call of Aug 26, and the reason given there, are on no chip)'})
G_AFTER = {'4.NV4-012': '; MA333 was withdrawn after the twenty-second reading as a duplicate of MA365, which carries the disclosure on the Times\'s row at Nov 7 with the filing\'s two other statements that this group\'s lines give',
           '6.NV6-021': '; the chip its reader named gave the halt and the transfer but not who asked for the pause, and since the twenty-second reading it quotes the Times\'s sentence that the Justice Department requested it',
           '1.G001': '; the chips its reader named give the gathering only through the company\'s explanation, and since Nov 17 the Times\'s first report (MA01) words the gathering itself',
           '1.G002': '; the chip its reader named gives the dinner only through the company\'s explanation, and since Nov 17 the Times\'s first report (MA01) words it'}
G_CTL_NOTE = {'2.NV2-319': ' (its one line is a planted control: the sentence is a cited passage of the White House\'s chip MA349, which the grouping reader did not name)'}
# groups whose reader named a chip that carries an outcome or a neighbouring act, not the act itself (the twenty-second reading): open again
G_REOPEN = {
 '6.NV6-036': 'its grouping reader named MA294 and MA348, which give his omission from the first list for the trip and the president\'s invitation, not the page\'s attribution of the exclusion to the State Department, which the line\'s reader calls unconfirmed',
}
# 6.NV6-046 (the FBI's inquiry of at least a year): opened again after the twenty-second reading because the chip its reader named does not give it; since the take-in of Nov 17 the attorney general's chip does
G_ALSO['6.NV6-046'] = 'MA168'
G_AFTER['6.NV6-046'] = ('; the chip its reader named (MA150) gives the inquiry into Megaspeed and into a recruitment, not an investigation of the relationship lasting at least a year, and the twenty-second reading had the group opened again; '
                        'since the take-in of Nov 17 the attorney general\'s chip of Nov 12 (MA168) gives CNN\'s sentence that the FBI has been investigating the affair for at least a year')
G_FIRST = {'3.MS05': 'unclear'}        # its grouping reader read before; a job advertisement the page calls recent is not shown to have been public before Oct 29 (the twenty-second reading)
G_NOTE = {'3.MS05': ' (first report: the builder reads unclear where its grouping reader read before, since a job advertisement the page calls recent is not shown to predate Oct 29: the twenty-second reading)'}
ADDED = ' (added and coded by the builder after the twenty-second reading, which found it on saved pages; no census line held it; a scan of the saved pages by the builder gave the pages listed, and no census reader has read them for it)'
ADDED_SPLIT = (' (registered as an act of its own by the builder after the twenty-second reading: census lines that named several investments at once had been counted as carried by a tie line that carries one of them (lines 1947 and 2012); a scan of the saved pages by the builder gave the other pages listed, and no census reader has read them for it)')
ADDED_LANE = ' (found on no chip by the reader of nine pages saved by hand and added on Nov 17, lane acts_nv8_added_a; worded and coded by the builder)'
ADDED_24 = ' (registered and coded by the builder after the twenty-fourth reading, which found it in a profile whose census reader had not listed it; no census line held it; a scan of the counted pages by the builder gave the seven pages listed, and may have missed others)'
ADDED_23 = ' (registered by the builder after the twenty-third reading; its one line is a census line whose reader had named a chip that does not carry it)'
# earlier acts that no census line held (the twenty-second reading found them); the wording, the class and the direction are the builder's
G_NEW = {
 'B.01': {'actor': 'ft', 'what': 'The FT recalls a letter of the year before in which leading Senate Democrats said national security decisions were being made at the behest of a well-connected chief executive who stood to gain from the lifting of export controls; the page names no signer.',
          'when': 'Last year (2025), as the page gives it.', 'kind': 'decision', 'first_reported': 'unclear', 'row_it_belongs_on': 'ft', 'direction': 'against Huang or Nvidia'},
 'B.02': {'actor': 'nvidia', 'what': 'Nvidia invested $2 billion in CoreWeave.', 'when': 'January 2026; one page says at the start of 2026, and the earliest names the investment without a date.',
          'kind': 'money', 'first_reported': 'before', 'row_it_belongs_on': 'nvidia', 'direction': 'neither'},
 'B.03': {'actor': 'nvidia', 'what': 'Nvidia invested $2 billion in Nebius.', 'when': 'March 2026; the earliest page names the investment without a date.',
          'kind': 'money', 'first_reported': 'before', 'row_it_belongs_on': 'nvidia', 'direction': 'neither'},
 'B.04': {'actor': 'nvidia', 'what': 'Nvidia signed preliminary agreements with six financial firms aimed at mobilizing more than $500 billion over time; Huang said Nvidia could backstop up to a quarter of it.',
          'when': 'August 2026.', 'kind': 'event', 'first_reported': 'before', 'row_it_belongs_on': 'nvidia', 'direction': 'neither'},
 'B.05': {'actor': 'nvidia', 'what': 'Nvidia invested in OpenAI; one page says an investment of $30 billion was finalized in March and completed by October.',
          'when': 'No date in the earliest pages; March and October 2026 in one page, which cites Reuters and The Information.', 'kind': 'money', 'first_reported': 'before', 'row_it_belongs_on': 'nvidia', 'direction': 'neither'},
 'B.06': {'actor': 'commerce', 'what': 'Reuters reported in June that the administration had held off adding the AI startup DeepSeek, the memory chipmaker CXMT and more than 100 other companies flagged as national security risks to a trade blacklist; one page adds that the department had added no Chinese company for fear of escalating tensions.',
          'when': 'By June 2026, as the pages give it; no additions to the list since October 2025.', 'kind': 'decision', 'first_reported': 'before', 'row_it_belongs_on': 'commerce', 'direction': 'against the administration'},
 'B.08': {'actor': 'huang', 'what': 'Huang personally delivered Nvidia\'s first DGX-1 AI supercomputer to OpenAI, then a nonprofit research lab, handing it to Elon Musk; one page says Nvidia donated it, another that he supplied the lab\'s first supercomputer.',
          'when': '2016; one page says a decade ago.', 'kind': 'event', 'first_reported': 'before', 'row_it_belongs_on': 'huang', 'direction': 'neither'},
 'B.07': {'actor': 'rubio', 'what': 'A blog reports that the secretary of state said he had shared information about the executive\'s connection to Nvidia with the president; it links no original, and no original or transcript of such a statement is saved.',
          'when': 'Last spring, as the page gives it.', 'kind': 'statement', 'first_reported': 'unclear', 'row_it_belongs_on': 'rubio', 'direction': 'against the administration'},
}
G_NEW_NOTE = {'B.08': ADDED_24, 'B.01': ADDED, 'B.04': ADDED, 'B.02': ADDED_SPLIT, 'B.03': ADDED_SPLIT, 'B.05': ADDED_SPLIT, 'B.06': ADDED_LANE, 'B.07': ADDED_23}
# census lines whose reader named a chip, assigned by the builder to an open act of the register (0-based row of the pool): line 2255 to B.07, line 2012 to B.05
L_ASSIGN = {2254: ('B.07', 'sw-sandrarosecom-01'), 2011: ('B.05', 'sw-hntrbrkcom-01')}
LB24 = 'added by the builder (twenty-fourth reading)'; LB23 = 'added by the builder (twenty-third reading)'; LBA = 'lane acts_nv8_added_a (a reader of nine pages added on Nov 17)'
# P06, P08 of the twenty-third reading, and the earlier acts the reader of the nine added pages found on no chip
R_ADDED_MORE = [('sw-venturebeatcom-01', 'nvidia', 'nvidia', 'neither', 'B.04', LB23), ('sw-datacenterdynamicscom-01', 'nvidia', 'nvidia', 'for Huang or Nvidia', '4.NV4-004', LB23),
                ('man-1c17777255e2', 'megaspeed', 'megaspeed', 'neither', '3.MS50', LBA), ('man-a8a33ade4ff1', 'huang', 'huang', 'neither', '2.NV2-194', LBA),
                ('man-reuters-1111-06', 'commerce', 'commerce', 'against the administration', 'B.06', LBA), ('man-c9469105da89', 'commerce', 'commerce', 'against the administration', 'B.06', LBA)]
# the delivery of 2016: the twenty-fourth reading found it in one profile; the builder's scan of the counted pages found it in six more
R_ADDED_MORE += [(pg, 'huang', 'huang', 'neither', 'B.08', LB24) for pg in ('sw-cnncom-02', 'art-fc-ht-econ-1109-survive', 'man-5dbffa3344fb', 'man-ft-1112-05', 'sw-financeyahoocom-30', 'sw-sfstandardcom-06', 'sw-teslaraticom-01')]
# the twenty-fifth reading: a later delivery in the same paragraph as the delivery of 2016; one more page that recalls the delivery of 2016; a page whose census reader had not listed the appointment to the president's council
ADDED_25 = ' (registered and coded by the builder after the twenty-fifth reading, which found it in the same paragraph as the delivery of 2016; no census line held it, and a search of the saved text of the counted pages found no other page that recalls it)'
G_NEW['B.09'] = {'actor': 'huang', 'what': 'Huang delivered one of the first units of Nvidia\'s desktop-size DGX Spark to Elon Musk at SpaceX\'s Starbase facility in Texas.', 'when': 'Nearly a decade after 2016, as the page gives it; no date.',
                 'kind': 'event', 'first_reported': 'unclear', 'row_it_belongs_on': 'huang', 'direction': 'neither'}
G_NEW_NOTE['B.09'] = ADDED_25
LB25 = 'added by the builder (twenty-fifth reading)'
R_ADDED_MORE += [('sw-financeyahoocom-30', 'huang', 'huang', 'neither', 'B.09', LB25), ('cnn-1111-live', 'huang', 'huang', 'neither', 'B.08', LB25 + '; the three entries that recall it are stamped Nov 12, a day after the page\'s day in the table'),
                 ('sw-implicatorai-02', 'huang', 'huang', 'neither', '2.NV2-285', LB25), ('sw-implicatorai-02', 'trump', 'trump', 'for Huang or Nvidia', '5.NV5-073', LB25)]
# the twenty-sixth reading: nine earlier acts it found on pages another session saved, which the table of counted pages does not hold (its P20, P22, P23, P29, P30, P37, P38, P39, P44). Registered by the builder, each read on its page;
# their lines are marked as coming from a page outside the table (R_OUTSIDE), and a scan of the counted pages of the days by keywords found one counted page that holds one of them (the land agreement, B.12)
ADDED_26 = (' (registered and coded by the builder after the twenty-sixth reading, which found it on a page another session of this project saved; that page is outside the table of counted pages, and its line says so; '
            'a scan of the counted pages by keywords found no other page that recalls it, and no census reader has read them for it)')
ADDED_26B = (' (registered and coded by the builder after the twenty-sixth reading, which found it on a page another session of this project saved, outside the table of counted pages; '
             'a scan of the counted pages by keywords found one that recalls it, whose census reader had not listed it)')
G_NEW.update({'B.10': {'actor': 'megaspeed', 'what': "A short seller's report of May 13, 2026, as a Taiwanese weekly relays it, says Supermicro once stood among the partners shown on Megaspeed's website and was later taken off; the weekly finds Nvidia, Intel and Gigabyte shown there now. The page gives the removal no day and does not say that a business relationship ended (Supermicro's statement that Megaspeed was never its customer is on the Justice Department's chip of Nov 12).", 'when': "By May 13, 2026, the day of the short seller's report; no day for the removal.", 'kind': 'event', 'first_reported': 'before', 'row_it_belongs_on': 'megaspeed', 'direction': 'neither'}, 'B.11': {'actor': 'megaspeed', 'what': "A listed Indonesian data-centre company's disclosure, as CNBC Indonesia reports it, names Megaspeed's Indonesian subsidiary and the telecoms company Indosat as tenants under agreements for two data centres the company is to build, one of 36 MW in Cikarang and a new one of 60 MW in Batang; CNBC Indonesia says it has asked Indosat to confirm its business with Megaspeed. The page does not say that the sites are built.", 'when': 'No day for the agreements or for the disclosure.', 'kind': 'event', 'first_reported': 'unclear', 'row_it_belongs_on': 'megaspeed', 'direction': 'neither'}, 'B.12': {'actor': 'megaspeed', 'what': "A unit of a listed Malaysian developer agreed to sell a parcel of 52.54 acres in an industrial park in Kota Tinggi, Johor, for RM263.21 million to MSFusion, a Malaysian company that reports link to Megaspeed; a year later the developer issued a notice over RM225.91 million in defaulted payments. The final payment that followed is the register's act 3.MS06.", 'when': 'August 2025 for the agreement and August 2026 for the notice, as the pages give them.', 'kind': 'money', 'first_reported': 'before', 'row_it_belongs_on': 'megaspeed', 'direction': 'neither'}, 'B.13': {'actor': 'whitehouse', 'what': "A Korean daily, relaying the Times's report of the clash between the Treasury and Commerce secretaries, writes that White House and intelligence officials had pushed for action against Megaspeed since the fall before, and that the Commerce secretary and senior officials of his department are said to have resisted. The Times's page as saved has no such sentence: it says that officials of several agencies agreed some months before that the company should be listed. The agencies' push and the department's delay of two months are on the FT's chip of Nov 10, and the deputies' meeting on the Times's chip of Nov 11.", 'when': 'Since the fall of 2025, as the relay gives it; it names no occasion.', 'kind': 'other', 'first_reported': 'in these days', 'row_it_belongs_on': 'whitehouse', 'direction': 'against the administration'}, 'B.14': {'actor': 'megaspeed', 'what': 'A crypto-news site writes that Megaspeed completed a bulk purchase of Nvidia equipment in the six weeks before May 15, 2025, the day on which a rule of the previous administration would have required permits for exports of AI chips to Southeast Asia; the rule was withdrawn before it took effect. The page names no source for the purchase and gives no sum, and its stamp says it was modified two days after it first ran. The purchase is not shown to be one of those the register holds with sums.', 'when': 'The six weeks before May 15, 2025.', 'kind': 'event', 'first_reported': 'unclear', 'row_it_belongs_on': 'megaspeed', 'direction': 'against Huang or Nvidia'}, 'B.15': {'actor': 'megaspeed', 'what': "A Singapore daily reports that on the day its former executive left the board of the Singapore-registered company, Megaspeed's present chairman and one other director were appointed; that director left the board seven weeks later, and his name still stands in the registration papers of subsidiaries abroad.", 'when': "Nov 10, 2023 for the appointments; Dec 28, 2023 for the other director's departure.", 'kind': 'event', 'first_reported': 'unclear', 'row_it_belongs_on': 'megaspeed', 'direction': 'neither'}, 'B.16': {'actor': 'nvidia', 'what': "At its annual meeting of shareholders in 2026, by a trading site's summary of CNBC's reporting, Nvidia told investors that it is committed to complying with all U.S. laws and works with the AI industry and the U.S. government.", 'when': '2026, at the annual meeting; the page gives no day.', 'kind': 'statement', 'first_reported': 'before', 'row_it_belongs_on': 'nvidia', 'direction': 'for Huang or Nvidia'}, 'B.17': {'actor': 'megaspeed', 'what': "A risk-research firm reads the securities disclosures of July 2025 of a listed Chinese company as saying that its cloud unit rented computing capacity from an unnamed supplier whose founding date and capital match Megaspeed's, and that two unnamed customers of that capacity match two Chinese technology companies. The identification is the firm's inference; it notes that rentals of computing capacity need not be reported as trade is.", 'when': 'By July 2025, the date of the disclosures.', 'kind': 'event', 'first_reported': 'in these days', 'row_it_belongs_on': 'megaspeed', 'direction': 'against Huang or Nvidia'}, 'B.18': {'actor': 'whitehouse', 'what': "Semafor recalls that in the fight over the defense bill of the year before, a bill to tighten controls on chip exports (the GAIN AI Act, which it calls an earlier version of the AI Overwatch Act) was in the Senate's version and was dropped from the House's after pressure from Nvidia, the wider semiconductor industry and the White House, the president's AI adviser of the time among them. The page does not say that the pressure was the only cause, and adds that Congress did include some investment controls.", 'when': "2025, in the fight over that year's defense bill; no day.", 'kind': 'other', 'first_reported': 'before', 'row_it_belongs_on': 'whitehouse', 'direction': 'against the administration'}})
G_NEW_NOTE.update({k: (ADDED_26B if k == 'B.12' else ADDED_26) for k in ('B.10', 'B.11', 'B.12', 'B.13', 'B.14', 'B.15', 'B.16', 'B.17', 'B.18')})
LB26 = 'added by the builder (twenty-sixth reading)'; LB26O = LB26 + ', from a page another session saved, outside the table of counted pages'
# lines on saved pages outside the table: (page, actor, row, direction, earlier act); the day of each is read from the page by scripts/nv8_page_dates.py (U.S. Eastern)
R_OUTSIDE = [('ms-gap-nova-trade-mirrormedia-original-d9d529', 'megaspeed', 'megaspeed', 'neither', 'B.10'), ('ms-gap-china-cnbc-indonesia-e33e31', 'megaspeed', 'megaspeed', 'neither', 'B.11'), ('ms-corp-edge-bfcc90', 'megaspeed', 'megaspeed', 'neither', 'B.12'), ('ms-gap-erc-herald-meeting-response-3983b6', 'whitehouse', 'whitehouse', 'against the administration', 'B.13'), ('ms-hl-protos-429bc0', 'megaspeed', 'megaspeed', 'against Huang or Nvidia', 'B.14'), ('ms-gap-offshoots-zaobao-kang-original-51f493', 'megaspeed', 'megaspeed', 'neither', 'B.15'), ('ms-gap-booking-newstreet-primexbt-relay-0cb27a', 'nvidia', 'nvidia', 'for Huang or Nvidia', 'B.16'), ('ms-gap-offshoots-kharon-network-183779', 'megaspeed', 'megaspeed', 'against Huang or Nvidia', 'B.17'), ('ms-relay-semafor-1112', 'whitehouse', 'whitehouse', 'against the administration', 'B.18')]
# a counted page whose census reader had not listed the land agreement or the payment that settled it; and a counted page of Oct 29 that describes the company's business in one sentence (P13): it buys Nvidia chips and rents computing power
# to Alibaba and other Chinese companies. Each half is filed with the act it describes; the page gives neither a sum nor a date, so that it means the same purchases is not proved
R_ADDED_MORE += [('cnbc-1112-megaspeed-asia', 'megaspeed', 'megaspeed', 'neither', 'B.12', LB26), ('cnbc-1112-megaspeed-asia', 'megaspeed', 'megaspeed', 'neither', '3.MS06', LB26),
                 ('sw-capitalbriefcom-57f178e4', 'megaspeed', 'megaspeed', 'against Huang or Nvidia', '3.MS01', LB26 + '; the page says only that the company buys Nvidia chips, with no sum and no dates'),
                 ('sw-capitalbriefcom-57f178e4', 'megaspeed', 'megaspeed', 'against Huang or Nvidia', '3.MS03', LB26 + '; the page says only that the company rents computing power to Alibaba and other Chinese companies, with no dates')]
# lines the census readers did not list, added by the builder after the twenty-second reading: (page, actor, row, direction, earlier act). The first two are pages whose reader missed an act that other pages' lines hold
R_ADDED = ([('sw-breitbartcom-08', 'nvidia', 'nvidia', 'for Huang or Nvidia', '4.NV4-004'), ('sw-implicatorai-01', 'megaspeed', 'megaspeed', 'against Huang or Nvidia', '3.MS01'), ('man-ft-1112-03', 'ft', 'ft', 'against Huang or Nvidia', 'B.01')]
           + [(pg, 'nvidia', 'nvidia', 'neither', 'B.02') for pg in ('sw-techcrunchcom-04', 'prospect-honeypot', 'sw-hntrbrkcom-01', 'sw-bitcoininsiderorg-04', 'sw-cnbccom-09', 'sw-financeyahoocom-31', 'sw-techcrunchcom-15', 'sw-venturebeatcom-01', 'man-cf6650e331b3')]
           + [(pg, 'nvidia', 'nvidia', 'neither', 'B.03') for pg in ('sw-techcrunchcom-04', 'sw-hntrbrkcom-01', 'man-ac79ea8f3db1', 'man-cf6650e331b3', 'sw-cnbccom-09', 'sw-financeyahoocom-31', 'sw-techcrunchcom-15')]
           + [(pg, 'nvidia', 'nvidia', 'neither', 'B.04') for pg in ('sw-techcrunchcom-04', 'sw-hntrbrkcom-01')]
           + [(pg, 'nvidia', 'nvidia', 'neither', 'B.05') for pg in ('man-nyt-1109-02', 'sw-techcrunchcom-04', 'prospect-honeypot', 'man-cf6650e331b3', 'sw-cnbccom-09', 'sw-ensedailycom-18', 'sw-financeyahoocom-31', 'sw-techcrunchcom-15', 'sw-gamerantcom-29658ce5', 'sw-venturebeatcom-01')])
R_OWN = 'open: the chip sits on its own day and the reader names an earlier page; not read again by the builder'
# the chips that sit on their own day and that a reader named from an EARLIER page: read by the builder on Nov 17, one disposition per (chips named, page, actor); None stands for any
R_LATE = [
 (('MA293',), None, 'commerce', 'carried earlier: the inspection of late 2024 is now worded on the Times\'s first report (MA01, Oct 29), the first saved page that carries it; the chip of Nov 10 says it repeats it'),
 (('MA293',), None, 'taiwan', 'carried earlier: the Journal\'s first report (MA06, Oct 30) now words the investigations in Singapore and Taiwan and the surveillance teams; the monitoring from 2024 at the suggestion of the U.S. is the Times\'s own report of Nov 10'),
 (('MA293',), None, 'megaspeed', 'drawn: MA360 (the Journal\'s report of the partnership letter of November 2023, on Nov 9); the chip of Nov 10 keeps the Times\'s detail and points to it'),
 (('MA293',), None, 'nvidia', 'drawn: MA360 (the Journal\'s report of the partnership letter of November 2023, on Nov 9); the chip of Nov 10 keeps the Times\'s detail and points to it'),
 (('MA72',), 'art-fc-bs-nyt-1110-woman', 'singapore', 'drawn: on the Times\'s chip of Nov 10 (MA293), which now carries the ban on leaving, the questioning and the finding of insufficient evidence as its profile reports them, two days before Singapore\'s statement'), (('MA72',), 'sw-fortunecom-05', 'singapore', 'drawn: on the Times\'s chip of Nov 10 (MA293), which now carries the ban on leaving, the questioning and the finding of insufficient evidence as its profile reports them, two days before Singapore\'s statement'), (('MA72',), 'sw-siliconcouk-01', 'singapore', 'drawn: on the Times\'s chip of Nov 10 (MA293), which now carries the ban on leaving, the questioning and the finding of insufficient evidence as its profile reports them, two days before Singapore\'s statement'), (('MA72',), 'sw-tomshardwarecom-14', 'singapore', 'drawn: on the Times\'s chip of Nov 10 (MA293), which now carries the ban on leaving, the questioning and the finding of insufficient evidence as its profile reports them, two days before Singapore\'s statement'),
 (('MA72',), 'man-ft-1110-02', 'singapore', 'carried: Singapore\'s inquiry into the company is on the Times\'s first report (MA01) and on its own chip of Oct 30 (MA70); the start this page gives for it is not worded on a chip'), (('MA72',), 'sw-cbsnewscom-07', 'singapore', 'carried: Singapore\'s inquiry into the company is on the Times\'s first report (MA01) and on its own chip of Oct 30 (MA70); the start this page gives for it is not worded on a chip'), (('MA70', 'MA72'), None, 'singapore', 'carried: Singapore\'s inquiry into the company is on the Times\'s first report (MA01) and on its own chip of Oct 30 (MA70); the start this page gives for it is not worded on a chip'),
 (('MA72',), 'cnn-1111-live', 'singapore', 'not moved: the live page\'s item gives the ministry\'s statement of Nov 12, the chip\'s day'),
 (('MA72',), None, 'singapore', 'carried earlier: Singapore\'s investigation and the questioning of 2025 are now worded on the Times\'s first report (MA01, Oct 29); its statement of Nov 12 stays its own act'), (('MA70',), None, 'singapore', 'carried earlier: Singapore\'s investigation and the questioning of 2025 are now worded on the Times\'s first report (MA01, Oct 29); its statement of Nov 12 stays its own act'),
 (('MA101',), 'sw-madrobotblog-01', None, 'not moved: the page, first published on Nov 8, says it was updated on Nov 12; these passages stand under its heading "Update" and follow the Times\'s reports of Nov 9 and 10'), (('MA138',), 'sw-madrobotblog-01', None, 'not moved: the page, first published on Nov 8, says it was updated on Nov 12; these passages stand under its heading "Update" and follow the Times\'s reports of Nov 9 and 10'), (('MA138', 'MT18'), 'sw-madrobotblog-01', None, 'not moved: the page, first published on Nov 8, says it was updated on Nov 12; these passages stand under its heading "Update" and follow the Times\'s reports of Nov 9 and 10'),
 (('MA101',), 'sw-siliconanglecom-01', 'commerce', 'carried: the Times\'s first report (MA01, Oct 29) carries the inquiry and its handover'),
 (('MA101',), 'sw-digitaltrendscom-01', 'commerce', 'carried earlier: the words are the Journal\'s of Oct 30, now on its chip (MA06)'),
 (('MA01', 'MA101'), 'sw-techcrunchcom-01', 'commerce', 'carried: the Times\'s first report (MA01, Oct 29) carries the inquiry; that the Times had first reported it in 2025 is not worded on a chip'),
 (('MA01', 'MA101'), 'man-923fe8754943', 'commerce', 'carried: the Journal\'s first report (MA06, Oct 30) now words the start of the inquiry in late 2024'),
 (('MA01', 'MA101'), 'sw-implicatorai-02', 'commerce', 'carried: the inquiry is on the Times\'s and the Journal\'s first reports (MA01, MA06); that no finding has been announced is the page\'s own remark'),
 (('MA01', 'MA101'), None, None, 'carried: the Times\'s first report (MA01, Oct 29) carries the handover to the Justice Department'),
 (('MA327',), 'sw-qzcom-01', 'huang', 'drawn: on the senator\'s chip of Oct 29 (MA357), which now adds this page\'s recall that Huang turned her request down'),
 (('MA08',), None, 'huang', 'not moved: the page gives the Times\'s first report (MA01, Oct 29), which speaks of a close relationship; the chip named is a later paper\'s own report'), (('MA06',), None, 'huang', 'not moved: the page gives the Times\'s first report (MA01, Oct 29), which speaks of a close relationship; the chip named is a later paper\'s own report'),
 (('MA05',), 'huffpost-live', 'huang', 'not moved: the live page\'s item is stamped Nov 11, the chip\'s day'),
 (('MA05',), 'sw-foreignpolicycom-01', 'huang', 'not moved: the page says it was updated on Nov 12, and the sentence follows the resignation'),
 (('MA146',), 'sw-foreignpolicycom-01', 'huang', 'not moved: the page says it was updated on Nov 12; the chip named is a commentator\'s remark of that day'),
 (('MA146',), 'sw-thedecodercom-01', 'huang', 'not moved: the chip named is a commentator\'s remark of Nov 12; that Huang named no successor is carried on Nov 9 (MA359, MA315)'),
 (('MA146',), 'sw-thezvisubstackcom-01', 'huang', 'not moved: his post of Nov 10 has its own chip (MA132); the chip named is a remark in his newsletter of Nov 12'),
 (('MA157',), None, 'megaspeed', 'carried earlier: the Journal\'s first report (MA06, Oct 30) now quotes the statement of late 2025; the chip of Nov 9 is the company\'s posting of it that day'),
 (('MA340', 'MA358'), 'sw-cnbccom-04', 'nvidia', 'drawn: MA358 (this page\'s recall, on Nov 10)'),
 (('MA138',), 'sw-engadgetcom-02', 'trump', 'drawn: MA366, on the FT\'s row at Nov 7 (this page\'s relay of the FT\'s report, that the president was among those notified before the trip, set beside what the saved copy of the FT\'s report says: top officials); it stood on the FT\'s chip of Nov 6 for one release, a day early (the twenty-third reading); the briefing aboard the plane is the Times\'s report of Nov 10 (the chip the reader named)'),
 (('MA138',), 'man-ft-1109-04', 'trump', 'drawn: MA361 (the FT\'s sentence of Nov 9, beside what its saved report of Nov 6 says and the president\'s reply)'),
 (('MA138',), 'sw-heisede-01', 'trump', 'carried earlier: that the president was told before the trip is worded from Nov 7 on the FT\'s row (MA366, as Engadget relays its report) and in the FT\'s own sentence of Nov 9 (MA361); the memo\'s circulation to officials is on MA08 and on the Times\'s chip of Nov 8 (MA04); this page names no source for the warning'),
 (('MA138',), 'sw-sandrarosecom-01', 'rubio', 'registered: this page reports that the secretary said he shared the information with the president; it links no original, and no original or transcript of such a statement is saved, so its occasion is unresolved and it is an open act of the register (B.07); the report is not disproved by his answer of Nov 8, that he could not comment (MA74). What the papers report of the memo is on their chips: he oversaw it and it went to cleared officials before the trip (MA04, the Times, Nov 8); the president was told (MA366 as relayed on Nov 7, MA361, MA138)'),
 (('MA04', 'MA138'), 'sw-todaycom-01', 'rubio', 'carried: the Times\'s report of Nov 8 (MA04), which since the twenty-second reading gives its sentences that the memo he oversaw warned top administration officials and went to cleared officials ahead of the trip; that he warned the White House is this page\'s wording of that report'),
]


def scrub(t):
    for pat, role in SCRUB:
        t = re.sub(pat, role, t)
    assert not any(re.search(pat, t) for pat, _ in SCRUB), t
    return t


def main():
    ids = {r['row_id'] for r in rows_map.rows()}
    for v in list(ONE.values()) + list(PARA.values()) + list(EARLIER.values()) + [x[3] for x in R_DONE] + list(R_EARLY.values()) + [x[3] for x in R_LATE] + list(R_WD.values()):
        for i in re.findall(r'MA\d+', v): assert i in ids, ('a disposition names an act that is not there', i)
    grp = {r['group_id']: r for r in csv.DictReader(open(L / 'single_nv8_a.groups.tsv'), delimiter='\t')}
    ctl = {r['group_id']: r for r in csv.DictReader(open(L / 'single_nv8_a.controls.tsv'), delimiter='\t')}
    out = []; c = Counter(); found = 0
    for r in csv.DictReader(open(L / 'single_nv8_a.out.csv')):
        b = r['group_id'].split('-')[0]; cand = r['verdict'].startswith('CANDIDATE'); isc = ctl[b]['is_control'] == 'yes'
        if isc:
            disp = 'a planted control: the act was held out of the reader\'s table (' + ctl[b]['control_for'] + ')'; found += cand
        elif cand:
            assert r['group_id'] in ONE, ('a candidate with no disposition', r['group_id'], r['actor']); disp = ONE[r['group_id']]
        else:
            assert r['group_id'] not in ONE, ('a disposition for a group the reader did not call a candidate', r['group_id']); disp = ''
        c[(r['verdict'], 'control' if isc else ('drawn' if disp.startswith('drawn') else ('not drawn' if cand else '')))] += 1
        first = scrub(' '.join(grp[b]['quoted_lines'].split()[:14])) if r['group_id'] == b else '(a passage beside the group\'s line)'
        out.append([r['group_id'], r['actor'], grp[b]['page_id'].split()[0], first, r['verdict'], r['act'], r['test'], 'yes' if isc else '', disp])
    n_ctl = sum(1 for x in ctl.values() if x['is_control'] == 'yes'); assert found == n_ctl, ('a planted control the reader did not call a candidate', found, n_ctl)
    with open(R / 'nv8_single_article_remarks.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['group', 'actor', 'page', 'first_words_of_the_quoted_line', 'reader_verdict', 'act_the_reader_named', 'test_the_reader_named', 'planted_control', 'builder_disposition_of_a_candidate']); w.writerows(out)
    base = [o for o in out if '-' not in o[0]]; cands = [o for o in out if o[4].startswith('CANDIDATE') and not o[7]]
    print('single-article quotations: groups', len(base), '| planted controls', n_ctl, 'found', found, '| passages beside a group', len(out) - len(base),
          '| reader verdicts', dict(Counter(o[4] for o in out)), '| candidates that are not controls', len(cands), '| drawn', sum(o[8].startswith('drawn') for o in cands), '| not drawn or already carried', sum(not o[8].startswith('drawn') for o in cands))
    pout = []; tot = Counter()
    blank = Counter()
    for lane in 'abcdefgh':
        acts = list(csv.DictReader(open(L / f'para_nv8_{lane}.acts.csv'))); lines = {r['line_id']: r['act_no'] for r in csv.DictReader(open(L / f'para_nv8_{lane}.lines.csv'))}
        n_in = sum(1 for _ in open(L / f'para_nv8_{lane}.lines_in.tsv')) - 1; assert len(lines) == n_in, ('a line the reader did not place', lane, len(lines), n_in)
        held = Counter(lines[r['line_id']] for r in csv.DictReader(open(L / f'para_nv8_{lane}.controls.tsv'), delimiter='\t') if r['only_a_held_out_act_carried_it'] == 'yes')
        for a in acts:
            cand = a['verdict'].startswith('CANDIDATE'); k = (lane, a['act_no'])
            if not a['verdict'].strip(): blank[(lane, 'acts')] += 1; blank[(lane, 'lines')] += int(a['lines'] or 0)
            if cand: assert k in PARA, ('a candidate with no disposition', k)
            else: assert k not in PARA, ('a disposition for an act the reader did not call a candidate', k)
            tot[(lane, 'acts')] += 1; tot[(lane, 'candidates')] += cand; tot[(lane, 'drawn')] += cand and PARA[k].startswith('drawn')
            pout.append(['para_nv8_' + lane, a['act_no'], a['actor'], a['lines'], held.get(a['act_no'], 0) or '', a['verdict'], a['chip'], scrub((a['chip_wording'] or a['note'])[:240]), PARA.get(k, '')])
        tot[(lane, 'lines')] = n_in
    with open(R / 'nv8_paraphrased_acts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['lane', 'act_as_the_reader_numbered_it', 'actor', 'census_lines_sorted_into_it', 'of_them_lines_only_a_held_out_act_carried', 'reader_verdict', 'chip_the_reader_named', 'what_it_is_in_the_reader_s_words', 'builder_disposition_of_a_candidate']); w.writerows(pout)
    print('paraphrased lines: ' + ' | '.join(f"{l}: lines {tot[(l, 'lines')]}, acts {tot[(l, 'acts')]}, candidates {tot[(l, 'candidates')]}, drawn {tot[(l, 'drawn')]}, no verdict {blank[(l, 'acts')]} acts ({blank[(l, 'lines')]} lines)" for l in 'abcdefgh'),
          '| all: lines', sum(tot[(l, 'lines')] for l in 'abcdefgh'), 'candidates', sum(tot[(l, 'candidates')] for l in 'abcdefgh'), 'drawn', sum(tot[(l, 'drawn')] for l in 'abcdefgh'))
    # the second reading of the set-aside items
    ein = {r['item']: r for r in csv.DictReader(open(L / 'earlier_nv8_a.items_in.tsv'), delimiter='\t')}; held = set((L / 'earlier_nv8_a.controls.txt').read_text().split())
    eout = []; ec = Counter(); back = set()
    for r in csv.DictReader(open(L / 'earlier_nv8_a.items.csv')):
        i = ein[r['item']]; cand = r['verdict'].startswith('CANDIDATE'); k = r['item']
        if k in E_CONTROL:
            assert E_CONTROL[k] in held and cand, ('a held-out act the reader did not call a candidate', k); back.add(E_CONTROL[k]); disp = 'a planted control: the act was held out of the reader\'s table (' + E_CONTROL[k] + ')'; kind = 'control'
        else:
            if cand: assert k in EARLIER, ('a candidate with no disposition', k)
            disp = EARLIER.get(k, ''); kind = 'drawn' if disp.startswith('drawn') else ('carried' if disp.startswith('carried') else ('not drawn' if disp else 'the reader\'s verdict stands'))
            if r['chip'] and not disp: assert all(x in ids for x in re.findall(r'MA\d+', r['chip'])), ('the reader names a chip that is not there', k, r['chip'])
        ec[kind] += 1
        first = scrub(' '.join((i['first_reader_exact_words'] or r['exact_words']).split()[:14]))
        eout.append([k, i['lane'], i['act_or_group'], i['actor'], i['page_id'].split()[0], first, 'outside the days', r['verdict'], r['chip'], r['report_day'], 'yes' if k in E_CONTROL else '', disp])
    assert len(eout) == len(ein) == 67 and not set(EARLIER) - set(ein), 'an item with no row, or a disposition for no item'
    with open(R / 'nv8_earlier_acts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['item', 'lane_of_the_first_reader', 'group_or_act_there', 'actor', 'page', 'first_words', 'first_reader_verdict', 'second_reader_verdict', 'chip_the_second_reader_named', 'report_day_the_second_reader_gave',
                    'planted_control', 'builder_disposition']); w.writerows(eout)
    drawn_acts = sorted({m for o in eout if o[11].startswith('drawn') for m in re.findall(r'MA\d+', o[11].split(' (')[0])}, key=lambda x: int(x[2:]))
    print('set-aside items read again:', len(eout), '| reader verdicts', dict(Counter(o[7] for o in eout)), '| held-out acts', len(held), 'with an item', len(set(E_CONTROL.values())), 'found', len(back),
          '| builder:', dict(ec), '| acts the drawn items sit on:', len(drawn_acts))
    # the reading of every counted article
    acts = {r['row_id']: r for r in rows_map.rows() if r['row_id'].startswith('MA')}; acts.update({'MA' + str(int(k[2:])): v for k, v in list(acts.items())})
    loose = lambda s: re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip(); sh = lambda s: {' '.join(w[i:i + 4]) for w in [loose(s).split()] for i in range(len(w) - 3)}
    pool = list(csv.DictReader(open(L / 'recall_nv8.pool.tsv'), delimiter='\t')); ctl = list(csv.DictReader(open(L / 'recall_nv8.controls.tsv'), delimiter='\t'))
    CTL_BY_HAND = {('recall_nv8_01', 'MA85'): 'contacted Commerce Under Secretary', ('recall_nv8_10', 'MA348'): 'Jensen is currently on Air Force One'}
    # the control lines are frozen as they were found when the census was first read (research/reading_lanes/recall_nv8.control_lines.tsv, from the table released at ee4f40d): a chip amended later
    # can come to share words with another line of its page, which is not a control (the first matcher, by shared words with the act as it stands, is kept below as a check on the frozen list)
    is_ctl = {int(r['row_in_the_pool']): r['act_held_out'] for r in csv.DictReader(open(L / 'recall_nv8.control_lines.tsv'), delimiter='\t')}; found = set(is_ctl.values())
    for k in ctl:
        if k['act_held_out'] in NOT_VALID_CTL: continue
        assert any(a == k['act_held_out'] and pool[n]['lane'] == k['lane'] and pool[n]['page_id'] == k['page_in_the_lane'] and pool[n]['verdict'].startswith('CANDIDATE') for n, a in is_ctl.items()), ('a control with no frozen line', k)
    NOT_VALID = NOT_VALID_CTL        # its earlier part (a refusal of June) is carried by two other chips, as its reader said: not a test of that reader
    assert {k['act_held_out'] for k in ctl} - found == NOT_VALID, ('controls not found', {k['act_held_out'] for k in ctl} - found)
    # the grouping lanes: every open candidate line (and the planted controls of the census) sorted into distinct earlier acts by six further readers
    grp = {}; line_g = {}; g_ctl = Counter(); n_in = 0
    for j in range(1, 7):
        nm = f'group_nv8_{j:02d}'; lin = [r['line'] for r in csv.DictReader(open(L / f'{nm}.lines_in.tsv'), delimiter='\t')]; n_in += len(lin)
        gs = {r['group']: r for r in csv.DictReader(open(L / f'{nm}.groups.csv'))}; asg = list(csv.DictReader(open(L / f'{nm}.lines.csv')))
        assert sorted(r['line'] for r in asg) == sorted(lin) and all(r['group'] in gs for r in asg), ('a line with no group or two', nm)
        cl = {r['line'] for r in csv.DictReader(open(L / f'{nm}.controls.tsv'), delimiter='\t')}
        for r in asg: line_g[int(r['line'][1:])] = f"{j}.{r['group']}"; g_ctl[f"{j}.{r['group']}"] += r['line'] in cl
        for k, g in gs.items(): grp[f'{j}.{k}'] = g
    assert not set(G_NEW) & set(grp); grp.update(G_NEW)
    all_ids = {r['row_id'] for r in rows_map.rows()} | {r['row_id'] for r in csv.DictReader(open(R / 'member_ties.csv'))}
    for n_, (k_, pg_) in L_ASSIGN.items(): assert n_ not in line_g and pool[n_]['page_id'] == pg_ and pool[n_]['verdict'] == 'carried', n_; line_g[n_] = k_
    g_lines = Counter(line_g.values()); g_disp = {}
    for k, g in grp.items():
        named = [x for x in re.findall(r'M[AT]\d+|TY\d+', g.get('carried_by') or '') if x in all_ids]
        assert bool(named) == bool((g.get('carried_by') or '').strip()), ('a group whose reader names a chip that is not there', k, g.get('carried_by'))
        if k in G_REOPEN: g_disp[k] = 'open: on no chip (' + G_REOPEN[k] + ': the twenty-second reading); not drawn until the owner decides what the image should carry'
        elif named: g_disp[k] = 'carried: ' + ', '.join(named + [G_ALSO[k]] if k in G_ALSO else named) + ' (the grouping reader\'s verdict)' + G_AFTER.get(k, '')
        elif k in G_BUILDER: g_disp[k] = G_BUILDER[k]
        elif k in G_PART: g_disp[k] = 'open, carried in part: ' + G_PART[k] + '; the rest is not drawn until the owner decides what the image should carry'
        else: g_disp[k] = G_OPEN + G_CTL_NOTE.get(k, '') + G_NOTE.get(k, '') + G_NEW_NOTE.get(k, '')
    assert set(G_NEW_NOTE) == set(G_NEW) and not set(G_PART) - set(grp) and all(g_disp[k].startswith('open, carried in part') for k in G_PART), 'a group to mark carried in part is not there, or another list took it'
    assert not (set(G_BUILDER) | set(G_ALSO) | set(G_CTL_NOTE) | set(G_AFTER) | set(G_REOPEN) | set(G_FIRST) | set(G_NOTE)) - set(grp), 'a reading for a group that is not there'
    assert all(g_disp[k].startswith('carried') for k in list(G_ALSO) + list(G_AFTER)) and all(g_disp[k].startswith('open') for k in list(G_NOTE) + [x for x in G_NEW if x not in G_BUILDER]), 'a note on a group of the other kind'
    assert all(any(i in all_ids for i in re.findall(r'M[AT]\d+', v)) for v in G_BUILDER.values()) and all(v in all_ids for v in G_ALSO.values())
    rout = []; rc = Counter(); used = Counter(); used_late = Counter(); used_wd = Counter()
    for n, r in enumerate(pool):
        v = r['verdict'].strip(); ids = ['MA' + str(int(x[2:])) for x in re.findall(r'MA\d+', r['chip_or_tie'])]
        done = [d for d in R_DONE if d[0] == r['page_id'] and d[1] == r['actor'] and d[2] in r['exact_words']]
        if n in is_ctl: disp = 'a planted control: the act was held out of the reader\'s table (' + is_ctl[n] + ')'
        elif done: disp = done[0][3]; used[done[0][:3]] += 1
        elif v == 'carried' and any((i, None) in R_WD for i in ids):
            w_ = next(i for i in ids if (i, None) in R_WD); assert acts[w_].get('withdrawn'), w_; disp = R_WD.get((w_, r['page_id']), R_WD[(w_, None)]); used_wd[(w_, r['page_id']) if (w_, r['page_id']) in R_WD else (w_, None)] += 1
        elif v == 'carried':
            late = [i for i in ids if acts[i]['date'] and r['page_day'] and r['page_day'] < acts[i]['date']]
            rep = [i for i in late if acts[i]['reported']]
            if rep: assert all(i in R_EARLY for i in rep), ('a report-dated chip named on an earlier page, with no disposition', rep, r['page_id']); disp = R_EARLY[rep[0]]
            elif late:
                key = tuple(re.findall(r'M[AT]\d+', r['chip_or_tie'])); hit = [x for x in R_LATE if x[0] == key and x[1] in (None, r['page_id']) and x[2] in (None, r['actor'])]
                assert hit, ('a chip on its own day named from an earlier page, with no disposition', key, r['page_id'], r['actor']); disp = hit[0][3]; used_late[R_LATE.index(hit[0])] += 1
            else: disp = ''
        else:
            assert n in line_g, ('an open candidate line that no grouping lane holds', n, r['page_id'])
            disp = g_disp[line_g[n]]
        rc[(v, disp.split(':')[0] if disp else 'the reader\'s verdict stands')] += 1
        rout.append([r['lane'], r['page_id'], r['page_day'], r['actor'], v, ' '.join(re.findall(r'M[AT]\d+', r['chip_or_tie'])), r['row_it_belongs_on'], r['direction'].strip(), disp, line_g.get(n, '')])
    assert all(used_wd[k] for k in R_WD), ('a disposition for no line', [k for k in R_WD if not used_wd[k]])
    art = {r['page_id']: r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}
    for page, actor, row, direction, k, *lab_ in R_ADDED + R_ADDED_MORE:        # lines no census reader listed: they join the act they belong to, with the lane column saying whose they are
        assert k in grp and art[page]['counted'] == 'yes' and '2026-10-29' <= art[page]['day'] <= '2026-11-12', (page, k)        # the act may be open, worded in part, or drawn since (B.05, B.08; the renting of 3.MS03)
        rc[('CANDIDATE occasion', g_disp[k].split(':')[0])] += 1; g_lines[k] += 1
        rout.append([lab_[0] if lab_ else 'added by the builder (twenty-second reading)', page, art[page]['day'], actor, 'CANDIDATE occasion', '', row, direction, g_disp[k], k])
    import nv8_page_dates
    for page, actor, row, direction, k in R_OUTSIDE:        # lines on pages another session saved, outside the table: the lane column says so, and the day is the page's own, read as U.S. Eastern
        assert k in G_NEW and page not in art and (R / 'primary' / page).is_dir(), (page, k); day = nv8_page_dates.day_of(page, *nv8_page_dates.meta(page))[0]; assert '2026-10-29' <= day <= '2026-11-12', (page, day)
        rc[('CANDIDATE occasion', g_disp[k].split(':')[0])] += 1; g_lines[k] += 1
        rout.append([LB26O, page, day, actor, 'CANDIDATE occasion', '', row, direction, g_disp[k], k])
    assert all(used_late[i] for i in range(len(R_LATE))), ('a disposition for no line', [R_LATE[i][:3] for i in range(len(R_LATE)) if not used_late[i]])
    assert all(used[d[:3]] for d in R_DONE), ('a line the builder says it acted on is not in the pool', [d[:3] for d in R_DONE if not used[d[:3]]])
    with open(R / 'nv8_recalls.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['lane', 'page', 'page_day', 'actor', 'reader_verdict', 'chip_or_tie_the_reader_named', 'row_the_reader_proposed', 'which_way_the_reader_says_it_cuts', 'builder_disposition', 'earlier_act']); w.writerows(rout)
    # the register of distinct earlier acts: one row for each group, in its reader's words (no words of pages), with the builder's disposition
    FR = lambda g, k='': G_FIRST.get(k) or next((x for x in ('in these days', 'before', 'unclear') if (g.get('first_reported') or '').strip().lower().startswith(x)), 'unclear')
    pages_of = defaultdict(set); days_of = defaultdict(list)
    for o in rout:
        if o[9]: pages_of[o[9]].add(o[1]); days_of[o[9]].append((o[2], o[1]))
    gout = []
    for k, g in sorted(grp.items(), key=lambda kv: (kv[1]['actor'], -len(pages_of[kv[0]]), kv[0])):
        first = min(days_of[k])
        gout.append([k, g['actor'], scrub(g['what']), scrub(g.get('when') or ''), (g.get('kind') or '').strip(), FR(g, k), first[1], first[0], g_lines[k], len(pages_of[k]), g_ctl[k] or '',
                     (g.get('row_it_belongs_on') or '').strip(), (g.get('direction') or '').strip(), g_disp[k]])
    with open(R / 'nv8_recall_groups.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['earlier_act', 'actor', 'what_it_is_in_the_grouping_reader_s_words', 'when_as_the_pages_give_it', 'kind', 'first_reported', 'earliest_page', 'earliest_day', 'lines', 'pages', 'of_them_planted_controls',
                    'row_the_reader_proposed', 'which_way_the_reader_says_it_cuts', 'builder_disposition']); w.writerows(gout)
    gop = [o for o in gout if o[13].startswith('open')]; n_ctl_lines = sum(g_ctl.values()); ctl_carried = sum(g_ctl[k] for k in grp if not g_disp[k].startswith('open'))
    print('grouping of the open lines: lines', n_in, 'of them planted controls', n_ctl_lines, 'in a carried group', ctl_carried, '| groups', len(gout), 'of them added by the builder', len(G_NEW), '| carried', len(gout) - len(gop), '| open', len(gop), 'with lines', sum(o[8] for o in gop), 'of them planted controls', sum(o[10] or 0 for o in gop), 'reader-carried lines assigned to an open act', len(L_ASSIGN), 'and added lines', len(R_ADDED) + len(R_ADDED_MORE), 'and lines on saved pages outside the table', len(R_OUTSIDE),
          '| open by first report', dict(Counter(o[5] for o in gop).most_common()), '| open by direction', dict(Counter(o[12] for o in gop).most_common()), '| open by kind', dict(Counter(o[4] for o in gop).most_common()),
          '| open in these days by direction', dict(Counter(o[12] for o in gop if o[5] == 'in these days').most_common()))
    npg = sum(1 for j in range(1, 13) for _ in csv.DictReader(open(L / f'recall_nv8_{j:02d}.pages.tsv'), delimiter='\t'))
    nread = sum(1 for j in range(1, 13) for x in csv.DictReader(open(L / f'recall_nv8_{j:02d}.pages_read.csv')) if x['read_whole'].strip().lower() == 'yes')
    cand = [o for o in rout if o[4].startswith('CANDIDATE')]
    print('every counted article read for reports of earlier acts: pages', npg, 'read whole', nread, '| lines', len(rout), 'of them added after the census', len(R_ADDED) + len(R_ADDED_MORE), dict(Counter(o[4] for o in rout)), '| held-out acts', len(ctl), 'valid', len(ctl) - len(NOT_VALID), 'found', len(found),
          '| candidate lines open', sum(1 for o in cand if o[8].startswith('open')), 'on pages', len({o[1] for o in cand if o[8].startswith('open')}), 'of them on saved pages outside the table: lines', sum(1 for o in cand if o[0] == LB26O and o[8].startswith('open')), 'pages', len({o[1] for o in cand if o[0] == LB26O}), '| by direction', dict(Counter(o[7] for o in cand if o[8].startswith('open')).most_common()),
          '| dispositions', {f'{k[0]} / {k[1]}': v for k, v in sorted(rc.items())})

    added_pages()


# what the builder did with each record of lane acts_nv8_added_a that its reader did not call carried, keyed by the physical line of its acts.csv (line 1 is the header)
NOREPLY = 'not drawn: a report that no reply had come to a request is not a refusal under the figure\'s rule'
ON72 = 'drawn: on MA72, from the ministry\'s own statement of Nov 12, which the chip already cited'
ONLET = 'drawn: on MA31 and MA152, from the letter itself'
OUT = 'the page is of Nov 15 or 16, outside the days, and was not added'
A_DISP = {6: 'open: an earlier act the register holds (3.MS50); this page\'s line is added to it', 12: 'not drawn: the page names no occasion; the ministry\'s statement of Nov 9 is on its chip in its own words (MA71)',
          17: 'open: an earlier act the register holds (2.NV2-194); this page\'s line is added to it', 30: NOREPLY, 31: NOREPLY, 60: NOREPLY, 61: NOREPLY, 80: NOREPLY,
          38: 'open: registered as a new earlier act (B.06)', 63: 'open: registered as a new earlier act (B.06)', 43: ON72, 44: ON72, 45: ON72, 52: ON72, 55: ON72,
          64: 'drawn: MA367 (on its own day, Thursday Nov 12: a second saved page gives the interview that day. When first drawn it sat on its report\'s day with a caution that the passage might be newer; this cell still said so until the twenty-sixth reading)', 69: ONLET, 70: ONLET, 77: 'drawn: MA368',
          73: 'not drawn: a summary that names no occasion; his advocacy on occasions the pages date is on his chips', 82: 'not drawn: names no purchase; the purchases the pages give with amounts are an open act of the register (3.MS01)',
          84: 'not drawn: the page describes what the company\'s site lists and gives it no day; not a statement on the matter', 87: 'not drawn: the outlet\'s own attempts to reach the company, not an act of the company',
          104: 'not registered: ' + OUT + '; the register holds acts that pages of the fifteen days recall', 111: 'not registered: ' + OUT + '; the register holds acts that pages of the fifteen days recall',
          114: 'drawn: on MA151, from a report of Nov 12 that another session of this project had saved and the table of pages does not hold (not from this page: ' + OUT + '). The builder had written that only this later page gives the date; the twenty-fourth reading found it in that report',
          115: 'not drawn: the only saved account of the post is this page; ' + OUT + '; the post itself is not saved (a lead for a search of his own channel)', 120: ONLET + ' (not from this page: ' + OUT + ')', 121: ONLET + ' (not from this page: ' + OUT + ')'}


def added_pages():
    acts = list(csv.DictReader(open(L / 'acts_nv8_added_a.acts.csv', newline='', encoding='utf-8'))); pr = {r['page_id']: r for r in csv.DictReader(open(L / 'acts_nv8_added_a.pages_read.csv', newline='', encoding='utf-8'))}
    ctl = {r['page_in_the_lane']: r['act_held_out'] for r in csv.DictReader(open(L / 'acts_nv8_added_a.controls.tsv', newline=''), delimiter='\t')}
    held = {r['row_id']: r for r in rows_map.rows() if r['row_id'] in set(ctl.values())}; art = {r['page_id']: r for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t')}
    loose = lambda t: re.sub(r'[^a-z0-9]+', ' ', t.lower()).strip(); out = []; found = set(); ids = {r['row_id'] for r in rows_map.rows()}
    for n, r in enumerate(acts, 2):
        v = r['verdict'].strip(); inw = r['page_id'] in art and art[r['page_id']]['counted'] == 'yes'; c = ctl.get(r['page_id'])
        isc = bool(c) and r['actor'] == held[c]['actor'] and any(loose(r['exact_words'])[:40] in loose(q) or loose(q)[:40] in loose(r['exact_words']) for q in held[c]['q'])
        if isc: assert v.startswith('CANDIDATE'), ('a planted control the reader called carried', n); found.add(c); disp = f'a planted control: carried by {c}, which was held out of the reader\'s table'; assert n not in A_DISP, n
        elif v == 'carried': assert n not in A_DISP, n; disp = '' if inw else OUT
        else: assert n in A_DISP, ('a candidate with no disposition', n, r['page_id'], r['actor']); disp = A_DISP[n]
        for i in re.findall(r'M[AT]\d+', disp): assert i in ids, i
        out.append([r['page_id'], pr[r['page_id']]['first_published_day'] or pr[r['page_id']]['updated_day'], 'yes' if inw else 'no', r['actor'], scrub(r['day_as_the_page_gives_it']), r['in_these_days_or_earlier'], v, ' '.join(re.findall(r'M[AT]\d+', r['chip_or_tie'])), r['direction'].strip(), disp])
    assert found == set(ctl.values()), ('controls not found', set(ctl.values()) - found)
    with open(R / 'nv8_added_pages_acts.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['page', 'day_the_page_prints', 'added_to_the_count', 'actor', 'day_of_the_act_as_the_page_gives_it', 'in_these_days_or_earlier', 'reader_verdict', 'chip_or_tie_the_reader_named', 'which_way_the_reader_says_it_cuts', 'builder_disposition']); w.writerows(out)
    cand = [o for o in out if o[6].startswith('CANDIDATE')]
    print('nine pages added on Nov 17, and two read and left out: records', len(out), dict(Counter(o[6] for o in out)), '| on pages added', sum(1 for o in out if o[2] == 'yes'), '| held-out chips', len(ctl), 'found', len(found),
          '| candidates by disposition', dict(Counter(o[9].split(':')[0] for o in cand).most_common()))


if __name__ == '__main__':
    main()
