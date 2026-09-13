#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding='utf-8')


def script_order() -> list[str]:
    return re.findall(r'<script\s+src="([^"]+)"', read('index.html'))


def parse_final_order(raw: str) -> tuple[list[str], list[str]]:
    main_match = re.search(r'const FINAL_MAIN_ORDER = Object\.freeze\(\[(.*?)\]\);', raw, re.S)
    appendix_match = re.search(r'FINAL_APPENDIX_KEYS = Object\.freeze\(\[(.*?)\]\);', raw, re.S)
    if not main_match or not appendix_match:
        raise RuntimeError('Timing audit FAILED: cannot parse final runtime order')
    main = re.findall(r"'([^']+)'", main_match.group(1))
    explicit_appendix = re.findall(r"'([^']+)'", appendix_match.group(1))
    if len(main) != len(set(main)):
        raise RuntimeError('Timing audit FAILED: duplicate main slide keys')
    return main, explicit_appendix


def authored_appendix_keys(deck_assets: list[str]) -> list[str]:
    keys: list[str] = []
    for asset in deck_assets:
        raw = read(asset)
        for key in re.findall(r'<section[^>]*data-kind=["\']appendix["\'][^>]*data-note-key=["\']([^"\']+)["\']', raw):
            if key not in keys:
                keys.append(key)
    return keys


def parse_speaker_overlay(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    json_match = re.search(r'window\.SPEAKER_SCRIPT\s*=\s*Object\.freeze\((\{.*\})\);\s*$', raw, re.S)
    if json_match:
        try:
            for key, body in json.loads(json_match.group(1)).items():
                result[key] = html.unescape(re.sub(r'\s+', ' ', str(body)).strip())
        except json.JSONDecodeError:
            pass
    for key, body in re.findall(r'\b([A-Za-z0-9_]+)\s*:\s*`(.*?)`\s*,', raw, re.S):
        result[key] = html.unescape(re.sub(r'\s+', ' ', body).strip())
    return result


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text))


def main() -> None:
    order = script_order()
    deck_assets = [name for name in order if name.startswith('deck-') and name != 'deck.js']
    speaker_assets = [name for name in order if re.fullmatch(r'speaker-script-.*\.js', name)]
    final_main, explicit_appendix = parse_final_order(read('deck-narrative-reframe.js'))
    final_appendix = list(dict.fromkeys(authored_appendix_keys(deck_assets) + explicit_appendix))

    speech: dict[str, str] = {}
    for asset in speaker_assets:
        speech.update(parse_speaker_overlay(read(asset)))
    missing = [key for key in final_main if key not in speech or not speech[key].strip()]
    if missing:
        raise RuntimeError('Timing audit FAILED: missing runtime speech entries: ' + ','.join(missing))

    words = sum(word_count(speech[key]) for key in final_main)
    seconds = round(words * 60 / 130)
    print(f'runtime main slides: {len(final_main)}')
    print(f'runtime appendix slides: {len(final_appendix)}')
    print(f'runtime main spoken words: {words}')
    print(f'rehearsal estimate at 130 wpm: {seconds // 60:02d}:{seconds % 60:02d}')
    if not (22 * 60 <= seconds <= 24 * 60):
        raise RuntimeError(f'Timing audit FAILED: runtime script outside 22-24 min: {seconds // 60:02d}:{seconds % 60:02d}')
    print('Timing audit PASS: final runtime main script stays inside the 22-24 minute rehearsal envelope for a 25-minute talk')


if __name__ == '__main__':
    main()
