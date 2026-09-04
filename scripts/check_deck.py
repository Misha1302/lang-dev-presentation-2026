#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
index=(ROOT/'index.html').read_text(encoding='utf-8')

def fragment_text(path):
    raw=path.read_text(encoding='utf-8')
    m=re.search(r'String\.raw`(.*)`\);\s*$',raw,re.S)
    assert m, f'cannot parse {path.name}'
    return m.group(1)
fragments='\n'.join(fragment_text(p) for p in sorted(ROOT.glob('deck-act-*.js'), key=lambda p:int(re.search(r'(\d+)',p.stem).group(1))))
class P(HTMLParser):
    def __init__(self): super().__init__(); self.slides=[]; self.cur=None; self.depth=0; self.buf=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if self.cur is None and tag=='section' and 'slide' in a.get('class','').split(): self.cur=a; self.depth=1; self.buf=[]; return
        if self.cur is not None and tag not in {'br','meta','link','img','input'}: self.depth+=1
    def handle_startendtag(self,tag,attrs):
        return
    def handle_endtag(self,tag):
        if self.cur is None:return
        self.depth-=1
        if self.depth==0 and tag=='section': self.slides.append((self.cur,' '.join(' '.join(self.buf).split()))); self.cur=None
    def handle_data(self,data):
        if self.cur is not None:self.buf.append(data)
p=P(); p.feed(fragments)
main=[s for s in p.slides if s[0].get('data-kind')!='appendix']; appendix=[s for s in p.slides if s[0].get('data-kind')=='appendix']
assert len(main)==65, f'expected 65 main slides, got {len(main)}'
assert len(appendix)==6, f'expected 6 appendix slides, got {len(appendix)}'
assert [x[0].get('data-note-key') for x in main]==[f'm{i}' for i in range(1,66)]
assert [x[0].get('data-note-key') for x in appendix]==[f'a{i}' for i in range(1,7)]
assert 'data-deck-qa-contract="semantic-composition-v1"' in index
for name in [f'deck-act-{i}.js' for i in range(1,10)]+['speaker-notes-hardening.js','speaker-notes-research.js','deck.js','styles.css','foundation.css','presenter.css']:
    assert (ROOT/name).exists(), f'missing runtime asset {name}'
text='\n'.join(x[1] for x in main)
foundation=['A small language rarely stays small','What if language features were reusable components','same bricks can produce different language profiles','Here “dialect” means language profile / configuration','The DSL declares WHAT language / policy we want','First, the generic compiler picture','Wist has a concrete multi-stage pipeline','A list of stages stops being enough','Definition → Compiler → Plan → Runtime','Extensibility can exist mostly during authoring and planning','Module boundaries should not become permanent optimization boundaries','FEASIBILITY FIRST. PREFERENCE SECOND.','Deep abstractions for authoring → one concrete compiler for optimization']
research=['Producer × consumer wiring does not scale','Change zero existing consumers','Stable semantic contracts','contextual Judgement','OBLIGATIONS','Lowering is not semantic refinement','upward semantic projection','Add a producer. Change zero consumers. Measure what actually improves.']
for anchor in foundation+research:
    assert anchor in text, f'missing narrative anchor: {anchor}'
pos={a:text.index(a) for a in foundation+research}
assert pos['Deep abstractions for authoring → one concrete compiler for optimization'] < pos['Producer × consumer wiring does not scale']
assert pos['Producer × consumer wiring does not scale'] < pos['contextual Judgement'] < pos['OBLIGATIONS'] < pos['upward semantic projection']
assert 'Not MLIR dialect' in text and text.index('Not MLIR dialect') < text.index('MLIR already makes extensibility')
assert 'CURRENT UT' in text and 'RESEARCH HYPOTHESIS' in text and 'DESIGN SKETCH' in text and 'ANALOGY' in text
for forbidden in ['zero overhead','fully eliminates N×M','first semantic query system','universal inverse lowering is always possible']:
    assert forbidden.lower() not in text.lower()
raw_notes=(ROOT/'speaker-notes-hardening.js').read_text(encoding='utf-8')
prefix='window.SPEAKER_NOTES = '
assert raw_notes.startswith(prefix) and raw_notes.rstrip().endswith(';')
notes=json.loads(raw_notes[len(prefix):].rstrip()[:-1])
raw_research=(ROOT/'speaker-notes-research.js').read_text(encoding='utf-8')
m=re.search(r'Object\.assign\(window\.SPEAKER_NOTES,\s*(\{.*\})\);\s*$',raw_research,re.S)
assert m
notes.update(json.loads(m.group(1)))
for key in [f'm{i}' for i in range(1,66)]+[f'a{i}' for i in range(1,7)]:
    assert key in notes and 'СКАЗАТЬ:' in notes[key], f'missing usable note {key}'
assert len(notes)==71
print('Deck contract PASS: 65 main + 6 appendix; foundation precedes Judgement/Obligations; current/proposed/prior-art boundaries present')
