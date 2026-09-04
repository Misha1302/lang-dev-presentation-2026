#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, shutil, subprocess, sys, time
ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=ROOT/'render-artifacts'
if ARTIFACTS.exists(): shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()
raw='\n'.join(p.read_text(encoding='utf-8') for p in sorted(ROOT.glob('deck-act-*.js')))
main_count=len(re.findall(r'data-kind="main"',raw)); appendix_count=len(re.findall(r'data-kind="appendix"',raw))
if main_count!=67 or appendix_count!=6:
    print(f'Render check FAILED: discovered {main_count} main + {appendix_count} appendix'); sys.exit(1)
targets=[f'#{i}' for i in range(1,main_count+1)]+[f'#a{i}' for i in range(1,appendix_count+1)]
browser=next((n for n in ['google-chrome-stable','google-chrome','chromium-browser','chromium'] if shutil.which(n)),None)
if browser is None: print('Render check FAILED: Chrome/Chromium was not found'); sys.exit(1)
server=subprocess.Popen([sys.executable,'-m','http.server','8878','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
common=[browser,'--headless=new','--disable-gpu','--disable-dev-shm-usage','--no-sandbox','--no-first-run']
required=[(1920,1080),(1366,768)]; stress=[(1536,864),(1280,720)]; screenshot_vp=required+[(1280,720)]; presenter_vp=[(1920,1080),(1366,768),(1280,720)]
presenter_targets=[f'#{i}' for i in [1,8,9,11,13,18,23,27,31,37,38,39,40,46,48,53,56,58,63,64,67]]+['#a5']

def inspect(width,height,target,presenter=False):
    mode='presenter=1&' if presenter else ''
    url=f'http://127.0.0.1:8878/?{mode}visual-check=1{target}'
    result=None
    for attempt in range(2):
        try: result=subprocess.run(common+[f'--window-size={width},{height}','--dump-dom',url],capture_output=True,text=True,timeout=25)
        except subprocess.TimeoutExpired:
            if attempt==0: time.sleep(.5); continue
            return 'browser timeout after retry'
        if result.returncode!=0:
            if attempt==0: time.sleep(.5); continue
            return f'browser exit {result.returncode} after retry'
        break
    if result and 'data-visual-check="ok"' in result.stdout: return None
    out=result.stdout if result else ''; marker='data-visual-errors="'; start=out.find(marker)
    if start<0:return 'visual status missing'
    start+=len(marker); end=out.find('"',start); return out[start:end]
try:
    time.sleep(.7); failures=[]
    for w,h in required+stress:
        for target in targets:
            detail=inspect(w,h,target)
            if detail: failures.append(f'audience {w}x{h} {target}: {detail}')
    for w,h in presenter_vp:
        for target in presenter_targets:
            detail=inspect(w,h,target,True)
            if detail: failures.append(f'presenter {w}x{h} {target}: {detail}')
    nav_url='http://127.0.0.1:8878/?nav-check=1#1'
    try: nav=subprocess.run(common+['--window-size=1366,768','--dump-dom',nav_url],capture_output=True,text=True,timeout=35)
    except subprocess.TimeoutExpired: failures.append('navigation: browser timeout')
    else:
        if nav.returncode!=0 or 'data-nav-check="ok"' not in nav.stdout:
            marker='data-nav-errors="'; start=nav.stdout.find(marker); detail='navigation status missing'
            if start>=0: start+=len(marker); detail=nav.stdout[start:nav.stdout.find('"',start)]
            failures.append(f'navigation: {detail}')
    for w,h in screenshot_vp:
        for target in targets:
            output=ARTIFACTS/f'{w}x{h}-{target[1:]}.png'; url=f'http://127.0.0.1:8878/{target}'
            try: shot=subprocess.run(common+[f'--window-size={w},{h}','--hide-scrollbars',f'--screenshot={output}',url],capture_output=True,text=True,timeout=25)
            except subprocess.TimeoutExpired: failures.append(f'screenshot {w}x{h} {target}: timeout'); continue
            if shot.returncode!=0 or not output.exists(): failures.append(f'screenshot {w}x{h} {target}: failed')
    for w,h in presenter_vp:
        for target in presenter_targets:
            output=ARTIFACTS/f'presenter-{w}x{h}-{target[1:]}.png'; url=f'http://127.0.0.1:8878/?presenter=1{target}'
            try: shot=subprocess.run(common+[f'--window-size={w},{h}','--hide-scrollbars',f'--screenshot={output}',url],capture_output=True,text=True,timeout=25)
            except subprocess.TimeoutExpired: failures.append(f'presenter screenshot {w}x{h} {target}: timeout'); continue
            if shot.returncode!=0 or not output.exists(): failures.append(f'presenter screenshot {w}x{h} {target}: failed')
    expected=len(targets)*len(screenshot_vp)+len(presenter_targets)*len(presenter_vp); actual=len(list(ARTIFACTS.glob('*.png')))
    if actual!=expected: failures.append(f'screenshot coverage: expected {expected}, got {actual}')
    if failures:
        print('Render check FAILED:'); [print(' - '+x) for x in failures]; sys.exit(1)
    geometry=len(targets)*(len(required)+len(stress))+len(presenter_targets)*len(presenter_vp)
    print(f'Render check OK: {main_count} main + {appendix_count} appendix; {expected} screenshots; {geometry} geometry states; navigation + presenter sync PASS')
finally:
    server.terminate()
    try: server.wait(timeout=5)
    except subprocess.TimeoutExpired: server.kill()
