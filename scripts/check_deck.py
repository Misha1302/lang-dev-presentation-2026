#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'rebuild-2026-09-17' / 'delegates-rebuild-deck.html'
SCRIPT = ROOT / 'rebuild-2026-09-17' / 'speaker-script-conference.md'

def read(p: Path) -> str:
    return p.read_text(encoding='utf-8')

def keys(raw: str) -> list[str]:
    return re.findall(r'<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*(?:data-note-key|data-note)="([^"]+)"', raw)

def main() -> None:
    index = read(ROOT / 'index.html')
    assert 'rebuild-2026-09-17/delegates-rebuild-deck.html' in index, 'index must route to the delegates rebuild deck'
    assert TARGET.exists(), 'delegates rebuild deck missing'
    assert SCRIPT.exists(), 'complete speaker script missing'
    raw = read(TARGET)
    slide_keys = keys(raw)
    assert len(slide_keys) >= 21, f'too few slides: {len(slide_keys)}'
    assert len(slide_keys) == len(set(slide_keys)), 'duplicate slide keys'
    main_keys = [k for k in slide_keys if k.startswith('m')]
    support_keys = [k for k in slide_keys if not k.startswith('m')]
    assert len(main_keys) >= 20, f'too few main slides: {len(main_keys)}'
    required = [
      'delegate Mapper(Int x) -> String', 'Extensible Programming, not just a compiler plugin',
      'NominalDelegateType', 'FunctionType([Int], String)', 'Pairwise hardcoding',
      'ITypeSystem', 'ConstructCallable(signature)', 'Assignable(source,target,ctx)',
      'Scenario B', 'Who owns each legality condition?', 'GLOBAL / PROFILE TIME',
      'Resolved compiler configuration', 'Structural composition is not semantic correctness',
      'exact target', 'Producer', 'Fail-closed', 'Facts have a lifecycle',
      'return Foo(42)', 'Prior art', 'research hypothesis', 'UniversalToolchain is evidence'
    ]
    missing = [s for s in required if s not in raw]
    assert not missing, 'missing required narrative moments: ' + ', '.join(missing)
    assert 'zero-cost' not in raw.lower(), 'unsupported zero-cost claim present'
    assert 'works with every type system' not in raw.lower(), 'over-broad type-system claim present'
    validation = read(ROOT / 'rebuild-2026-09-17' / 'VALIDATION.md')
    forbidden = ['rebuild-deck.js', 'speaker-script-canonical.js', 'scripts/validate-rebuild.mjs']
    leaks = [s for s in forbidden if s in validation]
    assert not leaks, 'VALIDATION still claims absent rebuild files: ' + ', '.join(leaks)
    script = read(SCRIPT)
    script_keys = re.findall(r'^##\s+(m\d+|a\d+)\s*$', script, re.M)
    missing_script = [k for k in slide_keys if k not in script_keys]
    assert not missing_script, 'speaker script missing entries: ' + ', '.join(missing_script)
    assert len(script_keys) >= len(slide_keys), 'speaker script unexpectedly shorter than slide set'
    print(f'Delegates rebuild deck PASS: {len(main_keys)} main + {len(support_keys)} support slides; required narrative moments, speaker script and validation record checked')
if __name__ == '__main__':
    main()
