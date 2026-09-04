#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib,os,re,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT/'production-artifacts'
if ARTIFACTS.exists(): shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()
PRODUCTION='https://misha1302.github.io/lang-dev-presentation-2026/'
sha=os.environ.get('GITHUB_SHA','unknown')
raw='\n'.join(p.read_text(encoding='utf-8') for p in sorted(ROOT.glob('deck-act-*.js')))
main_count=len(re.findall(r'data-kind="main"',raw)); appendix_count=len(re.findall(r'data-kind="appendix"',raw))
if (main_count,appendix_count)!=(67,6): print('Production check FAILED: local deck count contract mismatch'); sys.exit(1)
browser=next((n for n in ['google-chrome-stable','google-chrome','chromium-browser','chromium'] if shutil.which(n)),None)
if browser is None: print('Production check FAILED: Chrome/Chromium was not found'); sys.exit(1)
assets=['deck-act-2.js','deck-act-3.js','deck-act-4.js','deck-act-7.js','deck-act-8.js','foundation.css']
local_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in assets}
deadline=time.time()+360; last=''
while time.time()<deadline:
    stale=[]
    for name,expected in local_hashes.items():
        try:
            body=urlopen(f'{PRODUCTION}{name}?qa={quote(sha)}',timeout=15).read()
            actual=hashlib.sha256(body).hexdigest()
            if actual!=expected: stale.append(f'{name}:{actual[:12]}!=local:{expected[:12]}')
        except Exception as exc:
            stale.append(f'{name}:{exc}')
    if not stale: break
    last='; '.join(stale)
    time.sleep(5)
else: print(f'Production check FAILED: Pages did not reach exact final assets: {last}'); sys.exit(1)
common=[browser,'--headless=new','--disable-gpu','--disable-dev-shm-usage','--no-sandbox','--no-first-run']; failures=[]
nav_url=f'{PRODUCTION}?nav-check=1&qa={quote(sha)}#1'
try: nav=subprocess.run(common+['--window-size=1366,768','--dump-dom',nav_url],capture_output=True,text=True,timeout=35)
except subprocess.TimeoutExpired: failures.append('production navigation: browser timeout'); nav=None
if nav:
    if nav.returncode!=0 or 'data-nav-check="ok"' not in nav.stdout: failures.append('production navigation: nav-check did not pass')
    for marker in ['A small language rarely stays small','one representation abstraction actually disappears','Backends may differ in representation','Stable semantic contracts','upward semantic projection','soundness / false discharge']:
        if marker not in nav.stdout: failures.append(f'production narrative marker missing: {marker}')
    if 'data-deck-qa-contract="semantic-composition-v1"' not in nav.stdout: failures.append('production DOM contract marker mismatch')
representative=['#1','#5','#9','#11','#13','#18','#23','#28','#34','#37','#38','#39','#40','#45','#48','#53','#56','#58','#63','#64','#67','#a5','#a6']
for target in representative:
    url=f'{PRODUCTION}?visual-check=1&qa={quote(sha)}{target}'
    try: result=subprocess.run(common+['--window-size=1366,768','--dump-dom',url],capture_output=True,text=True,timeout=35)
    except subprocess.TimeoutExpired: failures.append(f'production {target}: browser timeout'); continue
    if result.returncode!=0 or 'data-visual-check="ok"' not in result.stdout: failures.append(f'production {target}: visual-check failed'); continue
    output=ARTIFACTS/f'1366x768-{target[1:]}.png'; shot_url=f'{PRODUCTION}?qa={quote(sha)}{target}'
    try: shot=subprocess.run(common+['--window-size=1366,768','--hide-scrollbars',f'--screenshot={output}',shot_url],capture_output=True,text=True,timeout=35)
    except subprocess.TimeoutExpired: failures.append(f'production screenshot {target}: timeout'); continue
    if shot.returncode!=0 or not output.exists(): failures.append(f'production screenshot {target}: failed')
if failures:
    print('Production check FAILED:'); [print(' - '+x) for x in failures]; sys.exit(1)
print(f'Production check OK: exact final asset hashes match Pages; {main_count} main + {appendix_count} appendix; navigation PASS; {len(representative)} representative live states PASS')
