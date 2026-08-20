#!/usr/bin/env python3
"""
Static site generator for reikocui.com.

Emits index.html, about.html and one page per project into the folder this
file lives in. Edit the CONTENT block below and re-run:  python3 build.py
"""

import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "Liling Cui"
CREATIVE_LABEL = "Creative work"
CREATIVE_URL = "https://lilingcui.com"

# ---------------------------------------------------------------- content

PROJECTS = [
    {
        "slug": "lartisan-parfumeur-pdp-enhancement",
        "pill": "L'Artisan Parfumeur",
        "title": "L'Artisan Parfumeur PDP Enhancement",
        # sampled from slide3-kggydka3Qfcg9Qb8.jpeg, which is #fffaf4 across
        # 83% of its area and identical in all four corners
        "bg": "255 250 244",
        "intro": [
            "As the white-label platform has been live for two years, this project "
            "focuses on general updates and enhancements. Based on insights gathered "
            "through Contentsquare, we identified opportunities to improve the Product "
            "Detail Page experience by reducing friction points that may impact customer "
            "conversion and engagement, while also supporting stronger business "
            "performance and sales growth.",
            "Working closely with the CRO team: gathering data insights, running internal "
            "workshops, user research, UI research and idea presentation.",
        ],
        "meta": [
            ("Role", ["Product Designer"]),
            ("Brand", ["L'Artisan Parfumeur", "Penhaligon's", "KAMA Ayurveda", "LOTOS"]),
            ("Scope", ["Data insights", "Workshop", "User research", "UI research"]),
        ],
    },
    {
        "slug": "white-label-project",
        "pill": "White Label",
        "title": "White Label Design System",
        "intro": [
            "A white label project aimed at building and developing a comprehensive "
            "designed platform and core components for different in-house brands, "
            "including L'Artisan Parfumeur, Penhaligon's, KAMA Ayurveda, LOTOS and "
            "Dr. Barbara Sturm.",
            "Upgraded the entire website and developed a comprehensive design system for "
            "the in-house brands. Collaborated closely with development, brand and "
            "e-commerce teams while presenting innovative ideas across multiple strategic "
            "directions.",
            "We structured the entire site in Figma into four collections, each containing "
            "related pages and features. This approach kept a clear hierarchy, streamlined "
            "design iterations, and made it easy for the team to navigate and collaborate.",
        ],
        "meta": [
            ("Role", ["Product Designer"]),
            (
                "Brand",
                [
                    "L'Artisan Parfumeur",
                    "Penhaligon's",
                    "KAMA Ayurveda",
                    "LOTOS",
                    "Dr. Barbara Sturm",
                ],
            ),
            (
                "Scope",
                [
                    "Design system",
                    "Design tokens",
                    "Foundation",
                    "Typography",
                    "Colour palette",
                    "Components",
                    "UAT",
                    "UET",
                ],
            ),
        ],
    },
    {
        "slug": "bmw-loyalty-programme",
        # sampled from design-1-H08vkdmLly5hIBJT.jpg: #fefdf9, identical in all four corners
        "bg": "254 253 249",
        "pill": "BMW Loyalty",
        "title": "BMW Loyalty Programme",
        "intro": [
            "The programme was created from the synergetic efforts of the BMW Group, "
            "facilitating an enriched lifestyle beyond driving for consumers.",
            "BMW Group aimed to develop an app to enhance the car purchasing experience "
            "and provide long-term services after purchase, including after-sales support. "
            "The app was designed specifically for BMW owners, reflecting the premium "
            "experience of the BMW ecosystem. Key brand differentiators \u2014 futuristic, "
            "innovative, premium and responsible \u2014 guided the overall tone, activities and "
            "user experience of the loyalty programme.",
            "Another important factor was delivering a state-of-the-art mobile experience "
            "tailored to the Chinese market. The app merges both Western and Chinese design "
            "influences to create a seamless and comprehensive user experience.",
        ],
        "meta": [
            ("Agency", ["Serviceplan"]),
            ("Role", ["Digital Art Director"]),
            ("Client", ["BMW CRM"]),
            ("Scope", ["0\u20131 build", "UI/UX", "Prototype", "Wireframe"]),
        ],
    },
    {
        "slug": "volkwagen-idhub",
        # sampled from vw3-hJO7s5DzPoxih9FV.jpg: #fefdf9, identical in all four corners
        "bg": "254 253 249",
        "pill": "Volkswagen ID. Hub",
        "title": "Volkswagen ID. Hub",
        "intro": [
            "The goal of this project is to help Chinese consumers gain a deeper "
            "understanding of Volkswagen's electric vehicles through this official "
            "platform. The platform showcases everything from concept cars and "
            "Volkswagen's MEB electric vehicle technology to the continuous release of new "
            "car information.",
            "It also provides a range of community services, fostering interactions both "
            "between Volkswagen and its consumers, and among consumers themselves \u2014 "
            "establishing a direct relationship with consumers via the official platform.",
            "Content first, mobile first.",
        ],
        "meta": [
            ("Agency", ["Cheil"]),
            ("Brand", ["Volkswagen"]),
            ("Role", ["Creative Art Director", "Product Designer"]),
            (
                "Scope",
                [
                    "Campaign idea",
                    "Content design",
                    "UI/UX design",
                    "Interactive design",
                    "Wireframing",
                    "Prototyping",
                    "Usability tests",
                    "Content structure",
                ],
            ),
        ],
    },
    {
        "slug": "kama-web-facelift",
        "pill": "KAMA Facelift",
        "title": "KAMA Web UI Upgrade",
        "intro": [
            "The brand required a UI facelift for the current website. After conducting an "
            "in-depth analysis and reviewing visual references, we identified that many of "
            "the issues stemmed from underdeveloped brand assets rather than structural UX "
            "problems.",
            "Given the limited project budget, our strategy focused on refining existing "
            "visual assets and introducing subtle but impactful design enhancements to "
            "elevate the overall experience and create a more premium feel.",
            "As part of the white label ecosystem, KAMA was the first brand to go live. "
            "Since its initial launch, several new features have been developed across the "
            "platform. We took this opportunity to incorporate those newly built features "
            "into the facelift, ensuring the refreshed experience not only looked more "
            "refined but also aligned with the latest product capabilities.",
        ],
        "meta": [
            ("Role", ["UI Design", "UAT", "User testing"]),
            ("Brand", ["KAMA Ayurveda"]),
            ("Pages", ["Homepage", "Product detail page", "Sitewide UI"]),
        ],
    },
    {
        "slug": "zmax-web-design",
        "pill": "ZMAX",
        "title": "ZMAX Web Design",
        "intro": [
            "ZMAX is a generative series of 3D NFT art pieces, intricately designed and set "
            "in the far future where the lines between the virtual and physical worlds have "
            "blurred.",
            "Idea, interactive design, animation, UI/UX design and web design.",
        ],
        "meta": [
            ("Client", ["ZMAX"]),
            ("Role", ["UI/UX Designer", "Interactive Design"]),
            ("Scope", ["Idea", "Interactive design", "Animation", "Web design"]),
        ],
    },
]

