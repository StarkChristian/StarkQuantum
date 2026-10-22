/* A surface-code playground: flip data qubits, see the syndrome, watch a
 * minimum-weight matching decoder repair it, and run many random trials.
 *
 * It models bit-flip (X) errors with perfect measurements, the simplest case.
 * Z errors are handled the same way by the X checks. No data leaves the page
 * and nothing is stored.
 */
(function () {
  "use strict";

  var root = document.getElementById("qec-playground");
  if (!root) { return; }

  var NS = "http://www.w3.org/2000/svg";
  var STEP = 58;
  var MARGIN = 44;

  // ---- the code -----------------------------------------------------------

  function layout(d) {
    var checks = [];
    for (var r = -1; r < d; r++) {
      for (var c = -1; c < d; c++) {
        var kind = (((r + c) % 2) + 2) % 2 === 0 ? "X" : "Z";
        var q = [];
        for (var rr = r; rr <= r + 1; rr++) {
          for (var cc = c; cc <= c + 1; cc++) {
            if (rr >= 0 && rr < d && cc >= 0 && cc < d) { q.push(rr * d + cc); }
          }
        }
        var bulk = q.length === 4;
        var topBottom = (r === -1 || r === d - 1) && q.length === 2 && c >= 0 && c < d - 1;
        var side = (c === -1 || c === d - 1) && q.length === 2 && r >= 0 && r < d - 1;
        if (bulk || (topBottom && kind === "X") || (side && kind === "Z")) {
          checks.push({ kind: kind, q: q, r: r, c: c });
        }
      }
    }
    return checks;
  }

  // The decoder works on the Z checks, which see X errors. A data qubit lies in
  // one or two of them: two make an edge between them, one makes an edge to the
  // boundary. Every edge has weight one.
  function buildGraph(d) {
    var checks = layout(d);
    var zIndex = [];
    checks.forEach(function (ch, i) { if (ch.kind === "Z") { zIndex.push(i); } });
    var n = zIndex.length;
    var boundary = n;
    var edges = []; // adjacency: node -> [{to, qubit}]
    for (var i = 0; i <= n; i++) { edges.push([]); }
    for (var q = 0; q < d * d; q++) {
      var inside = [];
      for (var k = 0; k < n; k++) {
        if (checks[zIndex[k]].q.indexOf(q) !== -1) { inside.push(k); }
      }
      if (inside.length === 2) {
        edges[inside[0]].push({ to: inside[1], qubit: q });
        edges[inside[1]].push({ to: inside[0], qubit: q });
      } else if (inside.length === 1) {
        edges[inside[0]].push({ to: boundary, qubit: q });
        edges[boundary].push({ to: inside[0], qubit: q });
      }
    }
    // Breadth-first search from every node: distances and the way back.
    var dist = [];
    var prev = [];
    for (var s = 0; s <= n; s++) {
      var dd = []; var pp = [];
      for (var t = 0; t <= n; t++) { dd.push(-1); pp.push(null); }
      dd[s] = 0;
      var queue = [s];
      while (queue.length) {
        var u = queue.shift();
        edges[u].forEach(function (e) {
          if (dd[e.to] < 0) { dd[e.to] = dd[u] + 1; pp[e.to] = { from: u, qubit: e.qubit }; queue.push(e.to); }
        });
      }
      dist.push(dd); prev.push(pp);
    }
    return { d: d, checks: checks, zIndex: zIndex, n: n, dist: dist, prev: prev };
  }

  function syndrome(g, errors) {
    var flagged = [];
    for (var k = 0; k < g.n; k++) {
      var count = 0;
      g.checks[g.zIndex[k]].q.forEach(function (q) { if (errors[q]) { count++; } });
      if (count % 2 === 1) { flagged.push(k); }
    }
    return flagged;
  }

  function pathQubits(g, from, to) {
    var out = [];
    var node = to;
    while (node !== from) {
      var step = g.prev[from][node];
      out.push(step.qubit);
      node = step.from;
    }
    return out;
  }

  // Exact minimum-weight matching over the flagged checks, each of which pairs
  // with another flagged check or with the boundary.
  function decode(g, flagged) {
    var m = flagged.length;
    var fix = {};
    if (m === 0) { return fix; }
    function toggle(list) { list.forEach(function (q) { fix[q] = !fix[q]; }); }

    if (m > 18) { // far past anything a code this size should be asked to fix
      var left = flagged.slice();
      while (left.length) {
        var a = left.shift();
        var best = -1; var bestD = g.dist[a][g.n];
        for (var i = 0; i < left.length; i++) {
          if (g.dist[a][left[i]] < bestD) { bestD = g.dist[a][left[i]]; best = i; }
        }
        if (best < 0) { toggle(pathQubits(g, a, g.n)); }
        else { toggle(pathQubits(g, a, left[best])); left.splice(best, 1); }
      }
      return fix;
    }

    var size = 1 << m;
    var cost = new Int16Array(size);
    var choice = new Int16Array(size);
    for (var mask = 1; mask < size; mask++) {
      var lo = 0;
      while (!(mask & (1 << lo))) { lo++; }
      var rest = mask & ~(1 << lo);
      var bestCost = g.dist[flagged[lo]][g.n] + cost[rest];
      var bestChoice = -1;
      for (var j = lo + 1; j < m; j++) {
        if (rest & (1 << j)) {
          var c = g.dist[flagged[lo]][flagged[j]] + cost[rest & ~(1 << j)];
          if (c < bestCost) { bestCost = c; bestChoice = j; }
        }
      }
      cost[mask] = bestCost;
      choice[mask] = bestChoice;
    }
    var cur = size - 1;
    while (cur) {
      var l = 0;
      while (!(cur & (1 << l))) { l++; }
      var pick = choice[cur];
      if (pick < 0) { toggle(pathQubits(g, flagged[l], g.n)); cur &= ~(1 << l); }
      else { toggle(pathQubits(g, flagged[l], flagged[pick])); cur &= ~(1 << l) & ~(1 << pick); }
    }
    return fix;
  }

  // The logical operator that matters here is a string of Z along the top row.
  // A leftover X error with no syndrome is harmless if it crosses that row an
  // even number of times, and a logical error if it crosses it an odd number.
  function outcome(g, errors, fix) {
    var odd = 0;
    var clean = true;
    var residual = [];
    for (var q = 0; q < g.d * g.d; q++) {
      residual.push(!!errors[q] !== !!fix[q]);
    }
    if (syndrome(g, residual).length) { clean = false; }
    for (var c = 0; c < g.d; c++) { if (residual[c]) { odd++; } }
    return { clean: clean, logical: odd % 2 === 1 };
  }

  // ---- drawing ------------------------------------------------------------

  var graphs = {};
  function graphFor(d) { if (!graphs[d]) { graphs[d] = buildGraph(d); } return graphs[d]; }

  function el(name, attrs, parent) {
    var node = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (parent) { parent.appendChild(node); }
    return node;
  }

  var state = { d: 3, errors: {} };
  var nodes = {};

  function pos(d, r, c) { return [MARGIN + STEP * c, MARGIN + STEP * r]; }

  function checkPath(d, ch) {
    var pts = ch.q.map(function (q) { return pos(d, Math.floor(q / d), q % d); });
    if (pts.length === 4) {
      return "M" + pts[0] + " L" + pts[1] + " L" + pts[3] + " L" + pts[2] + " Z";
    }
    var a = pts[0]; var b = pts[1];
    var nx = 0; var ny = 0;
    if (ch.r === -1) { ny = -1; } else if (ch.r === d - 1) { ny = 1; }
    else if (ch.c === -1) { nx = -1; } else { nx = 1; }
    var lift = STEP / 2 * 1.33;
    return "M" + a + " L" + b + " C" + (b[0] + nx * lift) + " " + (b[1] + ny * lift) + " " +
      (a[0] + nx * lift) + " " + (a[1] + ny * lift) + " " + a + " Z";
  }

  function checkCentre(d, ch) {
    var pts = ch.q.map(function (q) { return pos(d, Math.floor(q / d), q % d); });
    var x = 0; var y = 0;
    pts.forEach(function (p) { x += p[0]; y += p[1]; });
    x /= pts.length; y /= pts.length;
    if (pts.length === 2) {
      var half = STEP / 2 * 0.5;
      if (ch.r === -1) { y -= half; } else if (ch.r === d - 1) { y += half; }
      else if (ch.c === -1) { x -= half; } else { x += half; }
    }
    return [x, y];
  }

  var liveRegion;
  var svgHost;
  var summary;

  function build() {
    root.textContent = "";
    var g = graphFor(state.d);
    var size = STEP * (state.d - 1) + MARGIN * 2;

    var controls = document.createElement("div");
    controls.className = "pg-controls";
    controls.innerHTML =
      '<label class="pg-field">Code distance <select id="pg-d"><option value="3">3 (9 data qubits)</option><option value="5">5 (25 data qubits)</option></select></label>' +
      '<button type="button" class="tool" id="pg-clear">Clear</button>' +
      '<button type="button" class="tool" id="pg-random">Add random errors</button>' +
      '<label class="pg-field">Error chance per qubit <output id="pg-rate-out">8%</output>' +
      '<input id="pg-rate" type="range" min="1" max="30" value="8"></label>' +
      '<button type="button" class="tool" id="pg-trials">Run 2,000 trials</button>';
    root.appendChild(controls);

    svgHost = document.createElement("div");
    root.appendChild(svgHost);
    summary = document.createElement("div");
    summary.className = "calc-result";
    summary.setAttribute("aria-live", "polite");
    root.appendChild(summary);
    liveRegion = document.createElement("p");
    liveRegion.className = "pg-note muted";
    liveRegion.textContent = "This toy has only bit-flip errors and perfect measurements, so its threshold is far higher than the one on the threshold page.";
    root.appendChild(liveRegion);

    document.getElementById("pg-d").value = String(state.d);
    document.getElementById("pg-d").addEventListener("change", function (e) {
      state.d = parseInt(e.target.value, 10); state.errors = {}; build();
    });
    document.getElementById("pg-clear").addEventListener("click", function () { state.errors = {}; draw(); });
    var rate = document.getElementById("pg-rate");
    rate.addEventListener("input", function () {
      document.getElementById("pg-rate-out").textContent = rate.value + "%";
    });
    document.getElementById("pg-random").addEventListener("click", function () {
      var p = parseInt(rate.value, 10) / 100;
      state.errors = {};
      for (var q = 0; q < state.d * state.d; q++) { if (Math.random() < p) { state.errors[q] = true; } }
      draw();
    });
    document.getElementById("pg-trials").addEventListener("click", function () { runTrials(parseInt(rate.value, 10) / 100); });

    var svg = el("svg", { viewBox: "0 0 " + size + " " + size, "class": "pg-svg", role: "group",
      "aria-label": "Surface code patch of distance " + state.d + ". Activate a data qubit to flip it." });
    svgHost.appendChild(svg);
    nodes = { checks: [], qubits: [], rings: [] };

    g.checks.forEach(function (ch) {
      var path = el("path", { d: checkPath(g.d, ch), "class": "sc-" + ch.kind.toLowerCase() }, svg);
      nodes.checks.push(path);
    });
    g.checks.forEach(function (ch) {
      var c = checkCentre(g.d, ch);
      var t = el("text", { x: c[0], y: c[1] + 5, "class": "sc-label", "text-anchor": "middle" }, svg);
      t.textContent = ch.kind;
    });
    for (var q = 0; q < g.d * g.d; q++) {
      (function (qq) {
        var p = pos(g.d, Math.floor(qq / g.d), qq % g.d);
        var group = el("g", { "class": "pg-qubit", tabindex: "0", role: "button", "aria-pressed": "false" }, svg);
        var ring = el("circle", { cx: p[0], cy: p[1], r: 15, "class": "pg-ring" }, group);
        var dot = el("circle", { cx: p[0], cy: p[1], r: 9, "class": "sc-data" }, group);
        nodes.qubits.push(dot);
        nodes.rings.push(ring);
        group.addEventListener("click", function () { state.errors[qq] = !state.errors[qq]; draw(); });
        group.addEventListener("keydown", function (e) {
          if (e.key === "Enter" || e.key === " ") { e.preventDefault(); state.errors[qq] = !state.errors[qq]; draw(); }
        });
        nodes.qubits[qq].parentNode.setAttribute("data-q", String(qq));
      })(q);
    }
    draw();
  }

  function draw() {
    var g = graphFor(state.d);
    var flagged = syndrome(g, state.errors);
    var fix = decode(g, flagged);
    var result = outcome(g, state.errors, fix);
    var lit = {};
    flagged.forEach(function (k) { lit[g.zIndex[k]] = true; });
    g.checks.forEach(function (ch, i) {
      nodes.checks[i].setAttribute("class", "sc-" + ch.kind.toLowerCase() + (lit[i] ? " sc-lit" : ""));
    });
    var errCount = 0; var fixCount = 0;
    for (var q = 0; q < g.d * g.d; q++) {
      var isErr = !!state.errors[q];
      var isFix = !!fix[q];
      if (isErr) { errCount++; }
      if (isFix) { fixCount++; }
      nodes.qubits[q].setAttribute("class", "sc-data" + (isErr ? " sc-err" : ""));
      nodes.rings[q].setAttribute("class", "pg-ring" + (isFix ? " pg-fix" : ""));
      var group = nodes.qubits[q].parentNode;
      group.setAttribute("aria-pressed", isErr ? "true" : "false");
      group.setAttribute("aria-label", "Data qubit, row " + (Math.floor(q / g.d) + 1) + ", column " + (q % g.d + 1) +
        (isErr ? ", has an error" : ", no error") + (isFix ? ", decoder flips it" : ""));
    }
    var verdict;
    if (errCount === 0) { verdict = "No errors. Click a data qubit to add one."; }
    else if (!result.logical) { verdict = "Corrected. The decoder's flips together with your errors leave the logical qubit intact."; }
    else { verdict = "Logical error. The decoder's best guess is wrong, and the stored qubit is damaged."; }
    summary.textContent = "";
    var strong = document.createElement("strong");
    strong.textContent = errCount + " error" + (errCount === 1 ? "" : "s") + ", " + flagged.length + " check" +
      (flagged.length === 1 ? "" : "s") + " flagged, " + fixCount + " decoder flip" + (fixCount === 1 ? "" : "s") + ". ";
    summary.appendChild(strong);
    summary.appendChild(document.createTextNode(verdict));
  }

  function runTrials(p) {
    var out = [];
    [3, 5].forEach(function (d) {
      var g = graphFor(d);
      var fails = 0; var N = 2000;
      for (var t = 0; t < N; t++) {
        var errors = {};
        for (var q = 0; q < d * d; q++) { if (Math.random() < p) { errors[q] = true; } }
        var fix = decode(g, syndrome(g, errors));
        if (outcome(g, errors, fix).logical) { fails++; }
      }
      out.push("distance " + d + ": " + (100 * fails / N).toFixed(1) + "% fail");
    });
    summary.textContent = "At " + Math.round(p * 100) + "% error chance per qubit, in 2,000 random trials each, " +
      out.join("; ") + ". Below the toy's threshold the bigger code fails less often; above it, more often.";
  }

  build();
})();
