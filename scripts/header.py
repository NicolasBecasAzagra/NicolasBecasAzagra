#!/usr/bin/env python3
"""Render assets/boot.svg: a terminal boot log that types itself out (CSS only)."""
from html import escape
from pathlib import Path

LINES = [
    ("nicolas@becas:~$ boot --profile", "p"),
    ("[    0.000] education  BSc Computer Engineering, 2026, GPA 8.7/10 ........ ok", "o"),
    ("[    0.112] languages  rust  python  docker  linux  ci ................... ok", "o"),
    ("[    0.231] focus      ml pipelines, data systems, backend ................ ok", "o"),
    ("[    0.340] projects   rabbit  urban-mobility-engine  +4 ................. ok", "o"),
    ("[    0.450] spoken     es native  en c1  fr b1 ............................ ok", "o"),
    ("[    0.560] status     OPEN TO WORK  entry level  open to relocation", "s"),
]
STEP = 0.7
W, H = 900, 290

rows = []
for i, (text, kind) in enumerate(LINES):
    y = 62 + i * 30
    cls = {"p": "prompt", "o": "log", "s": "status"}[kind]
    rows.append(
        f'<text x="30" y="{y}" class="{cls} l" style="animation-delay:{0.4 + i * STEP:.2f}s">{escape(text)}</text>'
    )
cursor_y = 62 + len(LINES) * 30
cursor_delay = 0.4 + len(LINES) * STEP

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Boot log: Nicolas Becas, Computer Engineer, open to work">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:15px;white-space:pre}}
.prompt{{fill:#3fb950;font-weight:700}}
.log{{fill:#9da7b3}}
.status{{fill:#58a6ff;font-weight:700}}
.l{{animation:show .01s backwards}}
.cur{{fill:#3fb950;animation:show .01s backwards,blink 1s step-end infinite}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.l,.cur{{animation:none}}}}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="34" rx="12" fill="#161b22"/>
<rect x="0.5" y="24" width="{W - 1}" height="11" fill="#161b22"/>
<circle cx="22" cy="18" r="5" fill="#ff5f56"/><circle cx="40" cy="18" r="5" fill="#ffbd2e"/><circle cx="58" cy="18" r="5" fill="#27c93f"/>
<text x="{W // 2}" y="22" text-anchor="middle" style="font-size:12px;fill:#7d8590">nicolas-becas — boot.log</text>
{chr(10).join(rows)}
<text x="30" y="{cursor_y}" class="cur" style="animation-delay:{cursor_delay:.2f}s">█</text>
</svg>
"""
out = Path(__file__).resolve().parent.parent / "assets" / "boot.svg"
out.write_text(svg)
print(f"wrote {out}")
