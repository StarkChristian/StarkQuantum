/* Three small things: a mobile menu, a theme toggle, and an archive search.
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

  // Archive search over a small JSON index built at compile time.
  var shade = document.getElementById("search-shade");
  var input = document.getElementById("search-input");
  var results = document.getElementById("search-results");
  var opener = document.getElementById("search-open");
  if (!shade || !input || !results) { return; }

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
    loadIndex();
    input.focus();
    input.select();
  }

  function close() {
    shade.hidden = true;
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

  input.addEventListener("input", function () { render(input.value); });

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
