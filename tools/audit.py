#!/usr/bin/env python3
"""
Ocean City PAT Testing — SEO / quality audit.

Scans every indexable .html page and enforces the MRM-style ruleset used across
these static sites. Run before every commit:

    python3 tools/audit.py

Exit code 0 = all pass, 1 = one or more FAILs (WARNs never fail the build).
"""
import os
import re
import sys
import html
import glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.oceancitypattesting.co.uk"

# ---- thresholds (SEO Rules.txt master ruleset; this site = location tier) ----
META_DESC_MAX = 160          # chars — Google desktop truncation
META_DESC_MIN = 70
TITLE_MAX = 60               # Rule 3: keep page titles under 60 chars
ALT_MAX = 100                # Rule 6: ALT text <= 100 chars
MIN_INTERNAL_LINKS = 10      # Rule 7: >= 10 in-body internal links
MIN_IMAGES = 3               # Rule 6: >= 3 relevant images per indexable page
MIN_FAQS = 4                 # Rule 11: >= 4 on-topic FAQs on content pages
# Rule 1 word counts — per-site LOCATION TIER (chosen 2026-07-03):
MIN_WORDS_AREA = 1400        # location / area pages
MIN_WORDS_SERVICE = 1500     # service pages
MIN_WORDS_SOFT = 900         # everything else: WARN below this, never FAIL
BANNED_ANCHORS = {"click here", "read more", "learn more", "here", "more",
                  "this", "link", "book", "read article", "find out more"}
# H2s that are legitimate repeated site furniture (exempt from uniqueness)
FURNITURE_H2 = {
    "frequently asked questions",
    "ready to get safe and compliant?",
    "what customers across the south west say",
    "other electrical safety services",
}
# hub / listing / legal / form pages: exempt from FAQ + hard word-count + >=3 img
UTILITY_PAGES = {"contact.html", "privacy-policy.html", "terms.html",
                 "sitemap.html", "service-information.html",
                 "news-and-associates.html", "areas-covered.html",
                 "services.html", "pricing.html", "about.html", "index.html"}
NOINDEX_FILES = {"404.html"}

def word_min(path):
    """Return (min_words, is_hard_fail) for a page."""
    r = rel(path).replace(os.sep, "/")
    if r.startswith("areas-covered/"):
        return MIN_WORDS_AREA, True
    if r.startswith("services/"):
        return MIN_WORDS_SERVICE, True
    return MIN_WORDS_SOFT, False

# ---- helpers ----------------------------------------------------------------
def rel(path):
    return os.path.relpath(path, ROOT)

def url_for(path):
    """Map a file path to its clean site URL."""
    r = rel(path).replace(os.sep, "/")
    if r == "index.html":
        return "/"
    return "/" + re.sub(r"\.html$", "", r)

def strip_tags(s):
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def body_only(s):
    m = re.search(r"<body\b[^>]*>(.*)</body>", s, flags=re.S | re.I)
    return m.group(1) if m else s

def find_all(pat, s, flags=re.S | re.I):
    return re.findall(pat, s, flags)

# Share ONE clean-URL resolver with the preview server (tools/serve.py) so the
# audit's link check and the live preview can never disagree with each other.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import serve  # noqa: E402

def resolve(href):
    """Return the local file a clean internal URL maps to, or None if it 404s —
    using the exact same rules the production host / preview server apply."""
    href = href.split("#")[0].split("?")[0]
    if not href.startswith("/") or href.startswith("//"):
        return None
    file_path, status = serve.resolve_path(href)
    return file_path if status == 200 else None

# ---- collect pages ----------------------------------------------------------
pages = sorted(p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))
indexable = [p for p in pages if os.path.basename(p) not in NOINDEX_FILES]

problems = defaultdict(list)   # path -> [(level, rule, msg)]
def fail(path, rule, msg): problems[path].append(("FAIL", rule, msg))
def warn(path, rule, msg): problems[path].append(("WARN", rule, msg))

titles, h1s, descs, h2s = {}, {}, {}, {}

sitemap = ""
sm_path = os.path.join(ROOT, "sitemap.xml")
if os.path.isfile(sm_path):
    with open(sm_path, encoding="utf-8") as f:
        sitemap = f.read()
sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))

