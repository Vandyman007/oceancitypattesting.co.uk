# -*- coding: utf-8 -*-
"""Page content for Ocean City PAT Testing. Returns a list of page dicts."""

def build_pages(g):
    SITE = g["SITE"]; SERVICES = g["SERVICES"]; AREAS = g["AREAS"]; NEARBY = g["NEARBY"]
    ICONS = g["ICONS"]; service_cards = g["service_cards"]; page_banner = g["page_banner"]
    crumbs = g["crumbs_html"]; author = g["author_box"]; trust_block = g["trust_block"]
    cta_band = g["cta_band"]; mf = g["media_figure"]; logo_strip = g["logo_strip"]
    PRICE_TIERS = g["PRICE_TIERS"]; MIN_CALLOUT = g["MIN_CALLOUT"]; PRICE_FROM = g["PRICE_FROM"]
    PH = SITE["phone_display"]; TEL = SITE["phone_e164"]; EMAIL = SITE["email"]
    WA = g["WA_URL"]; AREA = SITE["area"]; YRS = SITE["experience_years"]

    pages = []

    # SEO title builder: "<head> | <brand>" but always < 60 chars (falls back
    # to a shorter brand suffix, then a hard trim) so no page title is ugly-cut.
    def mk_title(head, full="Ocean City PAT Testing", short="Ocean City"):
        head = g["strip_html"](head)
        for suffix in (full, short):
            t = f"{head} | {suffix}"
            if len(t) < 60:
                return t
        return f"{head} | {short}"[:59].rstrip(" |")

    # convenience: a row of area links
    def area_links():
        return ('<div class="area-links">'
                + ''.join(f'<a href="/areas-covered/{a[0]}">{ICONS["pin"]}{a[1]}</a>' for a in AREAS)
                + '</div>')

    def reviews_grid():
        return f"""
<section><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Reviews</span><h2>What customers across the South West say</h2></div>
  <div class="grid cols-3">
    <div class="card"><div class="stars" aria-label="5 out of 5 stars">{ICONS['star']*5}</div>
      <p>"Nathan tested every appliance in our holiday cottage and had the certificate to me before he'd left the drive. Professional, thorough and great value."</p><strong>— Hannah, Salcombe holiday let</strong></div>
    <div class="card"><div class="stars" aria-label="5 out of 5 stars">{ICONS['star']*5}</div>
      <p>"We use Ocean City for all six of our rental properties. Honest pricing, proper testing and always the paperwork our letting agent needs."</p><strong>— David, Plymouth landlord</strong></div>
    <div class="card"><div class="stars" aria-label="5 out of 5 stars">{ICONS['star']*5}</div>
      <p>"Came out to our café after hours so we didn't lose any trade. Spotted a dodgy kettle lead we'd never have noticed. Highly recommend."</p><strong>— Marie, Plymouth city centre café</strong></div>
  </div>
</div></section>"""

    # ===================================================================
    # HOME
    # ===================================================================
    home_hero = f"""
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <h1>PAT Testing in Plymouth, Devon &amp; South East Cornwall</h1>
      <p class="lead">Ocean City PAT Testing keeps you safe and compliant. We're a City &amp; Guilds qualified, Devon Trading Standards approved testing service providing portable appliance testing for landlords, holiday lets, businesses and community groups — with your certificate the same day.</p>
      <div class="hero-cta">
        <a class="btn btn-accent btn-lg" href="/contact">Get a free quote</a>
        <a class="btn btn-ghost btn-lg" href="tel:{TEL}">{ICONS['phone']}Call {PH}</a>
      </div>
      <div class="hero-trust">
        <span>{ICONS['check']}City &amp; Guilds qualified</span>
        <span>{ICONS['check']}Same-day certificates</span>
        <span>{ICONS['check']}{YRS}+ years' experience</span>
        <span>{ICONS['check']}Fully insured</span>
      </div>
    </div>
    <div class="hero-right">
    <div class="hero-card">
      <span class="tag">Fixed prices · free quote</span>
      <h2 style="margin-top:.6rem">From <span class="price">£{PRICE_FROM}</span></h2>
      <p style="color:var(--muted);margin:.2rem 0 0">Landlords from £{PRICE_FROM} per property, holiday lets from £65, businesses from £80 and just 90p per item for charities. Minimum call-out £{MIN_CALLOUT}.</p>
      <ul>
        <li>Visual inspection &amp; full electrical test</li>
        <li>Pass/fail label on every appliance</li>
        <li>Same-day PDF certificate emailed to you</li>
        <li>Honest advice — minor repairs on the spot</li>
      </ul>
      <a class="btn btn-primary btn-block" href="/pricing">See our prices</a>
    </div>
    </div>
  </div>
</div></section>

<section class="trust-strip tight"><div class="wrap">
  <div class="stat"><span class="n">Same day</span><span class="l">PDF certificates</span></div>
  <div class="stat"><span class="n">{YRS}+ yrs</span><span class="l">electrical experience</span></div>
  <div class="stat"><span class="n">{SITE['rating']}/5</span><span class="l">from {SITE['review_count']} reviews</span></div>
  <div class="stat"><span class="n">Devon &amp; Cornwall</span><span class="l">covered as standard</span></div>
</div></section>

<section><div class="wrap">
  <div class="section-head center"><span class="eyebrow">What we test</span>
    <h2>PAT testing and electrical safety for homes and businesses</h2>
    <p>One qualified, local engineer for every kind of electrical safety check — from a single rental flat to a full commercial premises. If it plugs in, we test it.</p>
  </div>
  {service_cards()}
</div></section>

<section class="section-cream"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">How it works</span>
    <h2>PAT testing in three simple steps</h2>
    <p>No fuss, no jargon and no waiting weeks for paperwork. Most jobs are booked, tested and certified inside a day.</p>
  </div>
  <div class="grid cols-3" style="margin-top:1.2rem">
    <div class="step"><h3>1. Tell us what you need</h3><p>Call or message {PH} with a rough idea of the property and how many appliances there are. We give you a fixed price up front — no surprises.</p></div>
    <div class="step"><h3>2. We test on site</h3><p>We arrive at an agreed time, visually inspect and electrically test every item, then label each one clearly as it passes. Minor faults are often fixed there and then.</p></div>
    <div class="step"><h3>3. Same-day certificate</h3><p>You get a full digital certificate the same day, ready for your insurer, letting agent, booking platform or a Health &amp; Safety inspector.</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="split">
    <div>
      <span class="eyebrow">Why Plymouth chooses us</span>
      <h2>Proper testing by a qualified engineer — not a sticker service</h2>
      <p>Some "PAT testers" do little more than glance at a plug and slap a label on it. We don't work that way. Every appliance gets a genuine visual inspection followed by a full electrical test — earth continuity, insulation resistance and polarity — using calibrated equipment, exactly as the IET Code of Practice sets out. That's the difference between a certificate that protects you and a sticker that doesn't.</p>
      <ul class="checklist">
        <li><strong>City &amp; Guilds qualified</strong> — testing carried out to the current IET Code of Practice.</li>
        <li><strong>Devon Trading Standards approved</strong> — a vetted local trader you can trust in your home.</li>
        <li><strong>Same-day certificates</strong> — digital paperwork that stands up to scrutiny.</li>
        <li><strong>Honest, fixed pricing</strong> — quoted before we start, with no hidden extras.</li>
      </ul>
      <a class="btn btn-primary" href="/about">More about Ocean City PAT Testing</a>
    </div>
    <div>
      <div class="info-card">
        <h3 style="margin-top:0">The PAT sticker traffic-light</h3>
        <p>Every item we test is labelled so anyone can see its status at a glance:</p>
        <ul class="pat-key">
          <li><span class="dot dot-green"></span><strong>Green</strong> — passed both the visual inspection and the electrical test. Safe to use.</li>
          <li><span class="dot dot-blue"></span><strong>Blue</strong> — passed a visual inspection only (for items that can't be fully tested).</li>
          <li><span class="dot dot-red"></span><strong>Red</strong> — failed. The item must be taken out of use immediately.</li>
        </ul>
        <p style="margin-bottom:0"><a href="/service-information">Read our full PAT testing guide &rarr;</a></p>
      </div>
    </div>
  </div>
</div></section>

<section class="section-light"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Areas covered</span>
    <h2>PAT testing across Plymouth, Devon &amp; South East Cornwall</h2>
    <p>From the Barbican to the South Hams and over the Tamar into Cornwall, we cover the whole region. Tap your area for local details.</p>
  </div>
  {area_links()}
  <p class="center" style="margin-top:1.4rem"><a class="btn btn-outline" href="/areas-covered">See all areas covered</a></p>
</div></section>
{reviews_grid()}
{logo_strip('Trusted locally', 'Businesses across the South West trust us with their safety', 'From holiday lets and dental practices to marine firms, care providers and letting agents, organisations across Plymouth, Devon and Cornwall rely on Ocean City PAT Testing for their electrical safety.')}
"""
    pages.append({
        "url": "/", "active": "home", "priority": 1.0,
        "title": "PAT Testing Plymouth | Landlord & Business | Ocean City",
        "desc": "City & Guilds qualified PAT testing in Plymouth, Devon & SE Cornwall — landlord, holiday let & business appliance testing, same-day certificate.",
        "og_alt": "Ocean City PAT Testing — Guiding You Safely",
        "breadcrumbs": [("Home", "/")],
        "body": home_hero,
        "faqs": [
            ("How much does PAT testing cost?",
             f"For landlords it starts at £{PRICE_FROM} per rental property, holiday lets from £65, businesses from £80 for the first 50 appliances and just 90p per item for charities and community groups. A minimum call-out of £{MIN_CALLOUT} applies. Every job includes a same-day certificate."),
            ("How quickly can you test and certify?",
             "Most appointments are offered within a day or two, and your full digital certificate is emailed to you the same day we test — there's no waiting around for paperwork."),
            ("Is PAT testing a legal requirement?",
             "There's no single law that says \"you must PAT test\", but the Electricity at Work Regulations 1989 require electrical equipment to be maintained in a safe condition. PAT testing is the recognised way to prove you've met that duty of care, and most insurers and letting agents expect to see a current certificate."),
            ("Do you cover my area?",
             f"We cover Plymouth, the South Hams and South East Cornwall as standard, including {', '.join(a[1] for a in AREAS[:6])} and many more. If you're nearby and not sure, just call {PH} and ask."),
        ],
    })

    # ===================================================================
    # SERVICES HUB
    # ===================================================================
    services_body = f"""
{page_banner('PAT Testing &amp; Electrical Safety Services', 'Portable appliance testing, EICR electrical reports and fire safety checks across Plymouth, Devon and South East Cornwall — all carried out by one qualified, fully insured local engineer.')}
{crumbs([('Home', '/'), ('Services', '/services')])}
<section><div class="wrap prose">
  <p>Ocean City PAT Testing offers a complete electrical safety service for homes, rental properties and businesses across {AREA}. Whether you're a landlord meeting your duty of care, a holiday-let owner protecting your guests, a business keeping its workplace compliant or a community group looking after volunteers, we have a service — and a price — to suit. Everything below is delivered by a City &amp; Guilds qualified engineer with over {YRS} years' hands-on electrical experience, and every job ends with a same-day certificate.</p>
</div></section>
<section class="tight"><div class="wrap">
  {service_cards()}
</div></section>
<section class="section-cream"><div class="wrap prose">
  <h2>Not sure which service you need?</h2>
  <p>Most of our customers start with <a href="/services/pat-testing">portable appliance testing</a> — the visual and electrical testing of everything that plugs into a socket. If you let property, our <a href="/services/landlord-pat-testing">landlord</a> and <a href="/services/holiday-let-pat-testing">holiday let</a> packages bundle that testing into a fixed price per property. Businesses usually want our <a href="/services/business-pat-testing">commercial testing</a>, which covers the first 50 appliances and adds an asset register. And if you need the fixed wiring checked rather than the appliances, that's an <a href="/services/eicr-electrical-testing">EICR</a>. Still unsure? Call {PH} and we'll point you the right way — advice is always free.</p>
</div></section>
"""
    pages.append({
        "url": "/services", "active": "services", "priority": 0.9,
        "title": "PAT Testing & Electrical Safety Services | Ocean City",
        "desc": "Our PAT testing, EICR and fire safety services for landlords, holiday lets, businesses and community groups across Plymouth, Devon and South East Cornwall.",
        "breadcrumbs": [("Home", "/"), ("Services", "/services")],
        "body": services_body,
    })

    # ===================================================================
    # SERVICE PAGES (per slug)
    # ===================================================================
    SERVICE_PAGES = {
        "pat-testing": {
            "h1": "PAT Testing Services in Plymouth",
            "sub": "Portable appliance testing for homes and businesses — visual inspection plus a full electrical test, certified the same day.",
            "lead": f"PAT testing — short for portable appliance testing — is the inspection and testing of electrical appliances to make sure they're safe to use. Ocean City PAT Testing provides thorough, no-shortcuts PAT testing across Plymouth, Devon and South East Cornwall, carried out by a City &amp; Guilds qualified engineer and backed by a same-day certificate.",
            "subject": "PAT testing", "kw": "PAT testing Plymouth",
            "sections": [
                ("What portable appliance testing actually involves",
                 "<p>There are two halves to a proper PAT test, and both matter. First comes the <strong>visual inspection</strong> — checking the plug, the cable, the casing and the fuse for damage, signs of overheating, the wrong fuse rating or a poorly wired plug. Industry figures suggest the large majority of faults are found at this stage, which is why a tester who skips it isn't really doing the job. Second comes the <strong>electrical test</strong>, carried out with a calibrated PAT tester: earth continuity, insulation resistance and, where relevant, polarity and lead checks. Only when an item passes both does it get a green pass label and go on your certificate.</p>"),
                ("What we test — and what counts as an 'appliance'",
                 "<p>If it plugs into a socket, it's in scope. That includes kettles, toasters, microwaves and fridges; computers, monitors, printers and chargers; power tools and extension leads; hairdryers, heaters, lamps and TVs; and larger fixed-plug equipment in workshops and kitchens. We test 240V equipment as standard and can also test 110V site equipment and 415V three-phase machinery. Extension leads and multi-way adaptors are tested too — they're one of the most common things to fail, and one of the most common things people forget.</p>"),
                ("How often should appliances be tested?",
                 "<p>There's no fixed legal interval. Instead, the IET Code of Practice recommends setting the frequency from a simple risk assessment — based on the type of equipment and the environment it's used in. As a rough guide, equipment on a construction site or in a busy commercial kitchen might be tested every few months, office IT every couple of years, and low-risk items in a quiet office less often again. For most landlords and small businesses, an annual or two-yearly test strikes the right balance. We're happy to advise on a sensible schedule for your particular setup — it's part of the service.</p>"),
            ],
            "faqs": [
                ("How long does PAT testing take?", "It depends on the number of appliances, but a typical rental property or small office takes one to two hours. We work efficiently and around you, so there's minimal disruption."),
                ("Will you remove items from use if they fail?", "Yes. Any item that fails is labelled red and we'll advise you to stop using it immediately. Many minor faults — a blown fuse, a damaged plug, a frayed lead end — can be repaired on the spot so the item passes."),
                ("Do I get a certificate?", "Always. You receive a full digital certificate the same day, listing every appliance tested with its result, ready for your insurer, letting agent or an inspector."),
                ("Can you test out of hours?", "Yes — for businesses especially, we're happy to test in the evening or at weekends so you don't lose any trade or disrupt your staff."),
            ],
        },
        "landlord-pat-testing": {
            "h1": "Landlord PAT Testing in Plymouth",
            "sub": "Keep your rental properties compliant and your tenants safe — fixed price per property, certified the same day.",
            "lead": f"As a landlord you have a legal duty to keep the electrical appliances you supply in a safe condition. Ocean City PAT Testing makes landlord PAT testing across Plymouth, Devon and South East Cornwall simple: a fixed price from £{PRICE_FROM} per property, a qualified engineer who works around your tenants, and the certificate your letting agent and insurer need — the same day.",
            "subject": "landlord PAT testing", "kw": "landlord PAT testing Plymouth",
            "sections": [
                ("Your responsibilities as a landlord",
                 "<p>The law is clear that any electrical appliance you provide as part of a tenancy — the cooker, the washing machine, the fridge, supplied lamps, the vacuum cleaner — must be safe. The Electricity at Work Regulations 1989, the Landlord and Tenant Act and your own insurance policy all point the same way: you need to be able to evidence that the equipment is maintained. PAT testing is the simplest, most widely accepted way to do exactly that. It sits alongside your EICR (the five-yearly fixed-wiring check that <em>is</em> a legal requirement for rentals in England) and your gas safety certificate as part of a complete, defensible safety file.</p>"),
                ("Why landlords choose Ocean City PAT Testing",
                 "<p>We understand letting. We coordinate access with tenants or agents, turn up on time, and work quickly so we're not in anyone's way. Our per-property pricing means no nasty surprises whether the flat has eight appliances or eighteen, and you get a clear digital certificate you can forward straight to your managing agent. For portfolio landlords we'll happily test multiple properties in a planned round and keep your renewal dates on file so you never fall out of date. It's the kind of reliable, low-hassle service that keeps landlords coming back year after year.</p>"),
                ("What happens if an appliance fails",
                 "<p>If something fails, we don't just condemn it and walk away. We explain what's wrong in plain English, label the item red so nobody uses it, and where it's a quick fix — a fuse, a plug top, a cable end — we can often repair it on the spot so it passes. If a tenant's own appliance is dangerous we'll flag it to you too, because a fault in their kettle can still cause a fire in your property. The goal is always a safe home and a clean certificate, not a list of problems.</p>"),
            ],
            "faqs": [
                ("Is PAT testing a legal requirement for landlords?", "PAT testing itself isn't named in law, but the duty to keep supplied appliances safe is — and PAT testing is the recognised way to prove you've met it. The separate EICR fixed-wiring check is a legal requirement for rented homes in England every five years."),
                ("How often should a rental property be PAT tested?", "Most landlords test annually or every two years, often timed to coincide with a change of tenancy. We'll advise a sensible interval based on the property and its appliances."),
                ("Do you test between tenancies?", "Yes — a void period is the ideal time to test, with no tenants to work around. We can usually fit in around your turnaround schedule at short notice."),
                ("Can you test several of my properties at once?", "Absolutely. We look after portfolio landlords across the South West and can plan a testing round, keep your renewal dates on record and remind you when each property is due."),
            ],
        },
        "holiday-let-pat-testing": {
            "h1": "Holiday Let &amp; Airbnb PAT Testing",
            "sub": "Protect your guests, your reviews and your insurance — PAT testing for cottages, Airbnbs and serviced lets across the South West.",
            "lead": "A holiday let is a workplace in the eyes of health and safety law, and it's full of appliances your guests will use unsupervised — kettles, toasters, hairdryers, heaters, hot tubs and kitchen white goods. Ocean City PAT Testing keeps self-catering properties across Plymouth, the South Hams and South East Cornwall safe and compliant, with flexible scheduling around your changeover days and a certificate the same day.",
            "subject": "holiday let PAT testing", "kw": "holiday let PAT testing Devon",
            "sections": [
                ("Why holiday lets need testing more than most",
                 "<p>Think about how a holiday property is used. Different people every week, all bringing their own habits — overloading sockets, leaving chargers plugged in, using the hairdryer in the bathroom. Guests can't be expected to spot a frayed lead or a cracked plug, so the responsibility to make sure everything is safe sits squarely with you, the owner. Your guests' safety is the first reason to test. The second is commercial: booking platforms increasingly ask owners to confirm their property meets safety standards, and a single electrical incident can end a season's worth of good reviews. Regular PAT testing protects all of it.</p>"),
                ("What we test in a typical holiday property",
                 "<p>We test everything provided for guest use: the kettle, toaster, microwave and coffee machine; the fridge, freezer, oven, hob and dishwasher; TVs, sound systems and games consoles; hairdryers, straighteners and bathroom heaters; lamps, fans and portable heaters; and any outdoor electricals like hot tub controls or patio heaters. Welcome-pack extras and that drawer of spare chargers count too. We label each item, note anything that needs replacing before your next guests arrive, and leave you with a complete record for your safety file.</p>"),
                ("Fitting around your changeovers",
                 "<p>We know a holiday let only sits empty for a few hours between bookings, so we're flexible. We'll work around your changeover schedule — testing on a turnaround day, between guests, or during a maintenance gap — and we're quick and tidy so your cleaners can get on around us. For owners with several cottages we can test the whole group in one visit and keep your renewal dates on file. It's a small, sensible cost that buys real peace of mind every time you hand over the keys.</p>"),
            ],
            "faqs": [
                ("Do holiday lets legally need PAT testing?", "Health and safety law treats a holiday let as a place of work, so you have a duty to ensure the electrical equipment provided is safe. PAT testing is the standard way to demonstrate that, and most holiday-let insurers expect to see a current certificate."),
                ("How often should a holiday let be tested?", "Because of the high turnover and unsupervised use, annual PAT testing is the usual recommendation for holiday lets — we'll confirm what's right for your property."),
                ("Can you test around our guests?", "Yes. We schedule around changeover days and work quickly so testing never clashes with a booking. For multiple properties we can plan a single efficient visit."),
                ("Will my booking platform accept the certificate?", "Yes — our digital certificates are a recognised record of testing and are exactly what platforms and insurers ask for as proof of electrical safety."),
            ],
        },
        "business-pat-testing": {
            "h1": "Business &amp; Commercial PAT Testing",
            "sub": "Offices, shops, salons, cafés, gyms and workshops — tested with same-day certification and an asset register, around your opening hours.",
            "lead": "Every business has a legal duty to keep its electrical equipment safe for staff, customers and visitors. Ocean City PAT Testing provides commercial PAT testing across Plymouth, Devon and South East Cornwall from £80 for your first 50 appliances, with a low per-item rate beyond that, an asset register and a same-day digital certificate — tested out of hours if you'd rather we didn't get in the way.",
            "subject": "business PAT testing", "kw": "business PAT testing Plymouth",
            "sections": [
                ("Your duty of care as an employer",
                 "<p>Under the Health and Safety at Work Act 1974 and the Electricity at Work Regulations 1989, employers and the people in control of commercial premises must keep electrical equipment maintained so it doesn't cause harm. If a portable appliance causes a fire or injures someone, the first thing an investigator or your insurer will ask for is evidence the equipment was being looked after — and a current PAT certificate is exactly that. Beyond the legal box-ticking, it's simply good business: faulty equipment causes downtime, and a quick test now prevents an expensive problem later.</p>"),
                ("Built around your business, not the other way round",
                 "<p>We know you can't down tools for a day while someone unplugs every computer in the office, so we work around you. We test out of hours, early mornings or weekends if that suits, move methodically through the premises and re-plug everything exactly as we found it. You get an asset register — a full inventory of every item with its test result and next-due date — which makes managing future testing straightforward and gives any inspector confidence that you've got a proper system in place. The first 50 appliances are covered in the base price, with a low fixed rate for anything beyond, all quoted before we start.</p>"),
                ("From small shops to busy workshops",
                 "<p>We test all kinds of commercial premises across the region — high-street shops and salons, offices and co-working spaces, cafés, restaurants and takeaways, gyms and studios, surgeries and care settings, and trade workshops with 110V and three-phase equipment. Whatever your setup, the approach is the same: a genuine inspection and test of every item, clear labelling, an honest conversation about anything that fails, and paperwork that stands up to scrutiny. We've built our reputation on doing it properly, and a lot of our commercial work comes from referrals.</p>"),
            ],
            "faqs": [
                ("How much does commercial PAT testing cost?", "Business testing starts at £80 for the first 50 appliances, with a low fixed rate per item after that. We quote the full price up front once we know roughly how many items you have — there are never hidden extras."),
                ("Can you test outside our opening hours?", "Yes. Out-of-hours, early-morning and weekend testing is no problem and is often the easiest way to avoid disrupting staff and customers."),
                ("Do we get an asset register?", "Yes — commercial jobs include a full asset register listing every appliance, its result and its next test date, alongside your digital certificate."),
                ("How often does a business need PAT testing?", "It depends on your environment and equipment. Offices are often tested every one to two years, while higher-risk settings like kitchens and workshops are tested more frequently. We'll recommend a schedule based on a quick risk assessment."),
            ],
        },
        "charity-community-pat-testing": {
            "h1": "Charity &amp; Community Group PAT Testing",
            "sub": "Churches, village halls, clubs, pre-schools and community projects — our lowest rate at just 90p per appliance.",
            "lead": "Keeping members, volunteers and visitors safe shouldn't stretch a tight budget. Ocean City PAT Testing offers charities, churches, clubs and community groups across Plymouth, Devon and South East Cornwall our lowest rate — just 90p per appliance tested — with the same qualified engineer, the same thorough test and the same same-day certificate as everyone else.",
            "subject": "charity PAT testing", "kw": "charity PAT testing Devon",
            "sections": [
                ("Affordable testing for not-for-profits",
                 "<p>Community spaces are often packed with electrical equipment that's been donated, borrowed or in use for years — urns and kettles in the kitchen, heaters and PA systems in the hall, kit for clubs and classes, toys and appliances in a pre-school. All of it needs to be safe for the people who use it, but we know that every pound a charity spends is a pound that could go elsewhere. That's why community groups get our 90p-per-item rate. It keeps you compliant and your insurance valid without taking a bite out of funds you'd rather spend on your members.</p>"),
                ("Who we help",
                 "<p>We test for all sorts of community organisations across the South West: parish churches and chapels, village and church halls, scout and guide groups, sports and social clubs, pre-schools and toddler groups, food banks and community kitchens, charity shops and not-for-profit projects. Whether you've a handful of appliances in a small hall or a building full of donated equipment, we'll work through it carefully, label everything clearly and leave you with a certificate for your records and your insurer. We're happy to schedule around your activities so testing never gets in the way of what you do.</p>"),
                ("The same thorough test, just cheaper",
                 "<p>A lower price never means a lower standard. Community groups get exactly the same service as our commercial customers — a full visual inspection and electrical test of every item, by the same City &amp; Guilds qualified engineer, with the same honest advice if something needs replacing. Many faults we find in community settings are simple to fix, and we'll sort minor ones on the spot. If you run a hall that's hired out to others, a current PAT certificate is also a reassurance you can offer every group that uses your space. We're also happy to work with trustees and volunteer committees who look after the paperwork, keeping your test dates on file and giving you a gentle reminder when the next round is due — so electrical safety stays one less thing for a busy, unpaid committee to chase up each year.</p>"),
            ],
            "faqs": [
                ("How much is charity PAT testing?", "Just 90p per appliance tested — our lowest rate, available to registered charities, churches, clubs and community groups. A minimum call-out of £%d applies." % MIN_CALLOUT),
                ("Do we still get a proper certificate?", "Yes. Community groups receive the same full digital certificate as every other customer, listing each appliance and its result — ideal for your records and your insurer."),
                ("Can you test our village hall around bookings?", "Of course. We'll fit testing around your hall's hire schedule and activities so it causes no disruption to the groups that use it."),
                ("Do you test donated and second-hand equipment?", "Yes — donated and older equipment is exactly the sort of thing that benefits most from testing, and we'll flag anything that's no longer safe to use."),
            ],
        },
        "eicr-electrical-testing": {
            "h1": "EICR &amp; Fixed Wire Testing in Plymouth",
            "sub": "Electrical Installation Condition Reports for landlords, homeowners and businesses — the five-yearly check of your fixed wiring.",
            "lead": "An EICR — Electrical Installation Condition Report — checks the safety of the fixed wiring in a property: the consumer unit, the circuits, the sockets and the switches, rather than the appliances that plug into them. Ocean City PAT Testing arranges EICR and fixed-wire testing across Plymouth, Devon and South East Cornwall through our qualified electricians, so you can sort your wiring and your appliances with one trusted local contact.",
            "subject": "EICR testing", "kw": "EICR Plymouth",
            "sections": [
                ("PAT testing vs an EICR — what's the difference?",
                 "<p>It's a common mix-up, so here's the simple version. <strong>PAT testing</strong> covers the things that plug in — the kettle, the computer, the lamp. An <strong>EICR</strong> covers the fixed electrical installation — the wiring in the walls, the fuse board, the sockets and light fittings. Both are part of keeping a property electrically safe, and most landlords and businesses need both. The big difference is that an EICR is a <em>legal requirement</em> for rented homes in England, which must have a satisfactory report at least every five years, whereas PAT testing is the recognised way to meet the separate duty to keep appliances safe.</p>"),
                ("What an EICR involves",
                 "<p>A qualified electrician inspects and tests the installation, then records its condition in a formal report. Any issues are coded: <strong>C1</strong> (danger present — immediate action required), <strong>C2</strong> (potentially dangerous — remedial work needed), or <strong>C3</strong> (improvement recommended). A report is judged 'satisfactory' or 'unsatisfactory' overall, and if remedial work is needed we'll explain exactly what's required and what it will cost. For landlords, a satisfactory EICR is the document you must be able to provide to your tenants and, on request, your local authority.</p>"),
                ("One contact for wiring and appliances",
                 "<p>Plenty of properties need both an EICR and PAT testing — a rental, a holiday let, a shop or an office. Rather than juggle two contractors, you can sort both through Ocean City PAT Testing and keep everything on one renewal schedule. We'll test your portable appliances and arrange the fixed-wire inspection, hand you both certificates, and keep your due dates on file so nothing slips. It's the straightforward, joined-up approach that busy landlords and business owners tell us they want.</p>"),
            ],
            "faqs": [
                ("Is an EICR a legal requirement?", "For rented homes in England, yes — landlords must have a satisfactory EICR at least every five years and provide a copy to tenants. For owner-occupied homes it's strongly recommended, especially when buying, selling or after major work."),
                ("How often do I need an EICR?", "At least every five years for rentals, or at change of occupancy. Commercial premises are typically every five years too, and older installations may warrant more frequent checks."),
                ("What's the difference between an EICR and PAT testing?", "An EICR checks the fixed wiring (consumer unit, circuits, sockets); PAT testing checks the appliances that plug into it. Most landlords and businesses need both, and we can arrange both."),
                ("What happens if my EICR is unsatisfactory?", "We'll explain the coded issues in plain terms and quote any remedial work needed to make the installation safe and achieve a satisfactory report."),
            ],
        },
        "fire-safety-testing": {
            "h1": "Fire Safety Testing in Plymouth",
            "sub": "Fire extinguisher, alarm and emergency lighting checks to complete your safety paperwork in one visit.",
            "lead": "Electrical safety and fire safety go hand in hand, so we make it easy to sort both together. Alongside PAT testing, Ocean City PAT Testing can check your fire extinguishers, fire alarm and emergency lighting across Plymouth, Devon and South East Cornwall — helping landlords, holiday-let owners and businesses keep a complete, up-to-date safety file from a single trusted contact.",
            "subject": "fire safety testing", "kw": "fire safety testing Plymouth",
            "sections": [
                ("Why fire safety sits alongside PAT testing",
                 "<p>Faulty electrics are one of the leading causes of accidental fires in homes and workplaces, which is why PAT testing and fire safety belong together. The Regulatory Reform (Fire Safety) Order 2005 places a duty on the 'responsible person' for most non-domestic premises — and many shared residential ones — to manage fire risk, which includes keeping fire-fighting and fire-detection equipment in working order. Pairing your appliance testing with a check of your extinguishers, alarms and emergency lighting means one visit, one contact and one tidy set of paperwork covering both electrical and fire safety.</p>"),
                ("What we check",
                 "<p>Depending on your premises, we can check that fire extinguishers are present, in date, correctly sited and properly pressurised; that your fire alarm and smoke and heat detectors are working and audible; and that emergency lighting comes on and stays lit when the power is cut. We'll point out anything missing or out of date — an extinguisher past its service date, a flat emergency light, a smoke alarm that's been taken down — and advise what's needed to put it right. For holiday lets in particular, working alarms and the right extinguishers and fire blanket are essentials your insurer will expect.</p>"),
                ("A complete safety package",
                 "<p>For landlords and holiday-let owners especially, it makes sense to keep all your safety obligations in one place. We can combine PAT testing, an EICR and a fire safety check into a single coordinated visit, so your property is covered from the wiring to the appliances to the smoke alarms — with all the certificates you need handed over together and your renewal dates kept on file. It's the simplest way to stay on top of compliance without chasing several different contractors around the calendar. And because everything sits on one schedule, you'll get a single reminder when anything is coming up for renewal — the extinguisher service, the emergency-light test, the next EICR — rather than trying to remember half a dozen different dates spread across the year.</p>"),
            ],
            "faqs": [
                ("Do you service fire extinguishers?", "We check that extinguishers are present, in date, correctly located and pressurised, and flag anything that needs a full service or replacement. We'll advise you clearly on what's required."),
                ("Can you check my holiday let's smoke alarms?", "Yes. We'll test smoke and heat alarms and emergency lighting and confirm you have the right fire equipment in place — exactly what holiday-let insurers and guests expect."),
                ("Can fire safety be done with my PAT testing?", "Yes — combining your PAT test, EICR and fire safety checks into one visit is the easiest way to keep a complete safety file and save on call-outs."),
                ("Who is the 'responsible person' for fire safety?", "In most workplaces and shared premises it's the employer, owner or whoever has control of the premises. They have a duty to manage fire risk, which includes keeping fire equipment maintained."),
            ],
        },
    }

    # Verified image placements per service page (image, alt, caption) — produced
    # and adversarially relevance-checked by the pat-image-placement workflow.
    SERVICE_FIG = {
        "pat-testing": ("uk-plug-wiring-fuse.webp",
            "Inside a UK 13A plug showing live, neutral and earth wires and fuse during PAT testing Plymouth",
            "A correctly wired and fused UK 13A plug, checked during the visual and electrical PAT testing process."),
        "landlord-pat-testing": ("landlord-pat-testing-advert.webp",
            "Landlord PAT testing Plymouth from £35 for rental property electrical safety checks",
            "Affordable landlord PAT testing in Plymouth from £35, helping landlords meet their duty of care."),
        "holiday-let-pat-testing": ("holiday-let-pat-testing-advert.webp",
            "Holiday let PAT testing Devon — Airbnb and self-catering appliance safety from £65",
            "Holiday let PAT testing across Devon from £65, keeping Airbnb and self-catering guests safe."),
        "business-pat-testing": ("business-pat-testing-advert.webp",
            "Business PAT testing Plymouth from £80 for commercial premises and employer duty of care",
            "Business PAT testing in Plymouth from £80, helping employers meet their electrical safety duty."),
        "charity-community-pat-testing": ("charity-pat-testing-advert.webp",
            "Charity PAT testing Devon at 90p per item for community groups across the South West",
            "Charity and community group PAT testing across Devon from just 90p per item."),
        "eicr-electrical-testing": ("uk-plug-wiring-fuse.webp",
            "EICR Plymouth electrical testing — live, neutral and earth wiring with a 13A fuse in a UK plug",
            "A fixed-wire EICR checks the wiring and connections in your installation, like the conductors in this UK plug."),
        "fire-safety-testing": ("electrical-compliance-stamp.webp",
            "Compliance stamp for fire safety testing Plymouth — extinguishers, alarms and emergency lighting",
            "Staying compliant with fire safety duty-of-care paperwork across Plymouth and the South West."),
    }

    for slug, label, blurb, icon, kw in SERVICES:
        c = SERVICE_PAGES[slug]
        sections_html = "".join(
            f'<h2>{title}</h2>{body}' for title, body in c["sections"]
        )
        _fig = SERVICE_FIG.get(slug)
        fig_html = mf(*_fig) if _fig else ""
        body = f"""
{page_banner(c['h1'], c['sub'])}
{crumbs([('Home', '/'), ('Services', '/services'), (g['strip_html'](label), f'/services/{slug}')])}
<section><div class="wrap">
  <div class="split">
    <div class="prose">
      <p class="lead-p">{c['lead']}</p>
      {fig_html}
      {sections_html}
    </div>
    <aside class="side">
      <div class="side-card">
        <h3>Book {g['strip_html'](label).lower()}</h3>
        <p>Fast, friendly and fully qualified. Tell us about your property and we'll give you a fixed price the same day.</p>
        <a class="btn btn-primary btn-block" href="/contact">Get a free quote</a>
        <a class="btn btn-outline btn-block" href="tel:{TEL}" style="margin-top:.5rem">{ICONS['phone']}Call {PH}</a>
        <ul class="side-list">
          <li>{ICONS['check']}City &amp; Guilds qualified</li>
          <li>{ICONS['check']}Same-day certificate</li>
          <li>{ICONS['check']}Fully insured</li>
          <li>{ICONS['check']}{YRS}+ years' experience</li>
        </ul>
      </div>
      <div class="side-card side-areas">
        <h3>Where we test</h3>
        <p>{', '.join(a[1] for a in AREAS)} and across {AREA}.</p>
        <a href="/areas-covered">See all areas covered &rarr;</a>
      </div>
    </aside>
  </div>
  <div class="prose" style="margin-top:1.4rem">
    {trust_block(c['subject'], kw)}
  </div>
  {author()}
</div></section>
<section class="section-cream"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">More services</span><h2>Other electrical safety services</h2></div>
  {service_cards(exclude=slug)}
</div></section>
"""
        pages.append({
            "url": f"/services/{slug}", "active": "services", "priority": 0.8,
            "title": mk_title(c["h1"]),
            "desc": g["strip_html"](c["sub"])[:155],
            "breadcrumbs": [("Home", "/"), ("Services", "/services"), (g['strip_html'](label), f'/services/{slug}')],
            "body": body,
            "faqs": c["faqs"],
        })

    # ===================================================================
    # PRICING
    # ===================================================================
    tier_cards = ""
    for t in PRICE_TIERS:
        money = t.get("money") or f"£{t['from']}"
        inc = "".join(f"<li>{ICONS['check']}{x}</li>" for x in t["includes"])
        tier_cards += f"""
    <div class="price-card">
      <div class="ico">{ICONS.get(t['icon'], ICONS['plug'])}</div>
      <h3>{t['name']}</h3>
      <div class="price-amt"><span class="amt">{money}</span> <span class="unit">{t['unit']}</span></div>
      <p>{t['blurb']}</p>
      <ul class="price-inc">{inc}</ul>
      <a class="btn btn-primary btn-block" href="/contact">Get a quote</a>
    </div>"""
    pricing_body = f"""
{page_banner('PAT Testing Prices', f'Honest, fixed pricing with no hidden extras. Landlords from £{PRICE_FROM}, holiday lets from £65, businesses from £80 and just 90p per item for charities — every job includes a same-day certificate.')}
{crumbs([('Home', '/'), ('Pricing', '/pricing')])}
<section><div class="wrap prose">
  <p class="lead-p">PAT testing prices shouldn't be a mystery. At Ocean City PAT Testing we quote a fixed price up front based on your property and the number of appliances, so you know exactly what you'll pay before we start. Every price below includes the visual inspection, the full electrical test, clear pass/fail labelling and a same-day digital certificate. A minimum call-out of £{MIN_CALLOUT} applies to every visit.</p>
</div></section>
<section class="tight"><div class="wrap">
  <div class="price-grid">{tier_cards}</div>
  <p class="center" style="margin-top:1rem;color:var(--muted)">All prices exclude VAT where applicable. Larger sites and multi-property rounds are quoted individually — <a href="/contact">ask for a tailored quote</a>.</p>
  {mf("minimum-call-out-advert.webp", f"Ocean City PAT Testing prices with a minimum call-out of £{MIN_CALLOUT} across Plymouth and the South West", f"Every visit has a £{MIN_CALLOUT} minimum call-out, which also covers a typical small rental property.")}
</div></section>
<section class="section-cream"><div class="wrap prose">
  <h2>What's always included in the price</h2>
  <p>Whatever you're booking, every Ocean City PAT Testing job includes the same thorough service. We carry out a full visual inspection of every appliance, plug, lead and fuse; a complete electrical test using calibrated equipment; clear traffic-light labelling on each item; minor repairs such as replacing a fuse or rewiring a plug top where they're quick to do; honest advice on anything that needs replacing; and a same-day digital certificate listing every item and its result. There's no charge for the advice and no pressure to spend money you don't need to.</p>
  <h2>How we work out your price</h2>
  <p>For landlords and holiday lets we price per property, because it's predictable and fair — you're not counting plugs or watching a meter. For businesses we cover the first 50 appliances in the base price and add a low fixed rate per item beyond that, quoted before we begin. For charities and community groups we simply charge 90p per appliance tested. If your job is unusual — a large commercial site, a property packed with equipment, or a mix of 240V, 110V and three-phase machinery — we'll come back with a tailored quote. Either way, the number we give you is the number you pay.</p>
  <h2>Why the cheapest quote isn't always the best value</h2>
  <p>You'll occasionally see eye-catching low prices for "PAT testing" that turn out to be little more than a quick look and a sticker. A certificate is only worth having if the testing behind it was done properly — and if it ever has to satisfy an insurer or a Health &amp; Safety inspector after an incident, a box-ticked job can leave you exposed. We'd rather do it right: a genuine test of every item, by a qualified engineer, with paperwork that holds up. That's the value in our pricing, and it's why customers stay with us.</p>
  <h2>Discounts for multiple properties</h2>
  <p>If you're a portfolio landlord, a letting agent or a holiday-let owner with several cottages, it's almost always cheaper to test them together. We'll plan an efficient round, quote a combined price that reflects the saved travel and setup time, and keep all your renewal dates on a single schedule so nothing slips out of date. The same applies to businesses with more than one site. Just tell us how many properties are involved and roughly where they are, and we'll put together a tailored quote.</p>
  <h2>What can affect the final price</h2>
  <p>For most jobs the headline price is all there is to it, but a few things genuinely change the amount of work involved, and we'll always tell you up front if they apply. A property crammed with appliances — a fully equipped holiday cottage, say, or a busy café kitchen — takes longer than a sparsely furnished flat. Specialist equipment such as 110V site tools or 415V three-phase machinery needs different testing. And a site that needs out-of-hours access or has equipment spread across several floors or buildings adds time too. None of these are hidden surcharges sprung on you at the end; they're simply factored into the fixed price we agree before we start.</p>
  <h2>How and when you pay</h2>
  <p>Payment is due on completion, once your testing is finished and your certificate is on its way to you. We accept cash, card and bank transfer, whichever is easiest for you, and we'll provide a receipt and an invoice for your records if you need them for business or tax purposes. There's no deposit to pay and no charge at all for giving you a quote or talking through what you need — we only ask for payment once the work is done and you're holding a certificate you can rely on.</p>
</div></section>
"""
    pages.append({
        "url": "/pricing", "active": "pricing", "priority": 0.9,
        "title": "PAT Testing Prices Plymouth | From £35 | Ocean City",
        "desc": f"Fixed PAT testing prices: landlords from £{PRICE_FROM} per property, holiday lets from £65, businesses from £80, charities 90p per item. Same-day certificate. Free quote.",
        "breadcrumbs": [("Home", "/"), ("Pricing", "/pricing")],
        "body": pricing_body,
        "faqs": [
            ("Is there a minimum charge?", f"Yes — a minimum call-out of £{MIN_CALLOUT} applies to every visit, which also covers landlord testing for a typical small rental property."),
            ("Are your prices fixed or estimates?", "Fixed. Once we know your property and roughly how many appliances are involved, we give you a set price up front — there are no hidden extras added on the day."),
            ("Do you charge for items that fail?", "No. You're charged for testing, not results, and minor repairs like a new fuse or plug top are usually included so the item can pass."),
            ("Can you quote for multiple properties?", "Yes — portfolio landlords and multi-site businesses get a tailored quote, and we'll keep your renewal dates on file so you never fall out of date."),
        ],
    })

    # ===================================================================
    # AREAS HUB
    # ===================================================================
    areas_body = f"""
{page_banner('Areas We Cover', f'PAT testing, EICR and fire safety across Plymouth, Devon and South East Cornwall — covering {", ".join(a[1] for a in AREAS[:6])} and far beyond.')}
{crumbs([('Home', '/'), ('Areas Covered', '/areas-covered')])}
<section><div class="wrap prose">
  <p class="lead-p">Ocean City PAT Testing is based in Plymouth and covers a wide stretch of the South West — the whole of the city, out across the South Hams, and over the Tamar into South East Cornwall. Wherever you are in the region, you get the same qualified engineer, the same thorough testing and the same same-day certificate. Choose your area below for local details, or call {PH} if your town isn't listed — chances are we cover it.</p>
</div></section>
<section class="tight"><div class="wrap">
  {area_links()}
</div></section>
<section class="section-cream"><div class="wrap prose">
  <h2>Plymouth, the South Hams and South East Cornwall</h2>
  <p>From our base in Plymouth we regularly test in {', '.join(a[1] for a in AREAS)}, as well as {', '.join(NEARBY[:8])} and the surrounding villages. That covers city-centre offices and shops, harbourside holiday lets in the South Hams, rental properties across the suburbs, and community halls and clubs in the Cornish towns just over the river. Travel within the area is included in our pricing, so a property in Saltash or Salcombe costs the same to test as one in the centre of Plymouth.</p>
  <h2>One local contact for your whole portfolio</h2>
  <p>If you own or manage property in more than one of these areas, you don't need a different tester for each. We look after landlords and holiday-let owners with properties spread right across Devon and Cornwall, planning efficient testing rounds and keeping every renewal date on file. It's the same joined-up, low-hassle service whether you have one flat or twenty — and it's why so much of our work comes from repeat customers and referrals across the South West.</p>
</div></section>
"""
    pages.append({
        "url": "/areas-covered", "active": "areas", "priority": 0.8,
        "title": "Areas Covered | PAT Testing Plymouth, Devon & Cornwall",
        "desc": "PAT testing across Plymouth, the South Hams & South East Cornwall — Saltash, Torpoint, Tavistock, Liskeard, Salcombe and more. Same-day certificates.",
        "breadcrumbs": [("Home", "/"), ("Areas Covered", "/areas-covered")],
        "body": areas_body,
    })

    # ===================================================================
    # AREA PAGES
    # ===================================================================
    AREA_BLURB = {
        "plymouth": ("Plymouth", "Devon", "the Barbican, the city centre, Mutley, Mannamead, Stoke, Devonport and the newer estates at Sherford and Saltram Meadow",
                     "As our home city, Plymouth is where we test most — from harbourside holiday flats and city-centre cafés to rental terraces and busy offices."),
        "plympton": ("Plympton", "Devon", "Plympton St Maurice, Underwood, Chaddlewood and Colebrook",
                     "Plympton's mix of family homes, rentals and small businesses keeps us busy, and it's just minutes from our base."),
        "saltash": ("Saltash", "Cornwall", "the town centre, Burraton, Latchbrook and the waterside properties along the Tamar",
                    "Just over the bridge into Cornwall, Saltash is firmly within our standard coverage — landlords and businesses here pay no more than those in the city."),
        "torpoint": ("Torpoint", "Cornwall", "the town, Antony and the Rame Peninsula villages",
                     "We reach Torpoint via the ferry and cover the Rame Peninsula's holiday cottages and community halls as part of our South East Cornwall round."),
        "callington": ("Callington", "Cornwall", "the town and surrounding villages towards Kit Hill",
                       "Callington and the surrounding parishes sit comfortably within our Cornwall coverage, with plenty of rural lets and community buildings."),
        "tavistock": ("Tavistock", "Devon", "the town centre, Whitchurch and the western edge of Dartmoor",
                      "This historic stannary town on the edge of Dartmoor has a strong holiday-let and hospitality trade that relies on regular testing."),
        "liskeard": ("Liskeard", "Cornwall", "the town centre and nearby villages towards the moor",
                     "Liskeard anchors our reach into mid-Cornwall, with market-town shops, rentals and community groups all on our books."),
        "looe": ("Looe", "Cornwall", "East and West Looe and the surrounding coastline",
                 "Looe's busy holiday-let and hospitality scene means plenty of appliances and high guest turnover — exactly where thorough PAT testing matters most."),
        "kingsbridge": ("Kingsbridge", "Devon", "the town and the South Hams estuary villages",
                        "At the head of its estuary, Kingsbridge and the surrounding South Hams are full of self-catering cottages that we test every season."),
        "salcombe": ("Salcombe", "Devon", "the town and the high-end holiday lets along the estuary",
                     "Salcombe's premium holiday properties carry a lot of guest-use equipment, and owners here value testing that protects both guests and reviews."),
        "totnes": ("Totnes", "Devon", "the town centre, Bridgetown and the surrounding South Hams",
                   "Totnes's independent shops, cafés and community spaces make it a regular stop on our South Hams testing rounds."),
        "dartmouth": ("Dartmouth", "Devon", "the town, the waterfront and the South Hams coast",
                      "Dartmouth's harbourside holiday lets, hotels and hospitality businesses keep us testing along this stretch of the South Hams coast."),
    }
    for slug, name in AREAS:
        nm, county, districts, hook = AREA_BLURB[slug]
        nm_plain = nm
        # Plymouth gets its true local image (Smeaton's Tower on the Hoe); other
        # towns stay text+sidebar to avoid repeating one generic photo sitewide.
        area_fig = mf("plymouth-hoe-lighthouse-sunset.webp",
                      "Smeaton's Tower on Plymouth Hoe at sunset, home base for PAT testing Plymouth services",
                      "PAT testing across Plymouth, from the Hoe and city centre to every surrounding neighbourhood.") if slug == "plymouth" else ""
        body = f"""
{page_banner(f'PAT Testing in {nm}', f'Qualified portable appliance testing, EICR and fire safety checks for homes, holiday lets and businesses in {nm}, {county} — certified the same day.')}
{crumbs([('Home', '/'), ('Areas Covered', '/areas-covered'), (nm_plain, f'/areas-covered/{slug}')])}
<section><div class="wrap">
  <div class="split">
    <div class="prose">
      <p class="lead-p">Looking for reliable PAT testing in {nm}? Ocean City PAT Testing provides City &amp; Guilds qualified portable appliance testing across {nm} and {county}, covering {districts}. {hook} Whether you're a landlord, a holiday-let owner, a business or a community group, you'll get a thorough test of every appliance and a same-day certificate.</p>
      {area_fig}
      <h2>Local PAT testing you can count on in {nm}</h2>
      <p>Because we're a Plymouth-based service covering the whole region, {nm} is well within our standard area — and travel is included, so testing here costs no more than it does in the city. We arrive when we say we will, test efficiently around your tenants, guests or staff, and leave you with paperwork that satisfies your insurer, letting agent or an inspector. Every item gets a full visual inspection and electrical test, a clear pass or fail label, and a place on your digital certificate.</p>
      <h2>Who we test for in {nm}</h2>
      <p>Our {nm} customers are a real cross-section of the community. We test for <strong>landlords</strong> keeping rental properties compliant, <strong>holiday-let and Airbnb owners</strong> protecting their guests and their reviews, <strong>businesses</strong> from shops and cafés to offices and workshops, and <strong>charities and community groups</strong> on our discounted 90p-per-item rate. Whatever the setting, the standard is the same: a proper test by a qualified engineer, honest advice on anything that fails, and minor repairs sorted on the spot where we can.</p>
      <h2>Certificates and compliance sorted in {nm}</h2>
      <p>Once the testing in {nm} is done, you won't be left chasing paperwork. Your digital certificate lists every appliance we checked, its pass-or-fail result and the date it's next due, and it lands in your inbox the same day we visit — ready to forward straight to a letting agent, an insurer or an environmental health officer. For {nm} landlords and holiday-let owners that's one less worry at inspection time; for businesses across {county} it's clean, dated evidence that your electrical safety is genuinely under control rather than something you're hoping nobody asks about.</p>
      <h2>Book your {nm} PAT testing</h2>
      <p>Getting booked in is simple. Call or message {PH} with a rough idea of the property and how many appliances are involved, and we'll give you a fixed price the same day. Most {nm} appointments are offered within a day or two, and your certificate lands in your inbox the same day we test. If you have several properties in and around {nm}, we'll plan an efficient round and keep your renewal dates on file so you never fall out of date.</p>
    </div>
    <aside class="side">
      <div class="side-card">
        <h3>PAT testing in {nm}</h3>
        <p>Fixed prices from £{PRICE_FROM}. Same-day certificate. Fully qualified and insured.</p>
        <a class="btn btn-primary btn-block" href="/contact">Get a free quote</a>
        <a class="btn btn-outline btn-block" href="tel:{TEL}" style="margin-top:.5rem">{ICONS['phone']}Call {PH}</a>
        <ul class="side-list">
          <li>{ICONS['check']}Covers {nm} &amp; {county}</li>
          <li>{ICONS['check']}Travel included in the price</li>
          <li>{ICONS['check']}Landlord, holiday let &amp; business</li>
          <li>{ICONS['check']}Same-day PDF certificate</li>
        </ul>
      </div>
      <div class="side-card side-areas">
        <h3>Our services</h3>
        <p>{''.join(f'<a href="/services/{s[0]}">{s[1]}</a><br>' for s in SERVICES)}</p>
      </div>
    </aside>
  </div>
  <div class="prose" style="margin-top:1.4rem">
    {trust_block('PAT testing', f'PAT testing {nm}')}
  </div>
  {author()}
</div></section>
<section class="section-cream"><div class="wrap">
  <div class="section-head center"><span class="eyebrow">Nearby</span><h2>PAT testing near {nm}</h2>
  <p>We also cover {', '.join(x[1] for x in AREAS if x[0] != slug)} as part of our {county} and Devon round.</p></div>
  <div class="area-links" style="margin-top:1rem">{''.join(f'<a href="/areas-covered/{x[0]}">{ICONS["pin"]}{x[1]}</a>' for x in AREAS if x[0] != slug)}</div>
</div></section>
"""
        pages.append({
            "url": f"/areas-covered/{slug}", "active": "areas", "priority": 0.7,
            "title": mk_title(f"PAT Testing {nm}"),
            "desc": f"PAT testing in {nm}, {county} by a City & Guilds engineer — landlord, holiday let & business testing with a same-day certificate from £{PRICE_FROM}.",
            "breadcrumbs": [("Home", "/"), ("Areas Covered", "/areas-covered"), (nm_plain, f'/areas-covered/{slug}')],
            "body": body,
            "faqs": [
                (f"How much is PAT testing in {nm}?", f"Landlords start at £{PRICE_FROM} per property, holiday lets from £65, businesses from £80 and charities 90p per item. Travel to {nm} is included, so you pay the same as customers in Plymouth."),
                (f"Do you really cover {nm}?", f"Yes — {nm} in {county} is part of our standard coverage area from our Plymouth base. Call {PH} to book."),
                ("How soon can you come out?", f"Most {nm} appointments are offered within a day or two, and your certificate is emailed the same day we test."),
                ("Can you test several properties here?", f"Yes. If you have multiple properties in or around {nm} we'll plan an efficient testing round and keep your renewal dates on file."),
            ],
        })

    # ===================================================================
    # ABOUT
    # ===================================================================
    about_body = f"""
{page_banner('About Ocean City PAT Testing', 'Guiding you safely — a qualified, local electrical safety service you can trust in your home or business.')}
{crumbs([('Home', '/'), ('About', '/about')])}
<section><div class="wrap prose">
  <p class="lead-p">Ocean City PAT Testing is a Plymouth-based electrical safety service built on one simple idea: testing should be done properly, explained honestly and priced fairly. Our name nods to Plymouth — the Ocean City — and our lighthouse logo reflects what we're here to do: guide you safely through the business of keeping electrical equipment safe, so you can get on with everything else.</p>
  <h2>Qualified, experienced and local</h2>
  <p>Our testing is carried out by a City &amp; Guilds qualified engineer with over {YRS} years of hands-on electrical experience. That background matters: it means we don't just run a tester over an appliance and print a label — we understand what we're looking at, spot the faults that a quick glance would miss, and can often put minor problems right on the spot. We're approved by Devon Trading Standards too, which means we've been vetted as a trader you can welcome into your home or business with confidence.</p>
  <h2>What we believe in</h2>
  <p>We've all heard the horror stories — the "PAT tester" who tested forty appliances in twenty minutes, or the certificate that turned out to be worthless when it mattered. We started Ocean City PAT Testing to be the opposite of that. Every item gets a genuine visual inspection and a full electrical test. Every customer gets the truth about what we find, whether that's good news or a heater that needs to go in the bin. And every job ends with a clear, same-day certificate that will stand up to scrutiny from an insurer or a Health &amp; Safety inspector. No shortcuts, no scare tactics, no hidden costs.</p>
  <h2>Who we work with</h2>
  <p>We test for landlords and letting agents keeping rental properties compliant, holiday-let and Airbnb owners protecting their guests, businesses of every kind from cafés to workshops, and charities and community groups on our discounted rate. From a single rental flat in Plymouth to a portfolio spread across Devon and Cornwall, the service is the same — reliable, thorough and refreshingly straightforward. A lot of our work comes from referrals and repeat customers, which is exactly how we like it.</p>
  <h2>The standards and qualifications we hold</h2>
  <p>Credentials matter when someone is judging whether your electrical equipment is safe, so it's worth being clear about ours. Our testing is carried out by a City &amp; Guilds qualified engineer and follows the IET Code of Practice for In-service Inspection and Testing of Electrical Equipment — the document the whole industry works to. We're approved by Devon Trading Standards, which means we've been independently vetted as a trustworthy local trader, and we carry full public liability insurance for every job. Our test equipment is calibrated, so the readings on your certificate are accurate and defensible. Put together, that's the difference between a certificate that genuinely protects you and a sticker that simply looks the part — and it's why letting agents, insurers and inspectors across the South West are happy to accept our paperwork.</p>
  <div class="cred-figs">
    <figure><img src="/images/pat-qualification-certificate.webp" alt="City &amp; Guilds PAT testing qualification certificate held by Ocean City PAT Testing" loading="lazy" decoding="async"><figcaption>City &amp; Guilds PAT testing qualification.</figcaption></figure>
    <figure><img src="/images/devon-trading-standards-approved.webp" alt="Devon Trading Standards approved trader badge for Ocean City PAT Testing" loading="lazy" decoding="async"><figcaption>Devon Trading Standards approved trader.</figcaption></figure>
  </div>
  <h2>Our testing process, step by step</h2>
  <p>People are sometimes surprised by how methodical a proper test is. We start by agreeing access and a time that suits your tenants, guests or staff. On site, we work room by room so nothing gets missed, unplugging each appliance, inspecting the plug, fuse, lead and casing, and then running the electrical tests with calibrated equipment. Every item that passes is labelled there and then, and anything that fails is set aside with a clear explanation of why. Before we leave, we re-plug everything exactly as we found it, run through our findings with you and confirm when your certificate will arrive — usually within hours. It's careful, unhurried work, because that's the only way to do it properly.</p>
  <h2>Why using a local tester matters</h2>
  <p>You could call a national chain and have a stranger sent from goodness-knows-where. We think there's real value in using someone local. We know Plymouth, the South Hams and South East Cornwall — the back lanes of the Rame Peninsula, the parking realities of the Barbican, the holiday-let hotspots along the estuaries — so we turn up prepared and on time. Being local also means we're accountable: our reputation here is everything, and you can always get hold of us afterwards if you have a question about your certificate or need something retested. When you book Ocean City PAT Testing, you're dealing with the person who actually does the work, start to finish.</p>
  <h2>Guiding you safely</h2>
  <p>Electrical safety law can feel daunting, full of regulations, codes of practice and acronyms. Our job is to take that worry off your hands. We'll tell you what you need, when you need it, and what it will cost — and we'll never sell you a test you don't require. Whether you're a first-time landlord trying to do the right thing or a business owner with a long compliance checklist, think of us as the local experts in your corner. That's what "guiding you safely" means to us.</p>
  {author()}
</div></section>
{reviews_grid()}
"""
    pages.append({
        "url": "/about", "active": "about", "priority": 0.7,
        "title": "About Us | Ocean City PAT Testing Plymouth",
        "desc": "City & Guilds qualified, Devon Trading Standards approved PAT testing in Plymouth — 20+ years' electrical experience, guiding you safely.",
        "breadcrumbs": [("Home", "/"), ("About", "/about")],
        "body": about_body,
        "faqs": [
            ("Are you qualified to carry out PAT testing?", "Yes — our testing is done by a City & Guilds qualified engineer with over 20 years' electrical experience, and we're approved by Devon Trading Standards."),
            ("Are you insured?", "Yes, we carry full public liability insurance, and every job is carried out to the IET Code of Practice."),
            ("What areas do you cover?", f"Plymouth, the South Hams and South East Cornwall, including {', '.join(a[1] for a in AREAS[:6])} and more."),
            ("Do I deal with the same person throughout?", "You do. When you book Ocean City PAT Testing you deal directly with the engineer who carries out the work from start to finish — no call centres, no subcontractors, and someone you can always get hold of afterwards if you have a question about your certificate."),
        ],
    })

    # ===================================================================
    # SERVICE INFORMATION / PAT GUIDE
    # ===================================================================
    guide_body = f"""
{page_banner('PAT Testing Guide &amp; Service Information', 'Plain-English answers to the questions we get asked most — what PAT testing is, why it matters, how often you need it and what the stickers mean.')}
{crumbs([('Home', '/'), ('PAT Guide', '/service-information')])}
<section><div class="wrap prose narrow">
  <p class="lead-p">PAT testing comes wrapped in a lot of jargon, regulations and half-remembered rules. This guide cuts through it. If you're a landlord, business owner or community group trying to work out what you actually need, here's everything explained simply — and if anything's still unclear, just call {PH}.</p>
  <h2>What is PAT testing?</h2>
  <p>PAT testing — portable appliance testing — is the examination of electrical appliances and equipment to make sure they're safe to use. It has two parts: a visual inspection of the plug, cable, fuse and casing, and an electrical test using calibrated equipment to check earth continuity, insulation resistance and polarity. A 'portable appliance' is really anything that connects to the mains by a plug and lead — from a kettle or computer to a large floor-standing machine in a workshop. The visual inspection is a vital part of the process; a great many faults are caught just by looking carefully, which is why we never skip it.</p>
  {mf("uk-plug-wiring-fuse.webp", "UK 13A plug wiring and 13A fuse, checked during a PAT testing visual inspection", "Inside a UK 13A plug: correct wiring and the right fuse are exactly what a PAT test's visual inspection checks for.")}
  <h2>Who needs to carry out testing?</h2>
  <p>Inspection and testing should be carried out by a competent person — someone with the knowledge, experience and proper equipment to do it safely and interpret the results. For low-risk environments that can sometimes be a trained member of staff, but for a certificate that genuinely protects you, it's worth using a qualified, experienced engineer. That's what you get with Ocean City PAT Testing: a City &amp; Guilds qualified tester who tests to the IET Code of Practice and gives you paperwork that stands up.</p>
  <h2>Why is PAT testing needed?</h2>
  <p>The headline reason is safety — faulty electrical equipment causes fires, shocks and injuries every year, and most of it is preventable. The legal reason is duty of care: the Electricity at Work Regulations 1989 require electrical equipment to be maintained to prevent danger, and the Health and Safety at Work Act places broad duties on employers and those in control of premises. The practical reason is insurance: if an appliance causes damage or injury, your insurer will want evidence the equipment was maintained, and a current PAT certificate provides it. Without that proof, a claim can be challenged or refused — and you could be held liable.</p>
  <h2>How often do appliances need testing?</h2>
  <p>There's no single legal interval. Instead, the recommended approach is to base testing frequency on a risk assessment that considers the type of equipment and the environment it's used in. Equipment in tough environments — building sites, commercial kitchens, workshops — needs testing more often than, say, a desktop computer in a quiet office. As a general guide, many landlords and offices test every one to two years, while higher-risk settings test more frequently. We're always happy to recommend a sensible schedule for your situation.</p>
  <h2>What do the PAT testing stickers mean?</h2>
  <p>After testing, each item is labelled so its status is obvious at a glance — a simple traffic-light system:</p>
  <ul class="pat-key">
    <li><span class="dot dot-green"></span><strong>Green</strong> — the item passed both the visual inspection and the electrical test, and is safe to use.</li>
    <li><span class="dot dot-blue"></span><strong>Blue</strong> — the item passed a visual inspection only, used where a full electrical test isn't appropriate.</li>
    <li><span class="dot dot-red"></span><strong>Red</strong> — the item failed inspection or testing and must be taken out of use immediately.</li>
  </ul>
  {mf("pat-pass-fail-labels.webp", "Green PASSED and red FAILED electrical safety test labels used in PAT testing", "The green PASSED and red FAILED labels we apply so an appliance's status is obvious at a glance.")}
  <h2>What happens if something fails?</h2>
  <p>A fail isn't the end of the world. We label the item red so nobody uses it, explain clearly what's wrong, and tell you what it would take to fix. A surprising number of fails are simple things — a wrong or blown fuse, a damaged plug, a frayed lead end — which we can often repair on the spot so the item passes. Where an item is genuinely beyond economical repair, we'll say so plainly so you can replace it. Either way, only items that are actually safe end up with a green label on your certificate.</p>
  <h2>Still have a question?</h2>
  <p>This guide covers the essentials, but every property is different. If you're not sure what you need — or you just want a straight answer without any sales pressure — call or message us on <a href="tel:{TEL}">{PH}</a>. Advice is always free, whether or not you book.</p>
</div></section>
"""
    pages.append({
        "url": "/service-information", "active": "guide", "priority": 0.75,
        "title": "PAT Testing Guide: What It Is & Why You Need It",
        "desc": "A plain-English PAT testing guide: what it is, why it's needed, how often, and what the green, blue and red stickers mean. Plymouth & the South West.",
        "breadcrumbs": [("Home", "/"), ("PAT Guide", "/service-information")],
        "body": guide_body,
        "faqs": [
            ("Is PAT testing a legal requirement?", "There's no law that names PAT testing directly, but the Electricity at Work Regulations 1989 require electrical equipment to be kept safe. PAT testing is the recognised way to prove you've met that duty, and insurers and letting agents generally expect a current certificate."),
            ("How long does a PAT certificate last?", "A certificate reflects the date of testing; how long until the next test depends on a risk assessment of your equipment and environment — commonly one to two years for offices and rentals, more often for higher-risk settings."),
            ("Can I do my own PAT testing?", "Testing must be done by a competent person with the right equipment and knowledge. For a certificate that genuinely protects you with insurers and inspectors, most people use a qualified engineer."),
            ("What's the difference between PAT testing and an EICR?", "PAT testing checks appliances that plug in; an EICR checks the fixed wiring of the building. Most landlords and businesses need both — we can arrange them together."),
        ],
    })

    # ===================================================================
    # NEWS & ASSOCIATES
    # ===================================================================
    news_body = f"""
{page_banner('News &amp; Associates', 'A note on who we work with, the standards we test to, and the local businesses and organisations that trust Ocean City PAT Testing.')}
{crumbs([('Home', '/'), ('News &amp; Associates', '/news-and-associates')])}
<section><div class="wrap prose">
  <p class="lead-p">We're proud of the company we keep. Over the years Ocean City PAT Testing has become a trusted name for electrical safety across Plymouth, Devon and South East Cornwall, working with letting agents, holiday-let owners, hospitality businesses, marine firms, dental and veterinary practices, care providers and community organisations throughout the region.</p>
  <h2>The standards we test to</h2>
  <p>All of our testing follows the IET Code of Practice for In-service Inspection and Testing of Electrical Equipment — the recognised industry standard. We're City &amp; Guilds qualified and approved by Devon Trading Standards, and we carry full public liability insurance. Our equipment is calibrated so that every reading we record is accurate and defensible. When you hand our certificate to an insurer, a letting agent or a Health &amp; Safety inspector, it carries the weight of being done properly.</p>
  <h2>Who we work with</h2>
  <p>We're trusted by a broad mix of organisations across the South West — including local letting and property management agents, holiday-let and serviced-accommodation owners, hospitality venues, marine and superyacht businesses around the Plymouth waterfront, dental and veterinary practices, care and support providers, and a number of charities and community groups. Many came to us through word of mouth, and many have stayed with us for years. We're always glad to be a reliable fixture in the local business community.</p>
  <h2>Working together</h2>
  <p>If you're a letting agent, property manager or facilities company looking for a dependable PAT testing partner for your portfolio or your clients, we'd love to hear from you. We can plan testing rounds, keep renewal dates on file and turn certificates around the same day, taking electrical safety off your to-do list entirely. Get in touch on <a href="tel:{TEL}">{PH}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a> to talk it through.</p>
</div></section>
{logo_strip('Our associates &amp; clients', 'Some of the organisations we keep safe', 'A selection of the businesses, practices and community organisations across Plymouth, Devon and South East Cornwall that trust Ocean City PAT Testing with their electrical safety.')}
"""
    pages.append({
        "url": "/news-and-associates", "active": "", "priority": 0.5,
        "title": "News & Associates | Ocean City PAT Testing Plymouth",
        "desc": "Who we work with and the standards we test to — City & Guilds qualified, Devon Trading Standards approved and trusted across the South West.",
        "breadcrumbs": [("Home", "/"), ("News & Associates", "/news-and-associates")],
        "body": news_body,
    })

    # ===================================================================
    # CONTACT
    # ===================================================================
    contact_body = f"""
{page_banner('Get a Free PAT Testing Quote', 'Tell us about your property or premises and we&rsquo;ll come back with a fixed price the same day. No obligation, no hard sell.')}
{crumbs([('Home', '/'), ('Contact', '/contact')])}
<section><div class="wrap">
  <div class="split">
    <div class="prose">
      <p class="lead-p">The quickest way to get a price is to call or message us on <a href="tel:{TEL}">{PH}</a> with a rough idea of your property and how many appliances are involved. Prefer to write it down? Fill in the form and we'll get straight back to you, usually the same day.</p>
      <h2>How to reach us</h2>
      <p><strong>Phone:</strong> <a href="tel:{TEL}">{PH}</a><br>
      <strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a><br>
      <strong>Area covered:</strong> {AREA}<br>
      <strong>Hours:</strong> {SITE['hours_human']}</p>
      <h2>What to tell us</h2>
      <p>To give you an accurate fixed price first time, it helps to know: the type of property or premises (rental, holiday let, shop, office, hall and so on), roughly how many electrical appliances there are, where it is, and whether you also need an EICR or fire safety check. Don't worry if you're not sure of the appliance count — a rough idea is plenty, and we'll never charge more than the price we quote you.</p>
      <p>We aim to reply to every enquiry the same day. For anything urgent, calling is always fastest.</p>
    </div>
    <aside class="side">
      <div class="side-card">
        <h3>Request a quote</h3>
        <form class="quote-form" action="https://formspree.io/f/your-form-id" method="POST">
          <label>Your name<input type="text" name="name" required autocomplete="name"></label>
          <label>Phone<input type="tel" name="phone" required autocomplete="tel"></label>
          <label>Email<input type="email" name="email" required autocomplete="email"></label>
          <label>Property type
            <select name="property_type">
              <option>Rental property</option>
              <option>Holiday let / Airbnb</option>
              <option>Business / commercial</option>
              <option>Charity / community group</option>
              <option>Home</option>
              <option>Other</option>
            </select>
          </label>
          <label>Area / town<input type="text" name="area" placeholder="e.g. Plymouth, Saltash, Salcombe"></label>
          <label>How can we help?<textarea name="message" rows="4" placeholder="Roughly how many appliances? Do you also need an EICR or fire safety check?"></textarea></label>
          <button class="btn btn-primary btn-block" type="submit">Send my enquiry</button>
          <p class="form-note">By sending this you agree we can contact you about your enquiry. We never share your details. See our <a href="/privacy-policy">privacy policy</a>.</p>
        </form>
      </div>
    </aside>
  </div>
</div></section>
<section class="section-cream"><div class="wrap prose">
  <h2>What happens after you get in touch</h2>
  <p>Getting booked in with Ocean City PAT Testing is refreshingly simple. As soon as we hear from you we'll confirm a fixed price based on the details you've given — there's no waiting days for a written estimate. Once you're happy, we agree a date and a time that works around your tenants, guests or staff, and we'll text you a reminder beforehand. On the day we arrive when we say we will, test everything thoroughly, talk you through anything that needs attention, and email your certificate the same day. From first message to certificate in your inbox, most jobs are wrapped up within a few days.</p>
  <h2>Where we cover</h2>
  <p>We're based in Plymouth and cover the whole surrounding region as standard — the entire city, out across the South Hams to {', '.join(a[1] for a in AREAS if a[0] in ('kingsbridge','salcombe','totnes','dartmouth'))}, and over the Tamar into South East Cornwall including {', '.join(a[1] for a in AREAS if a[0] in ('saltash','torpoint','callington','liskeard','looe'))}. Travel within the area is included in our pricing, so wherever you are in {AREA}, you'll pay the same fair price. If you're just outside and not sure whether we reach you, ask anyway — we often do, and we're always happy to help.</p>
  <h2>Prefer to talk it through?</h2>
  <p>Some jobs are easier to explain in a quick conversation, and that's absolutely fine. If your property is unusual, you're juggling several at once, or you simply want a straight answer without filling in a form, just call or message <a href="tel:{TEL}">{PH}</a>. You'll get through to the person who actually does the testing, not a call centre, and there's never any pressure or hard sell. We'll happily talk you through what you need, what it costs and when we can fit you in — and if it turns out you don't need a test yet, we'll tell you that too.</p>
</div></section>
"""
    pages.append({
        "url": "/contact", "active": "contact", "priority": 0.85, "no_cta": True,
        "title": "Contact & Free Quote | Ocean City PAT Testing Plymouth",
        "desc": f"Get a free, fixed-price PAT testing quote the same day. Call {PH} or message Ocean City PAT Testing — covering Plymouth, Devon and South East Cornwall.",
        "breadcrumbs": [("Home", "/"), ("Contact", "/contact")],
        "body": contact_body,
        "faqs": [
            ("How do I get a quote?", f"Call or text {PH}, email {EMAIL}, or fill in the form on this page with a few details about your property. We reply the same day with a fixed price."),
            ("How quickly will you reply?", "We aim to respond to every enquiry the same day. For anything urgent, calling is always the fastest way to reach us."),
            ("Is the quote free and without obligation?", "Completely. We'll give you a fixed price with no obligation and no hard sell — advice is always free whether or not you book."),
        ],
    })

    # ===================================================================
    # PRIVACY POLICY
    # ===================================================================
    privacy_body = f"""
{page_banner('Privacy Policy', 'How Ocean City PAT Testing collects, uses and protects your personal information.')}
{crumbs([('Home', '/'), ('Privacy Policy', '/privacy-policy')])}
<section><div class="wrap prose narrow">
  <p>This privacy policy explains how Ocean City PAT Testing ("we", "us") handles the personal information you give us. We are the data controller for that information and we comply with the UK GDPR and the Data Protection Act 2018. Last updated {SITE['year']}.</p>
  <h2>What we collect</h2>
  <p>When you contact us for a quote or book testing, we collect the details you provide — typically your name, phone number, email address, the address of the property to be tested and any information you include in your message. We do not collect special category data, and we do not knowingly collect information from children.</p>
  <h2>How we use it</h2>
  <p>We use your information only to respond to your enquiry, provide a quote, arrange and carry out testing, issue your certificate, take payment and keep the records we're required to keep. We may use your contact details to remind you when testing is due again. Our lawful bases are your consent (when you enquire), the performance of a contract (when you book), and our legitimate interest in running and improving our business.</p>
  <h2>Who we share it with</h2>
  <p>We do not sell your data and we do not share it for marketing. We only share information where necessary to deliver our service — for example with a payment provider, or with our email/form provider to receive your enquiry — and where the law requires it. Your testing certificate is provided to you; if you ask us to send it to your letting agent or insurer, we'll do so on your instruction.</p>
  <h2>How long we keep it</h2>
  <p>We keep enquiry and customer records only for as long as necessary — to provide the service, to meet our legal and insurance obligations, and to remind you of future testing. When information is no longer needed, we delete or securely destroy it.</p>
  <h2>Your rights</h2>
  <p>You have the right to access the personal data we hold about you, to ask us to correct or delete it, to object to or restrict its processing, and to withdraw consent at any time. To exercise any of these rights, contact us on <a href="tel:{TEL}">{PH}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a>. You also have the right to complain to the Information Commissioner's Office (ico.org.uk) if you're unhappy with how we've handled your data.</p>
  <h2>Cookies</h2>
  <p>This website is a simple static site and does not set tracking or advertising cookies. Embedded content such as a map may set its own cookies; you can control these through your browser settings.</p>
  <h2>Contact</h2>
  <p>Any questions about this policy or your data? Get in touch on <a href="mailto:{EMAIL}">{EMAIL}</a> and we'll be glad to help.</p>
</div></section>
"""
    pages.append({
        "url": "/privacy-policy", "active": "", "priority": 0.3, "no_cta": True,
        "title": "Privacy Policy | Ocean City PAT Testing",
        "desc": "How Ocean City PAT Testing collects, uses and protects your personal data in line with UK GDPR and the Data Protection Act 2018.",
        "breadcrumbs": [("Home", "/"), ("Privacy Policy", "/privacy-policy")],
        "body": privacy_body,
    })

    # ===================================================================
    # TERMS
    # ===================================================================
    terms_body = f"""
{page_banner('Terms &amp; Conditions', 'The terms on which Ocean City PAT Testing provides its services.')}
{crumbs([('Home', '/'), ('Terms', '/terms')])}
<section><div class="wrap prose narrow">
  <p>These terms apply to PAT testing, EICR, fire safety and related services provided by Ocean City PAT Testing. By booking our services you agree to them. Last updated {SITE['year']}.</p>
  <h2>Our service</h2>
  <p>We carry out inspection and testing of electrical equipment to the IET Code of Practice, using calibrated equipment and a qualified engineer. Testing establishes whether equipment is safe to use at the time of testing; it cannot guarantee that equipment will not develop a fault afterwards. You remain responsible for using equipment correctly and reporting any subsequent damage or fault.</p>
  <h2>Quotes and prices</h2>
  <p>Quotes are based on the information you provide about the property and the number of appliances. If the actual scope differs significantly — for example far more appliances than described — we'll agree any change with you before proceeding. A minimum call-out charge of £{MIN_CALLOUT} applies. Prices exclude VAT where applicable.</p>
  <h2>Access and your responsibilities</h2>
  <p>You agree to provide safe access to the property and to the equipment to be tested at the agreed time. Items must be accessible and able to be unplugged for testing. We're not responsible for items we're unable to access or test on the day; these can be tested on a return visit, which may incur a further call-out.</p>
  <h2>Results and failed items</h2>
  <p>Items that fail are labelled and must be taken out of use. Where we identify a minor fault that can be safely repaired on site, we may do so as part of the service. We are not liable for the cost of replacing equipment that fails, nor for any loss arising from equipment we have advised should be removed from use but which continues to be used.</p>
  <h2>Payment</h2>
  <p>Payment is due on completion unless otherwise agreed, by cash, card or bank transfer. Certificates are issued once testing is complete.</p>
  <h2>Liability</h2>
  <p>We carry public liability insurance and will perform our services with reasonable skill and care. Nothing in these terms excludes liability that cannot lawfully be excluded. Otherwise, our liability is limited to the value of the services provided.</p>
  <h2>Contact</h2>
  <p>Questions about these terms? Contact us on <a href="tel:{TEL}">{PH}</a> or <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
"""
    pages.append({
        "url": "/terms", "active": "", "priority": 0.3, "no_cta": True,
        "title": "Terms & Conditions | Ocean City PAT Testing",
        "desc": "The terms and conditions on which Ocean City PAT Testing provides PAT testing, EICR and fire safety services across Plymouth, Devon and South East Cornwall.",
        "breadcrumbs": [("Home", "/"), ("Terms", "/terms")],
        "body": terms_body,
    })

    # ===================================================================
    # SITEMAP (HTML)
    # ===================================================================
    sm_services = ''.join(f'<li><a href="/services/{s[0]}">{s[1]}</a></li>' for s in SERVICES)
    sm_areas = ''.join(f'<li><a href="/areas-covered/{a[0]}">PAT testing {a[1]}</a></li>' for a in AREAS)
    sitemap_body = f"""
{page_banner('Sitemap', 'Every page on the Ocean City PAT Testing website, in one place.')}
{crumbs([('Home', '/'), ('Sitemap', '/sitemap')])}
<section><div class="wrap prose">
  <h2>Main pages</h2>
  <ul>
    <li><a href="/">Home</a></li>
    <li><a href="/services">Services</a></li>
    <li><a href="/pricing">Pricing</a></li>
    <li><a href="/areas-covered">Areas covered</a></li>
    <li><a href="/about">About us</a></li>
    <li><a href="/service-information">PAT testing guide</a></li>
    <li><a href="/news-and-associates">News &amp; associates</a></li>
    <li><a href="/contact">Contact &amp; quote</a></li>
  </ul>
  <h2>Services</h2>
  <ul>{sm_services}</ul>
  <h2>Areas covered</h2>
  <ul>{sm_areas}</ul>
  <h2>Legal</h2>
  <ul>
    <li><a href="/privacy-policy">Privacy policy</a></li>
    <li><a href="/terms">Terms &amp; conditions</a></li>
  </ul>
</div></section>
"""
    pages.append({
        "url": "/sitemap", "active": "", "priority": 0.3, "no_cta": True,
        "title": "Sitemap | Ocean City PAT Testing",
        "desc": "Browse every page on the Ocean City PAT Testing website — services, areas covered, pricing, guides and more.",
        "breadcrumbs": [("Home", "/"), ("Sitemap", "/sitemap")],
        "body": sitemap_body,
    })

    # ===================================================================
    # 404
    # ===================================================================
    notfound_body = f"""
<section class="page-banner"><div class="wrap" style="text-align:center">
  <img src="/images/logo.png" width="120" height="120" alt="Ocean City PAT Testing lighthouse logo" style="margin:0 auto 1rem">
  <h1>Page not found</h1>
  <p style="margin:0 auto">Even a lighthouse can't light every path. The page you're after has moved or never existed.</p>
</div></section>
<section><div class="wrap prose center">
  <p>Try one of these instead:</p>
  <p>
    <a class="btn btn-primary" href="/">Back to home</a>
    <a class="btn btn-outline" href="/services">Our services</a>
    <a class="btn btn-outline" href="/contact">Get a quote</a>
  </p>
  <p style="margin-top:1.4rem">Or call us on <a href="tel:{TEL}">{PH}</a> — we're happy to help.</p>
</div></section>
"""
    pages.append({
        "url": "/404", "active": "", "noindex": True, "no_cta": True,
        "title": "Page Not Found | Ocean City PAT Testing",
        "desc": "The page you were looking for could not be found.",
        "breadcrumbs": [("Home", "/")],
        "body": notfound_body,
    })

    return pages
