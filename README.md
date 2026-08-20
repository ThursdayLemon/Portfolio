# reikocui.com — static site

Portfolio site for Liling Cui. Structure, typography scale and interaction
patterns follow rodrigosens.com; all content, imagery and copy are Liling's own.

## Run it

```bash
cd ~/Documents/reikocui-site
python3 -m http.server 8899
# open http://localhost:8899
```

Opening `index.html` directly with `file://` mostly works, but a couple of
things (page-transition links, the theme toggle's `localStorage`) behave better
over HTTP.

## Structure

```
index.html                  home — pill nav + hover backdrop + giant title
about.html                  about / CV
<slug>.html                 one page per project (6)
build.py                    regenerates every HTML file from the data at the top
manifest.json               per project: the images in reading order, recovered
                            from reikocui.com's page model ({src, kind})
assets/css/style.css        the whole design system
assets/js/app.js            all interaction
assets/img/<slug>/          project images (102 files, pulled from the live site)
assets/cursor-*.svg         custom dot cursor
```

### Editing content

All copy, project order, sidebar metadata and section labels live in the
`PROJECTS` / `ABOUT_*` blocks at the top of `build.py`. Change them and run:

```bash
python3 build.py
```

Editing the `.html` files by hand works too, but a rebuild overwrites them.

### Adding a project

1. Drop its images into `assets/img/<slug>/`
2. Add rows under `"<slug>"` in `manifest.json`, **in the order they should be
   read**. Each row is `{"src": "assets/img/<slug>/file.jpg", "kind": "el"}`.
   (`kind` records whether the image opened a section on the original site. It
   is kept for reference and no longer affects the layout.)
3. Add an entry to `PROJECTS` in `build.py`
4. Add its cover filename to `COVERS`
5. `python3 build.py`

The nav shows the first 6 pills and reveals the rest behind a `+` button — set
by `show="6"` on `<nav class="menu-projects">` in `build.py`. Past six projects
that button appears automatically.

## Design system

| Token | Value |
|---|---|
| Grid | 6 columns, 20px gap, 20px page padding |
| Colours | `--white: #fff` / `--black: #282828`, swapped in dark mode |
| Muted | `#919191` |
| Display type | 96px / weight 300 (56px under 700px wide) |
| Body type | 18px, line-height 1.5–1.6 |
| Pills | 40px tall, 20px radius, 1px border, 24px type — same size on mobile |

### Fonts

The reference uses **Tiempos Fine** and **Tiempos Text** — commercial faces from
Klim Type Foundry. This build falls back to **Instrument Serif** (display) and
**Newsreader** (body) from Google Fonts, which sit close in colour and contrast.

To switch to the real thing once licensed: drop
`TiemposFine-Light.woff2` and `TiemposText-Regular.woff2` into `assets/fonts/`.
The `@font-face` rules at the top of `style.css` already point there and will
take over automatically — no other change needed.

## Page hierarchy

Only the home page carries the pill nav. Project and About pages drop it — the
Back button and the name in the top left are the way out. This is the
reference's model, on desktop and mobile alike.

Project pages put the title and the metadata sidebar on the **left**, the intro
**top right** (columns 3–5), and every image on the **right four columns** —
one uniform width, never full-bleed. Heights follow each image's own
proportions, so nothing is cropped.

Project pages carry no headings over the image sequence: the images run in the
order they do on reikocui.com and nothing is captioned that was not there.

## Interaction

- **Pill hover** (desktop only, >1000px): the project's cover fades in full-bleed
  behind a 25% dither wash, and the giant title swaps from the name to the
  project name.
- **Marquee**: if the title is wider than the viewport it scrolls seamlessly.
  Speed is `0.005s` per pixel of one repetition, matching the reference.
- **Theme**: follows the OS by default, and remembers a manual choice in
  `localStorage`. Set before first paint so there is no flash.
- **Page transitions**: internal links fade the page out before navigating.
- **Scroll-in**: `data-aos="fade-up"` via IntersectionObserver. Scoped to `.js`
  so nothing is invisible if scripting fails.
- **Dither wash**: `assets/dither-light.png` / `dither-dark.png` are 2x2 tiles
  with one opaque pixel and three transparent — a pixel-exact rebuild of the
  reference's `white.gif` / `darkgrey.gif`. Tiled at `2px 2px` with
  `image-rendering: pixelated`, it lays a 25% white (or #282828) dot screen over
  the photo so the nav stays legible and the image keeps its texture.
- **Top-right button**: a 28px black ringed planet that expands into a "Creative
  work" pill on hover and links to lilingcui.com. Body and ring flip to the
  page colour together once the pill is behind them.

## Still to do

- **Creative Campaign section.** Deliberately out of scope — only the six UI/UX
  projects are built. The eight Creative projects still live on the old site.
- **Image order** comes straight from reikocui.com and is never reshuffled. All
  images share one width; reordering means reordering the rows in
  `manifest.json`.
- **Video.** The reference uses looping Vimeo backgrounds on hover. All covers
  here are stills or GIFs; swapping any `.bg-image` for an `<iframe>` works.
