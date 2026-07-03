/* =====================================================================
   No Time 2 Waste — online booking app
   Vanilla JS, no dependencies. Reads window.N2W_PRICES (js/prices.js).
   ===================================================================== */
(function () {
  "use strict";
  var DATA = window.N2W_PRICES;
  var ROOT = document.getElementById("booking-app");
  if (!DATA || !ROOT) { return; }

  var CATS = DATA.categories || [];
  var PHONE = DATA.phone, TEL = (DATA.tel || "").replace(/[^+\d]/g, ""), EMAIL = DATA.email;
  var FORMSPREE = (ROOT.getAttribute("data-formspree") || "").trim(); // set to "https://formspree.io/f/xxxx" to enable
  var DEPOSIT_PCT = DATA.depositPercent || 0;   // % of total taken as a deposit
  var BANK = DATA.bank || {};                   // {name, sort, account}
  var HOURS = DATA.hours || {};                 // {weekdayIndex: {open, close}}, Sun=0
  var WIN = DATA.bookingWindow || { open: "09:00", close: "15:00" }; // bookable slot window

  // ---- opening hours / working days ----
  function parseHM(s) { var p = String(s).split(":"); return parseInt(p[0], 10) * 60 + parseInt(p[1], 10); }
  function dayHours(iso) { if (!iso) return null; return HOURS[new Date(iso + "T12:00:00").getDay()] || null; }
  function dayName(iso) { return new Date(iso + "T12:00:00").toLocaleDateString("en-GB", { weekday: "long" }); }
  function isoOffset(days) { var d = new Date(Date.now() + days * 86400000); d.setMinutes(d.getMinutes() - d.getTimezoneOffset()); return d.toISOString().slice(0, 10); }
  function nextOpenISO() { for (var i = 0; i < 21; i++) { var iso = isoOffset(i); if (dayHours(iso)) return iso; } return isoOffset(0); }
  function maxISO() { return isoOffset(120); }
  function slotsFor(iso) {
    var h = dayHours(iso); if (!h) return [];
    // bookable range = opening hours clamped to the booking window (e.g. 9–3)
    var o = Math.max(parseHM(h.open), parseHM(WIN.open));
    var c = Math.min(parseHM(h.close), parseHM(WIN.close));
    if (o >= c) return [];
    var out = [];
    [["Morning (9am–12pm)", 9 * 60, 12 * 60], ["Afternoon (12pm–3pm)", 12 * 60, 15 * 60]]
      .forEach(function (w) { if (w[0] !== null && Math.max(w[1], o) < Math.min(w[2], c)) out.push(w[3] || w[0]); });
    out.push("Flexible (" + WIN.open + "–" + WIN.close + ")");
    return out;
  }
  function depositDue(total) { return Math.round(total * DEPOSIT_PCT / 100); }
  function balanceDue(total) { return total - depositDue(total); }

  // ---- state (basket persisted in localStorage) ----
  var STORE = "n2w_basket_v1";
  var basket = load();
  var activeCat = CATS.length ? CATS[0].id : null;
  var step = 1;
  var justAdded = null;   // key of the most recently added item (for the add animation)

  function load() {
    try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; }
  }
  function save() { try { localStorage.setItem(STORE, JSON.stringify(basket)); } catch (e) {} }

  // ---- helpers ----
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function money(n) { return "£" + n; }
  function mins(m) {
    var h = Math.floor(m / 60), mm = m % 60, p = [];
    if (h) p.push(h + " hr");
    if (mm) p.push(mm + " min");
    return p.join(" ") || "—";
  }
  function catById(id) { for (var i = 0; i < CATS.length; i++) { if (CATS[i].id === id) return CATS[i]; } return null; }
  function keyOf(catId, idx) { return catId + ":" + idx; }
  function lines() {
    var out = [];
    Object.keys(basket).forEach(function (k) {
      var b = basket[k];
      if (b && b.qty > 0) out.push(b);
    });
    return out;
  }
  function totalPrice() { return lines().reduce(function (s, b) { return s + b.price * b.qty; }, 0); }
  function totalMins() { return lines().reduce(function (s, b) { return s + b.mins * b.qty; }, 0); }
  function totalQty() { return lines().reduce(function (s, b) { return s + b.qty; }, 0); }

  function qtyOf(catId, idx) { var b = basket[keyOf(catId, idx)]; return b ? b.qty : 0; }
  function setQty(cat, idx, item, q) {
    var k = keyOf(cat.id, idx);
    var was = basket[k] ? basket[k].qty : 0;
    if (q <= 0) { delete basket[k]; }
    else { basket[k] = { cat: cat.id, catName: stripTags(cat.name), idx: idx, name: item.name, price: item.price, mins: item.mins, qty: q }; }
    if (was === 0 && q > 0) justAdded = k;
    save(); renderCart(); renderGrid(); renderTabs();
  }
  function stripTags(s) { return String(s).replace(/<[^>]+>/g, ""); }

  // ---- category icons ----
  function svg(p) { return '<svg viewBox="0 0 24 24" aria-hidden="true">' + p + "</svg>"; }
  var BKI = {
    "mixed-household": svg('<path d="M6 8h12l-1 12H7zM9 8V6a3 3 0 0 1 6 0v2h-2V6a1 1 0 0 0-2 0v2z"/>'),
    "small-items": svg('<path d="M5 9l7-3 7 3v6l-7 3-7-3zm7-1 4 1.7-4 1.7-4-1.7z"/>'),
    "medium-items": svg('<path d="M4 8l8-4 8 4v8l-8 4-8-4zm8-1.8L17 8l-5 2.2L7 8z"/>'),
    "large-items": svg('<path d="M3 11a2 2 0 0 1 2-2v-1a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v1a2 2 0 0 1 2 2v6h-2v-2H5v2H3zm4-3h10V8a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1z"/>'),
    "wood": svg('<path d="M3 5h18v4H3zm0 5h18v4H3zm0 5h18v4H3z"/>'),
    "shed-garage": svg('<path d="M12 3 2 11h3v9h6v-6h2v6h6v-9h3z"/>'),
    "soil-rubble": svg('<path d="M3 5h7v5H3zm8 0h10v5H11zM3 14h10v5H3zm11 0h7v5h-7z"/>'),
    "garden-waste": svg('<path d="M17 8C8 10 5.9 16.2 3.8 21.1l1.8.8.5-1.1C7 19 8.5 18 12 18c6 0 9-4 9-10 0-1-1-1-2-1-4 0-7 0-9.5 3C12 9 14 8.5 17 8z"/>')
  };
  function catIcon(id) { return BKI[id] || svg('<path d="M4 4h16v16H4z"/>'); }

  // ---- shell ----
  ROOT.innerHTML =
    '<div class="bk" data-cur="1">' +
      '<ol class="bk-steps" aria-hidden="true">' +
        '<li data-s="1"><span class="bk-stepnum">1</span><span class="bk-steplbl">Choose items</span></li>' +
        '<li data-s="2"><span class="bk-stepnum">2</span><span class="bk-steplbl">Date &amp; details</span></li>' +
        '<li data-s="3"><span class="bk-stepnum">3</span><span class="bk-steplbl">Confirm</span></li>' +
      '</ol>' +
      '<div class="bk-step" data-step="1">' +
        '<div class="bk-layout">' +
          '<div class="bk-tabs" id="bkTabs" role="tablist" aria-label="Waste categories"></div>' +
          '<div class="bk-main">' +
            '<p class="bk-cat-blurb" id="bkBlurb"></p>' +
            '<div class="bk-grid" id="bkGrid"></div>' +
          '</div>' +
          '<aside class="bk-cart" id="bkCart" aria-live="polite"></aside>' +
        '</div>' +
      '</div>' +
      '<div class="bk-step" data-step="2" hidden></div>' +
      '<div class="bk-step" data-step="3" hidden></div>' +
    '</div>' +
    '<div class="bk-mobilebar" id="bkMobileBar" hidden></div>';

  var elBk = ROOT.querySelector(".bk");
  var elTabs = ROOT.querySelector("#bkTabs");
  var elGrid = ROOT.querySelector("#bkGrid");
  var elBlurb = ROOT.querySelector("#bkBlurb");
  var elCart = ROOT.querySelector("#bkCart");
  var elMobileBar = ROOT.querySelector("#bkMobileBar");
  var steps = ROOT.querySelectorAll(".bk-step");
  var stepBar = ROOT.querySelectorAll(".bk-steps li");

  // deep-link ?category=
  var params = new URLSearchParams(location.search);
  var qc = params.get("category");
  if (qc && catById(qc)) activeCat = qc;

  // ---- render: tabs ----
  function renderTabs() {
    elTabs.innerHTML = CATS.map(function (c) {
      var active = c.id === activeCat ? " is-active" : "";
      var n = countInCat(c.id);
      var badge = n > 0 ? '<span class="bk-tab-badge">' + n + "</span>" : "";
      return '<button class="bk-tab' + active + '" role="tab" data-cat="' + c.id + '" aria-selected="' + (c.id === activeCat) + '">' +
        '<span class="bk-tab-ico">' + catIcon(c.id) + "</span>" + esc(stripTags(c.name)) + badge + "</button>";
    }).join("");
    var act = elTabs.querySelector(".is-active");
    if (act && act.scrollIntoView) act.scrollIntoView({ block: "nearest", inline: "center" });
  }
  function countInCat(id) { return lines().reduce(function (s, b) { return s + (b.cat === id ? b.qty : 0); }, 0); }

  // ---- render: grid ----
  function renderGrid() {
    var cat = catById(activeCat);
    if (!cat) { elGrid.innerHTML = ""; return; }
    elBlurb.textContent = stripTags(cat.blurb || "");
    if (!cat.items.length) {
      elGrid.innerHTML = '<div class="bk-empty">Prices for this category are on request. <a href="tel:' + TEL + '">Call ' + esc(PHONE) + "</a> or <a href=\"/contact\">send us the details</a> for a fast quote.</div>";
      return;
    }
    elGrid.innerHTML = cat.items.map(function (it, i) {
      var q = qtyOf(cat.id, i);
      var inCart = q > 0 ? " in-cart" : "";
      var added = keyOf(cat.id, i) === justAdded ? " just-added" : "";
      return '<div class="bk-card' + inCart + added + '" data-cat="' + cat.id + '">' +
        (q > 0 ? '<span class="bk-card-tick" aria-hidden="true">✓</span>' : "") +
        '<span class="bk-card-ico">' + catIcon(cat.id) + "</span>" +
        '<h3>' + esc(it.name) + "</h3>" +
        '<div class="bk-meta"><span class="bk-dur">' + mins(it.mins) + '</span><span class="bk-price">' + money(it.price) + "</span></div>" +
        (q > 0
          ? '<div class="bk-stepper" data-cat="' + cat.id + '" data-idx="' + i + '">' +
              '<button class="bk-dec" aria-label="Remove one">−</button>' +
              '<span class="bk-qty">' + q + "</span>" +
              '<button class="bk-inc" aria-label="Add one">+</button>' +
            "</div>"
          : '<button class="btn btn-primary bk-add" data-cat="' + cat.id + '" data-idx="' + i + '">Add</button>') +
        "</div>";
    }).join("");
    justAdded = null;   // one-shot: only animates the render right after adding
  }

  // ---- render: cart ----
  function renderCart() {
    var ls = lines(), n = totalQty(), t = totalPrice();
    var html = '<div class="bk-cart-head"><h3>Your booking</h3>' + (n ? '<span class="bk-cart-count">' + n + (n === 1 ? " item" : " items") + "</span>" : "") + "</div>";
    if (!ls.length) {
      html += '<div class="bk-cart-empty"><span class="bk-cart-empty-ico">' + catIcon("mixed-household") + "</span>No items yet — add what needs clearing and your price builds up here.</div>";
    } else {
      html += '<ul class="bk-cart-lines">' + ls.map(function (b) {
        return "<li><span class=\"bk-cl-name\">" + (b.qty > 1 ? b.qty + "× " : "") + esc(b.name) + '</span>' +
          '<span class="bk-cl-price">' + money(b.price * b.qty) + "</span>" +
          '<button class="bk-cl-rm" data-cat="' + b.cat + '" data-idx="' + b.idx + '" aria-label="Remove ' + esc(b.name) + '">×</button></li>';
      }).join("") + "</ul>";
      html += '<div class="bk-cart-tot"><span>Estimated time</span><span>' + mins(totalMins()) + "</span></div>";
      html += '<div class="bk-cart-tot bk-grand"><span>Total</span><span>' + money(t) + "</span></div>";
      html += '<div class="bk-cart-dep"><div><span>' + DEPOSIT_PCT + "% deposit to book</span><strong>" + money(depositDue(t)) + "</strong></div>" +
              '<div><span>Balance on completion</span><strong>' + money(balanceDue(t)) + "</strong></div></div>";
    }
    html += '<button class="btn btn-primary btn-block bk-continue"' + (ls.length ? "" : " disabled") + ">Continue to date &amp; details</button>";
    html += '<p class="bk-cart-help">' + shieldSvg() + " Fixed prices · all labour &amp; licensed disposal included · no payment taken online.</p>";
    elCart.innerHTML = html;
    renderMobileBar();
  }
  function shieldSvg() { return '<svg viewBox="0 0 24 24" class="bk-mini-ico" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.3 8 11 4.6-1.7 8-6 8-11V5zm-1.2 13L7 11.2 8.4 9.8l2.4 2.4 4.8-4.8L17 8.8z"/></svg>'; }

  // ---- mobile sticky checkout bar (step 1 only) ----
  function renderMobileBar() {
    var n = totalQty(), t = totalPrice();
    var onStep1 = step === 1, narrow = window.matchMedia("(max-width:900px)").matches;
    if (!n) { elMobileBar.hidden = true; elMobileBar.innerHTML = ""; document.body.style.paddingBottom = ""; return; }
    elMobileBar.hidden = false;
    elMobileBar.innerHTML =
      '<div class="bk-mb-info"><strong>' + n + (n === 1 ? " item" : " items") + "</strong><span>" + money(t) + "</span></div>" +
      '<button class="btn btn-primary bk-mb-continue">Review &amp; book</button>';
    // JS fallback for browsers without :has() — keep content clear of the fixed bar
    document.body.style.paddingBottom = (onStep1 && narrow) ? "76px" : "";
  }

  // ---- step navigation ----
  function goStep(n, skipScroll) {
    step = n;
    elBk.setAttribute("data-cur", n);
    for (var i = 0; i < steps.length; i++) {
      steps[i].hidden = (parseInt(steps[i].getAttribute("data-step"), 10) !== n);
    }
    for (var j = 0; j < stepBar.length; j++) {
      var sn = parseInt(stepBar[j].getAttribute("data-s"), 10);
      stepBar[j].className = sn === n ? "is-active" : (sn < n ? "is-done" : "");
    }
    if (n === 2) renderDetails();
    if (n === 3) renderConfirm();
    if (!skipScroll) {
      var top = ROOT.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: top, behavior: "smooth" });
    }
  }

  // ---- step 2: details ----
  function todayISO() {
    var d = new Date(); d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
    return d.toISOString().slice(0, 10);
  }
  var details = {};
  function renderDetails() {
    var el = steps[1];
    el.innerHTML =
      '<div class="bk-form-wrap"><div class="bk-form">' +
        '<button class="bk-back" type="button">&larr; Back to items</button>' +
        "<h2>When &amp; where?</h2>" +
        '<p class="bk-est">Estimated on-site time: <strong>' + mins(totalMins()) + "</strong> · Total <strong>" + money(totalPrice()) + "</strong></p>" +
        '<form id="bkForm" novalidate>' +
          '<div class="grid cols-2">' +
            '<div class="field"><label for="bkDate">Preferred date *</label><input type="date" id="bkDate" name="date" min="' + nextOpenISO() + '" max="' + maxISO() + '" required><span class="bk-err bk-date-err" id="bkDateErr" hidden></span></div>' +
            '<div class="field"><label for="bkSlot">Preferred time *</label><select id="bkSlot" name="slot" required><option value="">Choose a date first…</option></select></div>' +
            '<div class="field"><label for="bkName">Your name *</label><input type="text" id="bkName" name="name" required></div>' +
            '<div class="field"><label for="bkPhone">Phone *</label><input type="tel" id="bkPhone" name="phone" required></div>' +
            '<div class="field"><label for="bkEmail">Email</label><input type="email" id="bkEmail" name="email"></div>' +
            '<div class="field"><label for="bkPostcode">Postcode *</label><input type="text" id="bkPostcode" name="postcode" placeholder="e.g. PL9" required></div>' +
          "</div>" +
          '<div class="field"><label for="bkAddr">Collection address *</label><input type="text" id="bkAddr" name="address" required></div>' +
          '<div class="field"><label for="bkNotes">Access notes (stairs, parking, where the waste is)</label><textarea id="bkNotes" name="notes"></textarea></div>' +
          '<p class="bk-err" id="bkErr" hidden></p>' +
          '<button class="btn btn-primary btn-lg btn-block" type="submit">Review my booking</button>' +
          '<p class="form-note">By continuing you agree to us contacting you about this booking. See our <a href="/privacy-policy">privacy policy</a>.</p>' +
        "</form>" +
      "</div>" + cartMini() + "</div>";

    el.querySelector(".bk-back").addEventListener("click", function () { goStep(1); });
    // restore non-date/slot fields
    ["name", "phone", "email", "postcode", "address", "notes"].forEach(function (k) {
      var f = el.querySelector('[name="' + k + '"]'); if (f && details[k]) f.value = details[k];
    });

    var dateInput = el.querySelector("#bkDate"), slotSel = el.querySelector("#bkSlot"), dateErr = el.querySelector("#bkDateErr");
    function refreshSlots() {
      var v = dateInput.value;
      if (!v) { slotSel.innerHTML = '<option value="">Choose a date first…</option>'; return; }
      if (!dayHours(v)) {
        dateErr.hidden = false; dateErr.textContent = "Sorry, we don't collect on " + dayName(v) + "s. Please choose another day.";
        slotSel.innerHTML = '<option value="">—</option>'; return;
      }
      dateErr.hidden = true;
      var s = slotsFor(v);
      slotSel.innerHTML = '<option value="">Choose…</option>' + s.map(function (x) { return "<option>" + x + "</option>"; }).join("");
      if (details.slot && s.indexOf(details.slot) > -1) slotSel.value = details.slot;
    }
    dateInput.addEventListener("change", refreshSlots);
    dateInput.addEventListener("focus", function () {
      if (window.matchMedia("(max-width:900px)").matches) {
        setTimeout(function () { dateInput.scrollIntoView({ behavior: "smooth", block: "center" }); }, 50);
      }
    });
    dateInput.value = details.date || nextOpenISO();
    refreshSlots();

    el.querySelector("#bkForm").addEventListener("submit", function (e) {
      e.preventDefault();
      var f = e.target, req = ["date", "slot", "name", "phone", "postcode", "address"], miss = [];
      req.forEach(function (n) { if (!f[n].value.trim()) miss.push(n); });
      var err = el.querySelector("#bkErr");
      if (miss.length) { err.hidden = false; err.textContent = "Please fill in the required fields marked *."; f[miss[0]].focus(); return; }
      if (!dayHours(f.date.value)) { err.hidden = false; err.textContent = "We don't collect on " + dayName(f.date.value) + "s — please pick a working day."; f.date.focus(); return; }
      ["date", "slot", "name", "phone", "email", "postcode", "address", "notes"].forEach(function (n) { details[n] = f[n] ? f[n].value.trim() : ""; });
      goStep(3);
    });
  }

  function cartMini() {
    return '<aside class="bk-cart bk-cart-mini"><h3>Your booking</h3><ul class="bk-cart-lines">' +
      lines().map(function (b) { return "<li><span>" + (b.qty > 1 ? b.qty + "× " : "") + esc(b.name) + "</span><span>" + money(b.price * b.qty) + "</span></li>"; }).join("") +
      '</ul><div class="bk-cart-tot bk-grand"><span>Total</span><span>' + money(totalPrice()) + "</span></div></aside>";
  }

  // ---- step 3: confirm ----
  function reference() {
    var d = (details.date || todayISO()).replace(/-/g, "").slice(2);
    var r = "";
    for (var i = 0; i < 3; i++) r += "ABCDEFGHJKLMNPQRSTUVWXYZ23456789".charAt(Math.floor(Math.random() * 32));
    return "N2W-" + d + "-" + r;
  }
  var bookingRef = null;

  function depositPanelHtml() {
    var t = totalPrice(), dep = depositDue(t);
    return '<div class="bk-dep">' +
           '<div class="bk-dep-row"><span>' + DEPOSIT_PCT + "% deposit to secure your slot</span><strong>" + money(dep) + "</strong></div>" +
           '<div class="bk-dep-row"><span>Balance on completion (cash or bank transfer)</span><strong>' + money(t - dep) + "</strong></div></div>";
  }

  function summaryText(ref) {
    var t = "NEW BOOKING REQUEST — No Time 2 Waste\nRef: " + ref + "\n\n";
    lines().forEach(function (b) { t += "• " + (b.qty > 1 ? b.qty + "x " : "") + b.name + " (" + b.catName + ") — " + money(b.price * b.qty) + "\n"; });
    t += "\nTOTAL: " + money(totalPrice()) + " (est. " + mins(totalMins()) + " on site)\n";
    t += DEPOSIT_PCT + "% deposit to secure: " + money(depositDue(totalPrice())) +
         " · Balance on completion (cash/bank transfer): " + money(balanceDue(totalPrice())) + "\n\n";
    t += "Date: " + details.date + "  " + details.slot + "\n";
    t += "Name: " + details.name + "\nPhone: " + details.phone + "\nEmail: " + (details.email || "—") + "\n";
    t += "Address: " + details.address + ", " + details.postcode + "\n";
    if (details.notes) t += "Notes: " + details.notes + "\n";
    return t;
  }

  function renderConfirm() {
    var el = steps[2];
    bookingRef = bookingRef || reference();
    var rows = lines().map(function (b) {
      return "<tr><td>" + (b.qty > 1 ? b.qty + "× " : "") + esc(b.name) + "</td><td>" + money(b.price * b.qty) + "</td></tr>";
    }).join("");
    el.innerHTML =
      '<div class="bk-form-wrap"><div class="bk-form">' +
        '<button class="bk-back" type="button">&larr; Edit details</button>' +
        "<h2>Review &amp; confirm</h2>" +
        '<table class="bk-review"><tbody>' + rows +
          '<tr class="bk-review-tot"><td>Total</td><td>' + money(totalPrice()) + "</td></tr></tbody></table>" +
        '<div class="bk-review-when">' +
          "<p><strong>When:</strong> " + esc(details.date) + " · " + esc(details.slot) + "</p>" +
          "<p><strong>Where:</strong> " + esc(details.address) + ", " + esc(details.postcode) + "</p>" +
          "<p><strong>Contact:</strong> " + esc(details.name) + " · " + esc(details.phone) + (details.email ? " · " + esc(details.email) : "") + "</p>" +
          (details.notes ? "<p><strong>Notes:</strong> " + esc(details.notes) + "</p>" : "") +
        "</div>" +
        depositPanelHtml() +
        '<p class="bk-ref">Your reference: <strong>' + bookingRef + "</strong></p>" +
        '<button class="btn btn-primary btn-lg btn-block" id="bkSubmit">Confirm booking request</button>' +
        '<p class="form-note">No payment is taken online. We\'ll confirm your slot by text or call, usually within a couple of hours during opening times.</p>' +
        '<div id="bkResult" hidden></div>' +
      "</div>" + cartMini() + "</div>";
    el.querySelector(".bk-back").addEventListener("click", function () { goStep(2); });
    el.querySelector("#bkSubmit").addEventListener("click", submit);
  }

  function submit() {
    var btn = steps[2].querySelector("#bkSubmit");
    var result = steps[2].querySelector("#bkResult");
    btn.disabled = true; btn.textContent = "Sending…";
    var payload = {
      reference: bookingRef, total: money(totalPrice()), estimatedTime: mins(totalMins()),
      items: lines().map(function (b) { return (b.qty > 1 ? b.qty + "x " : "") + b.name + " — " + money(b.price * b.qty); }).join("; "),
      date: details.date, slot: details.slot, name: details.name, phone: details.phone,
      email: details.email, postcode: details.postcode, address: details.address, notes: details.notes,
      _subject: "Booking " + bookingRef + " — " + money(totalPrice())
    };
    function done() { showSuccess(result, btn); }
    if (FORMSPREE) {
      fetch(FORMSPREE, { method: "POST", headers: { "Content-Type": "application/json", "Accept": "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { done(); })
        .catch(function () { done(); });
    } else {
      // No backend configured: still capture the booking via WhatsApp / email.
      done();
    }
  }

  function showSuccess(result, btn) {
    var t = totalPrice(), dep = depositDue(t), bal = balanceDue(t);
    var txt = summaryText(bookingRef);
    var wa = "https://wa.me/" + TEL.replace(/^\+/, "") + "?text=" + encodeURIComponent(txt);
    var mail = "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Booking " + bookingRef) + "&body=" + encodeURIComponent(txt);
    var hasBank = BANK && BANK.sort && BANK.account;
    var bankLines = hasBank
      ? "<ul class=\"bk-bank\"><li><span>Account name</span><strong>" + esc(BANK.name || PHONE) + "</strong></li>" +
        "<li><span>Sort code</span><strong>" + esc(BANK.sort) + "</strong></li>" +
        "<li><span>Account no.</span><strong>" + esc(BANK.account) + "</strong></li>" +
        "<li><span>Reference</span><strong>" + bookingRef + "</strong></li></ul>"
      : "<p class=\"form-note\">We'll send you our bank details to pay the deposit when we confirm your slot.</p>";
    var depositBlock =
      '<div class="bk-dep-cta">' +
        "<p>To secure your booking, please pay your <strong>" + DEPOSIT_PCT + "% deposit (" + money(dep) +
        ")</strong> by bank transfer. The balance of <strong>" + money(bal) + "</strong> is payable on completion by cash or bank transfer.</p>" +
        bankLines +
      "</div>";
    var sent = !!FORMSPREE;
    var heading = sent ? "Thanks — your booking request is in!" : "One last step — send us your booking";
    var intro = sent
      ? "Reference <strong>" + bookingRef + "</strong>. We've got it and will confirm your slot shortly. You can also reach us here:"
      : "Reference <strong>" + bookingRef + "</strong>. Tap a button below to send it straight to us — that's what confirms your slot:";
    btn.hidden = true;
    result.hidden = false;
    result.innerHTML =
      '<div class="bk-success">' +
        '<div class="bk-tick">✓</div>' +
        "<h3>" + heading + "</h3>" +
        "<p>" + intro + "</p>" +
        '<div class="bk-success-cta">' +
          '<a class="btn btn-primary btn-lg" href="' + wa + '" target="_blank" rel="noopener">Send on WhatsApp</a>' +
          '<a class="btn btn-outline btn-lg" href="tel:' + TEL + '">Call ' + esc(PHONE) + "</a>" +
          '<a class="btn btn-outline btn-lg" href="' + mail + '">Email booking</a>' +
        "</div>" +
        depositBlock +
        "<p class=\"form-note\">We'll confirm your date and time directly. Keep your reference handy.</p>" +
      "</div>";
    // clear basket for a fresh next booking
    basket = {}; save();
    result.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  // ---- events (delegated) ----
  elTabs.addEventListener("click", function (e) {
    var t = e.target.closest(".bk-tab"); if (!t) return;
    activeCat = t.getAttribute("data-cat"); renderTabs(); renderGrid();
  });
  elGrid.addEventListener("click", function (e) {
    var add = e.target.closest(".bk-add");
    var inc = e.target.closest(".bk-inc");
    var dec = e.target.closest(".bk-dec");
    var box = e.target.closest(".bk-add, .bk-stepper");
    if (!box) return;
    var catId = box.getAttribute("data-cat"), idx = parseInt(box.getAttribute("data-idx"), 10);
    var cat = catById(catId); if (!cat) return; var item = cat.items[idx];
    if (add) setQty(cat, idx, item, 1);
    else if (inc) setQty(cat, idx, item, qtyOf(catId, idx) + 1);
    else if (dec) setQty(cat, idx, item, qtyOf(catId, idx) - 1);
  });
  elCart.addEventListener("click", function (e) {
    if (e.target.closest(".bk-continue") && lines().length) { goStep(2); return; }
    var rm = e.target.closest(".bk-cl-rm");
    if (rm) { var c = catById(rm.getAttribute("data-cat")); setQty(c, parseInt(rm.getAttribute("data-idx"), 10), null, 0); }
  });
  elMobileBar.addEventListener("click", function (e) {
    if (e.target.closest(".bk-mb-continue") && lines().length) goStep(2);
  });

  // ---- init ----
  renderTabs(); renderGrid(); renderCart(); goStep(1, true);

  // optional deep add ?add=catId:idx
  var qadd = params.get("add");
  if (qadd && qadd.indexOf(":") > -1) {
    var parts = qadd.split(":"), c2 = catById(parts[0]), i2 = parseInt(parts[1], 10);
    if (c2 && c2.items[i2]) { setQty(c2, i2, c2.items[i2], qtyOf(c2.id, i2) + 1); }
  }
})();
