"""Run: python3 -I scripts/nv8_remarks_no_chip.py      (written Nov 16, 2026, after the fourteenth reading)
A third gauge of the chips. The register of remarks (scripts/nv8_gaps.py) lists a quoted remark of a drawn actor only when two pages give it in
exactly the same words; the gauge by actor and day (scripts/nv8_actor_days.py) sees only days on which the actor has no chip. Between them
fell a remark that two articles quote in slightly different words on a day the speaker already had a chip: the president's answer of Nov 12
that it was not yet determined whether the woman in the reports was a spy. This gauge looks for that kind:
  every line of the census readings that is a direct quotation of seven words or more by a drawn actor, on a counted page;
  a line is carried when it shares five words in a row with the words or cited passages of any chip of that actor, or when three fifths of
  its words are in one chip's words and passages;
  lines not carried are grouped when they share five words in a row; a group found in two or more counted articles is listed, unless a line
  of the register of remarks (already judged there) shares five words in a row with it.
Each listed group was read by the builder: it is part of a statement a chip already carries in other words, or not of these days, or not on
the matter, or it got a chip or was added to one (those are no longer listed). A group with no reading stops the script.
Three readings of the builder were wrong (found by the sixteenth reading, Nov 16): a chairman's note to employees had been read as part of his
press statement, and two groups from a think tank's piece as part of a fellow's earlier posts. A similar position is not the same occurrence;
each is drawn now as its own act and is no longer listed.
Control: with the chip for the president's answer taken away, the gauge must list it.
Writes research/nv8_remarks_no_chip.tsv (the first twelve words of the longest line stand for the group; for one group, its other line). Limits: a remark that only one
counted article quotes is not seen; nor is one the census reader did not mark as a direct quotation, or of fewer than seven words."""
import csv, re, sys
from collections import defaultdict, Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; R = ROOT / 'research'; sys.path.insert(0, str(ROOT / 'scripts'))
import nv8_gaps as G, rows_map
N = 5
SAME = 'part of a statement a chip of that day already carries in other words: '
READ = {
    ('china', 'we have already made our position clear on the'): SAME + 'the ministry\'s replies of Nov 9 and Nov 12, in other translations (its chips for those days)',
    ('china', 'we stand ready to work with the us to'): 'not on the matter: the ministry on relations between the two countries',
    ('china', 'based on groundless speculation and is nothing more than'): SAME + 'the ministry\'s reply to the first report, in another translation (its chip for Oct 30)',
    ('coons', 'we write to request that the department of commerce'): SAME + 'the letter with Sen. Warren (his chip for Nov 11)',
    ('huang', 'my family bears no responsibility for my choices i'): SAME + 'his memo to staff (his chip for Nov 8)',
    ('jeffries', 'there are real concerns that need to be addressed'): SAME + 'his remarks of Nov 9 asking for a full briefing (his chip for that day)',
    ('kennedy', 'the obvious question is why did lutnick choose to'): SAME + 'his remarks to Politico that the Commerce secretary "needs to answer" (his chip for Nov 11)',
    ('kennedy', 'and they need to be investigated by the justice'): SAME + 'his remarks of Nov 10; the chip says he wants investigations',
    ('moolenaar', 'he has stated hes a patriot he has questioned'): SAME + 'his remarks of Nov 12 on the talks for an appearance before the committees (his chip for that day)',
    ('nvidia', 'datacenters and clouds built on american chips are the'): 'not on the matter: a statement on data-centre policy in reports that do not mention the affair',
    ('nvidia', 'the prc government is not seeking nvidia products from'): SAME + 'its reply to the first report (its chip for Oct 29, which carries its denial)',
    ('nvidia', 'we sell our data center gpus primarily to well'): 'not of these days: statements of 2025 that later reports quote as made "at the time"',
    ('schumer', 'one of our most important companies thats involved in'): SAME + 'his floor speech of Nov 10 (his chip for that day)',
    ('mcguire', 'the biggest problem remains unaddressed the department of commerce'): SAME + 'his posts of Nov 6 to Nov 8 asking why Commerce took no action (his chips for Nov 6 and Nov 8)',
    ('mcguire', 'bisgov has done so not only by permitting the'): SAME + 'his posts of Nov 6 to Nov 8 asking why Commerce took no action (his chips for Nov 6 and Nov 8)',
    ('mcguire', 'why is commerce protecting jensen and supporting his preferred'): SAME + 'his posts of Nov 6 to Nov 8 asking why Commerce took no action (his chips for Nov 6 and Nov 8)',
}
# One group is stood for by its other line: the release's scan for private names reads two pronouns in the longest line's first words as a name in its lists.
LOCATOR = {('moolenaar', 'he has stated hes a patriot he has questioned'): 'I would hope he would want to come in and have that discussion with us'}
CONTROL = ('trump', 'perhaps it would be different')          # the remark that showed the fault: its chip is taken away for the control


