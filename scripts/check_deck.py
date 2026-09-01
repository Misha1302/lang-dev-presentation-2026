#!/usr/bin/env python3
from html.parser import HTMLParser
from pathlib import Path
import json, re

root=Path(__file__).resolve().parents[1]
html=(root/'index.html').read_text(encoding='utf-8')
css=(root/'styles.css').read_text(encoding='utf-8')
js1=(root/'speaker-notes-1.js').read_text(encoding='utf-8')
js2=(root/'speaker-notes-2.js').read_text(encoding='utf-8')
js3=(root/'speaker-notes-hardening.js').read_text(encoding='utf-8')

m1=re.search(r"window\.SPEAKER_NOTES=(\{.*?\});\n",js1,re.S)
m2=re.search(r"Object\.assign\(window\.SPEAKER_NOTES,(\{.*?\})\);\n",js2,re.S)
m3=re.search(r"Object\.assign\(window\.SPEAKER_NOTES,\s*(\{.*?\})\s*\);",js3,re.S)
assert m1 and m2 and m3, 'speaker notes objects missing'
notes_by_key=json.loads(m1.group(1)); notes_by_key.update(json.loads(m2.group(1))); notes_by_key.update(json.loads(m3.group(1)))

class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.slides=[]; self._in=False; self._depth=0; self._buf=[]; self._attrs={}
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='section' and 'slide' in a.get('class',''):
            self._in=True; self._depth=1; self._buf=[]; self._attrs=a; return
        if self._in: self._depth+=1
    def handle_endtag(self,tag):
        if self._in:
            self._depth-=1
            if self._depth==0 and tag=='section':
                self.slides.append((self._attrs,' '.join(''.join(self._buf).split()))); self._in=False
    def handle_data(self,data):
        if self._in: self._buf.append(data)

p=SlideParser(); p.feed(html)
main=[s for s in p.slides if s[0].get('data-kind')!='appendix']
appendix=[s for s in p.slides if s[0].get('data-kind')=='appendix']
assert len(main)==16, f'expected 16 main slides, got {len(main)}'
assert len(appendix)==8, f'expected 8 appendix slides, got {len(appendix)}'

main_notes=[]
for n,(attrs,_) in enumerate(main,1):
    key=attrs.get('data-note-key')
    assert key in notes_by_key, f'main slide {n} missing speaker note key'
    notes=notes_by_key[key]
    main_notes.append(notes)
    assert len(notes)>300
    for marker in ['ЗАЧЕМ','СКАЗАТЬ','ПЕРЕХОД','НЕ ПЕРЕОБЕЩАТЬ']:
        assert marker in notes, f'main slide {n} notes missing {marker}'

notes_words=sum(len(re.findall(r'\b[\wА-Яа-яЁё.-]+\b',n)) for n in main_notes)
assert 2200<=notes_words<=3250, f'speaker notes word count out of contract: {notes_words}'

required=[
    'Build an Extensible Language,',
    'Run a Concrete One',
    'One fixed language is easy',
    'Wist infrastructure',
    'At first, this still looks like options',
    'Configuration becomes',
    'Local authors declare facts. The integrator chooses a language. The planner sees the whole.',
    'UTL2002',
    'PreferCapabilityProvider',
    'LanguageArtifactRoute',
    'LanguagePlan',
    'Open possibilities close',
    'LanguageRuntime.Create',
    'Extensible at composition time.',
    'Composition deabstraction',
    'No exact-current benchmark artifact',
    'Structural compatibility is not semantic compatibility',
    'Use the simplest owner',
    'TensorRules',
    'No exact-current raw result artifact',
    '7005371d6c30175dff4b0e9f906a26218b0ee54d'
]
full=re.sub(r'\s+',' ',html+' '+js1+' '+js2+' '+js3)
missing=[x for x in required if x not in full]
assert not missing, f'missing narrative/evidence elements: {missing}'

layout_primitives=[
    '.phase{', '.family-grid{', '.pillgrid{', '.interaction{', '.roles{',
    '.route-story{', '.plan-card{', '.timeline{', '.comparecards{', '.costs{', '.decisionrule{'
]
missing_layout=[x for x in layout_primitives if x not in css]
assert not missing_layout, f'missing current-deck layout primitives: {missing_layout}'

for forbidden in ['zero-cost extensibility','all abstractions disappear','StubLanguageCompiler']:
    assert forbidden.lower() not in full.lower(), f'forbidden/obsolete claim present: {forbidden}'

assert 'Build the Language, Then Make the Abstractions Disappear' not in html, 'old title remains in live deck'
assert '36206b66548fec365be6e03381ba44d50c2cafe5' not in html, 'stale source pin remains in live deck'
assert 'appendixBtn' in html
assert 'speaker-notes-1.js' in html and 'speaker-notes-2.js' in html and 'speaker-notes-hardening.js' in html
print(f'OK: {len(main)} main, {len(appendix)} appendix, {notes_words} speaker-note words')
