// Theme preference is the only thing this site stores in your browser.
// Loaded before the stylesheet paints so a stored choice never flashes.
try {
  var t = localStorage.getItem("sq-theme");
  if (t) { document.documentElement.setAttribute("data-theme", t); }
} catch (e) {}