ABOUT_TEXT = [
    "I’m a Product Designer and Creative Art Director based in London, with over "
    "10 years across luxury e-commerce, automotive and technology brands, delivering "
    "end-to-end digital products.",

    "I’m currently Senior Product Designer at PUIG, working on Penhaligon’s, "
    "L’Artisan Parfumeur and Uriage. Before that I was Senior Art Director at "
    "Ogilvy on Huawei, Group Head of Art at Cheil on Samsung and Volkswagen, Senior "
    "UI/UX Designer at Serviceplan on BMW and Porsche CRM, Senior Digital Designer at "
    "VML on BMW and MINI, and Digital UI Designer at Interone on BMW, Bosch and Canon.",

    "My work centres on wireframing, prototyping, UAT, data-driven optimisation and "
    "new feature development — building scalable design systems and product "
    "foundations aligned with brand guidelines and tonality, working closely with "
    "product, engineering and commercial teams to drive measurable business impact. "
    "Coming from advertising, where I led creative campaigns for BMW, Porsche, MINI, "
    "Samsung and HUAWEI, I bring a deep understanding of UI, brand tone and visual "
    "storytelling into conversion-focused product design.",

    "Alongside product work I’m a documentary and fashion photographer, with a "
    "focus on religious culture, public health, and women and girls’ issues. After "
    "many years visiting Tibetan regions I document and explore religious practice, "
    "paying particular attention to cultural erosion and the preservation of minority "
    "traditions. The work has shown at the London Contemporary Art Fair, VENICE "
    "CANVAS, the Julia Margaret Cameron Award and the Arte Laguna Prize, and was "
    "written up by "
    '<a href="https://www.itsnicethat.com/articles/liling-cui-project-photography-150223" '
    'target="_blank" rel="noopener">It’s Nice That</a> and '
    '<a href="https://www.itsliquid.com/interview-liling-cui.html" target="_blank" '
    'rel="noopener">ITSLIQUID</a>.',
]

