#!/usr/bin/env python3
"""Validate and render the actual self-contained production deck."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
from pathlib import Path
import subprocess
import tempfile
import threading

from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


GEOMETRY = r"""() => {
  const slide = document.querySelector('.slide.active');
  const stage = document.querySelector('#stage').getBoundingClientRect();
  const scale = stage.width / 1600;
  const problems = [];
  const body = slide.querySelector('.wrap > .body');
  const head = slide.querySelector('.head');
  const claim = slide.querySelector('.claim');
  if (body && head) {
    for (const child of body.children) {
      if (child.matches('.notes') || getComputedStyle(child).opacity === '0') continue;
      const r = child.getBoundingClientRect();
      if (r.top < head.getBoundingClientRect().bottom + 10*scale)
        problems.push({kind:'header-overlap', element:child.className});
      if (claim && getComputedStyle(claim).opacity !== '0' && r.bottom > claim.getBoundingClientRect().top - 10*scale)
        problems.push({kind:'claim-overlap', element:child.className});
    }
  }
  const record = slide.querySelector('.evidence-record');
  if (record && getComputedStyle(record).opacity !== '0' && record.getBoundingClientRect().height < 50*scale)
    problems.push({kind:'collapsed-evidence-record'});
  for (const panel of slide.querySelectorAll('.panel,.node,.chip')) {
    const r = panel.getBoundingClientRect();
    if (r.left < stage.left + 85*scale || r.right > stage.left + 1515*scale)
      problems.push({kind:'panel-bounds', element:panel.className});
  }
  const walker = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    const el = node.parentElement;
    if (!node.textContent.trim() || el.closest('.notes,title,desc,defs')) continue;
    if (getComputedStyle(el).display === 'none') continue;
    if ([...ancestors(el)].some(p => getComputedStyle(p).opacity === '0')) continue;
    const font = parseFloat(getComputedStyle(el).fontSize);
    if (font < 16) problems.push({kind:'small-font', text:node.textContent.trim(), font});
    const range = document.createRange(); range.selectNodeContents(node);
    const rects = [...range.getClientRects()];
    for (const r of rects) {
      if (!r.width || !r.height) continue;
      const x = (r.left - stage.left) / scale, y = (r.top - stage.top) / scale;
      const right = (r.right - stage.left) / scale, bottom = (r.bottom - stage.top) / scale;
      if (x < 75 || right > 1525 || y < 65 || bottom > (el.closest('.sources') ? 880 : 830))
        problems.push({kind:'content-bounds', text:node.textContent.trim(), x,y,right,bottom});
      const container = el.closest('.panel,.node,.chip');
      if (container && !el.closest('svg')) {
        const c = container.getBoundingClientRect();
        if (r.left < c.left + 8*scale || r.right > c.right - 8*scale)
          problems.push({kind:'panel-text-overflow', text:node.textContent.trim()});
      }
    }
  }
  function* ancestors(el) { while (el && el !== slide.parentElement) { yield el; el = el.parentElement; } }
  return problems;
}"""


def montage(paths: list[Path], output: Path, columns: int = 4, width: int = 480):
    height = round(width * 9 / 16)
    rows = (len(paths) + columns - 1) // columns
    canvas = Image.new('RGB', (columns * (width + 16) + 16, rows * (height + 40) + 16), '#131923')
    draw = ImageDraw.Draw(canvas)
    for i, path in enumerate(paths):
        x = 16 + i % columns * (width + 16)
        y = 16 + i // columns * (height + 40)
        with Image.open(path) as source:
            canvas.paste(source.convert('RGB').resize((width, height)), (x, y))
        draw.text((x, y + height + 8), path.stem, fill='#c7d4e4')
    canvas.save(output)


def validate(output: Path, browser_name: str = 'chromium'):
    output.mkdir(parents=True, exist_ok=True)
    html = (ROOT / 'index.html').read_text()
    script = html.split('<script>', 1)[1].split('</script>', 1)[0]
    with tempfile.TemporaryDirectory(prefix='langdev-js-') as temporary:
        script_path = Path(temporary) / 'deck.js'
        script_path.write_text(script)
        subprocess.run(['node', '--check', str(script_path)], check=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    errors, geometry, states, snapshots = [], [], [], []
    try:
        with sync_playwright() as p:
            browser = getattr(p, browser_name).launch()
            page = browser.new_page(viewport={'width':1600, 'height':900}, reduced_motion='reduce')
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
            embedded_fonts = page.evaluate("""async () => {
              const specs = [400,500,600,700,800].map(w => `${w} 26px DeckSans`)
                .concat([400,700].map(w => `${w} 26px DeckMono`));
              const loaded = await Promise.all(specs.map(s => document.fonts.load(s)));
              await document.fonts.ready;
              return loaded.map((faces,i) => ({spec:specs[i],count:faces.length,
                ready:faces.every(f => f.status === 'loaded')}));
            }""")
            assert all(f['count'] == 1 and f['ready'] for f in embedded_fonts), embedded_fonts
            assert page.locator('.slide').count() == 18
            metadata = page.locator('.slide').evaluate_all("ss => ss.map(s => ({id:s.id,seconds:+s.dataset.seconds,status:s.dataset.status,steps:[...s.querySelectorAll('[data-step]')].map(n=>+n.dataset.step)}))")
            assert [s['id'] for s in metadata] == [f'slide-{i}' for i in range(1, 19)]
            seconds = sum(s['seconds'] for s in metadata)
            assert 1260 <= seconds <= 1320, seconds
            assert all(s['status'] == 'proposed' for s in metadata[9:14])
            for s in metadata:
                assert s['steps'] == [] or sorted(set(s['steps'])) == list(range(1, max(s['steps']) + 1)), s
                notes = page.locator(f"#{s['id']} .notes").text_content()
                assert all(key in notes for key in ['ANCHOR:', 'FLOW:', 'TRANSITION:']), s['id']
            assert page.locator('[data-source]:not([href])').count() == 0
            for width, height in [(1600,900), (1920,1080)]:
                page.set_viewport_size({'width':width, 'height':height})
                for i in range(1,19):
                    page.evaluate('(n) => { LANGDEV_DECK.setReveal(false); LANGDEV_DECK.go(n); }', i)
                    path = output / f'{width}-slide-{i:02}.png'
                    page.screenshot(path=str(path))
                    if width == 1600: snapshots.append(path)
                    failures = page.evaluate(GEOMETRY)
                    if failures: geometry.append({'slide':i, 'width':width, 'problems':failures})
            page.set_viewport_size({'width':1600, 'height':900})
            for i, slide in enumerate(metadata, 1):
                page.evaluate('(n) => { LANGDEV_DECK.go(n); LANGDEV_DECK.setReveal(true); }', i)
                for step in range(max(slide['steps'], default=0) + 1):
                    page.evaluate('(s) => LANGDEV_DECK.setStep(s)', step)
                    path = output / f'reveal-{i:02}-{step}.png'
                    page.screenshot(path=str(path))
                    states.append(path)
                    failures = page.evaluate(GEOMETRY)
                    if failures: geometry.append({'slide':i, 'step':step, 'problems':failures})
            page.evaluate('() => {LANGDEV_DECK.setReveal(false); LANGDEV_DECK.go(1)}')
            for key in ['ArrowRight', 'ArrowDown', 'PageDown', 'Space', 'j']:
                before = page.evaluate('LANGDEV_DECK.active')
                page.keyboard.press(key)
                assert page.evaluate('LANGDEV_DECK.active') == before + 1, key
            for key in ['ArrowLeft', 'ArrowUp', 'PageUp', 'Shift+Space', 'k']:
                before = page.evaluate('LANGDEV_DECK.active')
                page.keyboard.press(key)
                assert page.evaluate('LANGDEV_DECK.active') == before - 1, key
            page.keyboard.press('End'); assert page.evaluate('LANGDEV_DECK.active') == 18
            page.keyboard.press('Home'); assert page.evaluate('LANGDEV_DECK.active') == 1
            page.locator('#next').click(); assert page.evaluate('LANGDEV_DECK.active') == 2
            page.locator('#prev').click(); assert page.evaluate('LANGDEV_DECK.active') == 1
            page.keyboard.press('Space'); assert page.evaluate('LANGDEV_DECK.active') == 1
            page.evaluate('document.activeElement.blur()')
            page.keyboard.press('r'); page.evaluate('LANGDEV_DECK.setStep(0)')
            page.keyboard.press('Space'); assert page.evaluate('LANGDEV_DECK.active') == 1
            page.keyboard.press('Space'); assert page.evaluate('LANGDEV_DECK.active') == 2
            page.keyboard.press('a'); assert page.locator('.slide.active [data-step]:not(.shown)').count() == 0
            page.keyboard.press('p'); assert page.locator('#notesPanel').is_visible()
            assert 'ANCHOR:' in page.locator('#notesPanel').text_content()
            assert page.locator('#notesPanel').bounding_box()['y'] < 120
            page.screenshot(path=str(output / 'presenter-notes-top.png'))
            page.keyboard.press('p'); page.keyboard.press('h'); assert page.locator('#helpOverlay').is_visible()
            page.keyboard.press('h'); page.keyboard.press('r')
            page.evaluate("location.hash = '#slide-12'"); page.wait_for_function('LANGDEV_DECK.active === 12')
            page.evaluate("location.hash = '#6'"); page.wait_for_function('LANGDEV_DECK.active === 6')
            page.locator('.dot').nth(3).click(); assert page.evaluate('LANGDEV_DECK.active') == 4
            page.mouse.wheel(0, 120); page.wait_for_function('LANGDEV_DECK.active === 5')
            page.mouse.wheel(0, 120); assert page.evaluate('LANGDEV_DECK.active') == 5
            page.evaluate("""() => {
              const target=document.querySelector('#stage');
              const touch=(y)=>new Touch({identifier:1,target,clientX:800,clientY:y});
              target.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[touch(600)]}));
              target.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[touch(400)]}));
            }""")
            assert page.evaluate('LANGDEV_DECK.active') == 6
            for size in [(1280,720), (1024,768), (390,844)]:
                page.set_viewport_size({'width':size[0], 'height':size[1]})
                page.evaluate('LANGDEV_DECK.go(11)')
                page.wait_for_function("() => {const r=document.querySelector('#stage').getBoundingClientRect();return r.left>=-.1 && r.top>=-.1 && r.right<=innerWidth+.1 && r.bottom<=innerHeight+.1}")
                rect = page.locator('#stage').bounding_box()
                assert abs(rect['width'] / rect['height'] - 16/9) < .01
                assert rect['x'] >= -.1 and rect['y'] >= -.1
                assert rect['x'] + rect['width'] <= size[0] + .1
                page.screenshot(path=str(output / f'fit-{size[0]}x{size[1]}.png'))
            page.set_viewport_size({'width':1600, 'height':900})
            page.context.set_offline(True)
            page.goto((ROOT / 'index.html').as_uri() + '#slide-18')
            assert page.evaluate('LANGDEV_DECK.active') == 18
            assert page.locator('#slide-18 img.qr').count() == 4
            assert page.locator('#slide-18 img.qr').evaluate_all(
                "els => els.every(e => e.src.startsWith('data:image/png;base64,') && e.complete && e.naturalWidth > 0)"
            )
            page.screenshot(path=str(output / 'offline-contact-slide.png'))
            page.context.set_offline(False)
            page.goto((ROOT / 'index.html').as_uri() + '#slide-8')
            assert page.evaluate('LANGDEV_DECK.active') == 8
            page.keyboard.press('ArrowRight'); assert page.evaluate('LANGDEV_DECK.active') == 9
            if browser_name == 'chromium':
                page.pdf(path=str(output / 'LangDev-2026.pdf'), width='1600px', height='900px', print_background=True, prefer_css_page_size=True)
            browser.close()
    finally:
        server.shutdown(); server.server_close(); worker.join()
    montage(snapshots, output / 'montage.png')
    for first in range(0,len(snapshots),4):
        montage(snapshots[first:first+4], output / f'contact-{first+1:02}.png', columns=2, width=800)
    montage([path for path in states if path.name.startswith(('reveal-11-', 'reveal-12-'))], output / 'proof-reveals.png', columns=3, width=640)
    for first in range(0,len(states),12):
        montage(states[first:first+12], output / f'reveal-contact-{first//12+1}.png', columns=3, width=600)
    report = {'browser':browser_name,'slides':len(metadata),'timing_seconds':seconds,'full_slide_screenshots':len(snapshots)*2,'reveal_states':len(states),'embedded_font_faces':len(embedded_fonts),'javascript_errors':errors,'geometry_issues':geometry,'navigation':'passed','touch_handler':'passed','local_file':'passed','responsive_fit':'passed'}
    (output / 'validation.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({key:value for key,value in report.items() if key != 'geometry_issues'},indent=2))
    print(f'Geometry issue groups: {len(geometry)}')
    assert not errors, errors
    assert not geometry, f'See {output / "validation.json"}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'qa')
    parser.add_argument('--browser', choices=['chromium','firefox'], default='chromium')
    args = parser.parse_args()
    validate(args.output.resolve(), args.browser)