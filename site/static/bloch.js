/* The Bloch sphere: the state of one qubit as a point on a sphere.
 *
 * Two angles set the state, |psi> = cos(theta/2)|0> + e^(i phi) sin(theta/2)|1>,
 * and the page shows the two amplitudes and the two measurement probabilities.
 * Nothing leaves the page and nothing is stored.
 */
(function () {
  "use strict";

  var root = document.getElementById("bloch");
  if (!root) { return; }

  var NS = "http://www.w3.org/2000/svg";
  var C = 150;      // centre of the drawing
  var R = 105;      // radius of the sphere
  var AZ = -38 * Math.PI / 180;
  var EL = 22 * Math.PI / 180;

  var state = { theta: 60, phi: 40 };

  function el(name, attrs, parent) {
    var node = document.createElementNS(NS, name);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (parent) { parent.appendChild(node); }
    return node;
  }

  // Rotate a point of the unit sphere into view. Returns screen x, screen y
  // (down is positive) and whether the point faces the viewer.
  function project(x, y, z) {
    var x1 = x * Math.cos(AZ) - y * Math.sin(AZ);
    var y1 = x * Math.sin(AZ) + y * Math.cos(AZ);
    var up = z * Math.cos(EL) + y1 * Math.sin(EL);
    var toward = -y1 * Math.cos(EL) + z * Math.sin(EL);
    return { x: C + R * x1, y: C - R * up, front: toward >= 0 };
  }

  function circlePath(fn) {
    var front = ""; var back = "";
    var prev = null;
    for (var i = 0; i <= 120; i++) {
      var t = 2 * Math.PI * i / 120;
      var p = fn(t);
      var s = project(p[0], p[1], p[2]);
      var cmd = (prev && prev.front === s.front) ? "L" : "M";
      var piece = cmd + s.x.toFixed(1) + " " + s.y.toFixed(1) + " ";
      if (s.front) { front += piece; } else { back += piece; }
      prev = s;
    }
    return { front: front, back: back };
  }

  function build() {
    root.textContent = "";

    var controls = document.createElement("div");
    controls.className = "pg-controls";
    controls.innerHTML =
      '<label class="pg-field">Polar angle <output id="bl-t-out"></output><input id="bl-t" type="range" min="0" max="180" step="1"></label>' +
      '<label class="pg-field">Azimuth <output id="bl-p-out"></output><input id="bl-p" type="range" min="0" max="359" step="1"></label>';
    root.appendChild(controls);

    var presets = document.createElement("div");
    presets.className = "pg-controls";
    [["|0⟩", 0, 0], ["|1⟩", 180, 0], ["|+⟩", 90, 0], ["|−⟩", 90, 180], ["|+i⟩", 90, 90]]
      .forEach(function (p) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "tool"; b.textContent = p[0];
        b.addEventListener("click", function () { state.theta = p[1]; state.phi = p[2]; sync(); draw(); });
        presets.appendChild(b);
      });
    root.appendChild(presets);

    var host = document.createElement("div");
    root.appendChild(host);
    var svg = el("svg", { viewBox: "0 0 300 300", "class": "bl-svg", role: "img",
      "aria-label": "Bloch sphere with a state vector. The numbers below the sphere give the same state." }, host);
    svg.appendChild(document.createElementNS(NS, "g")).setAttribute("id", "bl-layer");

    var out = document.createElement("div");
    out.className = "calc-result";
    out.id = "bl-out";
    out.setAttribute("aria-live", "polite");
    root.appendChild(out);

    var bars = document.createElement("div");
    bars.className = "bl-bars";
    bars.innerHTML =
      '<div class="bl-bar"><span>P(0)</span><span class="bl-track"><span id="bl-b0" class="bl-fill"></span></span><output id="bl-v0"></output></div>' +
      '<div class="bl-bar"><span>P(1)</span><span class="bl-track"><span id="bl-b1" class="bl-fill"></span></span><output id="bl-v1"></output></div>';
    root.appendChild(bars);

    document.getElementById("bl-t").addEventListener("input", function (e) { state.theta = parseInt(e.target.value, 10); draw(); readouts(); });
    document.getElementById("bl-p").addEventListener("input", function (e) { state.phi = parseInt(e.target.value, 10); draw(); readouts(); });
    sync();
    draw();
  }

  function sync() {
    document.getElementById("bl-t").value = String(state.theta);
    document.getElementById("bl-p").value = String(state.phi);
    readouts();
  }

  function readouts() {
    var th = state.theta * Math.PI / 180;
    var a = Math.cos(th / 2);
    var b = Math.sin(th / 2);
    var p0 = a * a; var p1 = b * b;
    document.getElementById("bl-t-out").textContent = state.theta + "°";
    document.getElementById("bl-p-out").textContent = state.phi + "°";
    var out = document.getElementById("bl-out");
    out.textContent = "";
    var strong = document.createElement("strong");
    strong.textContent = "State. ";
    out.appendChild(strong);
    out.appendChild(document.createTextNode(
      "α = " + a.toFixed(3) + ", β = " + b.toFixed(3) + " × e^(i·" + state.phi + "°). " +
      "A measurement gives 0 with probability " + (100 * p0).toFixed(1) + "% and 1 with probability " + (100 * p1).toFixed(1) +
      "%. The azimuth sets the phase, which changes no probability until the qubit interacts with another."));
    document.getElementById("bl-b0").style.width = (100 * p0) + "%";
    document.getElementById("bl-b1").style.width = (100 * p1) + "%";
    document.getElementById("bl-v0").textContent = (100 * p0).toFixed(1) + "%";
    document.getElementById("bl-v1").textContent = (100 * p1).toFixed(1) + "%";
  }

  function draw() {
    var layer = document.getElementById("bl-layer");
    layer.textContent = "";

    el("circle", { cx: C, cy: C, r: R, "class": "bl-sphere" }, layer);

    var eq = circlePath(function (t) { return [Math.cos(t), Math.sin(t), 0]; });
    var mer = circlePath(function (t) { return [Math.cos(t), 0, Math.sin(t)]; });
    [eq, mer].forEach(function (c) {
      el("path", { d: c.back, "class": "bl-circle bl-back" }, layer);
      el("path", { d: c.front, "class": "bl-circle" }, layer);
    });

    var axes = [["z", [0, 0, 1], "|0⟩"], ["-z", [0, 0, -1], "|1⟩"],
                ["x", [1, 0, 0], "x"], ["y", [0, 1, 0], "y"]];
    axes.forEach(function (a) {
      var tip = project(a[1][0], a[1][1], a[1][2]);
      el("line", { x1: C, y1: C, x2: tip.x, y2: tip.y, "class": "bl-axis" }, layer);
      var lx = C + (tip.x - C) * 1.14; var ly = C + (tip.y - C) * 1.14;
      var t = el("text", { x: lx, y: ly + 4, "class": "bl-label", "text-anchor": "middle" }, layer);
      t.textContent = a[2];
    });

    var th = state.theta * Math.PI / 180;
    var ph = state.phi * Math.PI / 180;
    var v = [Math.sin(th) * Math.cos(ph), Math.sin(th) * Math.sin(ph), Math.cos(th)];
    var tipP = project(v[0], v[1], v[2]);
    var foot = project(v[0], v[1], 0);
    el("line", { x1: C, y1: C, x2: foot.x, y2: foot.y, "class": "bl-guide" }, layer);
    el("line", { x1: foot.x, y1: foot.y, x2: tipP.x, y2: tipP.y, "class": "bl-guide" }, layer);
    el("line", { x1: C, y1: C, x2: tipP.x, y2: tipP.y, "class": "bl-vector" }, layer);
    el("circle", { cx: tipP.x, cy: tipP.y, r: 6, "class": "bl-tip" }, layer);
  }

  build();
})();