# Trailing block of standalone links, one per line, as on the reference.
ABOUT_LINKS = [
    ("Creative work", CREATIVE_URL),
]

# ---------------------------------------------------------------- helpers

with open(os.path.join(ROOT, "manifest.json")) as fh:
    MANIFEST = json.load(fh)

COVERS = {
    "white-label-project": "ecommerce-white-label-hostinger-website-builder-kopijtpacm10jqqz-Gi3H4V5oaueiGZ9J.jpg",
    "lartisan-parfumeur-pdp-enhancement": "portfolio-liling-cui-IZwBdF6kmGo51UQZ.gif",
    "bmw-loyalty-programme": "portfolio-liling-cui-CWf0nmMIYvAjCvkP.jpg",
    "volkwagen-idhub": "portfolio-liling-cui-B2Ny3sgGYGVtTypH.jpg",
    "kama-web-facelift": "portfolio-liling-cui-vFulycDlR9ORgaCJ.jpg",
    "zmax-web-design": "zmax-IRzhIGILPgQsXzVl.gif",
}

e = html.escape


def head(title, description, extra_body_class="", bg=None):
    # a page can recolour itself by overriding --bg; :root outranks the
    # stylesheet's html rule but still loses to .dark-theme, so dark mode
    # is left alone
    page_bg = f"\n<style>:root {{ --bg: {bg}; }}</style>" if bg else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="preload" href="assets/fonts/TiemposFine-Light.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/TiemposText-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/style.css">{page_bg}
<script>
  // mark that scripting is on, and set the theme before first paint
  (function () {{
    document.documentElement.classList.add('js');
    try {{
      var s = localStorage.getItem('theme');
      var d = s ? s === 'dark'
                : window.matchMedia('(prefers-color-scheme: dark)').matches;
      if (d) document.documentElement.classList.add('dark-theme');
    }} catch (e) {{}}
  }})();
