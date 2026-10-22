/* Surface-code overhead: physical qubits per logical qubit.
 *
 * One formula, stated on the page: p_L = A (p / p_th)^((d + 1) / 2), with the
 * constants A and p_th taken from the model chosen on the page, and 2 d^2 - 1
 * physical qubits for a rotated patch. It needs no data and nothing leaves
 * the page.
 */
(function () {
  "use strict";

  var A = 0.03;
  var pTh = 0.0057;
  var MAX_D = 201;

  var pIn = document.getElementById("oh-p");
  var targetIn = document.getElementById("oh-target");
  var thIn = document.getElementById("oh-th");
  var pOut = document.getElementById("oh-p-out");
  var result = document.getElementById("oh-result");
  var rows = document.getElementById("oh-rows");
  if (!pIn || !targetIn || !thIn || !result || !rows) { return; }

  var SUP = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
              "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
              "-": "⁻" };

  function sci(x) {
    if (x === 0) { return "0"; }
    var parts = x.toExponential(1).split("e");
    var exp = String(parseInt(parts[1], 10)).split("").map(function (c) { return SUP[c]; }).join("");
    return parts[0] + " × 10" + exp;
  }

  function logicalRate(p, d) { return A * Math.pow(p / pTh, (d + 1) / 2); }
  function qubits(d) { return 2 * d * d - 1; }

  function distanceFor(p, target) {
    for (var d = 3; d <= MAX_D; d += 2) {
      if (logicalRate(p, d) <= target) { return d; }
    }
    return null;
  }

  function line(text, strong) {
    var p = document.createElement("p");
    if (strong) {
      var s = document.createElement("strong");
      s.textContent = strong;
      p.appendChild(s);
    }
    p.appendChild(document.createTextNode(text));
    return p;
  }

  function update() {
    var p = Math.pow(10, parseFloat(pIn.value));
    var target = parseFloat(targetIn.value);
    var model = thIn.options[thIn.selectedIndex];
    A = parseFloat(model.getAttribute("data-a"));
    pTh = parseFloat(model.getAttribute("data-pth"));
    pOut.textContent = (p * 100).toPrecision(2) + "%";

    result.innerHTML = "";
    rows.innerHTML = "";

    if (p >= pTh) {
      result.appendChild(line(
        " At or above the threshold, a larger code makes the logical error rate worse, so no distance reaches the target.",
        "Above threshold."));
      return;
    }

    var d = distanceFor(p, target);
    if (d === null) {
      result.appendChild(line(
        " The target needs a code distance above " + MAX_D + ".",
        "Out of range."));
    } else {
      result.appendChild(line(
        " Code distance " + d + ", about " + qubits(d).toLocaleString("en-US") +
        " physical qubits for one logical qubit, at a logical error rate of " +
        sci(logicalRate(p, d)) + " per round.",
        "Estimate."));
    }

    [3, 5, 7, 11, 15, 25].forEach(function (dist) {
      var tr = document.createElement("tr");
      [String(dist), qubits(dist).toLocaleString("en-US"), sci(logicalRate(p, dist))]
        .forEach(function (cell) {
          var td = document.createElement("td");
          td.textContent = cell;
          tr.appendChild(td);
        });
      rows.appendChild(tr);
    });
  }

  pIn.addEventListener("input", update);
  targetIn.addEventListener("change", update);
  thIn.addEventListener("change", update);
  update();
})();
