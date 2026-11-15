"""Which harvested links belong to the Huang story. Used by build_sweep.py and build_manual_list.py.
scope(url, text) -> 'story' (about Huang, the relationship, the investigation or the exit),
                    'fallout' (export controls, Lutnick, Megaspeed-style diversion, the share price, the Anthropic offering),
                    or '' (Nvidia is mentioned but the piece is about something else)."""
import re
WHO = re.compile(r'huang|jensen|megaspeed|\balice\b|jen-hsun', re.I)
NV = re.compile(r'nvidia|nividia', re.I)
STORY = re.compile(r'spy|spies|spying|espionage|honey|affair|scandal|oust|resign|probe|investigat|successor|succession|\bceo\b|chief|\bboss\b|board|'
                   r'chair|interim|kress|harvey-?\s?jones|drama|crisis|fallout|turmoil|wachtell|shareholder', re.I)
# headlines that tell the story without naming Nvidia or Huang ("America's Top Chip Boss ... Suspected Chinese Spy")
UNNAMED = re.compile(r"(chinese|china'?s?)[- ]'?spy|spy'?[- ](scandal|allegations|thriller|operations)|honey[- ]?(trap|pot)|chip[- ]boss|i[- ]spy[- ]ai", re.I)
FALL = re.compile(r'lutnick|export|chip-?\s?controls|curbs|diver(t|sion)|smuggl|blacklist|entity-?\s?list|china|chinese|hong-?\s?kong|shares|stock|slump|'
                  r'slide|sell-?off|impact|commerce|where-the-chips|government|trump', re.I)


# words that put a piece on the story by themselves; the rest of STORY (probe, CEO, board, chief, crisis ...) are generic
SPECIFIC = re.compile(r'spy|spies|spying|espionage|honey|affair|scandal|oust|resign|successor|succession|interim|kress|harvey-?\s?jones|wachtell', re.I)
# a piece admitted on a generic word alone is left out when it names another subject (audit1b found six such among 1,732)
OTHER = re.compile(r'hugging[- ]?face|antitrust|ai[- ]competition|chip[- ]competition|tariff|bank[- ]of[- ]nvidia', re.I)


_READ = None


def read_in():
    """Addresses that a reading put on the story although the word rule leaves them out (research/coverage_scope_read.tsv:
    the links left out were read after the second audit found ten of 150 plainly on the story)."""
    global _READ
    if _READ is None:
        import csv
        from pathlib import Path
        p = Path(__file__).resolve().parents[1] / 'research' / 'coverage_scope_read.tsv'
        _READ = {r['url'] for r in csv.DictReader(open(p, newline='', encoding='utf-8'), delimiter='\t') if r['finding'] == 'on the story'} if p.exists() else set()
    return _READ


def scope(url, text):
    if url in read_in():
        return 'story'
    t = f'{url} {text}'
    if WHO.search(t) or UNNAMED.search(t):
        return 'story'
    if NV.search(t) and STORY.search(t):
        if SPECIFIC.search(t) or not OTHER.search(t):
            return 'story'
        return ''
    if re.search(r'lutnick', t, re.I) or (NV.search(t) and FALL.search(t)) or (re.search(r'anthropic', t, re.I) and re.search(r'\bipo\b|prospectus|s-1', t, re.I)):
        return 'fallout'
    return ''


if __name__ == '__main__':   # control: one of each
    assert scope('https://a/x', 'Nvidia Gets a Chinese Honeypot Lesson') == 'story'
    assert scope('https://a/trump-lutnick-nvidia', 'Trump sticks by Commerce Secretary Lutnick') == 'fallout'
    assert scope('https://a/canada-nvidia-back-cohere', 'Cohere completes the first close of a round') == ''
    assert scope('https://a/b', "Sleeping With The Enemy? America's Top Chip Boss And His Link To A Suspected Chinese Spy") == 'story'
    assert scope('https://a/b', 'Apple turns iCloud into spy cloud, will start looking at public share links') == ''
    assert scope('https://a/b', "DOJ Probes Nvidia's Hugging Face Deal Over AI Competition Concerns") == ''
    assert scope('https://a/b', 'Nvidia board launches independent inquiry following chief executive security concerns') == 'story'
    print('story_scope ok')
