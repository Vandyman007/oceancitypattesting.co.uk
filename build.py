#!/usr/bin/env python3
"""
Ocean City PAT Testing — static site generator.
Renders all HTML pages with a consistent SEO head / nav / footer / schema,
then writes sitemap.xml, robots.txt and llms.txt.

Run:  python3 build.py
"""
import os, html, datetime, re, urllib.parse

# ---------------------------------------------------------------------------
# SITE CONFIG
# ---------------------------------------------------------------------------
SITE = {
    "name": "Ocean City PAT Testing",
    "full_name": "Ocean City PAT Testing",
    "legal": "Ocean City PAT Testing",
    "slogan": "Guiding You Safely",
    "domain": "https://www.oceancitypattesting.co.uk",
    "phone_display": "07783 543958",
    "phone_e164": "+447783543958",
    "email": "oceancitypattesting@gmail.com",
    "area": "Plymouth, Devon &amp; South East Cornwall",
    "region": "Devon",
    "locality": "Plymouth",
    "postcode": "PL1",
    "lat": "50.37153",
    "lng": "-4.14305",
    "hours": [
        ("Monday,Tuesday,Wednesday,Thursday,Friday", "08:00", "18:00"),
        ("Saturday", "09:00", "16:00"),
    ],
    "hours_human": "Mon–Fri 8am–6pm · Sat 9am–4pm",
    "rating": "5.0",
    "review_count": "48",
    "year": "2026",
    "founded": "2018",          # trading name; 20+ years' hands-on electrical experience
    "experience_years": "20",
}
THIS_YEAR = SITE["year"]
TODAY = "2026-06-26"

# WhatsApp click-to-chat link with a pre-filled message (call buttons open this).
WA_URL = ("https://wa.me/" + SITE["phone_e164"].lstrip("+") + "?text="
          + urllib.parse.quote("Hi Ocean City PAT Testing, I'd like a quote for PAT testing."))

# ---------------------------------------------------------------------------
# SERVICES  (slug, nav label, short blurb, icon key, primary keyword)
# ---------------------------------------------------------------------------
SERVICES = [
    ("pat-testing", "PAT Testing",
     "Portable appliance testing for every plug-in item — visual inspection plus full electrical test.",
     "plug", "PAT testing Plymouth"),
    ("landlord-pat-testing", "Landlord PAT Testing",
     "Keep rental properties compliant with your duty of care — fixed price per property.",
     "house", "landlord PAT testing Plymouth"),
    ("holiday-let-pat-testing", "Holiday Let PAT Testing",
     "Airbnb, cottages &amp; serviced lets tested to keep guests safe and insurers happy.",
     "key", "holiday let PAT testing Devon"),
    ("business-pat-testing", "Business &amp; Commercial PAT Testing",
     "Offices, shops, salons, cafés and workshops tested with same-day certification.",
     "office", "business PAT testing Plymouth"),
    ("charity-community-pat-testing", "Charity &amp; Community PAT Testing",
     "Discounted per-item testing for charities, churches, clubs and community groups.",
     "heart", "charity PAT testing Devon"),
    ("eicr-electrical-testing", "EICR &amp; Electrical Testing",
     "Electrical Installation Condition Reports and fixed-wire testing by a qualified electrician.",
     "report", "EICR Plymouth"),
    ("fire-safety-testing", "Fire Safety Testing",
     "Fire extinguisher, alarm and emergency lighting checks to complete your safety paperwork.",
     "fire", "fire safety testing Plymouth"),
]
SERVICE_SLUGS = {s[0] for s in SERVICES}

# ---------------------------------------------------------------------------
# AREAS  (slug, name)
# ---------------------------------------------------------------------------
AREAS = [
    ("plymouth", "Plymouth"),
    ("plympton", "Plympton"),
    ("saltash", "Saltash"),
    ("torpoint", "Torpoint"),
    ("callington", "Callington"),
    ("tavistock", "Tavistock"),
    ("liskeard", "Liskeard"),
    ("looe", "Looe"),
    ("kingsbridge", "Kingsbridge"),
    ("salcombe", "Salcombe"),
    ("totnes", "Totnes"),
    ("dartmouth", "Dartmouth"),
]

# nearby towns referenced in coverage prose but without dedicated pages (yet).
NEARBY = ["Ivybridge", "Modbury", "Yealmpton", "Cawsand", "Polperro", "West Looe",
          "Newton Abbot", "Buckfastleigh", "Ashburton", "Paignton", "Torquay", "Brixham"]

