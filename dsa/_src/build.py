"""Builds the DSA Field Guide pages from topics/*.py.

Run from anywhere:  python3 dsa/_src/build.py
Each topic module defines META, BODY, PROBLEMS, QUIZ (see topics/arrays.py).
The folder starts with "_" so GitHub Pages (Jekyll) does not publish it.
"""
import html, importlib.util, json, pathlib, re, sys

SRC = pathlib.Path(__file__).resolve().parent
OUT = SRC.parent

# Reading order. "big-o" is a hand-written page that already exists.
ORDER = ["big-o", "arrays", "strings", "linked-lists", "trees", "stacks-queues", "graphs",
         "dp", "heaps", "hashing", "bits", "sorting", "searching",
         "patterns", "python", "interview",
         "sd-basics", "sd-scaling", "sd-caching", "sd-data", "sd-async", "sd-reliability",
         "sd-cases-1", "sd-cases-2", "sd-interview", "resources"]
STATIC = {"big-o": {"slug": "big-o", "title": "Big-O", "week": "Week 0",
                    "blurb": "How code scales: the seven complexity classes, analysis rules, Python costs.",
                    "group": "Foundations"}}

ANIM_KEYS = set(re.findall(r'G\["([^"]+)"\]', (OUT / "assets" / "anim.js").read_text()))

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600;700&display=swap">
<link rel="stylesheet" href="assets/dsa.css">
</head>
<body>
"""


def load(slug):
    path = SRC / "topics" / (slug.replace("-", "_") + ".py")
    spec = importlib.util.spec_from_file_location(slug, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.META.setdefault("slug", slug)
    return mod


def check(mod):
    """Enforce the house rules: real-life examples everywhere, a balanced quiz."""
    slug = mod.META["slug"]
    errs = []
    if 'class="real big-real"' not in mod.BODY:
        errs.append("no topic-level real-life example (div.real.big-real)")
    for i, card in enumerate(re.findall(r'<article class="pattern".*?</article>', mod.BODY, re.S)):
        if 'class="real"' not in card:
            name = re.search(r"<h3>(.*?)</h3>", card)
            errs.append("pattern card without a real-life example: " + (name.group(1) if name else str(i)))
    anims = re.findall(r'data-anim="([^"]+)"', mod.BODY)
    if not anims and mod.META.get("needs_anim", True):
        errs.append("no animation (figure.anim)")
    for k in anims:
        if k not in ANIM_KEYS:
            errs.append("unknown animation key: " + k)
    quiz = getattr(mod, "QUIZ", [])
    if quiz:
        for lv in ("easy", "medium", "hard"):
            if sum(q["lvl"] == lv for q in quiz) < 3:
                errs.append(f"quiz needs at least 3 {lv} questions")
        for n, q in enumerate(quiz):
            if not 0 <= q["a"] < len(q["opts"]):
                errs.append(f"quiz question {n + 1}: answer index out of range")
    if errs:
        sys.exit(f"[{slug}] " + "; ".join(errs))


def pid(slug, name):
    return slug + "-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def problems_html(mod):
    probs = getattr(mod, "PROBLEMS", [])
    if not probs:
        return "", []
    slug = mod.META["slug"]
    rows, ids = [], []
    for name, lc, lvl, hint in probs:
        i = pid(slug, name)
        ids.append(i)
        local = ".html" in lc or lc.startswith("#")
        href = lc if local else f"https://leetcode.com/problems/{lc}/"
        ext = "" if local else ' target="_blank" rel="noopener"'
        rows.append(
            f'<div class="prob"><input type="checkbox" id="{i}">'
            f'<label for="{i}"><a href="{href}"{ext}>{html.escape(name)}</a>'
            f'<span class="hint">{hint}</span></label><span class="lvl {lvl}">{lvl.title()}</span></div>')
    block = f"""
<section id="problems">
  <span class="eyebrow">Your checklist</span>
  <h2>{mod.META.get("problems_title", "Problems to solve")}</h2>
  <p>{mod.META.get("problems_intro", "These come from your 12-week checklist. Ticks are saved in this browser. The hint names the pattern, so cover it if you want a cold attempt.")}</p>
  <p class="progress"></p>
  <div class="problems">
    {''.join(rows)}
  </div>
</section>"""
    return block, ids


KIND = {"video": "Video", "course": "Course", "read": "Read", "visual": "Visualizer",
        "practice": "Practice", "book": "Book", "paper": "Paper"}


def learn_html(slug):
    from learn import LEARN
    items = LEARN.get(slug, [])
    if not items:
        return ""
    rows = "".join(
        f'<li><span class="kind k-{k}">{KIND[k]}</span><span class="lt"><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a>'
        f'<span class="hint">{html.escape(w)}</span></span></li>' for k, t, u, w in items)
    return f"""
<section id="learn">
  <span class="eyebrow">Go deeper</span>
  <h2>Learn more</h2>
  <div class="real"><p>Hearing the same idea from a second teacher often makes it click, the way a friend's directions can make sense after the map didn't. Try the problem first, then use these.</p></div>
  <ul class="learn">{rows}</ul>
  <p class="note">More channels, books and courses on the <a href="resources.html">Resources</a> page.</p>
