/* A mobile menu, a theme toggle, glossary popovers, and an archive search.
   Nothing is tracked. The only stored value is the theme preference. */

(function () {
  "use strict";

  var root = document.documentElement;

  // Mobile menu. A class toggle, no animation library, no dependencies.
  var menuToggle = document.getElementById("menu-toggle");
  var mastheadRight = document.getElementById("masthead-right");
  if (menuToggle && mastheadRight) {
    menuToggle.addEventListener("click", function () {
      var open = mastheadRight.classList.toggle("open");
      menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
      menuToggle.textContent = open ? "Close" : "Menu";
    });
  }

  // Theme: auto -> light -> dark -> auto.
  var toggle = document.getElementById("theme-toggle");
  if (toggle) {
    var order = ["auto", "light", "dark"];

    var describe = function (mode) {
      var next = order[(order.indexOf(mode) + 1) % order.length];
      toggle.setAttribute("aria-label", "Theme: " + mode + ". Switch to " + next + ".");
      toggle.setAttribute("title", "Theme: " + mode);
    };

    describe(root.getAttribute("data-theme") || "auto");

    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") || "auto";
      var next = order[(order.indexOf(current) + 1) % order.length];
      root.setAttribute("data-theme", next);
      describe(next);
      try {
        if (next === "auto") { localStorage.removeItem("sq-theme"); }
        else { localStorage.setItem("sq-theme", next); }
      } catch (e) {}
    });
  }

  // Glossary terms: the definition appears in a popover on hover or focus.
  // Without the Popover API, or without script, the link keeps its title.
  var termLinks = document.querySelectorAll("a.term");
  if (termLinks.length && typeof HTMLElement.prototype.showPopover === "function") {
    var pop = document.createElement("div");
    pop.className = "term-pop";
    pop.id = "term-pop";
    pop.setAttribute("popover", "manual");
    pop.setAttribute("role", "tooltip");
    document.body.appendChild(pop);

    var hidePop = function () {
      if (pop.matches(":popover-open")) { pop.hidePopover(); }
      for (var j = 0; j < termLinks.length; j++) { termLinks[j].removeAttribute("aria-describedby"); }
    };

    var showPop = function (link) {
      pop.textContent = "";
      var label = document.createElement("strong");
      label.textContent = link.textContent;
      pop.appendChild(label);
      pop.appendChild(document.createTextNode(link.getAttribute("data-def")));
      link.setAttribute("aria-describedby", "term-pop");
      if (!pop.matches(":popover-open")) { pop.showPopover(); }
      var r = link.getBoundingClientRect();
      var left = Math.min(Math.max(8, r.left), window.innerWidth - pop.offsetWidth - 8);
      var below = r.bottom + 8;
      var top = below + pop.offsetHeight > window.innerHeight ? r.top - pop.offsetHeight - 8 : below;
      pop.style.left = left + "px";
      pop.style.top = Math.max(8, top) + "px";
    };

    Array.prototype.forEach.call(termLinks, function (link) {
      link.setAttribute("data-def", link.getAttribute("title") || "");
      link.removeAttribute("title");
      link.addEventListener("pointerenter", function (e) {
        if (e.pointerType === "mouse") { showPop(link); }
      });
      link.addEventListener("pointerleave", hidePop);
      link.addEventListener("focus", function () { showPop(link); });
      link.addEventListener("blur", hidePop);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { hidePop(); } });
    window.addEventListener("scroll", hidePop, { passive: true });
  }

  // Archive search over a small JSON index built at compile time.
  var shade = document.getElementById("search-shade");
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var opener = document.getElementById("search-open");
  if (!shade || !input || !results) { return; }

  // Full-text search is Pagefind: a static index built next to the pages and
  // read in the browser. Queries are never sent anywhere. If /pagefind/ is
  // missing, the small title-and-summary index below takes over.
  var pagefind = null;
  var pagefindState = "idle"; // idle, loading, ready, failed
  var latest = 0;

  function loadPagefind() {
    if (pagefindState !== "idle") { return; }
    pagefindState = "loading";
    import("/pagefind/pagefind.js")
      .then(function (pf) {
        pagefind = pf;
        pagefindState = "ready";
        run(input.value);
      })
      .catch(function () { pagefindState = "failed"; loadIndex(); });
  }

  function run(query) {
    if (pagefindState === "failed") { render(query); return; }
    if (pagefindState !== "ready") { return; }
    var q = query.trim();
    var mine = ++latest;
    if (!q) { results.innerHTML = ""; return; }
    pagefind.debouncedSearch(q, {}, 120).then(function (found) {
      if (!found || mine !== latest) { return; }
      return Promise.all(found.results.slice(0, 8).map(function (r) { return r.data(); }))
        .then(function (items) { if (mine === latest) { renderFound(items); } });
    });
  }

  function renderFound(items) {
    results.innerHTML = "";
    if (items.length === 0) {
      var empty = document.createElement("li");
      empty.className = "search-hint";
      empty.textContent = "Nothing in the archive matches that.";
      results.appendChild(empty);
      return;
    }
    items.forEach(function (item) {
      // A glossary hit links to the one entry, not to the top of the page.
      var sub = item.sub_results && item.sub_results[0];
      var glossary = item.meta && item.meta.type === "Glossary" && sub;
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = glossary ? sub.url : item.url;
      var type = document.createElement("span");
      type.className = "r-type";
      type.textContent = (item.meta && item.meta.type) || "";
      var title = document.createElement("span");
      title.className = "r-title";
      title.textContent = glossary ? sub.title : (item.meta && item.meta.title) || item.url;
      var excerpt = document.createElement("span");
      excerpt.className = "r-excerpt";
      // Pagefind escapes the text and wraps matches in <mark>.
      excerpt.innerHTML = glossary ? sub.excerpt : item.excerpt;
      a.appendChild(type);
      a.appendChild(title);
      a.appendChild(excerpt);
      li.appendChild(a);
      results.appendChild(li);
    });
  }

  var index = null;
  var loading = false;

  function loadIndex() {
    if (index || loading) { return; }
    loading = true;
    fetch("/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; loading = false; render(input.value); })
      .catch(function () { loading = false; });
  }

  function open() {
    shade.hidden = false;
    loadPagefind();
    input.focus();
    input.select();
  }

  function close() {
    shade.hidden = true;
    latest++;
    input.value = "";
    results.innerHTML = "";
  }

  function score(entry, terms) {
    var title = entry.title.toLowerCase();
    var text = (entry.text || "").toLowerCase();
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (title.indexOf(t) === 0) { total += 6; }
      else if (title.indexOf(t) > -1) { total += 4; }
      else if (text.indexOf(t) > -1) { total += 1; }
      else { return 0; }
    }
    return total;
  }

  function render(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    results.innerHTML = "";
    if (!index || terms.length === 0) { return; }

    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var s = score(index[i], terms);
      if (s > 0) { hits.push({ entry: index[i], score: s }); }
    }
    hits.sort(function (a, b) { return b.score - a.score; });

    if (hits.length === 0) {
      var empty = document.createElement("li");
      empty.className = "search-hint";
      empty.textContent = "Nothing in the archive matches that.";
      results.appendChild(empty);
      return;
    }

    hits.slice(0, 10).forEach(function (hit) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = hit.entry.url;
      var type = document.createElement("span");
      type.className = "r-type";
      type.textContent = hit.entry.type + (hit.entry.meta ? " · " + hit.entry.meta : "");
      var title = document.createElement("span");
      title.className = "r-title";
      title.textContent = hit.entry.title;
      a.appendChild(type);
      a.appendChild(title);
      li.appendChild(a);
      results.appendChild(li);
    });
  }

  input.addEventListener("input", function () { run(input.value); });

  if (opener) {
    opener.addEventListener("click", function (e) { e.preventDefault(); open(); });
  }

  shade.addEventListener("click", function (e) {
    if (e.target === shade) { close(); }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !shade.hidden) { close(); }
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      shade.hidden ? open() : close();
    }
  });
})();