# ---------------------------------------------------------------------------
# PRICE LIST — SINGLE SOURCE OF TRUTH (drives the /pricing page)
# All figures are the owner's published prices. Same-day PDF certificate
# included with every job.
# ---------------------------------------------------------------------------
PRICE_TIERS = [
    {"id": "landlord", "name": "Landlord & Rental Property", "icon": "house",
     "from": 40, "unit": "per property",
     "blurb": "A complete portable appliance test for a rented house or flat, with your certificate the same day — exactly what you need to evidence your duty of care to tenants.",
     "includes": ["Visual inspection &amp; full electrical test of all portable appliances",
                  "Pass/fail labelling on every item tested",
                  "Same-day PDF certificate emailed to you",
                  "Advice on any item that fails or needs attention"]},
    {"id": "holiday-let", "name": "Holiday Let & Accommodation", "icon": "key",
     "from": 65, "unit": "from",
     "blurb": "Self-catering cottages, Airbnbs and serviced apartments carry more appliances and higher guest turnover. We test the lot and keep your booking platform and insurer satisfied.",
     "includes": ["All guest-use appliances tested — kettles, toasters, hairdryers, TVs, heaters",
                  "Kitchen white goods and any supplied electricals",
                  "Same-day certificate for your safety file",
                  "Flexible scheduling around changeover days"]},
    {"id": "business", "name": "Business & Commercial", "icon": "office",
     "from": 80, "unit": "first 50 tests",
     "blurb": "Offices, shops, salons, cafés, gyms and workshops. Pricing covers your first 50 appliances, with a low per-item rate beyond that — quoted up front before we start.",
     "includes": ["Up to 50 appliances tested in the base price",
                  "Low fixed rate per additional item",
                  "Asset register &amp; same-day digital certificate",
                  "Out-of-hours testing available to avoid disruption"]},
    {"id": "charity", "name": "Charity & Community Groups", "icon": "heart",
     "from": 0.90, "unit": "per test", "money": "90p",
     "blurb": "Churches, village halls, clubs, pre-schools and community projects get our lowest rate. Keeping your members and volunteers safe shouldn't cost the earth.",
     "includes": ["Just 90p per appliance tested",
                  "Ideal for halls, clubs and not-for-profits",
                  "Same-day certificate for your records",
                  "Friendly, flexible visits that fit around your activities"]},
]
# Minimum call-out applies to every visit.
MIN_CALLOUT = 40
PRICE_FROM = 40   # used for "from £X" marketing copy (landlord entry price = min call-out)

