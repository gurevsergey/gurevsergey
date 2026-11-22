#!/usr/bin/env python3
"""Builds the profile graphics: assets/{switch,mtcap}-{dark,light}.svg.

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
# The header is the front panel of a 1U switch: the name is the model label,
# every port is a technology. Edit PORTS to change them; None is a free port.

PORTS = [
    "Linux", "MikroTik", "Prometheus", "Grafana", "Ansible", "Docker",
    "nftables", "systemd", "Git", "Bash", "fish", None,
]


def header(c):
    W, H = 880, 280
    p = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" '
         f'fill="{c["bg"]}" stroke="{c["border"]}"/>',
         text(28, 34, "$ show interfaces status", c["muted"], 12)]

    dx, dy, dw, dh = 24, 50, 832, 184
    p.append(f'<rect x="{dx}.5" y="{dy}.5" width="{dw - 1}" height="{dh - 1}" rx="6" '
             f'fill="{c["panel"]}" stroke="{c["border"]}"/>')
    for ex in (dx, dx + dw - 30):                       # rack ears
        p.append(f'<rect x="{ex}.5" y="{dy}.5" width="29" height="{dh - 1}" rx="6" '
                 f'fill="{c["bg"]}" stroke="{c["border"]}"/>')
        for hy in (dy + 30, dy + dh - 30):
            p.append(f'<circle cx="{ex + 15}" cy="{hy}" r="5" fill="none" '
                     f'stroke="{c["dim"]}" stroke-width="2"/>')

    # model label and status LEDs
    p.append(text(72, 124, "gurevsergey", c["text"], 22, 700))
    p.append(text(72, 146, "networks · monitoring · automation", c["muted"], 11))
    for i, (name, on) in enumerate((("PWR", True), ("SYS", True), ("ALM", False))):
        lx = 76 + i * 62
        blink = ('<animate attributeName="opacity" values="1;0.3;1" dur="1.6s" '
                 'repeatCount="indefinite"/>' if name == "SYS" else "")
        p.append(f'<circle cx="{lx}" cy="174" r="3.5" '
                 f'fill="{c["good"] if on else c["dim"]}">{blink}</circle>')
        p.append(text(lx + 9, 178, name, c["muted"], 10))

    # ports: two rows of six
    x0, pitch, pw, ph = 329, 84, 46, 36
    for i, name in enumerate(PORTS):
        x, y = x0 + (i % 6) * pitch, 78 + (i // 6) * 80
        p.append(f'<rect x="{x}.5" y="{y}.5" width="{pw}" height="{ph}" rx="3" '
                 f'fill="{c["bg"]}" stroke="{c["border"]}"/>')
        p.append(f'<rect x="{x + 15}.5" y="{y + ph - 8}.5" width="16" height="8" '
                 f'fill="{c["panel"]}" stroke="{c["border"]}"/>')
        for k in range(6):                              # contacts
            p.append(f'<rect x="{x + 9 + k * 5}" y="{y + 6}" width="2" height="9" fill="{c["dim"]}"/>')
        link = c["good"] if name else c["dim"]
        p.append(f'<rect x="{x + 4}" y="{y - 10}" width="12" height="4" rx="1" fill="{link}"/>')
        if name:
            dur = 1.1 + (i * 37 % 9) / 10
            p.append(f'<rect x="{x + pw - 16}" y="{y - 10}" width="12" height="4" rx="1" fill="{c["warm"]}">'
                     f'<animate attributeName="opacity" values="1;0.15;1;1;0.15;1" '
                     f'dur="{dur:.1f}s" repeatCount="indefinite"/></rect>')
        else:
            p.append(f'<rect x="{x + pw - 16}" y="{y - 10}" width="12" height="4" rx="1" fill="{c["dim"]}"/>')
        p.append(text(x + pw / 2, y + ph + 17, name or "free", c["soft"] if name else c["muted"], 11,
                      extra='text-anchor="middle"'))

    up = sum(1 for n in PORTS if n)
    p.append(text(28, 260, f"{up} ports up, {len(PORTS) - up} free", c["muted"], 12))

    return svg(W, H, "\n".join(p),
               "gurevsergey: networks, monitoring, automation. Drawn as the front panel "
               "of a switch whose ports are " + ", ".join(n for n in PORTS if n) + ".")


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
        (OUT / f"switch-{name}.svg").write_text(header(c), encoding="utf-8")
        (OUT / f"mtcap-{name}.svg").write_text(card(c), encoding="utf-8")
    print("written:", ", ".join(sorted(f.name for f in OUT.glob("*.svg"))))


if __name__ == "__main__":
    main()
