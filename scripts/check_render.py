#!/usr/bin/env python3
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "render-artifacts"
if ARTIFACTS.exists():
    shutil.rmtree(ARTIFACTS)
ARTIFACTS.mkdir()

class DeckParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.kinds: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "section":
            return
        values = dict(attrs)
        if "slide" not in values.get("class", "").split():
            return
        self.kinds.append(values.get("data-kind", "main"))

parser = DeckParser()
parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
main_count = sum(kind != "appendix" for kind in parser.kinds)
appendix_count = sum(kind == "appendix" for kind in parser.kinds)
targets = [f"#{i}" for i in range(1, main_count + 1)] + [
    f"#a{i}" for i in range(1, appendix_count + 1)
]
if not targets:
    print("Render check FAILED: no slides discovered")
    sys.exit(1)

browser = next((name for name in [
    "google-chrome-stable", "google-chrome", "chromium-browser", "chromium"
] if shutil.which(name)), None)
if browser is None:
    print("Render check FAILED: Chrome/Chromium was not found")
    sys.exit(1)

server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8878", "--bind", "127.0.0.1"],
    cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
common = [browser, "--headless=new", "--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox", "--no-first-run"]
required_viewports = [(1920, 1080), (1366, 768)]
stress_viewports = [(1536, 864), (1280, 720)]

try:
    time.sleep(0.6)
    failures: list[str] = []
    for width, height in required_viewports + stress_viewports:
        for target in targets:
            url = f"http://127.0.0.1:8878/?visual-check=1{target}"
            try:
                result = subprocess.run(
                    common + [f"--window-size={width},{height}", "--dump-dom", url],
                    capture_output=True, text=True, timeout=20,
                )
            except subprocess.TimeoutExpired:
                failures.append(f"{width}x{height} {target}: browser timeout")
                continue
            if result.returncode != 0:
                failures.append(f"{width}x{height} {target}: browser exit {result.returncode}")
                continue
            if 'data-visual-check="ok"' not in result.stdout:
                marker = 'data-visual-errors="'
                start = result.stdout.find(marker)
                detail = "visual status missing"
                if start >= 0:
                    start += len(marker)
                    end = result.stdout.find('"', start)
                    detail = result.stdout[start:end]
                failures.append(f"{width}x{height} {target}: {detail}")

    nav_url = "http://127.0.0.1:8878/?nav-check=1#1"
    try:
        nav_result = subprocess.run(common + ["--window-size=1366,768", "--dump-dom", nav_url], capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        failures.append("navigation: browser timeout")
    else:
        if nav_result.returncode != 0 or 'data-nav-check="ok"' not in nav_result.stdout:
            marker = 'data-nav-errors="'
            start = nav_result.stdout.find(marker)
            detail = "navigation status missing"
            if start >= 0:
                start += len(marker)
                end = nav_result.stdout.find('"', start)
                detail = nav_result.stdout[start:end]
            failures.append(f"navigation: {detail}")

    for width, height in required_viewports:
        for target in targets:
            output = ARTIFACTS / f"{width}x{height}-{target[1:]}.png"
            url = f"http://127.0.0.1:8878/{target}"
            try:
                result = subprocess.run(
                    common + [f"--window-size={width},{height}", "--hide-scrollbars", f"--screenshot={output}", url],
                    capture_output=True, text=True, timeout=20,
                )
            except subprocess.TimeoutExpired:
                failures.append(f"screenshot {width}x{height} {target}: timeout")
                continue
            if result.returncode != 0 or not output.exists():
                failures.append(f"screenshot {width}x{height} {target}: failed")

    expected_screenshots = len(targets) * len(required_viewports)
    actual_screenshots = len(list(ARTIFACTS.glob("*.png")))
    if actual_screenshots != expected_screenshots:
        failures.append(f"screenshot coverage: expected {expected_screenshots}, got {actual_screenshots}")

    if failures:
        print("Render check FAILED:")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    geometry_states = len(targets) * (len(required_viewports) + len(stress_viewports))
    print(
        f"Render check OK: {main_count} main + {appendix_count} appendix; "
        f"{expected_screenshots} required screenshots; {geometry_states} geometry states; navigation PASS"
    )
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