# ---------------------------------------------------------------------------
# SVG ICON LIBRARY (inline, no external requests)
# ---------------------------------------------------------------------------
ICONS = {
    "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15.9 15.9 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.4 0 .7-.2 1l-2.3 2.2z"/></svg>',
    "whatsapp": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.1-1.3A10 10 0 1 0 12 2zm0 1.8a8.2 8.2 0 0 1 6.9 12.6l-.2.3.6 2.3-2.4-.6-.3.2A8.2 8.2 0 1 1 12 3.8zm-3.4 4.3c-.2 0-.4 0-.6.3-.2.2-.8.8-.8 1.9 0 1.2.8 2.3 1 2.5.1.2 1.7 2.7 4.2 3.7 2.1.8 2.5.6 3 .6.5 0 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.5-.3-1.5-.7c-.2-.1-.4-.1-.5.1l-.6.8c-.1.1-.3.2-.5.1-.3-.1-1.1-.4-2-1.2-.7-.7-1.2-1.5-1.4-1.7-.1-.2 0-.4.1-.5l.4-.5c.1-.1.1-.3.2-.4 0-.2 0-.3 0-.4l-.7-1.8c-.2-.4-.4-.4-.5-.4z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24"><path d="M4 4h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm0 4 8 5 8-5V6l-8 5-8-5v2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4 4 2.3-1 1.7-5-2.9V6h2v6.4z"/></svg>',
    "check": '<svg viewBox="0 0 24 24"><path d="M9 16.2 4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4z"/></svg>',
    "plug": '<svg viewBox="0 0 24 24"><path d="M9 2v6H7v2a5 5 0 0 0 4 4.9V22h2v-7.1A5 5 0 0 0 17 10V8h-2V2h-2v6h-2V2z"/></svg>',
    "house": '<svg viewBox="0 0 24 24"><path d="M12 3 2 11h3v9h6v-6h2v6h6v-9h3z"/></svg>',
    "key": '<svg viewBox="0 0 24 24"><path d="M14 2a6 6 0 0 0-5.7 8L2 16.3V22h5.7v-2h2v-2h2l1.6-1.6A6 6 0 1 0 14 2zm2 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3z"/></svg>',
    "office": '<svg viewBox="0 0 24 24"><path d="M4 3h9v18H4zM14 8h6v13h-6zM6 6h2v2H6zm3 0h2v2H9zm-3 4h2v2H6zm3 0h2v2H9z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24"><path d="M12 21S4 14.4 4 9a4 4 0 0 1 8-1 4 4 0 0 1 8 1c0 5.4-8 12-8 12z"/></svg>',
    "report": '<svg viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6zm8 1.5V8h4.5zM8 12h8v2H8zm0 4h8v2H8zm0-8h4v2H8z"/></svg>',
    "fire": '<svg viewBox="0 0 24 24"><path d="M13 2c1 3-1 4-2 6-1-1-1-2-1-3-2 2-4 4-4 8a6 6 0 0 0 12 0c0-4-3-6-5-11zm-1 17a3 3 0 0 1-3-3c0-1.6 1-2.7 1.8-3.6.3 1 .9 1.6 1.7 2.2 1-1 1.2-1.7 1.2-2.6 1 1 1.3 2.2 1.3 4a3 3 0 0 1-3 3z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24"><path d="M12 2 4 5v6c0 5 3.4 9.3 8 11 4.6-1.7 8-6 8-11V5zm-1.2 13L7 11.2 8.4 9.8l2.4 2.4 4.8-4.8L17 8.8z"/></svg>',
    "star": '<svg viewBox="0 0 24 24"><path d="m12 2 3 6.5 7 .6-5.3 4.6L18 21l-6-3.7L6 21l1.3-7.3L2 9.1l7-.6z"/></svg>',
    "pound": '<svg viewBox="0 0 24 24"><path d="M6 20v-2c1.5 0 2-1 2-2.5V13H6v-2h2V9a4 4 0 0 1 7.2-2.4l-1.7 1A2 2 0 0 0 10 9v2h4v2h-4v.5c0 1-.3 1.8-.9 2.5H18v2z"/></svg>',
    "calendar": '<svg viewBox="0 0 24 24"><path d="M7 2v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2V2h-2v2H9V2zm12 8H5v10h14zM5 6h14v2H5z"/></svg>',
    "badge": '<svg viewBox="0 0 24 24"><path d="M12 2a5 5 0 0 0-5 5c0 1.9 1 3.5 2.5 4.4L8 22l4-2 4 2-1.5-10.6A5 5 0 0 0 17 7a5 5 0 0 0-5-5zm0 2a3 3 0 1 1 0 6 3 3 0 0 1 0-6z"/></svg>',
    "lighthouse": '<svg viewBox="0 0 24 24"><path d="M11 2h2l1 4h-4zM9 8h6l1 13H8zM3 8l3 1M21 8l-3 1M4 13l3 .5M20 13l-3 .5"/></svg>',
}

# ---------------------------------------------------------------------------
# NAV
# ---------------------------------------------------------------------------
def nav_links(active):
    def li(href, label, slug):
        cls = ' class="active"' if slug == active else ''
        return f'<a href="{href}"{cls}>{label}</a>'
    drop = ''.join(f'<a href="/services/{s[0]}">{s[1]}</a>' for s in SERVICES)
    return f"""
    {li('/', 'Home', 'home')}
    <span class="has-drop">{li('/services', 'Services', 'services')}
      <span class="dropmenu"><a href="/services"><strong>All services</strong></a>{drop}</span>
    </span>
    {li('/pricing', 'Pricing', 'pricing')}
    {li('/areas-covered', 'Areas Covered', 'areas')}
    {li('/about', 'About', 'about')}
    {li('/service-information', 'PAT Guide', 'guide')}
    """

# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------
def org_schema():
    hours = ",".join(
        '{"@type":"OpeningHoursSpecification","dayOfWeek":[%s],"opens":"%s","closes":"%s"}'
        % (",".join('"%s"' % d for d in days.split(",")), o, c)
        for days, o, c in SITE["hours"]
    )
    knows = ",".join('"%s"' % re.sub("&amp;", "&", s[1]) for s in SERVICES)
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
        '"@type":["LocalBusiness","Electrician"],'
        '"@id":"%s/#organization","name":"%s","alternateName":"Ocean City PAT Testing Plymouth",'
        '"url":"%s/","telephone":"%s","email":"%s","image":"%s/images/logo.png",'
        '"logo":{"@type":"ImageObject","url":"%s/images/logo.png","width":727,"height":731},'
        '"description":"Portable appliance testing (PAT), EICR electrical reports and fire safety testing across Plymouth, Devon and South East Cornwall. Landlord, holiday let, business and charity PAT testing with same-day certificates.",'
        '"priceRange":"££","currenciesAccepted":"GBP","paymentAccepted":"Cash, Card, Bank Transfer",'
        '"foundingDate":"%s","slogan":"Guiding You Safely",'
        '"address":{"@type":"PostalAddress","addressLocality":"Plymouth","addressRegion":"Devon","postalCode":"PL1","addressCountry":"GB"},'
        '"geo":{"@type":"GeoCoordinates","latitude":"%s","longitude":"%s"},'
        '"areaServed":[{"@type":"City","name":"Plymouth"},{"@type":"AdministrativeArea","name":"Devon"},{"@type":"AdministrativeArea","name":"South Hams"},{"@type":"AdministrativeArea","name":"South East Cornwall"}],'
        '"openingHoursSpecification":[%s],'
        '"knowsAbout":[%s],'
        '"aggregateRating":{"@type":"AggregateRating","ratingValue":"%s","reviewCount":"%s","bestRating":"5","worstRating":"1"}}</script>'
        % (SITE["domain"], SITE["full_name"], SITE["domain"], SITE["phone_e164"], SITE["email"],
           SITE["domain"], SITE["domain"], SITE["founded"], SITE["lat"], SITE["lng"],
           hours, knows, SITE["rating"], SITE["review_count"]))

def webpage_schema(url, title, desc):
    return ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage",'
        '"url":"%s%s","name":%s,"description":%s,"inLanguage":"en-GB","dateModified":"%s",'
        '"isPartOf":{"@type":"WebSite","url":"%s","name":"%s"},'
        '"about":{"@id":"%s/#organization"}}</script>'
        % (SITE["domain"], url, jstr(title), jstr(desc), TODAY, SITE["domain"],
           SITE["full_name"], SITE["domain"]))

def breadcrumb_schema(crumbs):
    items = ",".join(
        '{"@type":"ListItem","position":%d,"name":%s,"item":"%s%s"}'
        % (i + 1, jstr(strip_html(name)), SITE["domain"], href)
        for i, (name, href) in enumerate(crumbs)
    )
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"BreadcrumbList","itemListElement":[%s]}</script>' % items)

def faq_schema(faqs):
    if not faqs:
        return ""
    items = ",".join(
        '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (jstr(strip_html(q)), jstr(strip_html(a))) for q, a in faqs
    )
    return ('<script type="application/ld+json">{"@context":"https://schema.org",'
            '"@type":"FAQPage","mainEntity":[%s]}</script>' % items)

def jstr(s):
    """JSON-encode a string for embedding in ld+json."""
    s = strip_html(s) if "<" in s else s
    s = s.replace("&amp;", "&").replace("\\", "\\\\").replace('"', '\\"')
    s = s.replace("\n", " ").replace("\r", " ")
    return '"%s"' % s

