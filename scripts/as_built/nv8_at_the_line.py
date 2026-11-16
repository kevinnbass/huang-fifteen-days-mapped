"""research/nv8_at_the_line.tsv: everyone named or quoted in three or four counted articles, with those articles, how many are separate
reports of something said or done on the matter, and whether the person is drawn. The readings below are the builder's, made by opening
each article (Nov 15 and 16, 2026); the article ids come from the tables, so a rebuild that changes anyone's articles stops here until the
person is read again.   Run: python3 -I scripts/nv8_at_the_line.py"""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'
sys.path.insert(0, str(ROOT / 'scripts'))
import member_mentions as M, rows_map
# name: (pages read, separate reports on the matter, drawn, the reading). The pages are the copies the reading opened, one per article.
# Sen. Ricketts was read here at four articles (three separate reports and one that names him for earlier work on chip exports); the pages
# saved by hand on Nov 16 add a fifth article, a Journal newsletter of Nov 10, so he is no longer at the line and his row left this table.
MEMBERS = {
 'Huizenga': (('sw-aljazeeracom-06', 'sw-cnbccom-09', 'sw-implicatorai-04', 'tnr-lutnick'), 3, 'yes', "His call for Commerce Secretary Lutnick to testify is on CNBC's live page of Nov 12 and in two other outlets' articles of that day (three separate reports); a fourth article names him only as cosponsor of a chip bill."),
 'Magaziner': (('cnbc-1108-bipartisan', 'sw-implicatorai-02', 'sw-politicalorg-11', 'x-dream1984-article'), 3, 'yes', "His call for Lutnick to testify alongside Huang is in three outlets' articles of Nov 8 and 9 (three separate reports); a fourth, a long post on X, says he quoted another post."),
 'Subramanyam': (('cnbc-1111-congress-resign', 'sw-americanbazaaronlineco-03', 'sw-winbuzzercom-b0d76647'), 3, 'yes', "CNBC's interview of Nov 11, in which he says Huang should resign, and two other outlets' articles of Nov 12 that report it."),
 'Bacon': (('cnbc-1111-congress-resign', 'sw-americanbazaaronlineco-03', 'sw-winbuzzercom-b0d76647'), 3, 'yes', "CNBC's interview of Nov 11, in which he says Huang should resign, and two other outlets' articles of Nov 12 that report it."),
 'Blumenthal': (('sw-cnbccom-02', 'sw-emptywheelnet-01', 'sw-semaforcom-04'), 3, 'yes', "His words to Semafor on a Senate investigation (Nov 9); CNBC's article of Nov 9, which says he renewed \"on Thursday\" his warning to donors to the president's ballroom, Nvidia among them; a blog's commentary on that demand (Nov 9)."),
 'Warner': (('sw-emptywheelnet-02', 'sw-semaforcom-04', 'sw-vinnewscom-03', 'art-line-straitstimes-bloomberg-1110'), 3, 'yes', "His words to Semafor (Nov 9); a report carried by VINnews that he \"said Monday\" he is interested in investigating further (Nov 10); and a Bloomberg report carried by the Straits Times that quotes him after the briefing of Nov 9. That third report was saved on Nov 16, after the eighth reading: until then it was known here only from a reader's comment under a blog post, which is the fourth page; the blog's own article does not name him."),
 'Neal': (('sw-cnbccom-09', 'man-9de9f2a5db75', 'man-a45550a35921'), 3, 'yes', "The letter of Nov 12 with Sen. Wyden, reported by CNBC, the Wall Street Journal and the Financial Times (three separate reports)."),
 'Scott': (('man-5db1c88adc15', 'man-9de9f2a5db75', 'man-nyt-1112-09', 'art-line-wex-scott-1112'), 3, 'yes', "His letters of Nov 12 are reported by the New York Times, the Wall Street Journal and the Washington Examiner (three separate reports). The Times's stand-alone article and the entry in its live page are one report, so the four articles are three. On Nov 15 he was withdrawn on the first two; the Examiner's article, which the aggregators listed on Nov 12 and which was not among the saved pages, was saved on Nov 16. A fifth piece listed that day, Politico's, names him in its headline and could not be saved."),
}
VOICES = {
 'Changpeng Zhao': ('zhao', ('cnn-1111-live', 'sw-cnbccom-09', 'sw-decryptco-31a5e63b', 'sw-newsbitcoincom-0ee6e1fb'), 4, 'yes', "His post of Nov 12 is quoted in four outlets' articles (four separate reports)."),
 'Ron Conway': ('conway', ('sw-sfstandardcom-04', 'sw-sfstandardcom-09', 'man-wapo-1112-02'), 3, 'yes', "His post of Nov 11 is reported in two different articles of the San Francisco Standard (a news report and a round-up of reactions) and quoted by the Washington Post."),
}


def main():
    art = {r['page_id']: r['article_id'] for r in csv.DictReader(open(R / 'nv8_articles.tsv', newline=''), delimiter='\t') if r['counted'] == 'yes'}
    n, hit, _ = M.count(); out = []
    at_line = sorted(s for s in M.FIRST if len(hit[s]) in (3, 4))
    assert at_line == sorted(MEMBERS), ('the members at three or four articles are not those read', sorted(set(at_line) ^ set(MEMBERS)))
    drawn = {a[2].split()[-1] for a in rows_map.ACTORS if a[4] is not None}
    for s, (pages, reports, d, words) in MEMBERS.items():
        ids = sorted(hit[s]); assert sorted({art[p] for p in pages}) == ids, ('the articles naming this member are not the ones read', s, ids, sorted({art.get(p) for p in pages}))
        assert (d == 'yes') == (s in drawn) and (reports >= 3) == (d == 'yes'), s
        out.append([s, 'member', len(ids), ' '.join(ids), reports, d, words])
    reg = {r['key']: r for r in csv.DictReader(open(R / 'nv8_gap_register.tsv', newline=''), delimiter='\t') if r['register'] == 'speaker'}
    for name, (key, pages, reports, d, words) in VOICES.items():
        ids = sorted({art[p] for p in pages}); assert int(reg[key]['pages']) == len(ids) and reg[key]['status'] == 'drawn', (name, reg[key]['pages'], ids)
        out.append([name, 'public voice', len(ids), ' '.join(ids), reports, d, words])
    voices_at_line = {k for k, r in reg.items() if r['status'] == 'drawn' and int(r['pages']) in (3, 4) and k in {a[0] for a in rows_map.ACTORS if a[1] == 'voices'}}
    assert voices_at_line == {v[0] for v in VOICES.values()}, ('the public voices at three or four articles are not those read', voices_at_line)
    with open(R / 'nv8_at_the_line.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['name', 'group', 'articles', 'article_ids', 'separate_reports_on_the_matter', 'drawn', 'reading']); w.writerows(out)
    print(len(out), 'people at three or four articles;', sum(o[5] == 'no' for o in out), 'not drawn')


if __name__ == '__main__':
    main()