</script>
</head>
<body class="{extra_body_class}">"""


# Ringed planet with sparkles. Layered rather than knocked out, so each part
# can flip colour independently when the label pill expands behind it:
# .planet-ink is the drawing, .planet-bg is the page colour used to case the
# ring where it passes behind the planet and to punch the highlights.
CONTACT_SVG = (
    '<svg viewBox="0 0 40 40" aria-hidden="true">'
    '<ellipse class="planet-ink" cx="35.0" cy="8.2" rx="0.95" ry="1.55" transform="rotate(28 35.0 8.2)"/>'
    '<ellipse class="planet-ink" cx="6.2" cy="13.0" rx="0.85" ry="1.4" transform="rotate(22 6.2 13.0)"/>'
    '<ellipse class="planet-ink" cx="9.4" cy="32.6" rx="0.85" ry="1.4" transform="rotate(-26 9.4 32.6)"/>'
    '<ellipse class="planet-ink" cx="35.6" cy="26.6" rx="0.9" ry="1.45" transform="rotate(26 35.6 26.6)"/>'
    '<path class="planet-ring" d="M37.29 13.71A18.4 5.2 -20.0 1 1 2.71 26.29'
    'A18.4 5.2 -20.0 1 1 37.29 13.71Z"/>'
    '<circle class="planet-bg-stroke" cx="20" cy="20" r="12.3" stroke-width="3.2"/>'
    '<circle class="planet-ink" cx="20" cy="20" r="12.3"/>'
    '<path class="planet-bg-stroke" stroke-width="4" d="M30.67 20.81A18.4 5.2 -20.0 1 1 6.71 20.86"/>'
    '<path class="planet-ring" d="M30.67 20.81A18.4 5.2 -20.0 1 1 6.71 20.86"/>'
    '<path class="planet-bg" d="M13.6 12.9a11 11 0 0 1 8.0-3.6 0.95 0.95 0 0 1 0.05 1.9'
    ' 9.1 9.1 0 0 0-6.6 3.0 0.95 0.95 0 0 1-1.45-1.3z"/>'
    '<circle class="planet-bg" cx="15.2" cy="17.2" r="1.05"/>'
    "</svg>"
)


def header(current, show_back=False, home_link=False, show_projects=True):
    """Header shared by every page. `current` is the active slug, if any.

    Only the home page carries the pill nav — project and About pages drop it,
    the way the reference does, leaving Back / the name as the way out.
    """
    left_label = NAME if home_link else "About"
    left_href = "index.html" if home_link else "about.html"

    back = ""
    if show_back:
        arrow = '<svg viewBox="0 0 21 18"><path d="M8.38 1 1 9m0 0 7.38 8M1 9h20"/></svg>'
        back = f"""
      <div class="btn">
        <a href="index.html" class="back-btn back">{arrow}<span>Back</span></a>
        <a href="#" class="back-btn top">{arrow}<span>Top</span></a>
      </div>"""

    nav = ""
    if show_projects:
        pills = "\n".join(
            '        <a href="{slug}.html" item="{slug}"{cls}>{label}</a>'.format(
                slug=p["slug"],
                label=e(p["pill"]),
                cls=' aria-current="page"' if p["slug"] == current else "",
            )
            for p in PROJECTS
        )
        nav = f"""
      <nav class="menu-projects" show="6" aria-label="Projects">
{pills}
        <button class="load-more hide-and-show" aria-label="Show more projects"
                aria-expanded="false"><span>Show more projects</span></button>
      </nav>"""

    return f"""
    <header class="menu">
      <div class="menu-about">
        <a href="{left_href}">{e(left_label)}</a>
        <button class="theme-toggle" aria-label="Toggle dark mode">
          <span class="toggle"></span>
        </button>
      </div>{back}{nav}
      <div class="menu-contact">
        <a href="{CREATIVE_URL}">
          <span class="btn-label">{CREATIVE_LABEL}</span>
          {CONTACT_SVG}
        </a>
      </div>
    </header>
"""


FOOT = """
<script src="assets/js/app.js"></script>
</body>
</html>
"""


IMG = '<img src="{src}" alt="" loading="lazy" decoding="async">'


def figure(src):
    return f'        <figure data-aos="fade-up">{IMG.format(src=src)}</figure>'


def group(row):
    """A justified row of images sharing the width of a single image slot.

    flex-grow is each image's aspect ratio, so the widths land in proportion
    and every image in the row ends up the same height.
    """
    # grow factors are normalised to sum to 100: only their ratio matters, and
    # a sum below 1 would make flex hand out just that fraction of the row
    total = sum(it["grow"] for it in row["items"]) or 1
    out = [f'        <div class="group" data-aos="fade-up" '
           f'style="gap:{row.get("gap", 6)}px">']
    for it in row["items"]:
        cap = f'<figcaption>{e(it["caption"])}</figcaption>' if it.get("caption") else ""
        out.append(f'          <figure style="flex-grow:{it["grow"] / total * 100:.4f}">'
                   f'{cap}{IMG.format(src=it["src"])}</figure>')
    out.append("        </div>")
    return "\n".join(out)


# ---------------------------------------------------------------- pages


def build_home():
    titles = [
        f'      <span class="title name" data-title="{e(NAME)}">{e(NAME)}</span>'
    ]
    for p in PROJECTS:
        titles.append(
            '      <span class="title" item="{slug}" data-title="{t}">{t}</span>'.format(
                slug=p["slug"], t=e(p["title"])
            )
        )

    bgs = []
    for p in PROJECTS:
        cover = COVERS[p["slug"]]
        src = f"assets/img/{p['slug']}/{cover}"
        bgs.append(
            f'    <div class="bg-image" item="{p["slug"]}" '
            f"style=\"background-image:url('{src}')\"></div>"
        )

    doc = head(
        f"{NAME} — Product Designer",
        "Product Designer and Creative Art Director. Selected UI/UX work for PUIG, "
        "BMW, Volkswagen and KAMA Ayurveda.",
        "home",
    )
    doc += header(current=None)
    doc += """
    <main>
      <h1 class="title-container" data-aos="fade-up">
{titles}
      </h1>
    </main>

    <div class="bg" aria-hidden="true">
{bgs}
      <div class="bg-veil"></div>
      <div class="bg-overlay"></div>
    </div>