# ---- per-page checks --------------------------------------------------------
for path in pages:
    with open(path, encoding="utf-8") as f:
        doc = f.read()
    base = os.path.basename(path)
    noindex_page = base in NOINDEX_FILES or re.search(r'name="robots"[^>]*noindex', doc, re.I)
    body = body_only(doc)
    text = strip_tags(body)
    words = len(text.split())

    # -- title
    m = re.search(r"<title>(.*?)</title>", doc, re.S | re.I)
    title = html.unescape(m.group(1).strip()) if m else ""
    if not title:
        fail(path, "title", "missing <title>")
    else:
        if len(title) > TITLE_MAX and not noindex_page:
            fail(path, "title", f"title {len(title)} chars (must be <{TITLE_MAX})")
        if not noindex_page:
            titles.setdefault(title, []).append(path)

    # -- meta description
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', doc, re.S | re.I)
    desc = html.unescape(m.group(1).strip()) if m else ""
    if not desc:
        if not noindex_page:
            fail(path, "meta-desc", "missing meta description")
    else:
        if len(desc) > META_DESC_MAX:
            fail(path, "meta-desc", f"meta description {len(desc)} chars (>{META_DESC_MAX})")
        elif len(desc) < META_DESC_MIN:
            warn(path, "meta-desc", f"meta description only {len(desc)} chars (<{META_DESC_MIN})")
        if not noindex_page:
            descs.setdefault(desc, []).append(path)

    # -- H1 (exactly one, and the FIRST heading on the page)
    h1 = find_all(r"<h1\b[^>]*>(.*?)</h1>", body)
    if len(h1) == 0:
        fail(path, "h1", "no <h1> on page")
    elif len(h1) > 1:
        fail(path, "h1", f"{len(h1)} <h1> tags (must be exactly 1)")
    else:
        h1text = strip_tags(h1[0])
        first_heading = re.search(r"<h([1-6])\b", body, re.I)
        if first_heading and first_heading.group(1) != "1":
            fail(path, "h1-first", f"an <h{first_heading.group(1)}> appears before the <h1>")
        if not noindex_page:
            h1s.setdefault(h1text, []).append(path)

    # -- H2 uniqueness sitewide (Rule 4). Genuine site furniture (FAQ / CTA /
    # reviews headings) is expected to repeat and is exempt.
    if not noindex_page:
        for h2 in find_all(r"<h2\b[^>]*>(.*?)</h2>", body):
            t = strip_tags(h2).lower()
            if t and t not in FURNITURE_H2:
                h2s.setdefault(t, set()).add(path)

    # -- web app manifest linked in <head> (Rule 9)
    if not re.search(r'<link\s+rel="manifest"', doc, re.I):
        fail(path, "manifest", "no <link rel=manifest> in <head>")

    # -- canonical
    m = re.search(r'<link\s+rel="canonical"\s+href="(.*?)"', doc, re.I)
    if not m:
        if not noindex_page:
            fail(path, "canonical", "missing canonical")
    else:
        can = m.group(1)
        if not can.startswith(DOMAIN):
            fail(path, "canonical", f"canonical off-domain: {can}")
        else:
            expected = DOMAIN + ("/" if url_for(path) == "/" else url_for(path) + "/")
            can_n = can if can.endswith("/") else can + "/"
            if can_n != expected and not noindex_page:
                warn(path, "canonical", f"canonical {can} != expected {DOMAIN}{url_for(path)}")

    # -- images: alt present, alt length, no duplicate src
    imgs = re.findall(r"<img\b[^>]*>", body, re.I)
    # dup-img only considers CONTENT images: strip header/footer/nav chrome
    # (site logo legitimately repeats in header + footer on every page).
    content_region = re.sub(r"<header\b.*?</header>|<footer\b.*?</footer>|<nav\b.*?</nav>",
                            " ", body, flags=re.S | re.I)
    CHROME_ASSETS = ("/images/logo.png", "/images/favicon.png",
                     "/images/apple-touch-icon.png")
    seen_src = defaultdict(int)
    for tag in imgs:
        src = (re.search(r'src="([^"]*)"', tag) or [None, ""])[1]
        alt_m = re.search(r'alt="(.*?)"', tag, re.S)
        decorative = re.search(r'(role="presentation"|aria-hidden="true")', tag, re.I)
        if alt_m is None:
            fail(path, "img-alt", f"<img> without alt: {src or tag[:60]}")
        else:
            alt = html.unescape(alt_m.group(1)).strip()
            if not alt and not decorative:
                fail(path, "img-alt", f"empty alt without role=presentation: {src}")
            if len(alt) > ALT_MAX:
                warn(path, "img-alt", f"alt {len(alt)} chars (>{ALT_MAX}): {src}")
        if (src and not src.startswith("data:") and src not in CHROME_ASSETS
                and src in content_region):
            seen_src[src] += 1
    for src, n in seen_src.items():
        if n > 1:
            fail(path, "dup-img", f"content image referenced {n}x on page: {src}")
    # -- >= 3 images per indexable page (Rule 6)
    if not noindex_page and len(imgs) < MIN_IMAGES:
        lvl = warn if base in UTILITY_PAGES else fail
        lvl(path, "img-count", f"{len(imgs)} <img> on page (want >={MIN_IMAGES})")

    # -- internal links: resolve + broken + descriptive anchor text
    links = re.findall(r'<a\b([^>]*)>(.*?)</a>', body, re.S | re.I)
    in_body_internal = 0
    for attrs, inner in links:
        hm = re.search(r'href="([^"]*)"', attrs)
        if not hm:
            continue
        href = hm.group(1)
        anchor = strip_tags(inner)
        aria = re.search(r'aria-label="([^"]*)"', attrs)
        label = (aria.group(1) if aria else anchor).strip().lower()
        # broken internal link check
        if href.startswith("/") and not href.startswith("//"):
            target = resolve(href)
            if target is None:
                fail(path, "broken-link", f"internal link 404s locally: {href}")
            else:
                in_body_internal += 1
            if ".html" in href.split("#")[0].split("?")[0]:
                fail(path, "clean-url", f"link uses .html instead of clean URL: {href}")
        # descriptive anchor text
        if href and not href.startswith(("tel:", "mailto:", "#")):
            if label in BANNED_ANCHORS:
                warn(path, "anchor-text", f'non-descriptive link text "{anchor or label}" -> {href}')
            elif not label:
                warn(path, "anchor-text", f"empty/iconic link with no aria-label -> {href}")

    # -- tel: + mailto: present somewhere on the page
    if "tel:" not in doc:
        fail(path, "contact", "no tel: link on page")
    if "mailto:" not in doc:
        warn(path, "contact", "no mailto: link on page")

    if noindex_page:
        continue

    # -- word count (location tier: area 1400 / service 1500 hard, else soft warn)
    is_utility = base in UTILITY_PAGES
    wmin, hard = word_min(path)
    if words < wmin:
        if hard:
            fail(path, "word-count", f"{words} words (<{wmin})")
        else:
            warn(path, "word-count", f"{words} words (<{wmin})")

    # -- internal link count (in body) — Rule 7: >= 10
    if in_body_internal < MIN_INTERNAL_LINKS:
        fail(path, "internal-links", f"{in_body_internal} in-body internal links (<{MIN_INTERNAL_LINKS})")

    # -- FAQ block + FAQPage schema (non-utility pages)
    has_faq_schema = '"FAQPage"' in doc
    faq_q = len(re.findall(r'"@type"\s*:\s*"Question"', doc))
    if not is_utility:
        if not has_faq_schema:
            fail(path, "faq", "no FAQPage schema")
        elif faq_q < MIN_FAQS:
            fail(path, "faq", f"only {faq_q} FAQ questions (<{MIN_FAQS})")

    # -- structured data: org / LocalBusiness present sitewide
    if "application/ld+json" not in doc:
        fail(path, "schema", "no JSON-LD structured data")

    # -- og:image matches a preloaded/hero image on-domain
    ogm = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', doc, re.I)
    if ogm and not ogm.group(1).startswith(DOMAIN):
        fail(path, "og-image", f"og:image off-domain: {ogm.group(1)}")

    # -- sitemap inclusion
    u = DOMAIN + (url_for(path) if url_for(path) != "/" else "/")
    if u not in sitemap_urls and (u.rstrip("/") not in {x.rstrip("/") for x in sitemap_urls}):
        fail(path, "sitemap", f"page not listed in sitemap.xml: {u}")

