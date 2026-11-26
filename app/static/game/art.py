"""PyPython pixel art: colours, the python skin, food sprites and the 5x7 bitmap font. Data and tiny
helpers only: nothing here draws or talks to the browser."""

STAR_NAME = "STBUERAK"                              # this player gets a shining star

# Colours are 0xRRGGBB integers: warm, slightly faded "vintage arcade" palette.
BG, SCAN, DOT = 0x1f1510, 0x1a110d, 0x33241a
PANEL_BG, BTN_BG, BTN_EDGE = 0x150e0a, 0x2b1c12, 0x7a5a3a
INK, MUTED, DARK = 0xf4e6c8, 0xa58d6c, 0x2a1a10
YEL, RUST, TONGUE_COL = 0xf0b44c, 0x9a3d22, 0xc2452d
WARM = (0xf2c14e, 0xf19a3e, 0xe4583f, 0xf19a3e)     # rolling colour wave for ranks 2 and 3

# Skin: b=tan body, h=head, c=cream lip, d=dark blotch/marking, m=blotch centre, e=gold eye, n=nostril
PY_BODY = {"b": 0xc9a063, "h": 0xd9ae68, "c": 0xecd9a8, "d": 0x5a3820, "m": 0x8f5d30, "e": 0xf2c14e, "n": 0x2b1a10}
PY_DEAD = {"b": 0xd0644c, "h": 0xdc7458, "c": 0xf2b8a2, "d": 0x6e2a22, "m": 0x9a3f32, "e": 0xffd9a0, "n": 0x2b1a10}

# Spade-shaped python head, drawn facing right (9 long x 7 wide); rotated for other headings
HEAD_RIGHT = ("  ccc    ",
              "hhhddeh  ",
              "hdddhhhhn",
              "hddddhhhh",
              "hdddhhhhn",
              "hhhddeh  ",
              "  ccc    ")


def rotate_head(rows, heading):
    h, w = len(rows), len(rows[0])
    if heading == (1, 0):
        return rows
    if heading == (-1, 0):
        return tuple(r[::-1] for r in rows)
    if heading == (0, 1):    # clockwise
        return tuple("".join(rows[h - 1 - j][i] for j in range(h)) for i in range(w))
    return tuple("".join(rows[j][w - 1 - i] for j in range(h)) for i in range(w))   # up


HEADS = {d: rotate_head(HEAD_RIGHT, d) for d in ((1, 0), (-1, 0), (0, 1), (0, -1))}
# forked tongue as (x, y, w, h) in art px relative to the head centre
TONGUE = {(1, 0): ((5, 0, 2, 1), (7, -1, 1, 1), (7, 1, 1, 1)),
          (-1, 0): ((-6, 0, 2, 1), (-7, -1, 1, 1), (-7, 1, 1, 1)),
          (0, 1): ((0, 5, 1, 2), (-1, 7, 1, 1), (1, 7, 1, 1)),
          (0, -1): ((0, -6, 1, 2), (-1, -7, 1, 1), (1, -7, 1, 1))}

# Sprites are (rows, palette). A space is transparent.
APPLE = (("   s  ", " rrrr ", "rhrrrr", "rrrrrr", " rrrr ", "  rr  "),
         {"s": 0x7ea84b, "r": 0xe4583f, "h": 0xf6a48a})
_B = {"b": 0x4f8fba, "h": 0xd3e8f2}
GEM_S = ((" bb ", "bhbb", "bbbb", " bb "), _B)
GEM_B = (("  bb  ", " bhbb ", "bhbbbb", "bbbbbb", " bbbb ", "  bb  "), _B)
_P = {"p": 0xa867b0, "H": 0xefd3ea}
SPIN = [(("  pp  ", " pHpp ", "pHpppp", "pppppp", " pppp ", "  pp  "), _P),
        ((" pp ", "pHpp", "pppp", "pppp", "pppp", " pp "), _P),
        (("Hp", "pp", "pp", "pp", "pp", "pp"), _P),
        ((" pp ", "ppHp", "pppp", "pppp", "pppp", " pp "), _P)]
COIN = (" yyyy ", "ywyyyy", "yyyyyy", "yyyoyy", "yyyyyy", " yyyy ")
STAR_S = (" y ", "ywy", " y ")
STAR_M = ("  y  ", " yyy ", "yywyy", " yyy ", "  y  ")
STAR_L = ("   y   ", "   y   ", "  yyy  ", "yyywyyy", "  yyy  ", "   y   ", "   y   ")

