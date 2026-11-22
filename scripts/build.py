#!/usr/bin/env python3
"""Builds the profile graphics: assets/{header,mtcap}-{dark,light}.svg.

Run from the repository root:  python3 scripts/build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg="#0b1016", panel="#111922", border="#22303c", text="#e6edf3",
        soft="#b4c0cb", muted="#7d8b99", accent="#5ec4d0", warm="#e8b88a",
        dim="#2a3a47", err="#e88879",
        s1="#1fa6ba", s2="#d67a2c", good="#4cc38a",
    ),
    "light": dict(
        bg="#f6f8f9", panel="#ffffff", border="#d3dce2", text="#17212b",
        soft="#3d4b57", muted="#647381", accent="#14808f", warm="#a8632a",
        dim="#c3ced6", err="#c0392b",
        s1="#0e8aa0", s2="#b8601c", good="#1a7f4b",
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
# The header is drawn as a monitoring dashboard: a top bar and four panels.
# The traffic series is illustrative, generated from a fixed seed.

def panel(x, y, w, h, title, c):
    return (f'<rect x="{x}.5" y="{y}.5" width="{w - 1}" height="{h - 1}" rx="8" '
            f'fill="{c["panel"]}" stroke="{c["border"]}"/>'
            + (text(x + 16, y + 23, title, c["muted"], 12) if title else ""))


def pill(x, y, label, c, fill=None):
    w = round(len(label) * 7.4 + 22)
    return w, (f'<rect x="{x}.5" y="{y}.5" width="{w}" height="24" rx="12" '
               f'fill="{fill or c["bg"]}" stroke="{c["border"]}"/>'
               + text(x + w / 2, y + 17, label, c["muted"], 12, extra='text-anchor="middle"'))


def series(seed, base, swing, n=44):
    """Deterministic wavy series in 0..100: two sines plus a little seeded noise."""
    import math
    import random
    rnd = random.Random(seed)
    return [
        max(4, min(96, base + swing * math.sin(i / 6 + seed)
                   + swing * 0.4 * math.sin(i / 1.7 + seed * 2) + rnd.uniform(-2, 2)))
        for i in range(n)
    ]


def polyline(values, x0, x1, y0, y1):
    """Map 0..100 values to plot coordinates; returns points and path length."""
    import math
    n = len(values)
    pts = [(x0 + (x1 - x0) * i / (n - 1), y1 - (y1 - y0) * v / 100) for i, v in enumerate(values)]
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(n - 1))
    return pts, length


def header(c):
    W, H = 880, 338
    p = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
         f'fill="{c["bg"]}" stroke="{c["border"]}"/>']

    # ---- top bar
    for i, (dx, dy) in enumerate([(0, 0), (10, 0), (0, 10), (10, 10)]):
        p.append(f'<rect x="{20 + dx}" y="{14 + dy}" width="7" height="7" rx="1.5" '
                 f'fill="{c["accent"] if i == 0 else c["dim"]}"/>')
    p.append(f'<text x="48" y="28" font-size="13" xml:space="preserve">'
             f'<tspan fill="{c["muted"]}">dashboards / </tspan>'
             f'<tspan fill="{c["text"]}" font-weight="700">gurevsergey</tspan></text>')
    w, body = pill(864 - 96, 11, "refresh 5s", c, c["panel"])
    p.append(body)
    w, body = pill(864 - 96 - 8 - 111, 11, "Last 6 hours", c, c["panel"])
    p.append(body)
    p.append(f'<circle cx="596" cy="23.5" r="4" fill="{c["good"]}">'
             f'<animate attributeName="opacity" values="1;0.35;1" dur="2s" '
             f'repeatCount="indefinite"/></circle>')
    p.append(text(606, 28, "live", c["muted"], 12))
    p.append(f'<line x1="1" y1="46.5" x2="{W-1}" y2="46.5" stroke="{c["border"]}"/>')

    # ---- panel: identity
    p.append(panel(16, 58, 420, 150, "", c))
    p.append(text(36, 92, "$ whoami", c["muted"], 13))
    p.append(text(36, 140, "gurevsergey", c["text"], 38, 700))
    p.append(f'<rect x="294" y="109" width="17" height="34" fill="{c["accent"]}">'
             f'<animate attributeName="opacity" values="1;0" dur="1.2s" '
             f'calcMode="discrete" repeatCount="indefinite"/></rect>')
    p.append(text(36, 174, "Networks, monitoring, automation, Rust CLI tools", c["soft"], 13))

    # ---- panel: topology
    p.append(panel(448, 58, 416, 150, "topology", c))
    nodes = {
        "a": (480, 142), "b": (556, 104), "c": (556, 180), "d": (642, 132),
        "e": (642, 188), "f": (728, 98), "g": (728, 166), "h": (832, 130),
    }
    links = ["ab", "ac", "bd", "cd", "ce", "df", "dg", "eg", "fh", "gh", "bf"]
    route = "abdgh"
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
        p.append(f'<circle cx="{nx}" cy="{ny}" r="{6 if on else 5}" fill="{c["panel"]}" '
                 f'stroke="{c["accent"] if on else c["muted"]}" stroke-width="2"/>')
    motion = ('<animateMotion dur="3.6s" repeatCount="indefinite" calcMode="linear">'
              '<mpath href="#route"/></animateMotion>')
    p.append(f'<circle r="11" fill="{c["warm"]}" opacity="0.22">{motion}</circle>')
    p.append(f'<circle r="4.5" fill="{c["warm"]}">{motion}</circle>')
    p.append(text(480, 166, "src", c["muted"], 11, extra='text-anchor="middle"'))
    p.append(text(832, 154, "dst", c["muted"], 11, extra='text-anchor="middle"'))

    # ---- panel: traffic (time series, one axis, two series)
    px, py, pw, ph = 16, 220, 420, 102
    p.append(panel(px, py, pw, ph, "traffic, Mbit/s", c))
    lx = px + pw - 16
    for name, key in (("tx", "s2"), ("rx", "s1")):          # legend, right-aligned
        p.append(text(lx, py + 23, name, c["muted"], 12, extra='text-anchor="end"'))
        p.append(f'<rect x="{lx - 28}" y="{py + 17}" width="10" height="3" rx="1.5" fill="{c[key]}"/>')
        lx -= 48
    x0, x1, y0, y1 = px + 44, px + pw - 44, py + 38, py + ph - 14
    for tick in (0, 50, 100):
        y = y1 - (y1 - y0) * tick / 100
        p.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{c["border"]}" '
                 f'stroke-width="1"{"" if tick == 0 else " stroke-dasharray=\"2 4\""}/>')
        p.append(text(x0 - 8, round(y + 3.5, 1), str(tick), c["muted"], 10, extra='text-anchor="end"'))
    draw = 3.0
    for name, key, vals in (("rx", "s1", series(7, 66, 14)), ("tx", "s2", series(3, 24, 7))):
        pts, length = polyline(vals, x0, x1, y0, y1)
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        if key == "s1":
            p.append(f'<path d="{d} L{x1},{y1} L{x0},{y1} Z" fill="{c[key]}" opacity="0.1">'
                     f'<animate attributeName="opacity" values="0;0;0.1" keyTimes="0;0.8;1" '
                     f'dur="{draw + 0.6}s" fill="freeze"/></path>')
        p.append(f'<path d="{d}" fill="none" stroke="{c[key]}" stroke-width="2" '
                 f'stroke-linejoin="round" stroke-linecap="round" stroke-dasharray="{length:.0f}">'
                 f'<animate attributeName="stroke-dashoffset" from="{length:.0f}" to="0" '
                 f'dur="{draw}s" fill="freeze"/></path>')
        ex, ey = pts[-1]
        shown = (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;0.96;1" '
                 f'dur="{draw + 0.1}s" fill="freeze"/>')
        p.append(f'<g>{shown}'
                 f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{c[key]}" opacity="0.3">'
                 f'<animate attributeName="r" values="4;9;4" dur="2s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.35;0;0.35" dur="2s" repeatCount="indefinite"/></circle>'
                 f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" fill="{c[key]}" stroke="{c["panel"]}" stroke-width="2"/>'
                 f'{text(round(ex + 10, 1), round(ey + 4, 1), name, c["soft"], 11)}</g>')

    # ---- panel: stack
    sx, sy = 448, 220
    p.append(panel(sx, sy, 416, 102, "stack", c))
    rows = [
        ["Linux", "MikroTik", "Prometheus", "Grafana"],
        ["Ansible", "nftables", "systemd", "fish"],
    ]
    for r, row in enumerate(rows):
        x, y = sx + 16, sy + 34 + r * 31
        for name in row:
            w, body = pill(x, y, name, c)
            p.append(body)
            x += w + 8

    return svg(W, H, "\n".join(p),
               "gurevsergey: networks, monitoring, automation, Rust CLI tools. "
               "Drawn as a dashboard with a network topology and a traffic chart.")


# ----------------------------------------------------------- project card

CYCLE = 16.0
SIZE = 13
CH = 7.8          # advance of one 13px monospace glyph
X0 = 44


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
        f'<clipPath id="t{idx}"><rect x="{cx - 2:.1f}" y="{y - 15}" '
        f'width="{full}" height="22">{anim}</rect></clipPath>'
        f'<g>{appear(max(start - 0.5, 0.01))}'
        f'{text(X0, y, "$", c["muted"], SIZE)}'
        f'<g clip-path="url(#t{idx})">{text(f"{cx:.1f}", y, cmd, c["text"], SIZE)}</g></g>'
    )


def output(y, parts, t, c):
    """parts: list of (string, colour key); laid out as one line."""
    spans = "".join(f'<tspan fill="{c[k]}">{escape(s)}</tspan>' for s, k in parts)
    return (f'<text x="{X0}" y="{y}" font-size="{SIZE}" xml:space="preserve">'
            f'{appear(t)}{spans}</text>')


def packet(line, proto, body, proto_colour="accent"):
    """Split a capture line into time, addresses, protocol and the rest."""
    i = line.index(proto, 12)
    return [(line[:12], "muted"), (line[12:i], "soft"),
            (proto, proto_colour), (line[i + len(proto):], body)]


def card(c):
    W, H = 880, 404
    p = [
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
    ]

    # title block
    p.append(text(32, 54, "mtcap", c["text"], 26, 700))
    p.append(f'<circle cx="131" cy="45" r="5" fill="{c["warm"]}"/>')
    p.append(text(144, 49.5, "Rust", c["muted"], 13))
    p.append(text(848, 50, "gurevsergey/mtcap →", c["accent"], 13, 700,
                  extra='text-anchor="end"'))
    p.append(text(32, 82, "Live packet capture from MikroTik routers into Wireshark",
                  c["soft"], 14))
    p.append(text(32, 104, "RouterOS API · TZSP · filter presets · capture reports · router watchdog",
                  c["muted"], 12.5))

    # terminal window
    top = 124
    p.append(f'<rect x="24.5" y="{top}.5" width="831" height="{H - top - 25}" rx="10" '
             f'fill="{c["panel"]}" stroke="{c["border"]}"/>')
    p.append(f'<line x1="25" y1="{top + 34}.5" x2="855" y2="{top + 34}.5" stroke="{c["border"]}"/>')
    for i in range(3):
        p.append(f'<circle cx="{46 + i * 18}" cy="{top + 17}" r="5" fill="{c["dim"]}"/>')
    p.append(text(440, top + 21, "mtcap", c["muted"], 12, extra='text-anchor="middle"'))

    y0, lh = top + 60, 22
    row = lambda n: y0 + n * lh

    p.append(typed(1, row(0), "mtcap home dns -i bridge", 0.6, 2.2, c))
    p.append(output(row(1), [("mtcap: ", "muted"),
                             ("home → 192.168.88.10, preset dns", "soft")], 2.6, c))
    p.append(output(row(2), [("       router sends: ", "muted"),
                             ("interface=bridge and port=53", "warm")], 2.6, c))
    p.append(output(row(3), [("mtcap: ", "muted"),
                             ("capturing from 192.168.88.1 on eth0 for up to 600 s; "
                              "Ctrl-C to stop", "soft")], 3.2, c))
    p.append(output(row(4), [("time                   source   destination      "
                              "proto   what", "muted")], 3.8, c))
    p.append(output(row(5), packet(
        "10:15:02.114           laptop → home             DNS       A     "
        "example.com → 93.184.215.14  17 ms", "DNS", "soft"), 4.8, c))
    p.append(output(row(6), packet(
        "10:15:07.920           laptop → home             DNS     ✗ AAAA  "
        "printer.lan  NXDOMAIN  1 ms", "DNS", "err"), 6.6, c))
    p.append(output(row(7), packet(
        "10:15:09.301            phone → home             DNS     ? A     "
        "slow.example  no answer seen", "DNS", "warm"), 9.4, c))
    p.append(output(row(8), packet(
        "10:15:11.530               tv → 192.168.88.255   UDP     "
        "52100 → 9999 Len=24  ×4", "UDP", "muted", "muted"), 11.0, c))

    return svg(W, H, "\n".join(p),
               "mtcap: live packet capture from MikroTik routers into Wireshark, "
               "with a terminal demo of a DNS capture")


def main():
    OUT.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(c), encoding="utf-8")
        (OUT / f"mtcap-{name}.svg").write_text(card(c), encoding="utf-8")
    print("written:", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
