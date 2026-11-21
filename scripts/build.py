#!/usr/bin/env python3
"""Builds the profile graphics: assets/{header,next-hop}-{dark,light}.svg.

Run from the repository root:  python3 scripts/build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg="#0b1016", panel="#111922", border="#22303c", text="#e6edf3",
        soft="#b4c0cb", muted="#7d8b99", accent="#5ec4d0", warm="#e8b88a",
        dim="#2a3a47",
    ),
    "light": dict(
        bg="#f6f8f9", panel="#ffffff", border="#d3dce2", text="#17212b",
        soft="#3d4b57", muted="#647381", accent="#14808f", warm="#a8632a",
        dim="#c3ced6",
    ),
}

FONT = ("ui-monospace, 'SF Mono', 'JetBrains Mono', 'Cascadia Mono', Menlo, "
        "Consolas, 'DejaVu Sans Mono', 'Liberation Mono', monospace")


def text(x, y, s, fill, size=14, weight=400, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" '
            f'font-weight="{weight}" xml:space="preserve" {extra}>{escape(s)}</text>')


def svg(w, h, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{escape(label)}" '
        f'font-family="{FONT}">\n{body}\n</svg>\n'
    )


# ---------------------------------------------------------------- header

def header(c):
    W, H = 880, 250
    nodes = {
        "a": (566, 127), "b": (636, 74), "c": (636, 182), "d": (710, 110),
        "e": (710, 196), "f": (782, 66), "g": (782, 158), "h": (838, 114),
    }
    links = ["ab", "ac", "bd", "cd", "ce", "df", "dg", "eg", "fh", "gh", "bf"]
    route = "abdgh"

    p = [
        f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1" fill="{c["dim"]}"/></pattern>'
        f'<linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">'
        f'<stop offset="0.35" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#fff" stop-opacity="0.9"/></linearGradient>'
        f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask></defs>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#dots)" mask="url(#m)"/>',
    ]

    # left column
    p.append(text(44, 58, "$ whoami", c["muted"], 14))
    p.append(text(44, 108, "gurevsergey", c["text"], 44, 700))
    p.append(
        f'<rect x="342" y="72" width="20" height="40" fill="{c["accent"]}">'
        f'<animate attributeName="opacity" values="1;0" dur="1.2s" '
        f'calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    p.append(text(44, 142, "Networks, monitoring, automation, Rust CLI tools",
                  c["soft"], 15.5))
    rows = [
        ["Rust", "Linux", "MikroTik", "Prometheus", "Grafana", "Ansible"],
        ["sing-box", "nftables", "systemd", "fish"],
    ]
    for r, row in enumerate(rows):
        x, y = 44, 166 + r * 32
        for name in row:
            w = round(len(name) * 7.4 + 22)
            p.append(f'<rect x="{x}.5" y="{y}.5" width="{w}" height="24" rx="12" '
                     f'fill="{c["panel"]}" stroke="{c["border"]}"/>')
            p.append(text(x + w / 2, y + 17, name, c["muted"], 12,
                          extra='text-anchor="middle"'))
            x += w + 8

    # route graph
    for a, b in links:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{c["dim"]}" stroke-width="1.5"/>')
    d = "M" + " L".join(f"{nodes[n][0]},{nodes[n][1]}" for n in route)
    p.append(f'<path id="route" d="{d}" fill="none" stroke="{c["accent"]}" '
             f'stroke-width="2" stroke-linejoin="round" stroke-dasharray="6 6">'
             f'<animate attributeName="stroke-dashoffset" from="24" to="0" '
             f'dur="1.2s" repeatCount="indefinite"/></path>')
    for n, (nx, ny) in nodes.items():
        on = n in route
        p.append(f'<circle cx="{nx}" cy="{ny}" r="{6 if on else 5}" fill="{c["bg"]}" '
                 f'stroke="{c["accent"] if on else c["muted"]}" stroke-width="2"/>')
    motion = (f'<animateMotion dur="3.6s" repeatCount="indefinite" '
              f'calcMode="linear"><mpath href="#route"/></animateMotion>')
    p.append(f'<circle r="11" fill="{c["warm"]}" opacity="0.22">{motion}</circle>')
    p.append(f'<circle r="4.5" fill="{c["warm"]}">{motion}</circle>')
    p.append(text(566, 151, "src", c["muted"], 12, extra='text-anchor="middle"'))
    p.append(text(838, 138, "dst", c["muted"], 12, extra='text-anchor="middle"'))

    return svg(W, H, "\n".join(p),
               "gurevsergey: networks, monitoring, automation, Rust CLI tools")


# ----------------------------------------------------------- project card

CYCLE = 14.0
CH = 8.4          # advance of one 14px monospace glyph
X0 = 46


def kt(t):
    return f"{t / CYCLE:.4f}".rstrip("0").rstrip(".") or "0"


def appear(t):
    """Hidden until t, then visible for the rest of the cycle."""
    return (f'<animate attributeName="opacity" values="0;1" '
            f'keyTimes="0;{kt(t)}" dur="{CYCLE}s" calcMode="discrete" '
            f'repeatCount="indefinite"/>')


def typed(idx, y, cmd, start, end, c):
    n = len(cmd)
    full = round(n * CH + 12)
    times = [0.0] + [start + (end - start) * i / n for i in range(1, n + 1)]
    widths = [0] + [round(i * CH + 3) for i in range(1, n)] + [full]
    anim = (f'<animate attributeName="width" values="{";".join(map(str, widths))}" '
            f'keyTimes="{";".join(kt(t) for t in times)}" dur="{CYCLE}s" '
            f'calcMode="discrete" repeatCount="indefinite"/>')
    cx = X0 + 2 * CH
    return (
        f'<clipPath id="t{idx}"><rect x="{cx - 2:.1f}" y="{y - 16}" '
        f'width="{full}" height="24">{anim}</rect></clipPath>'
        f'<g>{appear(max(start - 0.5, 0.01))}'
        f'{text(X0, y, "$", c["muted"])}'
        f'<g clip-path="url(#t{idx})">{text(f"{cx:.1f}", y, cmd, c["text"])}</g></g>'
    )


def output(y, parts, t, c):
    """parts: list of (string, colour key); laid out as one line."""
    spans = "".join(f'<tspan fill="{c[k]}">{escape(s)}</tspan>' for s, k in parts)
    return (f'<text x="{X0}" y="{y}" font-size="14" xml:space="preserve">'
            f'{appear(t)}{spans}</text>')


def card(c):
    W, H = 880, 340
    p = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
        # terminal window
        f'<rect x="24.5" y="24.5" width="500" height="291" rx="10" '
        f'fill="{c["panel"]}" stroke="{c["border"]}"/>',
        f'<line x1="25" y1="58.5" x2="524" y2="58.5" stroke="{c["border"]}"/>',
    ]
    for i in range(3):
        p.append(f'<circle cx="{46 + i * 18}" cy="42" r="5" fill="{c["dim"]}"/>')
    p.append(text(274, 46, "hop", c["muted"], 12, extra='text-anchor="middle"'))

    p.append(typed(1, 90, "hop warsaw", 0.6, 1.5, c))
    p.append(output(114, [("→ ", "accent"), ("🇵🇱 Warsaw, Poland", "soft")], 1.9, c))

    p.append(typed(2, 150, "hop rule tun firefox oulu", 3.2, 5.0, c))
    p.append(output(174, [("added: app  firefox  ", "soft"), ("tun", "warm"),
                          (" → ", "accent"), ("🇫🇮 Oulu, Finland", "soft")], 5.4, c))

    p.append(typed(3, 210, "hop off", 6.8, 7.4, c))
    p.append(output(234, [("main route direct, still through tunnel:", "soft")], 7.8, c))
    p.append(output(258, [("  app  firefox  ", "soft"), ("tun", "warm"),
                          (" → ", "accent"), ("🇫🇮 Oulu, Finland", "soft")], 7.8, c))

    p.append(
        f'<g>{appear(8.6)}{text(X0, 294, "$", c["muted"])}'
        f'<rect x="{X0 + 2 * CH:.1f}" y="280" width="9" height="18" fill="{c["accent"]}">'
        f'<animate attributeName="opacity" values="1;0" dur="1.2s" '
        f'calcMode="discrete" repeatCount="indefinite"/></rect></g>'
    )

    # description column
    x = 556
    p.append(text(x, 70, "next-hop", c["text"], 26, 700))
    p.append(f'<circle cx="{x + 5}" cy="92" r="5" fill="{c["warm"]}"/>')
    p.append(text(x + 18, 96.5, "Rust", c["muted"], 13))
    p.append(text(x, 132, "Command-line location switcher", c["soft"], 14))
    p.append(text(x, 152, "for sing-box", c["soft"], 14))
    for i, line in enumerate([
        "per-app and per-site routing",
        "latency checks and failover",
        "nftables kill switch",
        "switching without reconnects",
        "fish, Waybar and rofi bits",
    ]):
        y = 186 + i * 22
        p.append(text(x, y, "›", c["accent"], 13, 700))
        p.append(text(x + 16, y, line, c["muted"], 13))
    p.append(text(x, 306, "gurevsergey/next-hop →", c["accent"], 13, 700))

    return svg(W, H, "\n".join(p),
               "next-hop: command-line location switcher for sing-box, "
               "with a terminal demo of the hop command")


def main():
    OUT.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(c), encoding="utf-8")
        (OUT / f"next-hop-{name}.svg").write_text(card(c), encoding="utf-8")
    print("written:", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