# ---- cross-page uniqueness --------------------------------------------------
for label, store in (("title", titles), ("h1", h1s), ("meta-desc", descs)):
    for value, paths in store.items():
        if len(paths) > 1:
            for p in paths:
                fail(p, f"dup-{label}", f'duplicate {label} shared by {len(paths)} pages: "{value[:60]}"')

# duplicate H2 text across the site (Rule 4) — reported as a summary below.
dup_h2 = {v: p for v, p in h2s.items() if len(p) > 1}

# sitemap URLs that have no file
for u in sorted(sitemap_urls):
    p = u[len(DOMAIN):]
    if resolve(p if p else "/") is None:
        problems[sm_path].append(("FAIL", "sitemap-orphan", f"sitemap lists non-existent page: {u}"))

# ---- report -----------------------------------------------------------------
n_fail = n_warn = 0
clean = []
for path in sorted(problems):
    issues = problems[path]
    fails = [i for i in issues if i[0] == "FAIL"]
    warns = [i for i in issues if i[0] == "WARN"]
    n_fail += len(fails)
    n_warn += len(warns)

for path in sorted(pages) + ([sm_path] if sm_path in problems else []):
    issues = problems.get(path)
    if not issues:
        if path in pages:
            clean.append(path)
        continue
    print(f"\n\033[1m{rel(path)}\033[0m")
    for level, rule, msg in sorted(issues, key=lambda x: (x[0] != "FAIL", x[1])):
        colour = "\033[31m" if level == "FAIL" else "\033[33m"
        print(f"  {colour}{level}\033[0m [{rule}] {msg}")

