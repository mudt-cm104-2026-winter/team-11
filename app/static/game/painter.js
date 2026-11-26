"use strict";
/* Thin JavaScript painter. Python (painter.py) sends a flat list of drawing commands; this file only
   draws them. No game logic lives here.
   Every command is 8 integers: RECT = fill a rectangle, BLIT = draw a cached image, anything else = a box
   with a border. */
(() => {
  const images = new Map(), colors = new Map();
  const css = n => {
    let c = colors.get(n);
    if (!c) { c = "#" + n.toString(16).padStart(6, "0"); colors.set(n, c); }
    return c;
  };

  // Called by Python to register a pre-rendered image (text, sprites): a list of [x, y, w, h, colour] rectangles.
  window.pypRenderer = {
    define(id, w, h, rects) {
      const c = document.createElement("canvas");
      c.width = w; c.height = h;
      const g = c.getContext("2d");
      for (let i = 0; i < rects.length; i += 5) {
        g.fillStyle = css(rects[i + 4]);
        g.fillRect(rects[i], rects[i + 1], rects[i + 2], rects[i + 3]);
      }
      images.set(id, c);
    },
  };

  const RECT = 0, BLIT = 1;
  window.pypPaint = (ctx, c) => {
    ctx.imageSmoothingEnabled = false;
    for (let i = 0; i < c.length; i += 8) {
      const op = c[i];
      if (op === RECT) {
        ctx.fillStyle = css(c[i + 5]);
        ctx.fillRect(c[i + 1], c[i + 2], c[i + 3], c[i + 4]);
      } else if (op === BLIT) {
        ctx.drawImage(images.get(c[i + 1]), c[i + 2], c[i + 3]);
      } else {
        ctx.fillStyle = css(c[i + 5]);
        ctx.fillRect(c[i + 1], c[i + 2], c[i + 3], c[i + 4]);
        ctx.strokeStyle = css(c[i + 6]); ctx.lineWidth = c[i + 7];
        ctx.strokeRect(c[i + 1], c[i + 2], c[i + 3], c[i + 4]);
      }
    }
  };
})();
