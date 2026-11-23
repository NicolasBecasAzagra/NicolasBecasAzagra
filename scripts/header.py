#!/usr/bin/env python3
"""Render the terminal boot-log headers (CSS only, no JS).

assets/boot.svg         wide, for desktop
assets/boot-mobile.svg  narrow, so the text stays readable on a phone
"""
from html import escape
from pathlib import Path

WIDE = {
    "name": "boot.svg",
    "w": 900,
    "h": 290,
    "font": 16,
    "lines": [
        ("nicolas@becas:~$ boot --profile", "p"),
        ("[    0.000] education  BSc Computer Engineering, 2026, GPA 8.7/10 ........ ok", "o"),
        ("[    0.112] languages  rust  python  docker  linux  ci ................... ok", "o"),
        ("[    0.231] focus      ml pipelines, data systems, backend ................ ok", "o"),
        ("[    0.340] projects   rabbit  urban-mobility-engine  +4 ................. ok", "o"),
        ("[    0.450] spoken     es native  en c1  fr b1 ............................ ok", "o"),
        ("[    0.560] status     OPEN TO WORK  entry level  open to relocation", "s"),
    ],
}
NARROW = {
    "name": "boot-mobile.svg",
    "w": 460,
    "h": 250,
    "font": 15,
    "lines": [
        ("nicolas@becas:~$ boot --profile", "p"),
        ("[ 0.000] education  BSc Computer Eng. 2026", "o"),
        ("[ 0.112] stack      rust python docker linux", "o"),
        ("[ 0.231] focus      ML, data systems, backend", "o"),
        ("[ 0.340] spoken     es native, en c1, fr b1", "o"),
        ("[ 0.450] status     OPEN TO WORK", "s"),
    ],
}
STEP = 0.7


def render(cfg):
    w, h, font = cfg["w"], cfg["h"], cfg["font"]
    lines = cfg["lines"]
    rows = []
    for i, (text, kind) in enumerate(lines):
        y = 66 + i * 30
        cls = {"p": "prompt", "o": "log", "s": "status"}[kind]
        rows.append(
            f'<text x="30" y="{y}" class="{cls} l" style="animation-delay:{0.4 + i * STEP:.2f}s">{escape(text)}</text>'
        )
    cursor_y = 66 + len(lines) * 30
    cursor_delay = 0.4 + len(lines) * STEP
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Boot log: Nicolas Becas, Computer Engineer, open to work">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{font}px;white-space:pre}}
.prompt{{fill:#3fb950;font-weight:700}}
.log{{fill:#9da7b3}}
.status{{fill:#58a6ff;font-weight:700}}
.l{{animation:show .01s backwards}}
.cur{{fill:#3fb950;animation:show .01s backwards,blink 1s step-end infinite}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.l,.cur{{animation:none}}}}
</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="34" rx="12" fill="#161b22"/>
<rect x="0.5" y="24" width="{w - 1}" height="11" fill="#161b22"/>
<circle cx="22" cy="18" r="5" fill="#ff5f56"/><circle cx="40" cy="18" r="5" fill="#ffbd2e"/><circle cx="58" cy="18" r="5" fill="#27c93f"/>
<text x="{w // 2}" y="22" text-anchor="middle" style="font-size:12px;fill:#7d8590">nicolas-becas — boot.log</text>
{chr(10).join(rows)}
<text x="30" y="{cursor_y}" class="cur" style="animation-delay:{cursor_delay:.2f}s">█</text>
</svg>
"""
    out = Path(__file__).resolve().parent.parent / "assets" / cfg["name"]
    out.write_text(svg)
    print(f"wrote {out}")


if __name__ == "__main__":
    render(WIDE)
    render(NARROW)
