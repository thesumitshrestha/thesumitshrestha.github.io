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
<link rel="stylesheet" href="assets/checklist.css">
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


from quiz_dsa import MORE as _QD
from quiz_sd import MORE as _QS
EXTRA_QUIZ = {**_QD, **_QS}
QUIZ_MIN, LEVEL_MIN = 20, 6


def check_quiz(slug, quiz):
    errs = []
    if len(quiz) < QUIZ_MIN:
        errs.append(f"quiz has {len(quiz)} questions; needs at least {QUIZ_MIN}")
    for lv in ("easy", "medium", "hard"):
        n = sum(q["lvl"] == lv for q in quiz)
        if n < LEVEL_MIN:
            errs.append(f"quiz has {n} {lv} questions; needs at least {LEVEL_MIN}")
    seen = set()
    for n, q in enumerate(quiz):
        if not 0 <= q["a"] < len(q["opts"]):
            errs.append(f"question {n + 1}: answer index out of range")
        if len(set(q["opts"])) != len(q["opts"]):
            errs.append(f"question {n + 1}: duplicate options")
        if q["q"] + q.get("code", "") in seen:
            errs.append(f"question {n + 1}: duplicate question")
        seen.add(q["q"] + q.get("code", ""))
    if errs:
        sys.exit(f"[{slug}] " + "; ".join(errs))


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
    if slug not in NO_CHECKLIST:
        check_quiz(slug, getattr(mod, "QUIZ", []))
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


def lc_chips(items):
    out = []
    for it in items:
        name, slug, lvl = it[:3]
        prem = len(it) > 3 and it[3]
        out.append(f'<a class="lcq" href="https://leetcode.com/problems/{slug}/" target="_blank" rel="noopener">'
                   f'{html.escape(name)}<span class="lvl {lvl}">{lvl[0].upper()}</span>'
                   + ('<span class="prem" title="Needs LeetCode Premium">Premium</span>' if prem else "") + '</a>')
    return "".join(out)


def add_leetcode(slug, body):
    from practice import PATTERN_LC, DEEP_LC
    pats = PATTERN_LC.get(slug)
    if pats:
        parts = re.split(r"(</article>)", body)
        n = sum(1 for x in parts if x == "</article>")
        if n != len(pats):
            sys.exit(f"[{slug}] {n} pattern cards but {len(pats)} LeetCode lists")
        i, out = 0, []
        for x in parts:
            if x == "</article>":
                out.append(f'<div class="lc"><span class="lc-label">Practice on LeetCode</span>{lc_chips(pats[i])}</div>\n  ')
                i += 1
            out.append(x)
        body = "".join(out)
    deep = DEEP_LC.get(slug)
    if deep:
        a = body.index('<section id="deep">')
        b = body.index("</section>", a)
        body = body[:b] + f'<div class="lc"><span class="lc-label">Solve it on LeetCode</span>{lc_chips(deep)}</div>\n' + body[b:]
    return body


def sd_lc_html(slug):
    from practice import SD_LC
    if slug not in SD_LC:
        return ""
    intro, items = SD_LC[slug]
    return f"""
<section id="leetcode">
  <span class="eyebrow">Code it</span>
  <h2>Related LeetCode problems</h2>
  <div class="real"><p>A model train set teaches how real railways work in a size you can hold. These coding problems are small, runnable versions of the system ideas on this page.</p></div>
  <p>{intro}</p>
  <div class="lc">{lc_chips(items)}</div>
  <p class="note">"Premium" problems need a LeetCode subscription; you can still read their descriptions and discussions in many free write-ups.</p>
</section>"""


NO_CHECKLIST = {"resources"}
BIGO_STEPS = [("read", "Read the page, including every real-life example"),
              ("anim", "Played with the growth slider at several sizes"),
              ("quiz", "Answered the practice questions, most of them right"),
              ("done", "Done with this topic")]


