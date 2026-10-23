/* A Bell pair: two qubits measured at angles the reader chooses.
 *
 * For the state (|00> + |11>)/sqrt(2), measuring both qubits along axes in the
 * same plane at angles a and b gives results that agree with probability
 * cos^2((a - b) / 2). The page draws pairs from that prediction and tallies
 * them. It shows what the numbers are; it cannot show that no local hidden
 * variable could produce them. Only experiments with real entangled particles
 * can do that. Nothing leaves the page and nothing is stored.
 */
(function () {
  "use strict";

  var root = document.getElementById("bell");
  if (!root) { return; }

  var SHOTS = 2000;

  root.innerHTML =
    '<div class="pg-controls dr-controls">' +
    '<label class="pg-field" for="bl-a">Alice measures at <output id="bl-a-out"></output><input id="bl-a" type="range" min="0" max="180" step="5" value="0"></label>' +
    '<label class="pg-field" for="bl-b">Bob measures at <output id="bl-b-out"></output><input id="bl-b" type="range" min="0" max="180" step="5" value="45"></label>' +
    '</div>' +
    '<div class="pg-controls">' +
    '<button type="button" class="tool" id="bell-run">Measure 2,000 pairs</button>' +
    '<button type="button" class="tool" id="bell-chsh">Run the four-setting test</button>' +
    '</div>' +
    '<div class="calc-result" id="bell-out" aria-live="polite"></div>';

  var a = document.getElementById("bl-a");
  var b = document.getElementById("bl-b");
  var out = document.getElementById("bell-out");

  function rad(deg) { return deg * Math.PI / 180; }

  // One pair: Alice's result is a fair coin; Bob's agrees with it with the
  // probability the quantum state predicts for the two angles.
  function pair(angleA, angleB) {
    var ra = Math.random() < 0.5 ? 1 : -1;
    var same = Math.random() < Math.pow(Math.cos((rad(angleA) - rad(angleB)) / 2), 2);
    return [ra, same ? ra : -ra];
  }

  function run(angleA, angleB, n) {
    var tally = { pp: 0, pm: 0, mp: 0, mm: 0, bobPlus: 0 };
    for (var i = 0; i < n; i++) {
      var r = pair(angleA, angleB);
      if (r[0] === 1 && r[1] === 1) { tally.pp++; }
      else if (r[0] === 1) { tally.pm++; }
      else if (r[1] === 1) { tally.mp++; }
      else { tally.mm++; }
      if (r[1] === 1) { tally.bobPlus++; }
    }
    tally.n = n;
    tally.e = (tally.pp + tally.mm - tally.pm - tally.mp) / n;
    return tally;
  }

  function show() {
    document.getElementById("bl-a-out").textContent = a.value + "°";
    document.getElementById("bl-b-out").textContent = b.value + "°";
  }

  function pct(x, n) { return (100 * x / n).toFixed(1) + "%"; }

  function measure() {
    var aa = parseInt(a.value, 10); var bb = parseInt(b.value, 10);
    var t = run(aa, bb, SHOTS);
    var predicted = Math.cos(rad(aa - bb));
    out.textContent = "";
    var s = document.createElement("strong");
    s.textContent = SHOTS.toLocaleString("en-US") + " pairs. ";
    out.appendChild(s);
    out.appendChild(document.createTextNode(
      "Alice and Bob agreed in " + pct(t.pp + t.mm, t.n) + " of them (+ + " + pct(t.pp, t.n) +
      ", − − " + pct(t.mm, t.n) + ", disagreed " + pct(t.pm + t.mp, t.n) + "). " +
      "The correlation is " + t.e.toFixed(2) + "; the prediction is " + predicted.toFixed(2) + ". " +
      "Bob alone got + in " + pct(t.bobPlus, t.n) + " of them, about half, whatever Alice's angle: " +
      "Bob's results on their own say nothing about what Alice chose."));
  }

  function chsh() {
    var as = [0, 90]; var bs = [45, 135];
    var e = [];
    as.forEach(function (x) { bs.forEach(function (y) { e.push(run(x, y, SHOTS).e); }); });
    // S = E(a,b) - E(a,b') + E(a',b) + E(a',b')
    var S = e[0] - e[1] + e[2] + e[3];
    out.textContent = "";
    var s = document.createElement("strong");
    s.textContent = "Four-setting test (CHSH). ";
    out.appendChild(s);
    out.appendChild(document.createTextNode(
      "Alice uses 0° and 90°, Bob uses 45° and 135°, " + SHOTS.toLocaleString("en-US") +
      " pairs per combination. S = " + S.toFixed(2) + ". Any theory in which each particle carries pre-set answers " +
      "cannot give an S above 2. The quantum prediction is 2.83. This page draws its pairs from that prediction, " +
      "so it only shows the number; real experiments with entangled particles are what rule the pre-set answers out."));
  }

  [a, b].forEach(function (el) { el.addEventListener("input", show); });
  document.getElementById("bell-run").addEventListener("click", measure);
  document.getElementById("bell-chsh").addEventListener("click", chsh);
  show();
  measure();
})();
