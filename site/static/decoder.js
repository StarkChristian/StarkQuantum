/* The decoder's deadline: error-correction rounds arrive on a fixed clock, and
 * a decoder that is slower than the clock falls further behind with every round.
 *
 * An idealised queue: one round of syndrome arrives every cycle time, and k
 * decoders working in parallel each take a fixed time to process a round.
 * Nothing leaves the page and nothing is stored.
 */
(function () {
  "use strict";

  var root = document.getElementById("decoder-race");
  if (!root) { return; }

  var NS = "http://www.w3.org/2000/svg";
  var W = 560, H = 300, ML = 62, MR = 16, MT = 16, MB = 44;
  var ROUNDS = 1000;
  var RUN = 1000000;

  function el(name, attrs, parent) {
    var node = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (parent) { parent.appendChild(node); }
    return node;
  }

  function field(id, label, min, max, step, value) {
    return '<label class="pg-field" for="' + id + '">' + label + ' <output id="' + id + '-out"></output>' +
      '<input id="' + id + '" type="range" min="' + min + '" max="' + max + '" step="' + step + '" value="' + value + '"></label>';
  }

  root.innerHTML =
    '<div class="pg-controls dr-controls">' +
    field("dr-cycle", "Cycle time", 0.5, 10, 0.1, 1.1, "µs") +
    field("dr-dec", "Decoder time per round", 0.2, 20, 0.1, 1.5, "µs") +
    field("dr-k", "Decoders in parallel", 1, 8, 1, 1) +
    '</div><div id="dr-svg-host"></div>' +
    '<div class="calc-result" id="dr-out" aria-live="polite"></div>';

  var cycle = document.getElementById("dr-cycle");
  var dec = document.getElementById("dr-dec");
  var kIn = document.getElementById("dr-k");
  var out = document.getElementById("dr-out");
  var host = document.getElementById("dr-svg-host");

  function fmt(x) {
    if (x >= 1e6) { return (x / 1e6).toFixed(1) + " million"; }
    if (x >= 1000) { return Math.round(x).toLocaleString("en-US"); }
    return x.toFixed(x < 10 ? 1 : 0);
  }

  function update() {
    var tc = parseFloat(cycle.value);
    var td = parseFloat(dec.value);
    var k = parseInt(kIn.value, 10);
    document.getElementById("dr-cycle-out").textContent = tc.toFixed(1) + " µs";
    document.getElementById("dr-dec-out").textContent = td.toFixed(1) + " µs";
    document.getElementById("dr-k-out").textContent = String(k);

    var load = td / (k * tc);           // share of the decoder's capacity in use
    var growth = Math.max(0, 1 - 1 / load); // rounds of backlog added per round
    var backlogRun = growth * RUN;
    var clearTime = backlogRun * (td / k); // microseconds to work off the backlog

    host.textContent = "";
    var svg = el("svg", { viewBox: "0 0 " + W + " " + H, "class": "dr-svg", role: "img",
      "aria-label": "Backlog of unprocessed rounds over the first " + ROUNDS + " rounds. " +
        (growth > 0 ? "It grows steadily." : "It stays at zero.") }, host);
    var maxY = Math.max(10, growth * ROUNDS * 1.15);
    function sx(n) { return ML + (n / ROUNDS) * (W - ML - MR); }
    function sy(v) { return H - MB - (v / maxY) * (H - MT - MB); }

    [0, 0.25, 0.5, 0.75, 1].forEach(function (f) {
      var y = sy(maxY * f);
      el("line", { x1: ML, x2: W - MR, y1: y, y2: y, "class": "ch-grid" }, svg);
      var t = el("text", { x: ML - 8, y: y + 4, "class": "ch-tick", "text-anchor": "end" }, svg);
      t.textContent = fmt(maxY * f);
    });
    [0, 250, 500, 750, 1000].forEach(function (n) {
      var t = el("text", { x: sx(n), y: H - MB + 18, "class": "ch-tick", "text-anchor": "middle" }, svg);
      t.textContent = String(n);
    });
    el("line", { x1: ML, x2: W - MR, y1: H - MB, y2: H - MB, "class": "ch-axis" }, svg);
    el("line", { x1: ML, x2: ML, y1: MT, y2: H - MB, "class": "ch-axis" }, svg);
    var xl = el("text", { x: ML + (W - ML - MR) / 2, y: H - 8, "class": "ch-title", "text-anchor": "middle" }, svg);
    xl.textContent = "Rounds since the start (one round every " + tc.toFixed(1) + " µs)";
    var yl = el("text", { transform: "translate(14 " + (MT + (H - MT - MB) / 2) + ") rotate(-90)", "class": "ch-title", "text-anchor": "middle" }, svg);
    yl.textContent = "Rounds waiting";
    el("polyline", { points: sx(0) + "," + sy(0) + " " + sx(ROUNDS) + "," + sy(growth * ROUNDS), "class": "ch-line dr-line" + (growth > 0 ? " dr-late" : "") }, svg);

    out.textContent = "";
    var strong = document.createElement("strong");
    out.appendChild(strong);
    if (growth === 0) {
      strong.textContent = "It keeps up. ";
      out.appendChild(document.createTextNode(
        "The decoder uses " + Math.round(load * 100) + "% of its capacity, so rounds never pile up. " +
        "Its latency, the time from a round arriving to its answer, adds delay to a logical operation but does not make it fall behind."));
    } else {
      strong.textContent = "It falls behind. ";
      out.appendChild(document.createTextNode(
        "The decoder would need " + Math.round(load * 100) + "% of its capacity. Every 1,000 rounds add about " +
        fmt(growth * ROUNDS) + " rounds to the queue. After " + fmt(RUN) + " rounds, which take " +
        (RUN * tc / 1e6).toFixed(1) + " s at this cycle time, " + fmt(backlogRun) + " rounds would be waiting, about " +
        (clearTime / 1e6).toFixed(1) + " s of extra decoding. A computation cannot continue until the oldest round is decoded."));
    }
  }

  [cycle, dec, kIn].forEach(function (i) { i.addEventListener("input", update); });
  update();
})();
