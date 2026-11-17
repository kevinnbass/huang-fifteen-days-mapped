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
from collections import Counter
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
 'a:A047': D('MA333') + ' (the reader\'s page is a later copy of the dispatch; the chip cites the earliest saved copy, of the same day)',
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
 'g:A049': D('MA169') + ' (added to the department\'s act of that day, which already cited the page)',
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
]
# chips the readers named as carrying a line from a page EARLIER than the chip's day, and what the builder did
R_EARLY = {
 'MA330': 'moved: the chip now sits on Oct 29, the day of the first pages that recall the permission',
 'MA329': 'moved: the chip now sits on Nov 8, the day of the first page that recalls the bargain',
 'MA301': 'moved: the chip now sits on Nov 10, the day of the first saved relay of the report',
 'MA322': 'moved: the chip now sits on Nov 7, the day of the first page that recalls the approvals',
 'MA345': 'split: the remark to a podcaster has its own chip on Nov 9 (MA359); this chip keeps the interview first recalled on Nov 11',
 'MA333': 'not moved: the page of Nov 5 does not mention the affair (the chip names it); a page of Nov 8 carries the sentence only after an update on Nov 9',
 'MA319': 'not moved: the earlier page recalls the president\'s share trades, which are tie lines; the White House\'s reply drawn here is in the page of Nov 12',
 'MA323': 'not moved: the earlier pages speak of the inquiry in general or give Megaspeed\'s own statement (its chip); the audits as this chip words them are in the page of Nov 12',
 'MA353': 'not moved: the earlier pages carry Huang\'s refusal of June, which is on the Times\'s chip of Nov 5 and on her chip of Oct 29; the letter of July 2025 is first in the page of Nov 10',
 'MA355': 'not moved: the earlier pages carry Huang\'s refusal of June, which is on the Times\'s chip of Nov 5 and on her chip of Oct 29; her joining the bill is first in the page of Nov 12',
 'MA169': 'open: the earlier pages recall the indictment of March; whether each ties it to Megaspeed has not been read by the builder',
}
R_OPEN = 'open: not yet grouped or drawn'
R_OWN = 'open: the chip sits on its own day and the reader names an earlier page; not read again by the builder'


def scrub(t):
    for pat, role in SCRUB:
        t = re.sub(pat, role, t)
    assert not any(re.search(pat, t) for pat, _ in SCRUB), t
    return t


def main():
    ids = {r['row_id'] for r in rows_map.rows()}
    for v in list(ONE.values()) + list(PARA.values()) + list(EARLIER.values()) + [x[3] for x in R_DONE] + list(R_EARLY.values()):
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
    is_ctl = {}; found = set()
    for k in ctl:
        a = acts[k['act_held_out']]; want = set()
        for q in list(a['q']) + [a['what']]: want |= sh(q)
        for n, r in enumerate(pool):
            if r['lane'] == k['lane'] and r['page_id'] == k['page_in_the_lane'] and r['verdict'].startswith('CANDIDATE') and (len(want & sh(r['exact_words'])) >= 2 or CTL_BY_HAND.get((k['lane'], k['act_held_out']), '\0') in r['exact_words']):
                is_ctl[n] = k['act_held_out']; found.add(k['act_held_out'])
    NOT_VALID = {'MA327'}        # its earlier part (a refusal of June) is carried by two other chips, as its reader said: not a test of that reader
    assert {k['act_held_out'] for k in ctl} - found == NOT_VALID, ('controls not found', {k['act_held_out'] for k in ctl} - found)
    rout = []; rc = Counter(); used = Counter()
    for n, r in enumerate(pool):
        v = r['verdict'].strip(); ids = ['MA' + str(int(x[2:])) for x in re.findall(r'MA\d+', r['chip_or_tie'])]
        done = [d for d in R_DONE if d[0] == r['page_id'] and d[1] == r['actor'] and d[2] in r['exact_words']]
        if n in is_ctl: disp = 'a planted control: the act was held out of the reader\'s table (' + is_ctl[n] + ')'
        elif done: disp = done[0][3]; used[done[0][:3]] += 1
        elif v == 'carried':
            late = [i for i in ids if acts[i]['date'] and r['page_day'] and r['page_day'] < acts[i]['date']]
            rep = [i for i in late if acts[i]['reported']]
            if rep: assert all(i in R_EARLY for i in rep), ('a report-dated chip named on an earlier page, with no disposition', rep, r['page_id']); disp = R_EARLY[rep[0]]
            elif late: disp = R_OWN
            else: disp = ''
        else: disp = R_OPEN
        rc[(v, disp.split(':')[0] if disp else 'the reader\'s verdict stands')] += 1
        rout.append([r['lane'], r['page_id'], r['page_day'], r['actor'], v, ' '.join(re.findall(r'M[AT]\d+', r['chip_or_tie'])), r['row_it_belongs_on'], r['direction'].strip(), disp])
    assert all(used[d[:3]] for d in R_DONE), ('a line the builder says it acted on is not in the pool', [d[:3] for d in R_DONE if not used[d[:3]]])
    with open(R / 'nv8_recalls.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['lane', 'page', 'page_day', 'actor', 'reader_verdict', 'chip_or_tie_the_reader_named', 'row_the_reader_proposed', 'which_way_the_reader_says_it_cuts', 'builder_disposition']); w.writerows(rout)
    npg = sum(1 for j in range(1, 13) for _ in csv.DictReader(open(L / f'recall_nv8_{j:02d}.pages.tsv'), delimiter='\t'))
    nread = sum(1 for j in range(1, 13) for x in csv.DictReader(open(L / f'recall_nv8_{j:02d}.pages_read.csv')) if x['read_whole'].strip().lower() == 'yes')
    cand = [o for o in rout if o[4].startswith('CANDIDATE')]
    print('every counted article read for reports of earlier acts: pages', npg, 'read whole', nread, '| lines', len(rout), dict(Counter(o[4] for o in rout)), '| held-out acts', len(ctl), 'valid', len(ctl) - len(NOT_VALID), 'found', len(found),
          '| candidate lines open', sum(1 for o in cand if o[8] == R_OPEN), 'on pages', len({o[1] for o in cand if o[8] == R_OPEN}), '| by direction', dict(Counter(o[7] for o in cand if o[8] == R_OPEN).most_common()),
          '| dispositions', {f'{k[0]} / {k[1]}': v for k, v in sorted(rc.items())})


if __name__ == '__main__':
    main()