def nw(s):
    return re.sub(r'[^a-z0-9 ]+', ' ', s.lower().replace('’', "'").replace("'", '')).split()


def sh(w, n=N):
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}


def groups(lines, acts, reg):
    chip_sh = defaultdict(set); chip_words = defaultdict(list)
    for a in acts:
        t = a['what'] + ' ' + ' '.join(a['q']); chip_sh[a['actor']] |= sh(nw(t)); chip_words[a['actor']].append(G.words(t))
    out = []
    for a, ls in sorted(lines.items()):
        unc = [l for l in ls if not (l['sh'] & chip_sh[a]) and not any(len(l['w']) >= 4 and len(l['w'] & cw) / len(l['w']) >= 0.6 for cw in chip_words[a])]
        parent = list(range(len(unc)))

        def find(x):
            while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
            return x
        first = {}
        for i, l in enumerate(unc):
            for s in l['sh']:
                if s in first: parent[find(i)] = find(first[s])
                else: first[s] = i
        cl = defaultdict(list)
        for i, l in enumerate(unc): cl[find(i)].append(l)
        for c in cl.values():
            arts = {l['art'] for l in c}; every = set().union(*[l['sh'] for l in c])
            if len(arts) < 2 or any(rs & every for rs in reg[a]): continue
            longest = max(c, key=lambda l: (len(l['text']), l['text']))
            out.append({'actor': a, 'articles': len(arts), 'days': ' '.join(sorted({l['day'] for l in c if l['day']})), 'key': ' '.join(nw(longest['text'])[:9]), 'first_words': ' '.join(longest['text'].split()[:12]), 'every': every})
    return out


def main():
    art = G.article_of(); lines = defaultdict(list); actors = {a[0] for a in rows_map.ACTORS}
    for r in G.lane_rows('remarks'):
        if r.get('page_id') not in art or (r.get('direct_quote') or '').strip().lower() != 'yes': continue
        a = G.actor_of(G.canon(r.get('speaker') or ''), r.get('kind', '')); w = nw(r.get('remark') or '')
        if a in actors and len(w) >= 7:
            lines[a].append({'art': art[r['page_id']], 'day': (r.get('day') or '').strip(), 'text': r['remark'], 'sh': sh(w), 'w': G.words(r['remark'])})
    reg = defaultdict(list)
    for x in csv.DictReader(open(R / 'nv8_gap_register.tsv'), delimiter='\t'):
        if x['register'] == 'remark': reg[x['key'].split('|')[0]].append(sh(nw(x['role'])))
    acts = [a for a in rows_map.acts() if not a.get('withdrawn')]
    out = groups(lines, acts, reg)
    key = lambda o: next((k for k in READ if k[0] == o['actor'] and o['key'].startswith(k[1])), None)
    unread = [(o['actor'], o['articles'], o['key']) for o in out if not key(o)]; assert not unread, ('a quoted remark in two or more articles that no chip carries, with no reading', unread)
    stale = sorted(set(READ) - {key(o) for o in out}); assert not stale, ('a reading for a group no longer listed', stale)
    held = [a for a in acts if a['actor'] == CONTROL[0] and CONTROL[1] in a['what']]; assert len(held) == 1, 'control: the chip for the remark that showed the fault'
    ctl = [o for o in groups(lines, [a for a in acts if a is not held[0]], reg) if o['actor'] == CONTROL[0] and any(CONTROL[1] in s for s in o['every'])]
    assert ctl, 'control: with that chip taken away the gauge does not list the remark'
    with open(R / 'nv8_remarks_no_chip.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n'); w.writerow(['actor', 'counted_articles', 'days_the_census_gives', 'first_words_of_a_line_of_the_group', 'reading'])
        w.writerows([o['actor'], o['articles'], o['days'], LOCATOR.get(key(o), o['first_words']), READ[key(o)]] for o in sorted(out, key=lambda o: (-o['articles'], o['actor'], o['key'])))
    print('quoted lines of drawn actors on counted pages', sum(len(v) for v in lines.values()), '| groups in two or more articles that no chip carries and the register has not judged:', len(out),
          '(each read) | control: listed without its chip, in', ctl[0]['articles'], 'articles')


if __name__ == '__main__':
    main()