def strip_html(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").strip()

# ---------------------------------------------------------------------------
# SHARED CHROME
# ---------------------------------------------------------------------------
def header_html(active):
    return f"""
<div class="brand-bar" aria-hidden="true"></div>
<div class="topbar"><div class="wrap">
  <div>{ICONS['shield']} City &amp; Guilds qualified · Devon Trading Standards approved · {SITE['experience_years']}+ years' experience</div>
  <div class="tb-right">
    <a href="tel:{SITE['phone_e164']}">{ICONS['phone']}{SITE['phone_display']}</a>
    <a href="mailto:{SITE['email']}">{ICONS['mail']}{SITE['email']}</a>
  </div>
</div></div>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="Ocean City PAT Testing — Plymouth, home">
    <img class="brand-logo" src="/images/logo.png" width="64" height="64" alt="Ocean City PAT Testing lighthouse logo">
    <span class="brand-text"><strong>Ocean City PAT Testing</strong><em>Guiding You Safely · Plymouth &amp; the South West</em></span>
  </a>
  <nav class="primary" aria-label="Primary">{nav_links(active)}</nav>
  <div class="header-cta">
    <a class="btn btn-outline call-btn" href="tel:{SITE['phone_e164']}">{ICONS['phone']}Call now</a>
    <a class="btn btn-primary" href="/contact">Get a quote</a>
    <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" onclick="document.getElementById('mnav').classList.add('open');this.setAttribute('aria-expanded','true')">
      <svg viewBox="0 0 24 24"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>
    </button>
  </div>
</div></header>
<div class="mobile-nav" id="mnav">
  <div class="panel">
    <button class="closex" aria-label="Close menu" onclick="document.getElementById('mnav').classList.remove('open');var t=document.querySelector('.nav-toggle');if(t)t.setAttribute('aria-expanded','false')">&times;</button>
    <div style="clear:both"></div>
    <a href="/">Home</a>
    <details class="m-sub">
      <summary>Services</summary>
      <a href="/services">All services</a>
      {''.join(f'<a href="/services/{s[0]}">{s[1]}</a>' for s in SERVICES)}
    </details>
    <a href="/pricing">Pricing</a>
    <a href="/areas-covered">Areas Covered</a>
    <a href="/about">About</a>
    <a href="/service-information">PAT Testing Guide</a>
    <a href="/news-and-associates">News &amp; Associates</a>
    <div class="m-cta">
      <a class="btn btn-primary" href="tel:{SITE['phone_e164']}">{ICONS['phone']}Call {SITE['phone_display']}</a>
      <a class="btn btn-accent" href="/contact">Get a quote</a>
    </div>
  </div>
</div>
"""

def footer_html():
    svc = ''.join(f'<a href="/services/{s[0]}">{s[1]}</a>' for s in SERVICES)
    areas = ''.join(f'<a href="/areas-covered/{a[0]}">PAT testing {a[1]}</a>' for a in AREAS[:6])
    return f"""
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      <div class="footer-brand"><img class="mark" src="/images/logo.png" width="44" height="44" alt="Ocean City PAT Testing lighthouse logo"> Ocean City PAT Testing</div>
      <p>City &amp; Guilds qualified portable appliance testing, EICR electrical reports and fire safety testing across Plymouth, Devon and South East Cornwall. Same-day certificates, every time.</p>
      <p style="margin-bottom:.4rem"><a href="tel:{SITE['phone_e164']}">{SITE['phone_display']}</a></p>
      <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      <div class="footer-map">
        <iframe title="Map of our Plymouth and South West coverage area" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps?q=Plymouth,+Devon&output=embed"></iframe>
      </div>
    </div>
    <div><h4>Services</h4>{svc}</div>
    <div><h4>Popular areas</h4>{areas}<a href="/areas-covered"><strong>All areas &rarr;</strong></a></div>
    <div>
      <h4>Company</h4>
      <a href="/about">About us</a>
      <a href="/pricing">Pricing</a>
      <a href="/service-information">PAT testing guide</a>
      <a href="/news-and-associates">News &amp; associates</a>
      <a href="/contact">Contact &amp; quote</a>
      <a href="/sitemap">Sitemap</a>
      <a href="/privacy-policy">Privacy policy</a>
      <a href="/terms">Terms &amp; conditions</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>&copy; {THIS_YEAR} {SITE['full_name']}. City &amp; Guilds qualified &amp; Devon Trading Standards approved. All testing carried out to IET Code of Practice (5th Edition).</span>
    <span>Plymouth · {SITE['hours_human']}</span>
  </div>
</div></footer>
<div class="callbar">
  <a class="btn btn-primary" href="tel:{SITE['phone_e164']}">{ICONS['phone']}Call</a>
  <a class="btn btn-accent" href="/contact">Get a quote</a>
</div>
"""

# ---------------------------------------------------------------------------
# PAGE RENDER
# ---------------------------------------------------------------------------
def render(page):
    url = page["url"]
    canonical = SITE["domain"] + url
    title = page["title"]
    desc = page["desc"]
    og_image = SITE["domain"] + "/" + page.get("og_image", "images/og-share.jpg")
    active = page.get("active", "")
    crumbs = page.get("breadcrumbs", [("Home", "/")])
    faqs = page.get("faqs", [])

    try:
        _cssv = str(int(os.path.getmtime(os.path.join(os.path.dirname(os.path.abspath(__file__)), "css", "site.css"))))
    except OSError:
        _cssv = "1"
    css_href = f"/css/site.css?v={_cssv}"

    schema_blocks = "\n  ".join([
        org_schema(),
        webpage_schema(url, title, desc),
        breadcrumb_schema(crumbs),
        faq_schema(faqs),
    ])

    head = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{attr(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="{'noindex,follow' if page.get('noindex') else 'index,follow,max-image-preview:large'}">
  <meta name="author" content="{SITE['full_name']}">
  <meta name="theme-color" content="#206F8B">
  <meta name="geo.region" content="GB-DEV">
  <meta name="geo.placename" content="Plymouth">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{SITE['full_name']}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:title" content="{attr(title)}">
  <meta property="og:description" content="{attr(desc)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:alt" content="{attr(page.get('og_alt','Ocean City PAT Testing — Guiding You Safely'))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{attr(title)}">
  <meta name="twitter:description" content="{attr(desc)}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="icon" href="/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css_href}">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' https:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com data:; frame-src https://www.google.com https://maps.google.com; connect-src 'self' https://formspree.io; object-src 'none'; base-uri 'self'; form-action 'self' https://formspree.io mailto:">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  {schema_blocks}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header_html(active)}
<main id="main">
{page['body']}
{render_faq_section(faqs) if faqs else ''}
{'' if page.get('no_cta') else cta_band()}
</main>
{footer_html()}
{page.get('scripts', '')}
</body>
</html>"""
    return head

def attr(s):
    return strip_html(s).replace('"', "&quot;").replace("&", "&amp;")

# ---------------------------------------------------------------------------
# REUSABLE CONTENT BLOCKS
# ---------------------------------------------------------------------------
def crumbs_html(crumbs):
    parts = []
    for i, (name, href) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<span aria-current="page">{name}</span>')
        else:
            parts.append(f'<a href="{href}">{name}</a><span>/</span>')
    return f'<div class="crumbs"><div class="wrap">{"".join(parts)}</div></div>'

def render_faq_section(faqs):
    items = ""
    for q, a in faqs:
        items += f'<details><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>'
    return f"""
<section class="section-light">
  <div class="wrap">
    <div class="section-head center"><span class="eyebrow">FAQs</span>
      <h2>Frequently asked questions</h2>
      <p>Everything customers ask before booking PAT testing. Still unsure? Call {SITE['phone_display']} — advice is always free.</p>
    </div>
    <div class="faq" style="margin:0 auto">{items}</div>
  </div>
</section>"""

def cta_band():
    return f"""
<section class="tight"><div class="wrap">
  <div class="cta-band">
    <h2>Ready to get safe and compliant?</h2>
    <p>Tell us what needs testing and we'll give you a fixed price the same day. Landlord, holiday let, business or community group — we'll keep you on the right side of the law.</p>
    <div class="hero-cta">
      <a class="btn btn-accent btn-lg" href="/contact">Get a free quote</a>
      <a class="btn btn-ghost btn-lg" href="tel:{SITE['phone_e164']}">{ICONS['phone']}Call {SITE['phone_display']}</a>
    </div>
  </div>
</div></section>"""

def service_cards(limit=None, exclude=None):
    cards = ""
    shown = 0
    for slug, label, blurb, icon, kw in SERVICES:
        if exclude and slug == exclude:
            continue
        cards += f"""
    <div class="card">
      <div class="ico">{ICONS.get(icon, ICONS['plug'])}</div>
      <h3>{label}</h3>
      <p>{blurb}</p>
      <a class="more" href="/services/{slug}" aria-label="{strip_html(label)} — service details">{label} &rarr;</a>
    </div>"""
        shown += 1
        if limit and shown >= limit:
            break
    # complete the grid with a "something else" CTA card when the full set shows
    if exclude is None and not limit:
        cards += f"""
    <div class="card svc-cta">
      <div class="ico">{ICONS['mail']}</div>
      <h3>Something else?</h3>
      <p>Need emergency lighting, microwave leakage or a specialist test? Tell us what you need and we'll quote it.</p>
      <a class="more" href="/contact" aria-label="Ask about another testing service">Ask us &rarr;</a>
    </div>"""
    # exclude -> 6 cards (clean 3-col rows); full set -> 8 cards (clean 4-col rows)
    cols = "cols-3" if exclude else "cols-4"
    return f'<div class="grid {cols} svc-grid">{cards}</div>'

def page_banner(h1, sub):
    return f'<section class="page-banner"><div class="wrap"><h1>{h1}</h1><p>{sub}</p></div></section>'

def author_box():
    return f"""<div class="author-box">
  <img class="av" src="/images/logo.png" width="64" height="64" alt="Ocean City PAT Testing lighthouse logo">
  <div class="meta"><strong>Ocean City PAT Testing</strong>
  City &amp; Guilds qualified and Devon Trading Standards approved, with over {SITE['experience_years']} years' hands-on electrical experience across Plymouth, Devon and South East Cornwall. Every appliance is tested to the IET Code of Practice and certified the same day.</div>
</div>"""

def trust_block(subject, kw):
    """E-E-A-T expansion woven with the page's primary keyword. subject is a
    lower-case noun phrase (e.g. 'PAT testing'); kw is the primary keyword."""
    return f"""
  <h2>Experienced, qualified {subject} you can rely on</h2>
  <p>Ocean City PAT Testing has carried out {kw} for homeowners, landlords, holiday-let owners and businesses right across {SITE['area']}. The work is done by a City &amp; Guilds qualified engineer with over {SITE['experience_years']} years of hands-on electrical experience — not a box-ticking subcontractor — so every appliance gets a proper visual inspection and a full electrical test, not just a sticker. Because we're based here in Plymouth, we know the area, turn up when we say we will, and treat your home or premises with respect.</p>
  <h2>Why testing matters — and what the law says</h2>
  <p>Under the Electricity at Work Regulations 1989 and the Health and Safety at Work Act, anyone responsible for a workplace, a rented home or a public space has a duty to keep electrical equipment safe. Regular {subject} is the recognised way to evidence that duty of care. Just as importantly, if a faulty appliance ever causes a fire or injury, your insurer will ask for proof the equipment was maintained — and a current PAT certificate is exactly that proof. Skipping it can invalidate a claim and leave you personally liable.</p>
  <h2>Same-day certificates and honest advice</h2>
  <p>Every job finishes with a clear pass/fail label on each item and a full digital certificate emailed to you the same day, ready for your safety file, your letting agent, your insurer or an inspector. If something fails, we tell you plainly what's wrong and what it would take to put it right — many minor faults, like a worn fuse or a damaged plug, can often be repaired on the spot. There's never any pressure and never a charge for friendly advice.</p>
  <h2>Fair, fixed prices across the South West</h2>
  <p>Our {kw} is quoted up front with no hidden extras — landlords from £{PRICE_FROM} per property, holiday lets from £65, businesses from £80 for the first 50 appliances and just 90p per item for charities and community groups. We cover Plymouth, the South Hams and South East Cornwall as standard, and that straightforward, no-surprises approach is why customers rate us {SITE['rating']} out of 5. When safety is the whole point, you want someone who does it properly the first time.</p>
"""

# ---------------------------------------------------------------------------
# IMAGERY — client logos + figure/logo-strip helpers
# ---------------------------------------------------------------------------
# (slug -> display name) for the client logo files in /images/client-<slug>.webp
CLIENTS = [
    ("superyacht", "Superyacht Solutions"),
    ("rapid-marine", "Rapid Marine"),
    ("spa-dental", "Spa Dental Plymouth"),
    ("south-moor-vets", "South Moor Vets"),
    ("dame-hannahs", "Dame Hannah's"),
    ("hopscotch", "Hopscotch Homes"),
    ("unity-lettings", "Unity Lettings"),
    ("aspire", "Aspire Support"),
    ("millfields", "Millfields Union Street"),
    ("cactus-h3", "Cactus H3"),
    ("elivate-care", "Elivate Care"),
    ("path", "Path"),
    ("dartmouth-chamber", "Dartmouth Chamber"),
    ("simply-business", "Simply Business Insurance"),
]

def media_figure(src, alt, caption=""):
    """Inline <figure> for a content photo. Advert-style portrait graphics are
    auto-constrained so they don't dominate the column."""
    cls = "media-fig fig-advert" if "advert" in src else "media-fig"
    cap = f'<figcaption>{html.escape(strip_html(caption))}</figcaption>' if caption else ''
    return (f'<figure class="{cls}">'
            f'<img src="/images/{src}" alt="{attr(alt)}" loading="lazy" decoding="async">'
            f'{cap}</figure>')

def logo_strip(eyebrow, title, lead):
    items = ''.join(
        f'<img src="/images/client-{slug}.webp" alt="{name} — an Ocean City PAT Testing client" '
        f'loading="lazy" decoding="async" width="150" height="56">'
        for slug, name in CLIENTS)
    return f"""
<section class="section-light tight"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2><p>{lead}</p></div>
  <div class="logo-strip">{items}</div>
</div></section>"""

# ---------------------------------------------------------------------------
# imported page content
# ---------------------------------------------------------------------------
from content import build_pages  # noqa: E402

# ---------------------------------------------------------------------------
# WRITE OUTPUT
# ---------------------------------------------------------------------------
def main():
    root = os.path.dirname(os.path.abspath(__file__))
    pages = build_pages(globals())
    written = []
    for p in pages:
        url = p["url"]
        rel = "index.html" if url == "/" else url.strip("/") + ".html"
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(render(p))
        if not p.get("noindex"):
            written.append((url, rel, p.get("priority", 0.6)))
        print("  wrote", rel)

    write_sitemap(root, written)
    write_robots(root)
    write_llms(root, pages)
    write_manifest(root)
    write_redirects(root)
    audit_links(root, written)
    print(f"\nBuilt {len(written)} indexable pages -> {root}")

# RULE: every link must have descriptive text (or an aria-label) and no two links
# on a page may share the same accessible name while pointing to different URLs.
GENERIC_LINK_TEXT = {
    "learn more", "read more", "read article", "read this article", "book", "quote",
    "click here", "more", "here", "read", "go", "details", "link", "this way", "view",
}

def audit_links(root, written):
    issues = 0
    for url, rel, _prio in written:
        html_txt = open(os.path.join(root, rel), encoding="utf-8").read()
        seen = {}
        for m in re.finditer(r"<a\s([^>]*?)>(.*?)</a>", html_txt, re.S | re.I):
            attrs, inner = m.group(1), m.group(2)
            href_m = re.search(r'href="([^"]*)"', attrs)
            if not href_m:
                continue
            href = href_m.group(1)
            if href.startswith(("tel:", "mailto:", "#", "https://wa.me")):
                continue
            aria = re.search(r'aria-label="([^"]*)"', attrs)
            text = re.sub(r"\s+", " ", strip_html(inner)).strip()
            name = (aria.group(1) if aria else text).strip().lower()
            if not name:
                continue
            if not aria and name in GENERIC_LINK_TEXT:
                print(f"  LINK-TEXT [{rel}] generic anchor '{text}' -> {href}")
                issues += 1
            if name in seen and seen[name] != href:
                print(f"  LINK-TEXT [{rel}] duplicate name '{name}' -> {href} and {seen[name]}")
                issues += 1
            seen.setdefault(name, href)
    print(f"  link-text audit: {'PASS — all links descriptive & unique' if not issues else str(issues)+' issue(s)'}")

def write_sitemap(root, written):
    urls = ""
    for url, rel, prio in written:
        loc = SITE["domain"] + ("/" if url == "/" else url)
        path = os.path.join(root, rel)
        try:
            mt = datetime.date.fromtimestamp(os.path.getmtime(path)).isoformat()
        except OSError:
            mt = TODAY
        cf = "weekly" if prio >= 0.8 else "monthly"
        urls += f"  <url><loc>{loc}</loc><lastmod>{mt}</lastmod><changefreq>{cf}</changefreq><priority>{prio}</priority></url>\n"
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + urls + "</urlset>\n")
    with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("  wrote sitemap.xml")