def topic_steps(slug, mod):
    if slug == "big-o":
        return BIGO_STEPS
    if slug in NO_CHECKLIST:
        return []
    from learn import LEARN
    body, is_sd = mod.BODY, slug.startswith("sd-")
    steps = [("read", "Read the page, including every real-life example")]
    if "data-anim=" in body:
        steps.append(("anim", "Played every animation step by step"))
    if 'class="pattern"' in body and not is_sd:
        steps.append(("code", "Typed each pattern template from memory"))
    if is_sd:
        steps.append(("explain", "Explained each idea out loud in my own words"))
    if LEARN.get(slug):
        steps.append(("learn", "Watched or read at least one Learn more resource"))
    if getattr(mod, "QUIZ", []):
        steps.append(("quiz", "Scored 8 out of 10 or better on the quiz"))
    if getattr(mod, "PROBLEMS", []):
        steps.append(("problems", "Finished the practice list" if is_sd or slug in ("sd-interview",) else "Solved every problem on the list"))
    steps.append(("done", "Done with this topic"))
    return steps


def step_key(slug, k):
    return f"dsa:t:{slug}:{k}"


def checklist_html(slug, steps):
    if not steps:
        return ""
    rows = "".join(
        f'<li class="step-row{" final" if k == "done" else ""}"><input type="checkbox" id="step-{slug}-{k}" data-key="{step_key(slug, k)}">'
        f'<label for="step-{slug}-{k}">{html.escape(label)}</label></li>' for k, label in steps)
    keys = ",".join(step_key(slug, k) for k, _ in steps)
    return f"""
<section id="checklist">
  <span class="eyebrow">Track it</span>
  <h2>Your checklist for this topic</h2>
  <div class="real"><p>Like a pilot's checklist before takeoff: ticking each step means nothing gets skipped, and you can see at a glance what's left.</p></div>
  <p class="steps-progress" data-steps="{keys}"></p>
  <ul class="steps">{rows}</ul>
  <p class="note">Ticks are saved in this browser and shown on the <a href="index.html#topic-checklist">topic checklist</a>. To keep a backup or move them to another device, use <a href="index.html#backup">Back up or move your progress</a>.</p>
</section>"""


