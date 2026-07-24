/*
 * Proptechguiden – återanvändbar leadwidget.
 *
 * Droppa in var som helst på sajten:
 *
 *   <div data-lead-form
 *        data-source="roi-kalkylator"
 *        data-segment="fastighetsagare"     (valfritt, låser målgruppssteget)
 *        data-need="energi"                 (valfritt, låser behovssteget)
 *        data-title="Få offert på energioptimering"></div>
 *   <script src="/lead-engine.js"></script>
 *
 * Tre steg, i den ordning som kvalificerar hårdast först och lämnar
 * e-postadressen sist – då är användaren redan investerad i flödet.
 *   Steg 1: Vem är du och vad behöver du
 *   Steg 2: Hur stor är portföljen, när och med vilken budget
 *   Steg 3: Kontaktuppgifter och samtycke
 *
 * Kalkylatorer kan skicka med sina siffror genom att sätta
 * window.proptechCalcData = { ... } före submit.
 */
(function () {
  "use strict";

  var SEGMENTS = [
    { value: "fastighetsagare", label: "Fastighetsägare" },
    { value: "forvaltare", label: "Kommersiell förvaltare" },
    { value: "brf", label: "BRF-styrelse" }
  ];

  var NEEDS = [
    { value: "energi", label: "Energi & hållbarhet" },
    { value: "forvaltning", label: "Digital förvaltning & drift" },
    { value: "iot", label: "IoT & sensorer" },
    { value: "access", label: "Lås & passagesystem" },
    { value: "analys", label: "Analys & AI" },
    { value: "boende", label: "Boendeapp & hyresgäst" },
    { value: "uthyrning", label: "Uthyrning & marknad" },
    { value: "plattform", label: "Öppen plattform / integration" }
  ];

  var TIMEFRAMES = [
    { value: "omgaende", label: "Omgående" },
    { value: "inom_3_man", label: "Inom 3 månader" },
    { value: "3_6_man", label: "3–6 månader" },
    { value: "6_12_man", label: "6–12 månader" },
    { value: "orienterar", label: "Orienterar mig bara" }
  ];

  var BUDGETS = [
    { value: "beslutad", label: "Budget är beslutad" },
    { value: "under_beredning", label: "Budget under beredning" },
    { value: "ingen", label: "Ingen budget ännu" }
  ];

  var input =
    "w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 " +
    "focus:ring-sky-500 focus:border-transparent outline-none transition";
  var label = "block text-sm font-semibold text-slate-700 mb-1.5";

  function options(list, placeholder) {
    var html = placeholder ? '<option value="">' + placeholder + "</option>" : "";
    list.forEach(function (o) {
      html += '<option value="' + o.value + '">' + o.label + "</option>";
    });
    return html;
  }

  function render(el) {
    var source = el.dataset.source || "okand";
    var lockedSegment = el.dataset.segment || "";
    var lockedNeed = el.dataset.need || "";
    var title = el.dataset.title || "Få offerter från rätt leverantörer";
    var intro =
      el.dataset.intro ||
      "Svara på tre snabba frågor så matchar vi dig mot leverantörer som " +
      "faktiskt arbetar med din typ av fastighet.";
    var uid = "le" + Math.random().toString(36).slice(2, 8);

    var segmentField = lockedSegment
      ? ""
      : '<div><label class="' + label + '" for="' + uid + '-segment">Vem är du?</label>' +
        '<select id="' + uid + '-segment" name="segment" class="' + input + '" required>' +
        options(SEGMENTS, "Välj målgrupp") + "</select></div>";

    var needField = lockedNeed
      ? ""
      : '<div><label class="' + label + '" for="' + uid + '-need">Vad vill ni lösa?</label>' +
        '<select id="' + uid + '-need" name="need" class="' + input + '" required>' +
        options(NEEDS, "Välj område") + "</select></div>";

    el.innerHTML =
      '<div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">' +
        '<div class="bg-slate-900 text-white px-6 py-5">' +
          '<h3 class="text-xl font-extrabold tracking-tight">' + title + "</h3>" +
          '<p class="text-slate-300 text-sm mt-1">' + intro + "</p>" +
        "</div>" +
        '<div class="px-6 pt-5">' +
          '<div class="flex gap-2" data-progress>' +
            '<div class="h-1.5 flex-1 rounded-full bg-sky-600"></div>' +
            '<div class="h-1.5 flex-1 rounded-full bg-slate-200"></div>' +
            '<div class="h-1.5 flex-1 rounded-full bg-slate-200"></div>' +
          "</div>" +
          '<p class="text-xs text-slate-500 mt-2" data-stepcount>Steg 1 av 3</p>' +
        "</div>" +
        '<form class="p-6 space-y-4" novalidate>' +

          '<div data-step="0" class="space-y-4">' +
            segmentField + needField +
            '<div><label class="' + label + '" for="' + uid + '-role">Din roll</label>' +
            '<input id="' + uid + '-role" name="role" class="' + input + '" ' +
            'placeholder="T.ex. fastighetschef, förvaltare, styrelseordförande"></div>' +
          "</div>" +

          '<div data-step="1" class="space-y-4 hidden">' +
            '<div class="grid grid-cols-2 gap-4">' +
              '<div><label class="' + label + '" for="' + uid + '-sqm">Yta (kvm)</label>' +
              '<input id="' + uid + '-sqm" name="sqm" type="number" min="0" class="' + input + '" placeholder="10 000"></div>' +
              '<div><label class="' + label + '" for="' + uid + '-units">Antal enheter</label>' +
              '<input id="' + uid + '-units" name="units" type="number" min="0" class="' + input + '" placeholder="120"></div>' +
            "</div>" +
            '<div><label class="' + label + '" for="' + uid + '-timeframe">När vill ni vara igång?</label>' +
            '<select id="' + uid + '-timeframe" name="timeframe" class="' + input + '" required>' +
            options(TIMEFRAMES, "Välj tidsram") + "</select></div>" +
            '<div><label class="' + label + '" for="' + uid + '-budget">Budgetläge</label>' +
            '<select id="' + uid + '-budget" name="budget_state" class="' + input + '" required>' +
            options(BUDGETS, "Välj budgetläge") + "</select></div>" +
          "</div>" +

          '<div data-step="2" class="space-y-4 hidden">' +
            '<div class="grid grid-cols-2 gap-4">' +
              '<div><label class="' + label + '" for="' + uid + '-name">Namn</label>' +
              '<input id="' + uid + '-name" name="name" class="' + input + '" required></div>' +
              '<div><label class="' + label + '" for="' + uid + '-company">Företag / förening</label>' +
              '<input id="' + uid + '-company" name="company" class="' + input + '" required></div>' +
            "</div>" +
            '<div><label class="' + label + '" for="' + uid + '-email">E-post</label>' +
            '<input id="' + uid + '-email" name="email" type="email" class="' + input + '" required></div>' +
            '<div><label class="' + label + '" for="' + uid + '-phone">Telefon <span class="font-normal text-slate-400">(ger snabbare svar)</span></label>' +
            '<input id="' + uid + '-phone" name="phone" type="tel" class="' + input + '"></div>' +
            '<div><label class="' + label + '" for="' + uid + '-message">Något mer vi bör veta?</label>' +
            '<textarea id="' + uid + '-message" name="message" rows="2" class="' + input + '"></textarea></div>' +
            '<label class="flex gap-3 items-start text-sm text-slate-600 bg-slate-50 p-3 rounded-xl">' +
              '<input type="checkbox" name="consent" class="mt-1 h-4 w-4 rounded border-slate-300" checked>' +
              "<span>Ja, matcha mig med relevanta leverantörer och låt dem kontakta mig. " +
              'Vi delar aldrig uppgifterna med någon annan. <a href="/privacy-policy" class="underline">Integritetspolicy</a></span>' +
            "</label>" +
          "</div>" +

          '<p class="text-sm text-red-600 hidden" data-error></p>' +

          '<div class="flex gap-3 pt-1">' +
            '<button type="button" data-back class="hidden px-5 py-3 rounded-xl font-bold text-slate-600 hover:bg-slate-100 transition">Tillbaka</button>' +
            '<button type="submit" data-next class="flex-1 bg-sky-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-sky-700 transition shadow-lg shadow-sky-600/25">Nästa</button>' +
          "</div>" +
          '<p class="text-xs text-slate-400 text-center">Kostnadsfritt och utan köpkrav. Vi är oberoende av leverantörerna.</p>' +
        "</form>" +
      "</div>";

    wire(el, { source: source, segment: lockedSegment, need: lockedNeed });
  }

  function wire(el, locked) {
    var form = el.querySelector("form");
    var steps = el.querySelectorAll("[data-step]");
    var bars = el.querySelectorAll("[data-progress] div");
    var counter = el.querySelector("[data-stepcount]");
    var errorEl = el.querySelector("[data-error]");
    var backBtn = el.querySelector("[data-back]");
    var nextBtn = el.querySelector("[data-next]");
    var current = 0;

    function show(i) {
      current = i;
      steps.forEach(function (s, idx) { s.classList.toggle("hidden", idx !== i); });
      bars.forEach(function (b, idx) {
        b.className = "h-1.5 flex-1 rounded-full " + (idx <= i ? "bg-sky-600" : "bg-slate-200");
      });
      counter.textContent = "Steg " + (i + 1) + " av 3";
      backBtn.classList.toggle("hidden", i === 0);
      nextBtn.textContent = i === 2 ? "Skicka förfrågan" : "Nästa";
      errorEl.classList.add("hidden");
    }

    function validate(i) {
      var fields = steps[i].querySelectorAll("[required]");
      for (var n = 0; n < fields.length; n++) {
        if (!fields[n].value.trim()) return "Fyll i alla fält för att gå vidare.";
        if (fields[n].type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(fields[n].value)) {
          return "Kontrollera e-postadressen.";
        }
      }
      // Steg 2 behöver minst ett storleksmått för att kunna poängsättas.
      if (i === 1) {
        var sqm = steps[1].querySelector('[name="sqm"]').value;
        var units = steps[1].querySelector('[name="units"]').value;
        if (!sqm && !units) return "Ange yta eller antal enheter så kan vi matcha rätt.";
      }
      return null;
    }

    function fail(msg) {
      errorEl.textContent = msg;
      errorEl.classList.remove("hidden");
    }

    backBtn.addEventListener("click", function () { show(current - 1); });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = validate(current);
      if (err) return fail(err);
      if (current < 2) {
        show(current + 1);
        track("lead_step", { step: current + 1, source: locked.source });
        return;
      }
      submit();
    });

    function submit() {
      var data = new FormData(form);
      var payload = {
        email: data.get("email"),
        name: data.get("name") || null,
        company: data.get("company") || null,
        phone: data.get("phone") || null,
        role: data.get("role") || null,
        segment: locked.segment || data.get("segment") || null,
        need: locked.need || data.get("need") || null,
        sqm: data.get("sqm") ? parseInt(data.get("sqm"), 10) : null,
        units: data.get("units") ? parseInt(data.get("units"), 10) : null,
        timeframe: data.get("timeframe") || null,
        budget_state: data.get("budget_state") || null,
        message: data.get("message") || null,
        consent: data.get("consent") === "on",
        source: locked.source,
        calc_data: window.proptechCalcData || {}
      };

      nextBtn.disabled = true;
      nextBtn.textContent = "Skickar…";

      fetch("/api/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
        .then(function (r) {
          if (!r.ok) throw new Error("http " + r.status);
          return r.json();
        })
        .then(function (res) {
          track("lead_submit", { source: locked.source, grade: res.grade, need: payload.need });
          done(el, res);
        })
        .catch(function () {
          nextBtn.disabled = false;
          nextBtn.textContent = "Skicka förfrågan";
          fail("Något gick fel. Försök igen eller mejla oss på simon@adviseo.se.");
        });
    }

    show(0);
  }

  function done(el, res) {
    var partners = "";
    if (res.partners && res.partners.length) {
      partners =
        '<p class="text-slate-600 mt-4">Vi har matchat dig mot:</p><ul class="mt-2 space-y-1">' +
        res.partners
          .map(function (p) {
            return '<li><a class="font-bold text-sky-700 hover:underline" href="/leverantor/' +
              p.slug + '">' + p.name + "</a></li>";
          })
          .join("") +
        "</ul>";
    }
    el.innerHTML =
      '<div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 text-center">' +
        '<div class="w-14 h-14 mx-auto rounded-full bg-emerald-100 flex items-center justify-center mb-4">' +
          '<svg class="w-7 h-7 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
          '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>' +
        "</div>" +
        '<h3 class="text-2xl font-extrabold tracking-tight">Tack! Vi har tagit emot din förfrågan.</h3>' +
        '<p class="text-slate-600 mt-2">Du får en bekräftelse på mejlen. Vi återkommer med förslag inom en arbetsdag.</p>' +
        partners +
        '<a href="/directory" class="inline-block mt-6 text-sm font-bold text-slate-900 hover:text-sky-600">Under tiden: bläddra i leverantörskatalogen →</a>' +
      "</div>";
  }

  function track(name, params) {
    if (typeof window.gtag === "function") window.gtag("event", name, params || {});
  }

  function init() {
    document.querySelectorAll("[data-lead-form]").forEach(render);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