if dup_h2:
    print("\n\033[1mRepeated H2 headings (Rule 4 — non-blocking)\033[0m")
    for value, paths in sorted(dup_h2.items(), key=lambda x: -len(x[1])):
        print(f"  \033[33mWARN\033[0m [dup-h2] on {len(paths):>2} pages: \"{value[:60]}\"")

# ---- live end-to-end link check (--live) ------------------------------------
# Starts the real clean-URL server and requests EVERY internal link/asset,
# proving each one actually returns 200 through the exact server used to preview
# the site. This is the definitive "do all the links work?" test.
def live_link_check():
    import threading, urllib.request, urllib.error
    port = 8991
    httpd = serve.make_server(port)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    targets = {}   # url -> set(source pages)
    asset_re = re.compile(r'(?:src|href)="(/[^"#?]+\.'
                          r'(?:css|js|png|jpe?g|webp|svg|ico|gif|json|webmanifest|xml|txt|pdf))"', re.I)
    for path in pages:
        doc = open(path, encoding="utf-8").read()
        for href in re.findall(r'<a\b[^>]*\shref="([^"]+)"', doc, re.I):
            h = href.split("#")[0].split("?")[0]
            if h.startswith("/") and not h.startswith("//"):
                targets.setdefault(h, set()).add(rel(path))
        for src in asset_re.findall(doc):
            targets.setdefault(src, set()).add(rel(path))
    broken = []
    for url in sorted(targets):
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{port}{url}", method="HEAD")
            code = urllib.request.urlopen(req, timeout=5).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:                       # noqa: BLE001
            code = f"ERR:{e}"
        if code != 200:
            broken.append((url, code, sorted(targets[url])))
    httpd.shutdown()
    return broken, len(targets)

live_fail = 0
if "--live" in sys.argv:
    broken, n_targets = live_link_check()
    print(f"\n\033[1mLive link check\033[0m — {n_targets} unique internal links/assets requested "
          f"through tools/serve.py")
    if broken:
        for url, code, srcs in broken:
            live_fail += 1
            ex = srcs[0] + (f" +{len(srcs)-1} more" if len(srcs) > 1 else "")
            print(f"  \033[31mFAIL\033[0m [live-link] {code} {url}   (e.g. on {ex})")
    else:
        print("  \033[32mall links return 200 ✓\033[0m")

print("\n" + "=" * 64)
print(f"Pages scanned : {len(pages)}  (indexable {len(indexable)})")
print(f"Clean pages   : {len(clean)}")
print(f"\033[31mFAIL\033[0m: {n_fail + live_fail}   \033[33mWARN\033[0m: {n_warn}"
      + (f"   (incl. {live_fail} broken live links)" if live_fail else ""))
print("=" * 64)
sys.exit(1 if (n_fail or live_fail) else 0)
