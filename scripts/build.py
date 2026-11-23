#!/usr/bin/env python3
"""Regenerate the profile project cards.

Standard library only. Reads data/projects.json (hand-written copy) and the
public GitHub API. Uses GITHUB_TOKEN when present to avoid rate limits.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime
from html import escape
from pathlib import Path

OWNER = "NicolasBecasAzagra"
ROOT = Path(__file__).resolve().parent.parent
LANG_COLORS = {
    "Rust": "#dea584",
    "Python": "#3572A5",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Swift": "#F05138",
}


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-build"},
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def card_svg(project, language, pushed):
    rows = "".join(
        f'<text x="24" y="{66 + i * 18}" class="d">{escape(line)}</text>'
        for i, line in enumerate(project["lines"])
    )
    color = LANG_COLORS.get(language, "#8b949e")
    meta = escape(language or "n/a")
    if pushed:
        meta += f"  ·  updated {pushed}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="150" viewBox="0 0 400 150" role="img" aria-label="{escape(project['title'])}">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
.t{{font-size:15px;font-weight:700;fill:#e6edf3}}
.d{{font-size:13px;fill:#9da7b3}}
.m{{font-size:11px;fill:#7d8590}}
.g{{font-size:11px;fill:#3fb950}}
</style>
<rect x="0.5" y="0.5" width="399" height="149" rx="10" fill="#0d1117" stroke="#30363d"/>
<rect x="0.5" y="0.5" width="399" height="34" rx="10" fill="#161b22"/>
<rect x="0.5" y="24" width="399" height="11" fill="#161b22"/>
<circle cx="20" cy="18" r="4" fill="#ff5f56"/><circle cx="34" cy="18" r="4" fill="#ffbd2e"/><circle cx="48" cy="18" r="4" fill="#27c93f"/>
<text x="64" y="22" class="g">$ cd {escape(project['title'])}</text>
<text x="376" y="22" class="m" text-anchor="end">{escape(project['tag'])}</text>
{rows}
<circle cx="30" cy="132" r="5" fill="{color}"/>
<text x="42" y="136" class="m">{meta}</text>
</svg>
"""


def build_cards():
    projects = json.loads((ROOT / "data" / "projects.json").read_text())
    for project in projects:
        language, pushed = None, None
        try:
            info = api(f"/repos/{OWNER}/{project['repo']}")
            language = info.get("language")
            pushed = datetime.strptime(info["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %Y")
        except Exception as exc:  # keep the previous card if the API fails
            print(f"warn: {project['repo']}: {exc}", file=sys.stderr)
            if (ROOT / "assets" / "cards" / f"{project['repo']}.svg").exists():
                continue
        out = ROOT / "assets" / "cards" / f"{project['repo']}.svg"
        out.write_text(card_svg(project, language, pushed))


if __name__ == "__main__":
    build_cards()