_FONT = {
    "A": ".###./#...#/#...#/#####/#...#/#...#/#...#", "B": "####./#...#/#...#/####./#...#/#...#/####.",
    "C": ".###./#...#/#..../#..../#..../#...#/.###.", "D": "####./#...#/#...#/#...#/#...#/#...#/####.",
    "E": "#####/#..../#..../####./#..../#..../#####", "F": "#####/#..../#..../####./#..../#..../#....",
    "G": ".###./#...#/#..../#.###/#...#/#...#/.###.", "H": "#...#/#...#/#...#/#####/#...#/#...#/#...#",
    "I": "#####/..#../..#../..#../..#../..#../#####", "J": "..###/...#./...#./...#./...#./#..#./.##..",
    "K": "#...#/#..#./#.#../##.../#.#../#..#./#...#", "L": "#..../#..../#..../#..../#..../#..../#####",
    "M": "#...#/##.##/#.#.#/#.#.#/#...#/#...#/#...#", "N": "#...#/##..#/#.#.#/#..##/#...#/#...#/#...#",
    "O": ".###./#...#/#...#/#...#/#...#/#...#/.###.", "P": "####./#...#/#...#/####./#..../#..../#....",
    "Q": ".###./#...#/#...#/#...#/#.#.#/#..#./.##.#", "R": "####./#...#/#...#/####./#.#../#..#./#...#",
    "S": ".####/#..../#..../.###./....#/....#/####.", "T": "#####/..#../..#../..#../..#../..#../..#..",
    "U": "#...#/#...#/#...#/#...#/#...#/#...#/.###.", "V": "#...#/#...#/#...#/#...#/#...#/.#.#./..#..",
    "W": "#...#/#...#/#...#/#.#.#/#.#.#/##.##/#...#", "X": "#...#/#...#/.#.#./..#../.#.#./#...#/#...#",
    "Y": "#...#/#...#/.#.#./..#../..#../..#../..#..", "Z": "#####/....#/...#./..#../.#.../#..../#####",
    "0": ".###./#...#/#..##/#.#.#/##..#/#...#/.###.", "1": "..#../.##../..#../..#../..#../..#../.###.",
    "2": ".###./#...#/....#/...#./..#../.#.../#####", "3": "####./....#/....#/.###./....#/....#/####.",
    "4": "...#./..##./.#.#./#..#./#####/...#./...#.", "5": "#####/#..../####./....#/....#/#...#/.###.",
    "6": ".###./#..../#..../####./#...#/#...#/.###.", "7": "#####/....#/...#./..#../.#.../.#.../.#...",
    "8": ".###./#...#/#...#/.###./#...#/#...#/.###.", "9": ".###./#...#/#...#/.####/....#/....#/.###.",
    ".": "...../...../...../...../...../..##./..##.", "!": "..#../..#../..#../..#../..#../...../..#..",
    "+": "...../..#../..#../#####/..#../..#../.....", ":": "...../..#../...../...../..#../...../.....",
    "-": "...../...../...../#####/...../...../.....", "_": "...../...../...../...../...../...../#####",
    ",": "...../...../...../...../..##./...#./..#..", ">": "#..../.#.../..#../...#./..#../.#.../#....",
}
FONT = {ch: rows.split("/") for ch, rows in _FONT.items()}


def runs(row):
    """Yield (start, end, char) for each run of identical non-space characters."""
    i = 0
    while i < len(row):
        ch = row[i]
        if ch == " ":
            i += 1
            continue
        k = i
        while k < len(row) and row[k] == ch:
            k += 1
        yield i, k, ch
        i = k


def is_star(name):
    return (name or "").upper() == STAR_NAME


def mix(c1, c2, t):
    """Blend two 0xRRGGBB colours; t is snapped to 6 steps so the text images stay cacheable."""
    t = round(max(0.0, min(1.0, t)) * 5) / 5
    out = 0
    for shift in (16, 8, 0):
        a, b = (c1 >> shift) & 255, (c2 >> shift) & 255
        out |= round(a + (b - a) * t) << shift
    return out


def shine(i, t, n):
    """0..1 highlight sweeping across letter i of an n-letter name (t = sweep progress)."""
    return max(0.0, 1 - abs(i - ((t % (n + 8)) - 4)) / 2.2)