""".format(
        titles="\n".join(titles), bgs="\n".join(bgs)
    )
    doc += FOOT
    return doc


def build_project(p):
    slug = p["slug"]
    rows = [r for r in MANIFEST.get(slug, [])
            if not r.get("src", "").endswith(COVERS[slug])]

    sidebar = ['      <aside class="sidebar" data-aos="fade-up">']
    for heading, items in p["meta"]:
        sidebar.append(f"        <h2>{heading}</h2>")
        sidebar.append("        <ul>")
        for it in items:
            sidebar.append(f"          <li>{e(it)}</li>")
        sidebar.append("        </ul>")
    sidebar.append("      </aside>")

    body = [group(r) if r.get("kind") == "group" else figure(r["src"]) for r in rows]

    intro = "\n".join(f"          <p>{e(t)}</p>" for t in p["intro"])

    doc = head(
        f"{p['title']} — {NAME}",
        p["intro"][0][:180],
        "project-page",
        bg=p.get("bg"),
    )
    doc += header(current=slug, show_back=True, home_link=True, show_projects=False)
    doc += f"""
    <main class="project">
      <div class="text resume">
        <div class="text-content">
{intro}
        </div>
      </div>

      <h1 data-aos="fade-up">
        <span class="title name" data-title="{e(p['title'])}">{e(p['title'])}</span>
      </h1>

      <div class="content">
{chr(10).join(sidebar)}
{chr(10).join(body)}
        <div class="spacer"></div>
      </div>
    </main>
"""
    doc += FOOT
    return doc


def build_about():
    """Same shape as the reference's about page: one prose column at the top
    right, standalone links under it, a portrait, and the giant title pinned
    bottom left. No headings, no tables — it reads as continuous prose."""
    paras = "\n".join(f"          <p>{t}</p>" for t in ABOUT_TEXT)
    links = "<br>\n          ".join(
        f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>'
        for t, u in ABOUT_LINKS
    )
    photos = MANIFEST.get("about", [])
    portrait = (
        f'          <p><img src="{photos[0]["src"]}" alt="" loading="lazy"></p>'
        if photos
        else ""
    )

    doc = head(
        f"About — {NAME}",
        "Product Designer and Creative Art Director with 10+ years across luxury "
        "e-commerce, automotive and technology brands.",
        "about-page",
    )
    doc += header(current=None, home_link=True, show_projects=False)
    doc += f"""
    <main class="about">
      <div class="text" data-aos="fade-up">
{paras}
          <p>{links}</p>
{portrait}
      </div>

      <h1 data-aos="fade-up">
        <span class="title name" data-title="About">About</span>
      </h1>
    </main>
"""
    doc += FOOT
    return doc


def write(name, content):
    path = os.path.join(ROOT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"  {name}  ({len(content) // 1024} KB)")


if __name__ == "__main__":
    print("building:")
    write("index.html", build_home())
    write("about.html", build_about())
    for proj in PROJECTS:
        write(f"{proj['slug']}.html", build_project(proj))
    print("done.")
