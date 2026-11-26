"""PyPython painter: turns drawing calls into a flat list of commands for the JavaScript painter
(painter.js). Text and sprites are rendered once into small images and cost one command per use."""
from array import array

from js import pypRenderer              # the JavaScript painter (painter.js)
from pyodide.ffi import to_js

from art import FONT, INK, runs
from rules import COLS

PX = 4                      # one "art pixel" on screen
ART = 6                     # art pixels per grid cell
ARTB = COLS * ART           # board size in art pixels
WRAP_TOL = 2                # art px a part may overhang a wall in Teleport mode before it counts as crossing

RECT, BLIT, BOX = 0, 1, 2          # command types; every command is 8 ints


class Painter:
    def __init__(self):
        self.cmds = array("i")
        self.images = {}            # cache key -> (image id, width, height) for images living in JS
        self.next_image = 1
        self.teleport = False

    # ----- primitives -----
    def rect(self, x0, y0, x1, y1, color):
        self.cmds.extend((RECT, x0, y0, x1 - x0, y1 - y0, color, 0, 0))

    def box(self, x0, y0, x1, y1, fill, outline, width):
        self.cmds.extend((BOX, x0, y0, x1 - x0, y1 - y0, fill, outline, width))

    def blit(self, image_id, x, y):
        self.cmds.extend((BLIT, image_id, x, y, 0, 0, 0, 0))

    def register(self, w, h, rects):
        """Render rects [(x, y, w, h, colour), ...] once into an image kept by the JS painter."""
        image_id, self.next_image = self.next_image, self.next_image + 1
        pypRenderer.define(image_id, w, h, to_js(array("i", rects)))
        return image_id

    # ----- text (5x7 bitmap font, rendered once per string/size/colour) -----
    def text_img(self, s, scale, color):
        key = ("t", s, scale, color)
        img = self.images.get(key)
        if img is None:
            s = s.upper()
            w, h = max(1, (len(s) * 6 - 1) * scale), 7 * scale
            rects = []
            for n, ch in enumerate(s):
                for y, row in enumerate(FONT.get(ch, ())):
                    for i, k, _ in runs(row.replace(".", " ")):
                        rects += ((n * 6 + i) * scale, y * scale, (k - i) * scale, scale, color)
            img = self.images[key] = (self.register(w, h, rects), w, h)
        return img

    def text(self, s, x, y, scale=2, color=INK, anchor="nw", shadow=None):
        image_id, w, _ = self.text_img(s, scale, color)
        x = round(x - w / 2) if anchor == "n" else round(x - w) if anchor == "ne" else round(x)
        y = round(y)
        if shadow is not None:
            self.blit(self.text_img(s, scale, shadow)[0], x + scale, y + scale)
        self.blit(image_id, x, y)

    # ----- sprites -----
    def sprite(self, art, cx, cy, unit=PX):
        """Draw pixel art centred on screen point (cx, cy), snapped to a grid of `unit` px."""
        rows, pal = art
        w, h = max(map(len, rows)), len(rows)
        key = ("s", rows, tuple(pal.items()), unit)
        img = self.images.get(key)
        if img is None:
            rects = []
            for j, row in enumerate(rows):
                for i, k, ch in runs(row):
                    rects += (i * unit, j * unit, (k - i) * unit, unit, pal[ch])
            img = self.images[key] = (self.register(w * unit, h * unit, rects), w * unit, h * unit)
        self.blit(img[0], round(cx / unit - w / 2) * unit, round(cy / unit - h / 2) * unit)

    # ----- board-space rectangles (art pixels), always clipped to the board -----
    def offsets(self, x, y, w, h):
        """Wrap copies a rect needs (art px). Teleport only, and only for a real crossing:
        a part overhanging a wall by a pixel or two must not peek out on the far side."""
        def axis(a, size):
            offs = [0]
            if self.teleport:
                if a + size - ARTB > WRAP_TOL:
                    offs.append(-ARTB)
                if -a > WRAP_TOL:
                    offs.append(ARTB)
            return offs
        return axis(x, w), axis(y, h)

    def art(self, ax, ay, w, h, color, offs=None):
        xs, ys = offs or ([0], [0])
        for ox in xs:
            for oy in ys:
                x0, y0 = max(ax + ox, 0), max(ay + oy, 0)
                x1, y1 = min(ax + ox + w, ARTB), min(ay + oy + h, ARTB)
                if x0 < x1 and y0 < y1:
                    self.rect(x0 * PX, y0 * PX, x1 * PX, y1 * PX, color)