</section>"""


def quiz_html(mod):
    quiz = getattr(mod, "QUIZ", [])
    if not quiz:
        return ""
    data = json.dumps(quiz, ensure_ascii=False).replace("</", "<\\/")
    return f"""
<section id="quiz">
  <span class="eyebrow">Test yourself</span>
  <h2>Quiz</h2>
  <p>Answer before you click. Filter by level; hard questions are the kind of follow-ups Google interviewers ask.</p>
  <div class="qbar"><div class="filters" id="filters" role="group" aria-label="Filter by difficulty"></div><button class="btn" type="button" id="quiz-reset">Reset quiz</button></div>
  <div class="quiz" id="quiz"></div>
  <p class="score" id="score" aria-live="polite"></p>
  <script type="application/json" id="quiz-data">{data}</script>
</section>"""


def toc(body):
    items = re.findall(r'<section id="([^"]+)">\s*(?:<span class="eyebrow">.*?</span>\s*)?<h2>(.*?)</h2>', body, re.S)
    return items


def nav(slug, metas):
    i = ORDER.index(slug)
    prev = metas[ORDER[i - 1]] if i > 0 else None
    nxt = metas[ORDER[i + 1]] if i + 1 < len(ORDER) else None
    parts = []
    if prev:
        parts.append(f'<a href="{prev["slug"]}.html">← {html.escape(prev["title"])}</a>')
    if nxt:
        parts.append(f'<a href="{nxt["slug"]}.html">{html.escape(nxt["title"])} →</a>')
    return ('<nav class="topbar" aria-label="Guide navigation"><div class="topbar-in">'
            '<a class="home" href="index.html">DSA + System Design Guide</a>'
            f'<span class="pn">{"".join(parts)}</span></div></nav>')


def page(mod, metas):
    m = mod.META
    slug = m["slug"]
    probs, ids = problems_html(mod)
    qz = quiz_html(mod)
    lrn = learn_html(slug)
    sections = toc(mod.BODY + lrn + probs + qz)
    toc_html = '<nav class="toc" aria-label="On this page">' + "".join(
        f'<a href="#{sid}">{t}</a>' for sid, t in sections) + "</nav>"
    chips = [f'<span class="chip">{m["week"]}</span>']
    if ids:
        chips.append(f'<span class="chip">{len(ids)} problems</span>')
    if getattr(mod, "QUIZ", []):
        chips.append(f'<span class="chip">{len(mod.QUIZ)} quiz questions</span>')
    out = HEAD.format(title=html.escape(m["page_title"]), desc=html.escape(m["blurb"]))
    out += nav(slug, metas)
    out += f"""
<main class="wrap">
<header class="hero">
  <span class="eyebrow">{m["group"]}</span>
  <h1>{m["h1"]}</h1>
  <p class="lead">{m["lead"]}</p>
  <div class="meta">{''.join(chips)}</div>
  {toc_html}
</header>
{mod.BODY}
{lrn}
{probs}
{qz}
<footer>{nav_footer(slug, metas)}</footer>
</main>
<script src="assets/dsa.js"></script>
<script src="assets/anim.js"></script>
</body>
</html>
"""
    (OUT / f"{slug}.html").write_text(out)
    return ids


def nav_footer(slug, metas):
    i = ORDER.index(slug)
    nxt = metas[ORDER[i + 1]] if i + 1 < len(ORDER) else None
    s = '<a href="index.html">All topics</a>'
    if nxt:
        s += f' · Next: <a href="{nxt["slug"]}.html">{html.escape(nxt["title"])}</a>'
    return s


def index(metas, idmap):
    tiles = {}
    for slug in ORDER:
        m = metas[slug]
        ids = idmap.get(slug, [])
        extra = ('<div class="meter"><span></span></div><span class="count"></span>' if ids else "")
        attr = ' data-ids="' + ",".join(ids) + '"' if ids else ""
        tiles.setdefault(m["group"], []).append(
            f'<a class="tile" href="{slug}.html"{attr}>'
            f'<span class="wk">{m["week"]}</span><h3>{html.escape(m["title"])}</h3><p>{m["blurb"]}</p>{extra}</a>')
    groups = "".join(
        f'<section id="{re.sub(r"[^a-z]+", "-", g.lower()).strip("-")}"><h2>{g}</h2><div class="grid">{"".join(t)}</div></section>'
        for g, t in tiles.items())
    body = (SRC / "index_body.html").read_text().replace("<!--GROUPS-->", groups)
    out = HEAD.format(title="DSA + System Design Guide", desc="Data structures, algorithms and system design prep for Google SWE interviews.")
    out += body + '\n<script src="assets/dsa.js"></script>\n</body>\n</html>\n'
    (OUT / "index.html").write_text(out)


def main():
    mods, metas = {}, dict(STATIC)
    for slug in ORDER:
        if slug in STATIC:
            continue
        mod = load(slug)
        check(mod)
        mods[slug] = mod
        metas[slug] = mod.META
    idmap = {slug: page(mod, metas) for slug, mod in mods.items()}
    index(metas, idmap)
    print("built", len(mods), "topic pages + index;",
          sum(len(v) for v in idmap.values()), "problems,",
          sum(len(getattr(m, "QUIZ", [])) for m in mods.values()), "quiz questions")


if __name__ == "__main__":
    main()
