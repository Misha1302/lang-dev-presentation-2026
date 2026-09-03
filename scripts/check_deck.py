#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
html=(ROOT/'index.html').read_text()
notes_text=(ROOT/'speaker-notes-hardening.js').read_text()
class P(HTMLParser):
    def __init__(self): super().__init__(); self.slides=[]; self.cur=None; self.depth=0; self.buf=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if self.cur is None and tag=='section' and 'slide' in a.get('class','').split(): self.cur=a; self.depth=1; self.buf=[]; return
        if self.cur is not None and tag not in {'br','meta','link','img','input'}: self.depth+=1
    def handle_endtag(self,tag):
        if self.cur is None:return
        self.depth-=1
        if self.depth==0 and tag=='section': self.slides.append((self.cur,' '.join(''.join(self.buf).split()))); self.cur=None
    def handle_data(self,data):
        if self.cur is not None:self.buf.append(data)
p=P(); p.feed(html)
main=[s for s in p.slides if s[0].get('data-kind')!='appendix']; appendix=[s for s in p.slides if s[0].get('data-kind')=='appendix']
assert len(main)==27, f'expected 27 main slides, got {len(main)}'
assert len(appendix)==5, f'expected 5 appendix slides, got {len(appendix)}'
assert [x[0].get('data-note-key') for x in main]==[f'm{i}' for i in range(1,28)]
assert [x[0].get('data-note-key') for x in appendix]==[f'a{i}' for i in range(1,6)]
assert 'data-deck-qa-contract="semantic-composition-v1"' in html
anchors=['N producers × M consumers','add producer → change 0 consumers','Semantic contract','Judgement =','Writable','Small stable core','Operation-centric semantics','OBLIGATIONS','Lowering is not semantic refinement','upward semantic projection','One contract does not imply one engine','LanguagePlan is a consequence','None of these ideas is ours individually','research question — not a novelty claim','Strongest alternative','Make representations concrete']
text='\n'.join(x[1] for x in main)
missing=[a for a in anchors if a not in text]
assert not missing, f'missing semantic-composition anchors: {missing}'
for forbidden in ['Fact<T> — core innovation','first semantic query system','fully eliminates N×M','universal inverse lowering']:
    assert forbidden not in text
prefix='window.SPEAKER_NOTES = '
assert notes_text.startswith(prefix) and notes_text.rstrip().endswith(';')
notes=json.loads(notes_text[len(prefix):].rstrip()[:-1])
for k in [f'm{i}' for i in range(1,28)]+[f'a{i}' for i in range(1,6)]:
    assert k in notes and 'СКАЗАТЬ:' in notes[k], f'missing usable note {k}'
print('Deck contract PASS: 27 main + 5 appendix; semantic composition, obligations, multi-level lowering, upward projection, prior-art boundary and falsifiable experiment present')
