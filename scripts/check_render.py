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
presenter_viewports = [(1920, 1080), (1366, 768), (1280, 720)]
presenter_targets = [
    "#1",
    f"#{min(5, main_count)}",
    f"#{min(6, main_count)}",
    f"#{min(10, main_count)}",
    f"#{main_count}",
]
if appendix_count:
    presenter_targets.append(f"#a{min(5, appendix_count)}")
presenter_targets = list(dict.fromkeys(presenter_targets))


def inspect_dom(width: int, height: int, target: str, presenter: bool = False) -> str | None:
    mode = "presenter=1&" if presenter else ""
    url = f"http://127.0.0.1:8878/?{mode}visual-check=1{target}"
    result: subprocess.CompletedProcess[str] | None = None

    # Headless Chromium can occasionally stall on the first process startup on
    # a fresh hosted runner. Retry one isolated process failure; DOM/geometry
    # failures themselves are never retried or hidden.
    for attempt in range(2):
        try:
            result = subprocess.run(
                common + [f"--window-size={width},{height}", "--dump-dom", url],
                capture_output=True, text=True, timeout=20,
            )
        except subprocess.TimeoutExpired:
            if attempt == 0:
                time.sleep(0.5)
                continue
            return "browser timeout after retry"
        if result.returncode != 0:
            if attempt == 0:
                time.sleep(0.5)
                continue
            return f"browser exit {result.returncode} after retry"
        break

    assert result is not None
    if 'data-visual-check="ok"' in result.stdout:
        return None
    marker = 'data-visual-errors="'
    start = result.stdout.find(marker)
    if start < 0:
        return "visual status missing"
    start += len(marker)
    end = result.stdout.find('"', start)
    return result.stdout[start:end]

try:
    time.sleep(0.6)
    failures: list[str] = []
    for width, height in required_viewports + stress_viewports:
        for target in targets:
            detail = inspect_dom(width, height, target)
            if detail:
                failures.append(f"audience {width}x{height} {target}: {detail}")

    for width, height in presenter_viewports:
        for target in presenter_targets:
            detail = inspect_dom(width, height, target, presenter=True)
            if detail:
                failures.append(f"presenter {width}x{height} {target}: {detail}")

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

    for width, height in presenter_viewports:
        for target in presenter_targets:
            output = ARTIFACTS / f"presenter-{width}x{height}-{target[1:]}.png"
            url = f"http://127.0.0.1:8878/?presenter=1{target}"
            try:
                result = subprocess.run(
                    common + [f"--window-size={width},{height}", "--hide-scrollbars", f"--screenshot={output}", url],
                    capture_output=True, text=True, timeout=20,
                )
            except subprocess.TimeoutExpired:
                failures.append(f"presenter screenshot {width}x{height} {target}: timeout")
                continue
            if result.returncode != 0 or not output.exists():
                failures.append(f"presenter screenshot {width}x{height} {target}: failed")

    expected_audience_screenshots = len(targets) * len(required_viewports)
    expected_presenter_screenshots = len(presenter_targets) * len(presenter_viewports)
    expected_screenshots = expected_audience_screenshots + expected_presenter_screenshots
    actual_screenshots = len(list(ARTIFACTS.glob("*.png")))
    if actual_screenshots != expected_screenshots:
        failures.append(f"screenshot coverage: expected {expected_screenshots}, got {actual_screenshots}")

    if failures:
        print("Render check FAILED:")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    audience_geometry = len(targets) * (len(required_viewports) + len(stress_viewports))
    presenter_geometry = len(presenter_targets) * len(presenter_viewports)
    print(
        f"Render check OK: {main_count} main + {appendix_count} appendix; "
        f"{expected_audience_screenshots} audience screenshots + "
        f"{expected_presenter_screenshots} presenter screenshots; "
        f"{audience_geometry + presenter_geometry} geometry states; navigation + presenter sync PASS"
    )
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