def guard_ids(current):
    """Never let a rebuild drop a checkbox ID that already exists, or saved ticks would be orphaned."""
    lock = SRC / "ids.lock.json"
    old = set(json.loads(lock.read_text())) if lock.exists() else set()
    missing = sorted(old - set(current))
    if missing and "--allow-remove" not in sys.argv:
        sys.exit("Refusing to build: these saved-checkbox IDs would disappear and orphan your ticks:\n  "
                 + "\n  ".join(missing[:20]))
    lock.write_text(json.dumps(sorted(old | set(current)), indent=0))


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
    body = add_leetcode(slug, mod.BODY)
    sdlc = sd_lc_html(slug)
    steps = topic_steps(slug, mod)
    chk = checklist_html(slug, steps)
    sections = toc(body + sdlc + lrn + probs + qz + chk)
    toc_html = '<nav class="toc" aria-label="On this page">' + "".join(
        f'<a href="#{sid}">{t}</a>' for sid, t in sections) + "</nav>"
    chips = [f'<span class="chip">{m["week"]}</span>']
    if ids:
        chips.append(f'<span class="chip">{len(ids)} problems</span>')
    if getattr(mod, "QUIZ", []):
        chips.append(f'<span class="chip">{len(mod.QUIZ)} quiz questions</span>')
    if steps:
        keys = ",".join(step_key(slug, k) for k, _ in steps)
        chips.append(f'<a class="chip chip-steps" href="#checklist" data-steps="{keys}">Checklist</a>')
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
{body}
{sdlc}
{lrn}
{probs}
{qz}
{chk}
<footer>{nav_footer(slug, metas)}</footer>
</main>
<script src="assets/dsa.js"></script>
<script src="assets/anim.js"></script>
</body>
</html>
"""
    (OUT / f"{slug}.html").write_text(out)
    return ids, [step_key(slug, k) for k, _ in steps]


def nav_footer(slug, metas):
    i = ORDER.index(slug)
    nxt = metas[ORDER[i + 1]] if i + 1 < len(ORDER) else None
    s = '<a href="index.html">All topics</a>'
    if nxt:
        s += f' · Next: <a href="{nxt["slug"]}.html">{html.escape(nxt["title"])}</a>'
    return s


def index(metas, idmap, stepmap):
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
    rows_by_group = {}
    for slug in ORDER:
        keys = stepmap.get(slug)
        if not keys:
            continue
        m = metas[slug]
        rows_by_group.setdefault(m["group"], []).append(
            f'<li class="step-row"><input type="checkbox" id="topic-{slug}" data-key="{step_key(slug, "done")}">'
            f'<label for="topic-{slug}"><a href="{slug}.html">{html.escape(m["title"])}</a></label>'
            f'<a class="steps-count" href="{slug}.html#checklist" data-steps="{",".join(keys)}"></a></li>')
    checklist = "".join(f'<h3>{g}</h3><ul class="steps topics">{"".join(r)}</ul>' for g, r in rows_by_group.items())
    body = (SRC / "index_body.html").read_text().replace("<!--GROUPS-->", groups).replace("<!--CHECKLIST-->", checklist)
    out = HEAD.format(title="DSA + System Design Guide", desc="Data structures, algorithms and system design prep for Google SWE interviews.")
    out += body + '\n<script src="assets/dsa.js"></script>\n</body>\n</html>\n'
    (OUT / "index.html").write_text(out)


def patch_bigo_quiz():
    quiz = EXTRA_QUIZ["big-o"]
    check_quiz("big-o", quiz)
    class _M:  # minimal stand-in for a topic module
        QUIZ = quiz
    block = ("<!--QUIZ-START-->" + quiz_html(_M)
             + '\n<link rel="stylesheet" href="assets/quiz.css"><!--QUIZ-END-->')
    f = OUT / "big-o.html"
    s = f.read_text()
    s = re.sub(r"<!--QUIZ-START-->.*?<!--QUIZ-END-->", lambda _: block, s, flags=re.S)
    f.write_text(s)


def patch_bigo():
    """Add the checklist to the hand-written Big-O page, between markers, so rebuilding is safe."""
    f = OUT / "big-o.html"
    s = f.read_text()
    block = ("<!--CHECKLIST-START-->" + checklist_html("big-o", BIGO_STEPS)
             + '\n<link rel="stylesheet" href="assets/checklist.css"><script src="assets/dsa.js" defer></script><!--CHECKLIST-END-->')
    if "<!--CHECKLIST-START-->" in s:
        s = re.sub(r"<!--CHECKLIST-START-->.*?<!--CHECKLIST-END-->", lambda _: block, s, flags=re.S)
    else:
        anchor = '<section>\n  <span class="eyebrow">Avoid these</span>'
        i = s.index(anchor)
        end = s.index("</section>", i) + len("</section>")
        s = s[:end] + "\n\n" + block + s[end:]
    f.write_text(s)


def main():
    mods, metas = {}, dict(STATIC)
    for slug in ORDER:
        if slug in STATIC:
            continue
        mod = load(slug)
        mod.QUIZ = list(getattr(mod, "QUIZ", [])) + EXTRA_QUIZ.get(slug, [])
        check(mod)
        mods[slug] = mod
        metas[slug] = mod.META
    built = {slug: page(mod, metas) for slug, mod in mods.items()}
    idmap = {k: v[0] for k, v in built.items()}
    stepmap = {k: v[1] for k, v in built.items() if v[1]}
    stepmap["big-o"] = [step_key("big-o", k) for k, _ in BIGO_STEPS]
    patch_bigo()
    patch_bigo_quiz()
    index(metas, idmap, stepmap)
    guard_ids([i for v in idmap.values() for i in v] + [k for v in stepmap.values() for k in v])
    print("built", len(mods), "topic pages + index;",
          sum(len(v) for v in idmap.values()), "problems,",
          sum(len(getattr(m, "QUIZ", [])) for m in mods.values()), "quiz questions")


if __name__ == "__main__":
    main()
