#!/usr/bin/env python3
"""Render assets/boot.svg: a terminal boot log that types itself out (CSS only).

One wide canvas with large type and short lines: it fills the page on desktop
and the text is still readable when GitHub scales it down on a phone.
"""
from html import escape
from pathlib import Path

W, H = 900, 440
FONT = 26
TOP, STEP_Y = 112, 50
STEP = 0.7
LINES = [
    ("nicolas@becas:~$ boot --profile", "p"),
    ("[ 0.000] education  BSc Computer Eng. 2026, GPA 8.7", "o"),
    ("[ 0.112] stack      rust python docker linux", "o"),
    ("[ 0.231] focus      ML pipelines, data, backend", "o"),
    ("[ 0.340] spoken     es native, en c1, fr b1", "o"),
    ("[ 0.450] status     OPEN TO WORK", "s"),
]

rows = []
for i, (text, kind) in enumerate(LINES):
    y = TOP + i * STEP_Y
    cls = {"p": "prompt", "o": "log", "s": "status"}[kind]
    rows.append(
        f'<text x="40" y="{y}" class="{cls} l" style="animation-delay:{0.4 + i * STEP:.2f}s">{escape(text)}</text>'
    )
cursor_y = TOP + len(LINES) * STEP_Y
cursor_delay = 0.4 + len(LINES) * STEP

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Boot log: Nicolas Becas, Computer Engineer, open to work">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:{FONT}px;white-space:pre}}
.prompt{{fill:#3fb950;font-weight:700}}
.log{{fill:#9da7b3}}
.status{{fill:#58a6ff;font-weight:700}}
.l{{animation:show .01s backwards}}
.cur{{fill:#3fb950;animation:show .01s backwards,blink 1s step-end infinite}}
@keyframes show{{from{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.l,.cur{{animation:none}}}}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="#0d1117" stroke="#30363d"/>
<rect x="0.5" y="0.5" width="{W - 1}" height="46" rx="16" fill="#161b22"/>
<rect x="0.5" y="30" width="{W - 1}" height="17" fill="#161b22"/>
<circle cx="30" cy="24" r="7" fill="#ff5f56"/><circle cx="54" cy="24" r="7" fill="#ffbd2e"/><circle cx="78" cy="24" r="7" fill="#27c93f"/>
<text x="{W // 2}" y="30" text-anchor="middle" style="font-size:16px;fill:#7d8590">nicolas-becas — boot.log</text>
{chr(10).join(rows)}
<text x="40" y="{cursor_y}" class="cur" style="animation-delay:{cursor_delay:.2f}s">█</text>
</svg>
"""
out = Path(__file__).resolve().parent.parent / "assets" / "boot.svg"
out.write_text(svg)
print(f"wrote {out}")