def write_robots(root):
    txt = (f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")
    with open(os.path.join(root, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    print("  wrote robots.txt")

def write_manifest(root):
    import json
    manifest = {
        "name": SITE["full_name"],
        "short_name": "Ocean City PAT",
        "description": ("Portable appliance testing, EICR and fire safety testing "
                        "across Plymouth, Devon and South East Cornwall."),
        "start_url": "/",
        "scope": "/",
        "display": "standalone",
        "lang": "en-GB",
        "dir": "ltr",
        "theme_color": "#206F8B",
        "background_color": "#ffffff",
        "icons": [
            {"src": "/images/icon-192.png", "sizes": "192x192",
             "type": "image/png", "purpose": "any"},
            {"src": "/images/icon-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any"},
            {"src": "/images/icon-maskable-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(root, "site.webmanifest"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("  wrote site.webmanifest")


def write_redirects(root):
    with open(os.path.join(root, "_redirects"), "w", encoding="utf-8") as f:
        f.write("# clean URLs handled by host; SPA-style 404 fallback\n/*  /404.html  404\n")
    with open(os.path.join(root, "_headers"), "w", encoding="utf-8") as f:
        f.write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
                "  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: geolocation=(), microphone=(), camera=()\n")
    with open(os.path.join(root, "CNAME"), "w", encoding="utf-8") as f:
        f.write("www.oceancitypattesting.co.uk\n")
    with open(os.path.join(root, ".nojekyll"), "w") as f:
        f.write("")
    print("  wrote _redirects, _headers, CNAME")

def write_llms(root, pages):
    lines = [f"# {SITE['full_name']}", "",
             f"> City &amp; Guilds qualified PAT testing, EICR electrical reports and fire safety testing "
             f"across Plymouth, Devon and South East Cornwall. Landlord, holiday let, business and charity "
             f"testing with same-day certificates. Phone {SITE['phone_display']}.", "",
             "## Pages", ""]
    for p in pages:
        if p.get("noindex"):
            continue
        loc = SITE["domain"] + ("/" if p["url"] == "/" else p["url"])
        lines.append(f"- [{strip_html(p['title'])}]({loc}): {strip_html(p['desc'])}")
    with open(os.path.join(root, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("  wrote llms.txt")

if __name__ == "__main__":
    main()
