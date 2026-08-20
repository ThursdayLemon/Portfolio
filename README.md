# reikocui.com — static site

Portfolio site for Liling Cui. Structure, typography scale and interaction
patterns follow rodrigosens.com; all content, imagery and copy are Liling's own.

## Deploying

The site is plain static files with no build step at serve time and no external
requests, so any static host works. `.nojekyll` tells GitHub Pages to serve the
files as-is rather than running them through Jekyll.

Every path in the HTML is relative, so it works both at a domain root and under
a `/repo-name/` subpath.

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
CNAME                       the custom domain GitHub Pages serves from
index.html                  home — pill nav + hover backdrop + giant title
about.html                  about / CV
<slug>.html                 one page per project (6)
build.py                    regenerates every HTML file from the data at the top
manifest.json               per project: the images in reading order, recovered
                            from reikocui.com's page model ({src, kind})
assets/css/style.css        the whole design system
assets/js/app.js            all interaction
assets/img/<slug>/          project images, pulled from the live site
assets/cursor-*.svg         custom dot cursor
assets/LilingCui_CV.pdf     the CV the bottom-right button downloads
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
| Colours | `--white: rgb(var(--bg))` / `--black: #282828`, swapped in dark mode |
| Page colour | `--bg`, an `"r g b"` triple — default `255 255 255` |
| Muted | `#919191` |
| Display type | 96px / weight 300 — **same at every breakpoint** |
| Body type | 18px, line-height 1.5–1.6 |
| Pills | 40px tall, 20px radius, 1px border, 24px type — same size on mobile |

### Fonts

**Tiempos Fine** (display) and **Tiempos Text** (body), self-hosted from
`assets/fonts/` in woff2 / woff / ttf. No webfont CDN is used, so the site has
no external requests at all.

Both are commercial faces from **Klim Type Foundry** and the files here were
taken from the reference site. **A licence still needs buying** before this
goes live — see klim.co.nz. Nothing else has to change when you buy it; the
files simply become properly licensed.

Each face ships as one static weight, declared `font-weight: 100 900` so the
browser maps every requested weight onto the real file rather than
synthesising a fake bold.

### Paired images

A manifest row can hold two or more images that share one image slot:

```json
{ "kind": "group", "gap": 6,
  "items": [ { "src": "...", "grow": 0.2782, "caption": "Before" },
             { "src": "...", "grow": 0.2931, "caption": "After"  } ] }
```

`grow` is the image's aspect ratio (width ÷ height). `build.py` normalises the
row's grow factors to sum to 100 and emits them as `flex-grow`, so widths land
in proportion and the images come out the same height — a justified row filling
exactly the width of a single image. Normalising matters: raw ratios below 1
would make flex hand out only that fraction of the row.

`caption` is optional and renders above the image. `gap` defaults to 6px.
On phones the row keeps its side-by-side arrangement — so a Before/After
comparison still reads — but spans the full width, and the flex ratios scale
the images to whatever fits.

### Per-page background

A project can recolour its whole page by adding a `"bg"` key to its entry in
`PROJECTS`, as an `"r g b"` triple:

```python
"bg": "255 250 244",   # L'Artisan, sampled from its own slide artwork
```

In use: L'Artisan `255 250 244` (#fffaf4), Volkswagen and BMW `254 253 249`
(#fefdf9). All three were sampled from artwork already on the page.

`build.py` emits that as `<style>:root { --bg: ... }</style>` in the page head.
`:root` outranks the stylesheet's `html` rule but loses to `html.dark-theme`,
so the custom colour applies in light mode and dark mode is untouched. The
giant title's fade-out gradient mixes from the same `--bg`, so it never leaves
a white seam over a recoloured page.

### Type scale

Taken verbatim from the reference, which uses **one scale at every viewport** —
no `font-size` appears in any of its media queries. So a 96px title marquees
across a phone screen instead of shrinking. Verified against a live render of
rodrigosens.com: title ink, cap height, nav left edge and header baseline all
land on identical pixels.

## Page hierarchy

Only the home page carries the pill nav. Project and About pages drop it — the
Back button and the name in the top left are the way out. This is the
reference's model, on desktop and mobile alike.

On phones a project page puts the giant title *in the flow*, between the intro
and the images, rather than pinned over the first screen. The intro runs well
past one screen at that width, so a pinned title landed in the middle of it and
its gradient hid the lines behind.

**About** follows the reference's own about page: one prose column at columns
3–5, standalone links, a portrait, and the giant title (reading "About") fixed
bottom left. Continuous prose, no headings or tables.

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
- **Marquee**: if the title is wider than the viewport it scrolls seamlessly,
  at `0.005s` per pixel of one repetition, matching the reference. Driven by
  `element.animate()` rather than a CSS `@keyframes`: the distance is a measured
  pixel value, and Safari does not reliably resolve a custom property used
  inside `@keyframes`, which left the title motionless on iOS.
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
- **CV Download**: on the About page only, fixed bottom right — same pill as
  the Back button, with the page colour behind it so it stays readable over
  whatever scrolls under it. The `download` attribute makes the browser save the file
  rather than open it, and also tells the page-transition handler to leave the
  click alone. On phones the title band owns the bottom 134px, so the pill sits
  above it. It is emitted by `build_about()` rather than by `FOOT`, so no other
  page carries it. To swap the CV, replace `assets/LilingCui_CV.pdf` — or point
  `CV_FILE` in `build.py` somewhere else.
- **Top-right button**: a 36px black ringed planet with sparkles that expands
  into a "Creative work" pill on hover and links to lilingcui.com. The icon is
  layered rather than knocked out — `.planet-ink` / `.planet-ring` carry the
  drawing, `.planet-bg` / `.planet-bg-stroke` carry the page colour that cases
  the ring where it passes behind the planet and punches the highlights. On
  hover the two roles swap, so it reads on the dark pill too. The ring and
  sparkles are held within a radius of 20 viewBox units, which is what keeps
  them inside the pill's rounded end at this size.

## Still to do

- **Font licence.** Tiempos Fine / Tiempos Text are in `assets/fonts/` but not
  yet licensed. Buy from Klim Type Foundry before launch.
- **Creative Campaign section.** Deliberately out of scope — only the six UI/UX
  projects are built. The eight Creative projects still live on the old site.
- **Image order** comes straight from reikocui.com and is never reshuffled. All
  images share one width; reordering means reordering the rows in
  `manifest.json`.
- **Video covers.** ZMAX's cover is an MP4 (`COVER_VIDEOS` in `build.py`); the
  rest are stills. A video cover ships `preload="none"` with the still as its
  poster, so the file is only fetched when the pill is first hovered — app.js
  calls `play()` there and pauses on the way out.
