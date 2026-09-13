#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import json
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / 'render-artifacts'
if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

browser = next((name for name in [
    'google-chrome-stable', 'google-chrome', 'chromium-browser', 'chromium', 'chrome'
] if shutil.which(name)), None)
if browser is None:
    print('Render check FAILED: Chrome/Chromium was not found')
    sys.exit(1)

server = subprocess.Popen(
    [sys.executable, '-m', 'http.server', '8878', '--bind', '127.0.0.1'],
    cwd=ROOT,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
common = [
    browser, '--headless=new', '--disable-gpu', '--disable-dev-shm-usage',
    '--no-sandbox', '--no-first-run'
]
canonical_geometry = (1366, 768)
extra_audience_geometry = [(1920, 1080), (1536, 864), (1280, 720)]
extra_presenter_geometry = [(1920, 1080), (1280, 720)]


def dump_dom(width: int, height: int, url: str, timeout: int = 30) -> tuple[int, str, str]:
    result = subprocess.run(
        common + [f'--window-size={width},{height}', '--dump-dom', url],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.returncode, result.stdout, result.stderr


def data_attr(dom: str, name: str) -> str | None:
    match = re.search(rf'\bdata-{re.escape(name)}="([^"]*)"', dom)
    if not match:
        return None
    return html.unescape(match.group(1))


def runtime_manifest() -> tuple[list[str], list[str]]:
    url = 'http://127.0.0.1:8878/?runtime-manifest=1#1'
    last = ''
    for attempt in range(3):
        code, out, err = dump_dom(*canonical_geometry, url, timeout=35)
        last = out + err
        if code == 0:
            main_keys = data_attr(out, 'runtime-main-keys')
            appendix_keys = data_attr(out, 'runtime-appendix-keys')
            missing = data_attr(out, 'runtime-speech-missing')
            if main_keys is not None and appendix_keys is not None and missing is not None:
                main = [key for key in main_keys.split(',') if key]
                appendix = [key for key in appendix_keys.split(',') if key]
                if missing:
                    raise AssertionError(f'missing canonical speech for runtime keys: {missing}')
                if len(main) != len(set(main)) or len(appendix) != len(set(appendix)):
                    raise AssertionError('runtime slide keys are not unique')
                if set(main) & set(appendix):
                    raise AssertionError('runtime main and appendix keys overlap')
                if len(main) < 1 or len(appendix) < 1:
                    raise AssertionError(f'invalid runtime counts: {len(main)} main + {len(appendix)} appendix')
                return main, appendix
        time.sleep(.7)
    raise AssertionError('runtime manifest attributes missing or browser failed: ' + last[:500])


def runtime_targets(main_keys: list[str], appendix_keys: list[str]) -> dict[str, str]:
    mapping = {key: f'#{i + 1}' for i, key in enumerate(main_keys)}
    mapping.update({key: f'#a{i + 1}' for i, key in enumerate(appendix_keys)})
    return mapping


def semantic_sample(main_keys: list[str], appendix_keys: list[str]) -> list[str]:
    sample: list[str] = []
    if main_keys:
        sample.extend([main_keys[0], main_keys[-1]])
    if appendix_keys:
        sample.extend([appendix_keys[0], appendix_keys[-1]])
    contract_path = ROOT / 'CONTENT_NARRATIVE_CONTRACT.json'
    if contract_path.is_file():
        contract = json.loads(contract_path.read_text(encoding='utf-8'))
        for spec in contract.get('milestones', {}).values():
            owner = spec.get('owner')
            if owner:
                sample.append(owner)
    sample.extend(['m33', 'm34', 'm35', 'm36', 'm43', 'm45', 'm48', 'm49', 'pa4', 'pa5', 'pa7', 'pa2', 'pa8', 'm50'])
    known = set(main_keys) | set(appendix_keys)
    result: list[str] = []
    for key in sample:
        if key in known and key not in result:
            result.append(key)
    return result


def inspect(width: int, height: int, target: str, presenter: bool = False) -> str | None:
    mode = 'presenter=1&' if presenter else ''
    url = f'http://127.0.0.1:8878/?{mode}visual-check=1{target}'
    result = None
    for attempt in range(2):
        try:
            result = subprocess.run(
                common + [f'--window-size={width},{height}', '--dump-dom', url],
                capture_output=True,
                text=True,
                timeout=25,
            )
        except subprocess.TimeoutExpired:
            if attempt == 0:
                time.sleep(.5)
                continue
            return 'browser timeout after retry'
        if result.returncode != 0:
            if attempt == 0:
                time.sleep(.5)
                continue
            return f'browser exit {result.returncode} after retry'
        break
    if result and 'data-visual-check="ok"' in result.stdout:
        return None
    output = result.stdout if result else ''
    marker = 'data-visual-errors="'
    start = output.find(marker)
    if start < 0:
        return 'visual status missing'
    start += len(marker)
    end = output.find('"', start)
    return html.unescape(output[start:end])


def screenshot(width: int, height: int, target: str, output: Path, presenter: bool = False) -> str | None:
    mode = '?presenter=1' if presenter else ''
    url = f'http://127.0.0.1:8878/{mode}{target}'
    try:
        shot = subprocess.run(
            common + [f'--window-size={width},{height}', '--hide-scrollbars', f'--screenshot={output}', url],
            capture_output=True,
            text=True,
            timeout=25,
        )
    except subprocess.TimeoutExpired:
        return 'timeout'
    if shot.returncode != 0 or not output.exists():
        return f'failed exit={shot.returncode}'
    return None


try:
    time.sleep(.7)
    failures: list[str] = []
    try:
        main_keys, appendix_keys = runtime_manifest()
    except Exception as exc:
        print(f'Render check FAILED: {exc}')
        sys.exit(1)

    target_by_key = runtime_targets(main_keys, appendix_keys)
    all_targets = [target_by_key[key] for key in [*main_keys, *appendix_keys]]
    sample_targets = [target_by_key[key] for key in semantic_sample(main_keys, appendix_keys)]

    width, height = canonical_geometry
    for target in all_targets:
        detail = inspect(width, height, target)
        if detail:
            failures.append(f'audience {width}x{height} {target}: {detail}')
        detail = inspect(width, height, target, True)
        if detail:
            failures.append(f'presenter {width}x{height} {target}: {detail}')

    for width, height in extra_audience_geometry:
        for target in sample_targets:
            detail = inspect(width, height, target)
            if detail:
                failures.append(f'audience-sample {width}x{height} {target}: {detail}')
    for width, height in extra_presenter_geometry:
        for target in sample_targets:
            detail = inspect(width, height, target, True)
            if detail:
                failures.append(f'presenter-sample {width}x{height} {target}: {detail}')

    nav_url = 'http://127.0.0.1:8878/?nav-check=1#1'
    try:
        nav = subprocess.run(common + ['--window-size=1366,768', '--dump-dom', nav_url], capture_output=True, text=True, timeout=35)
    except subprocess.TimeoutExpired:
        failures.append('navigation: browser timeout')
    else:
        if nav.returncode != 0 or 'data-nav-check="ok"' not in nav.stdout:
            marker = 'data-nav-errors="'
            start = nav.stdout.find(marker)
            detail = 'navigation status missing'
            if start >= 0:
                start += len(marker)
                detail = html.unescape(nav.stdout[start:nav.stdout.find('"', start)])
            failures.append(f'navigation: {detail}')

    width, height = canonical_geometry
    for target in all_targets:
        output = ARTIFACTS / f'{width}x{height}-{target[1:]}.png'
        detail = screenshot(width, height, target, output)
        if detail:
            failures.append(f'screenshot {width}x{height} {target}: {detail}')
        output = ARTIFACTS / f'presenter-{width}x{height}-{target[1:]}.png'
        detail = screenshot(width, height, target, output, presenter=True)
        if detail:
            failures.append(f'presenter screenshot {target}: {detail}')

    expected = len(all_targets) * 2
    actual = len(list(ARTIFACTS.glob('*.png')))
    if actual != expected:
        failures.append(f'screenshot coverage: expected {expected}, got {actual}')
    if failures:
        print('Render check FAILED:')
        for failure in failures:
            print(' - ' + failure)
        sys.exit(1)

    canonical_states = len(all_targets) * 2
    sampled_states = len(sample_targets) * (len(extra_audience_geometry) + len(extra_presenter_geometry))
    print(
        f'Render check OK: {len(main_keys)} runtime main + {len(appendix_keys)} runtime appendix; '
        f'{expected} canonical screenshots; {canonical_states} full canonical audience/presenter states; '
        f'{sampled_states} sampled extra geometry states; navigation + canonical presenter sync PASS'
    )
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
