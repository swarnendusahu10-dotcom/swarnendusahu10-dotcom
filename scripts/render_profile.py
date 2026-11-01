"""Render Swarnendu Sahu's profile SVGs from data/*.json.

Original cyberpunk dark terminal renderer with animated neon gradients.
The portrait step renders a high-contrast ASCII cat face in terminal matrix styling.
Run: python scripts/render_profile.py
"""
import json
import math
import os
from datetime import datetime, timezone
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

FONT = ("ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, "
        "'Liberation Mono', monospace")
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
FG = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
CYAN = "#58d5e8"
PURPLE = "#bc8cff"
ORANGE = "#ffa657"
PINK = "#ff7b9c"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]


def esc(s):
    return escape(str(s), quote=True)


def load(name, default=None):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_svg(name, svg):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {name} ({len(svg) // 1024} KB)")


def window(width, height, title, body, extra_defs=""):
    """Terminal window chrome shared by every card."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="{FONT}">
<defs>{extra_defs}</defs>
<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>
<path d="M0.5 32 V10.5 a10 10 0 0 1 10 -10 H{width - 10.5} a10 10 0 0 1 10 10 V32 Z" fill="{PANEL}"/>
<line x1="0.5" y1="32" x2="{width - 0.5}" y2="32" stroke="{BORDER}"/>
<circle cx="18" cy="16" r="5.5" fill="#ff5f56"/><circle cx="36" cy="16" r="5.5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5.5" fill="#27c93f"/>
<text x="{width / 2}" y="20.5" fill="{MUTED}" font-size="12" text-anchor="middle">{esc(title)}</text>
{body}
</svg>
"""


# ---------------------------------------------------------------- header
NAME = "Swarnendu Sahu"
USERNAME = "swarnendusahu10-dotcom"
PROMPT_USER = "swarnendu"
PROMPT_HOST = "github"
ROLES = [
    "Full-Stack Developer & AI Enthusiast",
    "Open Source Contributor @ Rocket.Chat",
    "Building AI-DETECTION & FoodDelivery AI",
    "React • Node.js • Python • Machine Learning",
]
TAGLINE = "Bhubaneswar, IN • Full-Stack Systems and AI"


def header_svg():
    W, H = 860, 210
    char_w = 9.6
    slot, total_t = 5.0, 5.0 * len(ROLES)
    roles = []
    for k, role in enumerate(ROLES):
        w = len(role) * char_w
        t0 = k * slot
        typed, held, gone = t0 + len(role) * 0.055, t0 + slot - 1.1, t0 + slot - 0.35
        stops = sorted({0.0, t0 / total_t, typed / total_t, held / total_t,
                        gone / total_t, 1.0})
        keys = ";".join(f"{v:.4f}" for v in stops)
        width_at = {0.0: 0, t0 / total_t: 0, typed / total_t: w,
                    held / total_t: w, gone / total_t: 0, 1.0: 0}
        widths = ";".join(f"{width_at[v]:.1f}" for v in stops)
        xs = ";".join(f"{60 + width_at[v]:.1f}" for v in stops)
        roles.append(f"""<clipPath id="r{k}"><rect x="60" y="132" width="0" height="22">
<animate attributeName="width" values="{widths}" keyTimes="{keys}" dur="{total_t}s" repeatCount="indefinite"/></rect></clipPath>
<text x="60" y="148" font-size="16" fill="{FG}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" clip-path="url(#r{k})">{esc(role)}</text>
<rect x="60" y="134" width="9" height="18" fill="{GREEN}" opacity="0">
<animate attributeName="x" values="{xs}" keyTimes="{keys}" dur="{total_t}s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;{t0 / total_t:.4f};{gone / total_t:.4f};{min(gone / total_t + 0.0001, 0.9999):.4f};1" dur="{total_t}s" repeatCount="indefinite" calcMode="discrete"/>
</rect>""")
    prompt = f"{PROMPT_USER}@{PROMPT_HOST}:~$"
    cmd = "./hello.sh"
    cmd_x = 40 + len(prompt) * 8.4 + 8
    defs = f"""
<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GREEN}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;-1 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#ffffff" opacity="0.05"/></pattern>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{GREEN}" stop-opacity="0"/><stop offset="1" stop-color="{GREEN}" stop-opacity="0.08"/></linearGradient>
<clipPath id="inner"><rect x="1" y="33" width="{W - 2}" height="{H - 34}" rx="9"/></clipPath>
<clipPath id="cmdClip"><rect x="{cmd_x}" y="42" width="0" height="22"><animate attributeName="width" from="0" to="{len(cmd) * 8.4 + 6}" begin="0.3s" dur="0.55s" fill="freeze"/></rect></clipPath>
<style>
  .blink {{ animation: bl 1s steps(1) infinite; }}
  @keyframes bl {{ 50% {{ opacity: 0; }} }}
</style>
"""
    body = f"""
<g clip-path="url(#inner)">
  <rect x="0" y="33" width="{W}" height="{H - 33}" fill="url(#dots)"/>
  <rect x="0" y="33" width="{W}" height="40" fill="url(#scan)">
    <animate attributeName="y" from="33" to="{H - 40}" dur="4s" repeatCount="indefinite"/>
  </rect>
</g>
<text x="40" y="58" font-size="14" fill="{MUTED}"><tspan fill="{GREEN}">{prompt}</tspan></text>
<text x="{cmd_x}" y="58" font-size="14" font-weight="700" fill="{FG}" clip-path="url(#cmdClip)">{cmd}</text>
<text x="40" y="112" font-size="34" font-weight="900" letter-spacing="3" fill="url(#nameGrad)" filter="url(#glow)">{esc(NAME).upper()}</text>
<text x="40" y="148" font-size="16" fill="{MUTED}">&gt;</text>
{''.join(roles)}
<text x="40" y="184" font-size="12" fill="{MUTED}">{esc(TAGLINE)}</text>
"""
    write_svg("header.svg", window(W, H, f"~/{PROMPT_USER}: ash", body, defs))


# ---------------------------------------------------------------- cat portrait
def portrait_svg():
    src_candidates = [
        os.path.join(ROOT, "work", "cat_source.jpg"),
        os.path.join(ROOT, "work", "cat_source.png"),
        os.path.join(ROOT, "work", "source-prepped.png"),
    ]
    src = None
    for c in src_candidates:
        if os.path.exists(c):
            src = c
            break

    W, H = 370, 420
    ramp = " .`:-=+*cs#%@"
    cols, font, lh = 92, 6.2, 7.0
    cw = font * 0.6

    if src and os.path.exists(src):
        import numpy as np
        from PIL import Image, ImageOps
        img = Image.open(src).convert("L")
        img = ImageOps.autocontrast(img)
        w, h = img.size
        # crop slightly if tall or wide to focus on cat face
        if w > h:
            d = (w - h) // 2
            img = img.crop((d, 0, w - d, h))
        elif h > w:
            d = (h - w) // 2
            img = img.crop((0, d // 2, w, h - d // 2))

        rows = int(cols * cw / lh * img.height / img.width)
        max_rows = int((H - 52) / lh)
        if rows > max_rows:
            keep = int(img.height * max_rows / rows)
            img, rows = img.crop((0, 0, img.width, keep)), max_rows
        a = np.asarray(img.resize((cols, rows), Image.LANCZOS), dtype=np.float32) / 255.0
        nz = a[a > 0.04]
        lo, hi = np.percentile(nz, [5, 99]) if nz.size else (0, 1)
        a = np.where(a > 0.04, np.clip((a - lo) / (hi - lo), 0, 1) ** 0.85, 0)
        lines = ["".join(ramp[int(v * (len(ramp) - 1))] for v in a[r]) for r in range(rows)]
    else:
        # Fallback procedural cat face
        rows = 48
        lines = [" " * cols for _ in range(rows)]

    grid_w = cols * cw
    x0 = (W - grid_w) / 2
    y0 = 32 + (H - 32 - rows * lh) / 2 + lh * 0.8
    out = []
    for r in range(rows):
        line = lines[r]
        if not line.strip():
            continue
        y = y0 + r * lh
        begin, dur = 0.3 + r * 0.045, 0.55
        text = esc(line).replace(" ", "\u00a0")
        out.append(
            f'<clipPath id="c{r}"><rect x="{x0:.1f}" y="{y - lh:.1f}" width="0" height="{lh + 1}">'
            f'<animate attributeName="width" from="0" to="{grid_w:.1f}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x0:.1f}" y="{y:.1f}" textLength="{grid_w:.1f}" lengthAdjust="spacing" clip-path="url(#c{r})">{text}</text>'
            f'<rect x="{x0:.1f}" y="{y - lh + 1:.1f}" width="{cw:.1f}" height="{lh - 1}" fill="{GREEN}" opacity="0">'
            f'<set attributeName="opacity" to="1" begin="{begin:.2f}s"/>'
            f'<animate attributeName="x" from="{x0:.1f}" to="{x0 + grid_w:.1f}" begin="{begin:.2f}s" dur="{dur}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0" begin="{begin + dur:.2f}s"/></rect>')

    shimmer = 0.3 + rows * 0.045 + 0.6
    defs = f"""
<linearGradient id="ink" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
  <stop offset="0" stop-color="{GREEN}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{W} {H};0 0" begin="{shimmer:.2f}s" dur="10s" repeatCount="indefinite"/>
</linearGradient>"""
    body = f"""
<g fill="url(#ink)" font-size="{font}">{''.join(out)}</g>"""
    write_svg("ascii-portrait.svg", window(W, H, "cat.txt", body, defs))


# ---------------------------------------------------------------- info card
LANG_COLORS = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
    "CSS": "#663399", "HTML": "#e34c26", "Go": "#00ADD8", "Java": "#b07219",
    "Shell": "#89e051", "Dockerfile": "#384d54", "C++": "#f34b7d",
    "C#": "#178600", "Rust": "#dea584", "SCSS": "#c6538c", "Dart": "#00B4AB",
    "C": "#555555", "Kotlin": "#A97BFF", "Swift": "#F05138", "HCL": "#844FBA",
    "Jupyter Notebook": "#DA5B0B", "CMake": "#DA3434",
}
KEY_COLORS = [GREEN, CYAN, PURPLE, ORANGE, PINK]


def _uptime(created_iso):
    if not created_iso:
        return "-"
    c = datetime.fromisoformat(created_iso.replace("Z", "+00:00"))
    months = (datetime.now(timezone.utc) - c).days * 12 // 365
    y, m = divmod(months, 12)
    parts = ([f"{y} yr" + ("s" if y != 1 else "")] if y else [])
    if m or not y:
        parts.append(f"{m} mo" + ("s" if m != 1 else ""))
    return ", ".join(parts)


def info_card_svg():
    W, H = 490, 420
    prof = load("profile.json", {})
    gh = load("github.json", {})
    st = load("contributions.json", {}).get("stats", {})
    langs = prof.get("languages", {})
    top_langs = [l for l in langs if l != "Jupyter Notebook"][:3] or list(langs)[:3]

    rows = [
        ("Role", "Full-Stack Dev • AI Enthusiast"),
        ("Now", "Building AI-DETECTION & EmbeddedChat"),
        ("OSS", "Rocket.Chat (EmbeddedChat)"),
        ("Uptime", f"{_uptime(prof.get('created_at'))} on GitHub"
         if prof.get("created_at") else "-"),
        ("Langs", " • ".join(top_langs) or "JavaScript • Python"),
        ("Backend", "Python • Node.js • Express • REST APIs"),
        ("Frontend", "React • Next.js • Vite • Tailwind"),
        ("Projects", "AI-DETECTION • FoodDeliveryPrediction"),
        ("PRs", f"{gh.get('prs_merged', 2)} merged • {gh.get('prs_opened', 14)} opened"),
        ("Reviews", f"{gh.get('prs_reviewed', 0)} PRs reviewed • {gh.get('issues_opened', 0)} issues"),
        ("Repos", f"{prof.get('public_repos', 8)} public • {prof.get('stars', 0)} stars"),
        ("Streak", f"{st.get('current_streak', 1)}d current • {st.get('longest_streak', 7)}d best"),
    ]
    x, y = 24, 60
    head = f"{PROMPT_USER}@{PROMPT_HOST}"
    lines = [
        f'<g class="ln" style="animation-delay:0.50s"><text x="{x}" y="{y}" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> neofetch</text></g>',
        f'<g class="ln" style="animation-delay:0.59s"><text x="{x}" y="{y + 28}" font-size="15" font-weight="700"><tspan fill="{GREEN}">{PROMPT_USER}</tspan><tspan fill="{FG}">@{PROMPT_HOST}</tspan></text></g>',
        f'<g class="ln" style="animation-delay:0.68s"><line x1="{x}" y1="{y + 36}" x2="{x + len(head) * 9}" y2="{y + 36}" stroke="{BORDER}" stroke-dasharray="2 2"/></g>',
    ]
    ry = y + 54
    for k, (key, val) in enumerate(rows):
        color = KEY_COLORS[k % len(KEY_COLORS)]
        delay = 0.77 + k * 0.08
        lines.append(
            f'<g class="ln" style="animation-delay:{delay:.2f}s">'
            f'<text x="{x}" y="{ry}" font-size="11.5" fill="{color}" font-weight="700">{esc(key)}</text>'
            f'<text x="{x + 82}" y="{ry}" font-size="11.5" fill="{FG}">{esc(val)}</text></g>')
        ry += 19

    # Language breakdown bar
    bar_y = H - 38
    # filter out notebook or normalize
    chart_langs = [(k, v) for k, v in langs.items() if k != "Jupyter Notebook"]
    if not chart_langs:
        chart_langs = list(langs.items())
    total_bytes = sum(v for _, v in chart_langs[:5]) or 1
    bar_w = W - 2 * x
    bx, segs, leg = x, [], []
    for k, (lang, count) in enumerate(chart_langs[:4]):
        w = max(4, bar_w * count / total_bytes)
        c = LANG_COLORS.get(lang, GREEN)
        pct = 100 * count / total_bytes
        segs.append(f'<rect x="{bx:.1f}" y="{bar_y}" width="{w:.1f}" height="6" fill="{c}"/>')
        leg.append(f'<circle cx="{bx + 4:.1f}" cy="{bar_y + 18}" r="3.5" fill="{c}"/><text x="{bx + 11:.1f}" y="{bar_y + 21}" font-size="10" fill="{MUTED}">{esc(lang)} <tspan fill="{FG}">{pct:.1f}%</tspan></text>')
        bx += w + 2

    defs = f"""
<style>
  .ln {{ opacity: 0; animation: fin 0.4s ease-out forwards; }}
  @keyframes fin {{ from {{ opacity: 0; transform: translateY(2px); }} to {{ opacity: 1; transform: translateY(0); }} }}
</style>
<clipPath id="barClip"><rect x="{x}" y="{bar_y}" width="{bar_w}" height="6" rx="3"/></clipPath>
"""
    body = "\n".join(lines) + f'<g clip-path="url(#barClip)">{"".join(segs)}</g>' + "".join(leg)
    write_svg("info-card.svg", window(W, H, f"{PROMPT_USER}@{PROMPT_HOST}: ~", body, defs))


# ---------------------------------------------------------------- globe
HOME = ("Bhubaneswar", 20.2961, 85.8245)
ARCS = [
    ("Rocket.Chat", 40.71, -74.00),
    ("Open Source", 37.77, -122.41),
    ("Python OSS", 51.50, -0.12),
    ("Community", 48.14, 11.58),
]
GLOBE_R = 132
GLOBE_C = (215, 205)
GLOBE_TILT = math.radians(22)
GLOBE_PERIOD = 36
GLOBE_SAMPLES = 36
ARC_COLORS = [CYAN, PURPLE, ORANGE, PINK, "#79c0ff"]


def _slerp_point(p, q, t):
    def vec(lat, lon):
        la, lo = math.radians(lat), math.radians(lon)
        return (math.cos(la) * math.cos(lo), math.cos(la) * math.sin(lo), math.sin(la))
    v1, v2 = vec(*p), vec(*q)
    om = math.acos(max(-1.0, min(1.0, sum(x * y for x, y in zip(v1, v2)))))
    if om < 1e-6:
        return p
    s1 = math.sin((1 - t) * om) / math.sin(om)
    s2 = math.sin(t * om) / math.sin(om)
    v = tuple(s1 * x + s2 * y for x, y in zip(v1, v2))
    return (math.degrees(math.asin(max(-1.0, min(1.0, v[2])))),
            math.degrees(math.atan2(v[1], v[0])))


def globe_svg():
    W, H = 430, 400
    CX, CY, R = GLOBE_C[0], GLOBE_C[1], GLOBE_R
    lp = os.path.join(ROOT, "scripts", "land_points.json")
    land = [tuple(p) for p in json.load(open(lp))] if os.path.exists(lp) else []
    rings = {}
    for lat, lon in land:
        rings.setdefault(lat, []).append(lon)
    keyframes = []

    def ring(lat, lons, color, r, alt=1.0, back=0.0, anim=""):
        phi = math.radians(lat)
        a = alt * R * math.cos(phi)
        b = a * math.sin(GLOBE_TILT)
        ty = CY - alt * R * math.sin(phi) * math.cos(GLOBE_TILT)
        c0 = -math.tan(phi) * math.tan(GLOBE_TILT)
        if alt > 1:
            c0 -= (alt - 1) * 0.6
        k = len(keyframes)
        steps = " ".join(
            f"{100.0 * i / GLOBE_SAMPLES:.2f}%{{transform:translate({CX + a * math.sin(2 * math.pi * i / GLOBE_SAMPLES):.1f}px,{ty + b * math.cos(2 * math.pi * i / GLOBE_SAMPLES):.1f}px)}}"
            for i in range(GLOBE_SAMPLES + 1))
        keyframes.append(f"@keyframes k{k}{{{steps}}}.k{k}{{animation:k{k} {GLOBE_PERIOD}s linear infinite}}")
        dots = "".join(
            f'<circle r="{r}" class="k{k}" style="animation-delay:-{((lon - HOME[2]) % 360) / 360 * GLOBE_PERIOD:.2f}s">{anim}</circle>'
            for lon in lons)
        out = []
        if c0 < 1:
            out.append(f'<clipPath id="f{k}"><rect x="0" y="{ty + b * max(c0, -1.5):.2f}" width="{W}" height="{H}"/></clipPath>'
                       f'<g clip-path="url(#f{k})" fill="{color}">{dots}</g>')
        if back > 0 and c0 > -1:
            out.append(f'<clipPath id="b{k}"><rect x="0" y="0" width="{W}" height="{ty + b * min(c0, 1.5):.2f}"/></clipPath>'
                       f'<g clip-path="url(#b{k})" fill="{color}" opacity="{back}">{dots}</g>')
        return "".join(out)

    body_rings = [ring(lat, lons, GREEN, 1.25, back=0.18)
                  for lat, lons in sorted(rings.items())]

    # Home pulse
    body_rings.append(ring(HOME[1], [HOME[2]], PINK, 4.0, anim='<animate attributeName="r" values="3;5.5;3" dur="2s" repeatCount="indefinite"/>'))
    body_rings.append(ring(HOME[1], [HOME[2]], "#ffffff", 1.8))

    # Arcs
    for idx, (label, dlat, dlon) in enumerate(ARCS):
        c = ARC_COLORS[idx % len(ARC_COLORS)]
        pts = [_slerp_point(HOME[1:], (dlat, dlon), t / 14) for t in range(1, 14)]
        for t, (plat, plon) in enumerate(pts, 1):
            body_rings.append(ring(plat, [plon], c, 1.5, alt=1.0 + 0.22 * math.sin(math.pi * t / 14), back=0.08))
        body_rings.append(ring(dlat, [dlon], c, 2.5, back=0.12))

    defs = f"""
<radialGradient id="atmo" cx="50%" cy="50%" r="50%">
  <stop offset="70%" stop-color="{GREEN}" stop-opacity="0"/>
  <stop offset="98%" stop-color="{GREEN}" stop-opacity="0.18"/>
  <stop offset="100%" stop-color="{CYAN}" stop-opacity="0.45"/>
</radialGradient>
<radialGradient id="depth" cx="35%" cy="30%" r="70%">
  <stop offset="0%" stop-color="#16231c" stop-opacity="0.8"/>
  <stop offset="70%" stop-color="#0a120e" stop-opacity="0.95"/>
  <stop offset="100%" stop-color="#050807"/>
</radialGradient>
<style>
  {' '.join(keyframes)}
</style>
"""
    legend = [f'<circle cx="28" cy="{H - 22}" r="3" fill="{PINK}"/><text x="36" y="{H - 19}" font-size="10" fill="{MUTED}">{HOME[0]}</text>']
    lx = 110
    for idx, (label, _, _) in enumerate(ARCS[:3]):
        c = ARC_COLORS[idx % len(ARC_COLORS)]
        legend.append(f'<circle cx="{lx}" cy="{H - 22}" r="3" fill="{c}"/><text x="{lx + 8}" y="{H - 19}" font-size="10" fill="{MUTED}">{esc(label)}</text>')
        lx += len(label) * 6.2 + 20

    body = f"""
<circle cx="{CX}" cy="{CY}" r="{R}" fill="url(#depth)" stroke="{BORDER}"/>
<circle cx="{CX}" cy="{CY}" r="{R + 4}" fill="url(#atmo)"/>
{''.join(body_rings)}
<text x="24" y="58" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./open-source --from '{HOME[0].lower()}'</text>
{''.join(legend)}
"""
    write_svg("globe.svg", window(W, H, "globe.sh", body, defs))


# ---------------------------------------------------------------- 3D tech sphere
TECH = {
    "languages": ["Python", "JavaScript", "TypeScript", "HTML5", "CSS3", "SQL"],
    "backend": ["Node.js", "Express", "FastAPI", "Flask", "REST APIs"],
    "frontend": ["React", "Next.js", "Tailwind CSS", "Vite", "Redux"],
    "ai_ml": ["PyTorch", "XGBoost", "Scikit-Learn", "NumPy", "Pandas"],
    "tools": ["Git", "GitHub", "Docker", "Linux", "VS Code"],
}
TECH_COLORS = [CYAN, GREEN, ORANGE, PURPLE, PINK]


def tech_sphere_svg():
    W, H = 430, 400
    CX, CY, R = 215, 212, 128
    TILT = math.radians(18)
    PERIOD, SAMPLES = 30, 60

    def project(v, theta):
        x, y, z = v
        x, z = x * math.cos(theta) + z * math.sin(theta), \
            -x * math.sin(theta) + z * math.cos(theta)
        y, z = y * math.cos(TILT) - z * math.sin(TILT), \
            y * math.sin(TILT) + z * math.cos(TILT)
        return CX + R * x, CY - R * y, z

    labels = [(t, cat) for cat, items in TECH.items() for t in items]
    color = {cat: TECH_COLORS[k % len(TECH_COLORS)]
             for k, cat in enumerate(TECH)}
    N = len(labels)
    inc = math.pi * (3 - math.sqrt(5))
    pts = []
    for k in range(N):
        y = 1 - (k / float(N - 1)) * 2
        rad = math.sqrt(max(0.0, 1 - y * y))
        phi = k * inc
        pts.append((rad * math.cos(phi), y, rad * math.sin(phi)))

    items_svg = []
    for (t, cat), p in zip(labels, pts):
        col = color[cat]
        key_id = f"s{len(items_svg)}"
        kf = []
        for i in range(SAMPLES + 1):
            theta = 2 * math.pi * i / SAMPLES
            sx, sy, sz = project(p, theta)
            scale = 0.55 + 0.45 * (sz + 1) / 2
            op = 0.18 + 0.82 * (sz + 1) / 2
            kf.append(
                f"{100 * i / SAMPLES:.1f}%{{transform:translate({sx:.1f}px,{sy:.1f}px) scale({scale:.2f});opacity:{op:.2f};}}")
        items_svg.append(f"""
<g class="{key_id}">
  <text text-anchor="middle" dominant-baseline="middle" font-size="12" font-weight="700" fill="{col}">{esc(t)}</text>
</g>
<style>
  .{key_id} {{ animation: {key_id} {PERIOD}s linear infinite; }}
  @keyframes {key_id} {{ {' '.join(kf)} }}
</style>
""")

    legend_items = []
    lx = 24
    for k, cat in enumerate(TECH):
        col = TECH_COLORS[k % len(TECH_COLORS)]
        legend_items.append(f'<circle cx="{lx}" cy="{H - 22}" r="3" fill="{col}"/><text x="{lx + 8}" y="{H - 19}" font-size="10" fill="{MUTED}">{esc(cat)}</text>')
        lx += len(cat) * 6.5 + 18

    body = f"""
<circle cx="{CX}" cy="{CY}" r="{R}" fill="none" stroke="{BORDER}" stroke-dasharray="2 3"/>
{''.join(items_svg)}
<text x="24" y="58" font-size="12" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ls ~/stack --3d</text>
{''.join(legend_items)}
"""
    write_svg("tech-sphere.svg", window(W, H, "stack.sh", body))


# ---------------------------------------------------------------- skyline
def _weeks(days):
    """Group contribution days into Sunday-start weeks."""
    from datetime import date, timedelta
    if not days:
        return []
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    by_date = {d["date"]: d["count"] for d in days}
    weeks, cur = [], start
    last = date.fromisoformat(days[-1]["date"])
    while cur <= last:
        total = sum(by_date.get((cur + timedelta(days=i)).isoformat(), 0)
                    for i in range(7))
        weeks.append((cur, total))
        cur += timedelta(days=7)
    return weeks


def skyline_svg():
    W, H = 860, 470
    IX, IY = 11.2, 4.8
    JX, JY = -11.2, 6.0
    HMAX = 105
    INSET = 0.1
    TOPS = ["#1f2630", "#1a6b3c", "#1f9a4b", "#33c25a", "#5ae27a", "#9dffbe"]
    LEFT = ["#171d25", "#0f4a29", "#137034", "#22903f", "#36ad54", "#6fe597"]
    RIGHT = ["#12171e", "#0a3520", "#0d5226", "#196c30", "#26843f", "#4cc173"]
    from datetime import date, timedelta
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    if not days:
        return
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1
    peak = max(1, max(d["count"] for d in days))
    ox = (W - (cols + 7) * IX) / 2 + 7 * IX - 10
    oy = 92

    def P(i, j, h=0.0):
        return ox + i * IX + j * JX, oy + i * IY + j * JY - h

    def poly(pts, fill):
        return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}"/>'

    cells = []
    for d in days:
        off = (date.fromisoformat(d["date"]) - start).days
        cells.append((off // 7, off % 7, d))
    cells.sort(key=lambda t: (t[0] + t[1], t[1]))
    out, best_top = [], None
    a, b = INSET, 1 - INSET
    for i, j, d in cells:
        lvl = d["level"]
        if d["count"] == peak:
            lvl = 5
        h = 0 if d["count"] == 0 else 3 + math.sqrt(d["count"] / peak) * HMAX
        top = [P(i + a, j + a, h), P(i + b, j + a, h),
               P(i + b, j + b, h), P(i + a, j + b, h)]
        delay = 0.4 + i * 0.035 + j * 0.03
        tip = f"<title>{d['count']} contributions on {d['date']}</title>"
        if h == 0:
            out.append(f'<g class="t" style="animation-delay:{delay:.2f}s">{poly(top, TOPS[0])}{tip}</g>')
            continue
        left = [P(i + a, j + b, h), P(i + b, j + b, h),
                P(i + b, j + b), P(i + a, j + b)]
        right = [P(i + b, j + a, h), P(i + b, j + b, h),
                 P(i + b, j + b), P(i + b, j + a)]
        out.append(f'<g class="b" style="animation-delay:{delay:.2f}s">'
                   f'{poly(left, LEFT[lvl])}{poly(right, RIGHT[lvl])}{poly(top, TOPS[lvl])}{tip}</g>')
        if d["count"] == peak and best_top is None:
            best_top = (P(i + 0.5, j + 0.5, h), d)

    months, seen = [], set()
    for i, j, d in cells:
        dt = date.fromisoformat(d["date"])
        if j == 0 and dt.day <= 7 and dt.month not in seen:
            seen.add(dt.month)
            x, y = P(i + 0.2, 7.5)
            ang = math.degrees(math.atan2(IY, IX))
            months.append(f'<text x="{x:.1f}" y="{y + 8:.1f}" font-size="10" fill="{MUTED}" transform="rotate({ang:.1f} {x:.1f} {y + 8:.1f})">{dt.strftime("%b")}</text>')

    beacon = ""
    if best_top:
        (bx, by), bd = best_top
        label = f"peak {bd['count']} • {date.fromisoformat(bd['date']).strftime('%b %d')}"
        beacon = f"""
<g class="f" style="animation-delay:2.4s">
  <line x1="{bx:.1f}" y1="{by:.1f}" x2="{bx:.1f}" y2="{by - 32:.1f}" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="2 2"/>
  <circle cx="{bx:.1f}" cy="{by - 32:.1f}" r="3" fill="{ORANGE}"/>
  <text x="{bx + 6:.1f}" y="{by - 28:.1f}" font-size="11" font-weight="700" fill="{ORANGE}">{esc(label)}</text>
</g>
"""

    def fmt_range(r):
        if not r:
            return ""
        return f"{date.fromisoformat(r[0]).strftime('%b %Y')} - {date.fromisoformat(r[1]).strftime('%b %Y')}"

    legend_items = [
        ("current streak", f"{st.get('current_streak', 0)} days", CYAN),
        ("longest streak", f"{st.get('longest_streak', 0)} days", PURPLE),
        ("active days", f"{st.get('active_days', 0)} / 365", GREEN),
        ("busiest weekday", f"{st.get('busiest_weekday', '-')}", ORANGE),
    ]
    leg_lines = []
    ly = H - 84
    for k, (lbl, val, col) in enumerate(legend_items):
        leg_lines.append(
            f'<g class="f" style="animation-delay:{2.0 + k * 0.1:.2f}s">'
            f'<text x="40" y="{ly}" font-size="11" fill="{MUTED}">{esc(lbl)}</text>'
            f'<text x="160" y="{ly}" font-size="11" font-weight="700" fill="{col}">{esc(val)}</text></g>')
        ly += 17

    defs = f"""
<style>
  .t {{ opacity: 0; animation: f .4s ease-out forwards; }}
  .b {{ opacity: 0; transform-box: fill-box; transform-origin: bottom center; animation: grow .6s cubic-bezier(.2,.8,.2,1) forwards; }}
  .f {{ opacity: 0; animation: f .5s ease-out forwards; }}
  @keyframes f {{ to {{ opacity: 1; }} }}
  @keyframes grow {{ from {{ opacity: 0; transform: scaleY(0.05); }} to {{ opacity: 1; transform: scaleY(1); }} }}
</style>
"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> ./skyline --user {esc(data.get('username', USERNAME))} --3d</text>
<text x="{W - 36}" y="58" font-size="28" font-weight="800" fill="{GREEN}" text-anchor="end">{st.get('total', 0):,}</text>
<text x="{W - 36}" y="74" font-size="11" fill="{MUTED}" text-anchor="end">contributions in the last year</text>
<text x="{W - 36}" y="88" font-size="10" fill="{MUTED}" text-anchor="end">{fmt_range(st.get('range', []))}</text>
{''.join(out)}
{''.join(months)}
{beacon}
{''.join(leg_lines)}
"""
    write_svg("contrib-skyline.svg", window(W, H, "skyline.sh", body, defs))


# ---------------------------------------------------------------- heatmap
def heatmap_svg():
    W, H = 860, 270
    CELL, GAP = 12, 3.2
    STEP = CELL + GAP
    from datetime import date, timedelta
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    if not days:
        return
    first = date.fromisoformat(days[0]["date"])
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = (date.fromisoformat(days[-1]["date"]) - start).days // 7 + 1
    grid_w = cols * STEP - GAP
    x0 = (W - grid_w) / 2 + 14
    y0 = 92
    cells, months, last_month = [], [], None
    best_count = max(1, st.get("best_day", {}).get("count", 1))
    for d in days:
        dt = date.fromisoformat(d["date"])
        off = (dt - start).days
        c, r = divmod(off, 7)
        x, y = x0 + c * STEP, y0 + r * STEP
        lvl = d["level"]
        if d["count"] == best_count:
            lvl = 5
        delay = (c + r * 1.5) * 0.018
        cells.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[lvl]}" class="c" style="animation-delay:{delay:.3f}s"><title>{d["count"]} on {d["date"]}</title></rect>')
        if r == 0 and dt.month != last_month and dt.day <= 7 and c < cols - 2:
            months.append(f'<text x="{x:.1f}" y="{y0 - 9}" font-size="11" fill="{MUTED}">{dt.strftime("%b")}</text>')
            last_month = dt.month

    wd = "".join(
        f'<text x="{x0 - 10}" y="{y0 + r * STEP + 10}" font-size="10" fill="{MUTED}" text-anchor="end">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    legend_x = x0 + grid_w - 6 * 15 - 40
    ly = y0 + 7 * STEP + 14
    legend = (
        f'<text x="{legend_x - 8}" y="{ly + 10}" font-size="11" fill="{MUTED}" text-anchor="end">Less</text>'
        + "".join(f'<rect x="{legend_x + i * 15}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{p}"/>' for i, p in enumerate(PALETTE))
        + f'<text x="{legend_x + 6 * 15 + 4}" y="{ly + 10}" font-size="11" fill="{MUTED}">More</text>')

    best = st.get("best_day", {})
    try:
        best_label = date.fromisoformat(best.get("date", "")).strftime("%b %d")
    except Exception:
        best_label = ""
    groups = [
        (f"{st.get('total', 0):,}", "contributions", GREEN),
        (f"{st.get('current_streak', 0)}d", "current streak", CYAN),
        (f"{st.get('longest_streak', 0)}d", "longest streak", PURPLE),
        (f"{best.get('count', 0)}", f"best day • {best_label}", ORANGE),
    ]
    foot, sx = [], x0
    for i, (v, label, color) in enumerate(groups):
        foot.append(f'<g class="f" style="animation-delay:{1.6 + i * 0.15:.2f}s"><text x="{sx:.1f}" y="{H - 20}" font-size="15" font-weight="700" fill="{color}">{esc(v)}<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">{esc(label)}</tspan></text></g>')
        sx += (len(v) + len(label)) * 7.2 + 44

    clip_cells = "".join(c.split("<title>")[0].replace(' class="c"', "") + "</rect>" for c in cells)
    defs = f"""
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="gridClip">{clip_cells}</clipPath>
<style>.c{{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.2,1.6,.4,1) forwards}}@keyframes pop{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:scale(1)}}}}.f{{opacity:0;animation:fin .6s ease-out forwards}}@keyframes fin{{to{{opacity:1}}}}</style>
"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> git log --since="1 year ago" | heatmap</text>
{''.join(months)}
{wd}
{''.join(cells)}
<rect x="{x0}" y="{y0}" width="{grid_w}" height="{7 * STEP}" fill="url(#sweep)" clip-path="url(#gridClip)" opacity="0">
  <animate attributeName="x" from="{x0 - 200}" to="{x0 + grid_w + 200}" begin="1.2s" dur="1.2s" fill="freeze"/>
  <set attributeName="opacity" to="1" begin="1.2s"/>
  <set attributeName="opacity" to="0" begin="2.4s"/>
</rect>
{legend}
{''.join(foot)}
"""
    write_svg("contrib-heatmap.svg", window(W, H, "contributions.sh", body, defs))


# ---------------------------------------------------------------- activity
def activity_svg():
    W, H = 860, 400
    gh = load("github.json", {})
    act = load("activity.json", {})
    data = load("contributions.json", {})
    days, st = data.get("days", []), data.get("stats", {})
    total = st.get("total", 0) or 1
    commits = act.get("commits", 0)
    prs = act.get("pull_requests", 0) or gh.get("prs_opened", 0)
    issues_reviews = act.get("issues", 0) + act.get("reviews", 0)
    other = max(total - commits - prs - issues_reviews, 0)

    # Donut chart
    DCX, DCY, DR = 132, 168, 60
    circ = 2 * math.pi * DR
    items = [(commits, GREEN), (prs, CYAN), (issues_reviews, PURPLE), (other, "#6e7681")]
    gap = 3 if sum(1 for v, _ in items if v) > 1 else 0
    segs, cum = [], 0.0
    for k, (val, color) in enumerate(items):
        seg = circ * val / total
        if seg > gap:
            segs.append(
                f'<circle cx="{DCX}" cy="{DCY}" r="{DR}" fill="none" stroke="{color}" stroke-width="10" '
                f'stroke-dasharray="0 {circ:.1f}" stroke-dashoffset="{-cum:.1f}" transform="rotate(-90 {DCX} {DCY})">'
                f'<animate attributeName="stroke-dasharray" from="0 {circ:.1f}" to="{seg - gap:.1f} {circ:.1f}" '
                f'begin="{0.6 + k * 0.45:.2f}s" dur="0.7s" fill="freeze" calcMode="spline" keySplines=".3 .7 .3 1" keyTimes="0;1"/></circle>')
        cum += seg

    donut = (f'<circle cx="{DCX}" cy="{DCY}" r="{DR}" fill="none" stroke="{BORDER}" stroke-width="10"/>'
             + "".join(segs)
             + f'<g class="fin" style="animation-delay:.4s" text-anchor="middle">'
               f'<text x="{DCX}" y="{DCY + 6}" font-size="34" font-weight="800" fill="{FG}">{total:,}</text>'
               f'<text x="{DCX}" y="{DCY + 26}" font-size="11" fill="{MUTED}">contributions</text></g>')

    rows_svg = []
    for k, (label, val, color) in enumerate(
            [("Commits", commits, GREEN), ("Pull Requests", prs, CYAN),
             ("Issues + Reviews", issues_reviews, PURPLE)]):
        ry = 118 + k * 52
        share = 100 * val / total
        rows_svg.append(
            f'<g class="fin" style="animation-delay:{0.5 + k * 0.15:.2f}s">'
            f'<text x="248" y="{ry}" font-size="13" font-weight="700" fill="{color}">{esc(label)}</text>'
            f'<text x="382" y="{ry}" font-size="15" font-weight="700" fill="{FG}">{val}<tspan font-size="11" font-weight="400" fill="{MUTED}"> / {total:,}</tspan></text>'
            f'<text x="548" y="{ry}" font-size="11" fill="{MUTED}" text-anchor="end">share <tspan dx="4" fill="{color}" font-weight="700">{share:.1f}%</tspan></text>'
            f'<rect x="248" y="{ry + 10}" width="300" height="6" rx="3" fill="{BORDER}"/>'
            f'<rect x="248" y="{ry + 10}" width="0" height="6" rx="3" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{300 * val / total:.1f}" begin="{0.9 + k * 0.2:.2f}s" dur="1.1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect></g>')

    merged = gh.get("prs_merged", 2)
    opened = gh.get("prs_opened", 14) or 1
    block_rows = [
        f'<text x="610" y="106" font-size="11" fill="{MUTED}">merged pull requests</text>',
        f'<text x="610" y="146" font-size="40" font-weight="800" fill="url(#ghGrad)">{merged}</text>',
        f'<text x="610" y="170" font-size="12" fill="{FG}">{100 * merged / opened:.1f}% merge rate<tspan fill="{MUTED}">  •  {opened} opened</tspan></text>',
        f'<text x="610" y="210" font-size="16" font-weight="700" fill="{ORANGE}">{st.get("current_streak", 1)}d<tspan font-size="11" font-weight="400" fill="{MUTED}" dx="6">current streak</tspan></text>',
        f'<text x="610" y="228" font-size="11" fill="{MUTED}">{st.get("longest_streak", 7)}d best • {st.get("active_days", 22)} active days</text>',
    ]

    # Weekly histogram
    weeks = _weeks(days)
    tail_weeks = weeks[-52:] if len(weeks) > 52 else weeks
    wmax = max(1, max(c for _, c in tail_weeks)) if tail_weeks else 1
    wx0, wy0, ww, wh = 40, 310, 780, 48
    bw = (ww - (len(tail_weeks) - 1) * 3) / max(1, len(tail_weeks))
    bars = []
    for k, (dt, count) in enumerate(tail_weeks):
        h = max(2, wh * count / wmax) if count else 2
        col = ORANGE if count == wmax else (GREEN if count else "#21262d")
        bx = wx0 + k * (bw + 3)
        delay = 1.0 + k * 0.015
        bars.append(
            f'<rect x="{bx:.1f}" y="{wy0 + wh - h:.1f}" width="{bw:.1f}" height="{h:.1f}" rx="1.5" fill="{col}" class="fin" style="animation-delay:{delay:.2f}s">'
            f'<title>week of {dt.isoformat()}: {count}</title></rect>')

    # Month labels
    m_labels, seen_m = [], set()
    for k, (dt, _) in enumerate(tail_weeks):
        if dt.day <= 7 and dt.month not in seen_m:
            seen_m.add(dt.month)
            bx = wx0 + k * (bw + 3)
            m_labels.append(f'<text x="{bx:.1f}" y="{wy0 + wh + 14}" font-size="10" fill="{MUTED}">{dt.strftime("%b")}</text>')

    # Repo tags
    repos = act.get("repos", [["EmbeddedChat", 13], ["AI-DETECTION", 5], ["FoodDelivery", 2]])
    rtags, rx = [], 40
    for label, count in repos:
        pill_w = len(label) * 6.6 + len(str(count)) * 7 + 28
        rtags.append(
            f'<rect x="{rx}" y="{H - 34}" width="{pill_w}" height="20" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
            f'<text x="{rx + 10}" y="{H - 20}" font-size="11" fill="{FG}">{esc(label)} <tspan font-weight="700" fill="{CYAN}">{count}</tspan></text>')
        rx += pill_w + 8

    defs = f"""
<linearGradient id="ghGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{CYAN}"/>
</linearGradient>
<style>
  .fin {{ opacity: 0; animation: fin .5s ease-out forwards; }}
  @keyframes fin {{ to {{ opacity: 1; }} }}
</style>
"""
    body = f"""
<text x="36" y="62" font-size="13" fill="{FG}"><tspan fill="{GREEN}">$</tspan> github --user {USERNAME} --stats</text>
<text x="{W - 36}" y="62" font-size="11" fill="{MUTED}" text-anchor="end">github.com/{USERNAME}</text>
{donut}
{''.join(rows_svg)}
<g class="fin" style="animation-delay:0.8s">{''.join(block_rows)}</g>
<text x="40" y="296" font-size="11" fill="{MUTED}">contributions per week <tspan fill="{FG}">• {total} in the last year</tspan> <tspan fill="{MUTED}">• busiest on {st.get('busiest_weekday', '-')}</tspan></text>
{''.join(bars)}
{''.join(m_labels)}
{''.join(rtags)}
<circle cx="{W - 120}" cy="{H - 24}" r="3" fill="{ORANGE}"/>
<text x="{W - 110}" y="{H - 20}" font-size="11" fill="{MUTED}">best day <tspan fill="{ORANGE}" font-weight="700">• {st.get('best_day', {}).get('count', 0)}</tspan></text>
"""
    write_svg("github-activity.svg", window(W, H, "github.sh", body, defs))


def main():
    print("Rendering SVGs...")
    header_svg()
    portrait_svg()
    info_card_svg()
    globe_svg()
    tech_sphere_svg()
    skyline_svg()
    heatmap_svg()
    activity_svg()
    print("All SVGs rendered successfully!")


if __name__ == "__main__":
    main()
