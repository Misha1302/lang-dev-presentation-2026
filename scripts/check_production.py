#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "production-artifacts"
if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

PRODUCTION = "https://misha1302.github.io/lang-dev-presentation-2026/"
MARKER = "semantic-composition-v1"
THESIS = "Make representations concrete"
sha = os.environ.get("GITHUB_SHA", "unknown")

browser = next((name for name in [
    "google-chrome-stable", "google-chrome", "chromium-browser", "chromium"
] if shutil.which(name)), None)
if browser is None:
    print("Production check FAILED: Chrome/Chromium was not found")
    sys.exit(1)

deadline = time.time() + 300
asset_url = f"{PRODUCTION}deck.js?qa={quote(sha)}"
last_error = ""
while time.time() < deadline:
    try:
        with urlopen(asset_url, timeout=15) as response:
            body = response.read().decode("utf-8")
        if MARKER in body:
            break
        last_error = "semantic-composition release marker not present yet"
    except Exception as exc:
        last_error = str(exc)
    time.sleep(5)
else:
    print(f"Production check FAILED: public deck.js did not reach redesign marker: {last_error}")
    sys.exit(1)

common = [
    browser, "--headless=new", "--disable-gpu", "--disable-dev-shm-usage",
    "--no-sandbox", "--no-first-run",
]
failures: list[str] = []

nav_url = f"{PRODUCTION}?nav-check=1&qa={quote(sha)}#1"
try:
    nav_result = subprocess.run(
        common + ["--window-size=1366,768", "--dump-dom", nav_url],
        capture_output=True, text=True, timeout=30,
    )
except subprocess.TimeoutExpired:
    failures.append("production navigation: browser timeout")
else:
    if nav_result.returncode != 0 or 'data-nav-check="ok"' not in nav_result.stdout:
        marker = 'data-nav-errors="'
        start = nav_result.stdout.find(marker)
        detail = "navigation status missing"
        if start >= 0:
            start += len(marker)
            end = nav_result.stdout.find('"', start)
            detail = nav_result.stdout[start:end]
        failures.append(f"production navigation: {detail}")
    if THESIS not in nav_result.stdout:
        failures.append("production thesis: semantic-composition anchor missing from live DOM")
    if 'data-deck-qa-contract="semantic-composition-v1"' not in nav_result.stdout:
        failures.append("production marker: DOM contract is not semantic-composition-v1")

representative = [
    "#1", "#3", "#5", "#7", "#10", "#13", "#16", "#19", "#21", "#23", "#27",
    "#a1", "#a3", "#a4", "#a5",
]
for target in representative:
    url = f"{PRODUCTION}?visual-check=1&qa={quote(sha)}{target}"
    try:
        result = subprocess.run(
            common + ["--window-size=1366,768", "--dump-dom", url],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        failures.append(f"production {target}: browser timeout")
        continue
    if result.returncode != 0 or 'data-visual-check="ok"' not in result.stdout:
        marker = 'data-visual-errors="'
        start = result.stdout.find(marker)
        detail = "visual status missing"
        if start >= 0:
            start += len(marker)
            end = result.stdout.find('"', start)
            detail = result.stdout[start:end]
        failures.append(f"production {target}: {detail}")
        continue

    output = ARTIFACTS / f"1366x768-{target[1:]}.png"
    shot_url = f"{PRODUCTION}?qa={quote(sha)}{target}"
    try:
        shot = subprocess.run(
            common + [
                "--window-size=1366,768", "--hide-scrollbars",
                f"--screenshot={output}", shot_url,
            ],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        failures.append(f"production screenshot {target}: timeout")
        continue
    if shot.returncode != 0 or not output.exists():
        failures.append(f"production screenshot {target}: failed")

if failures:
    print("Production check FAILED:")
    for failure in failures:
        print(f" - {failure}")
    sys.exit(1)

print(
    f"Production check OK: marker={MARKER}; thesis present; "
    f"navigation PASS; {len(representative)} representative states PASS"
)
