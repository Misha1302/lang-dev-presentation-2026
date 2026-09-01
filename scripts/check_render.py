#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "render-artifacts"
ARTIFACTS.mkdir(exist_ok=True)

browser = next((name for name in [
    "google-chrome-stable", "google-chrome", "chromium-browser", "chromium"
] if shutil.which(name)), None
if browser is None:
    print("Render check FAILED: Chrome/Chromium was not found")
    sys.exit(1)

server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8878", "--bind", "127.0.0.1"],
    cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
common = [browser, "--headless=new", "--disable-gpu", "--disable-dev-shm-usage", "--no-sandbox", "--no-first-run"]

try:
    time.sleep(0.6)
    viewports = [(1920, 1080), (1366, 768)]
    targets = [f"#{i}" for i in range(1, 17)] + [f"#a{i}" for i in range(1, 9)]
    failures: list[str] = []
    for width, height in viewports:
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

    for width, height in viewports:
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

    if failures:
        print("Render check FAILED:")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print(f"Render check OK: {len(targets) * len(viewports)} slide/viewport states; {len(targets) * len(viewports)} screenshots")
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
