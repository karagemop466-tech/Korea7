/* Progressive enhancement for the static dashboard: per-table filtering.
   No data is loaded at runtime; all tables are present in the HTML. */
(function () {
  "use strict";

  function addFilter(table, wrap) {
    var row = document.createElement("div");
    row.className = "filter-row";
    var input = document.createElement("input");
    input.type = "search";
    input.setAttribute("aria-label", "Filter table rows");
    input.placeholder = "Filter rows…";
    row.appendChild(input);
    wrap.parentNode.insertBefore(row, wrap);
    var body = table.querySelector("tbody");
    if (!body) return;
    var rows = Array.prototype.slice.call(body.querySelectorAll("tr"));
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      rows.forEach(function (tr) {
        tr.hidden = q !== "" && tr.textContent.toLowerCase().indexOf(q) === -1;
      });
    });
  }

  document.querySelectorAll("table.data-table").forEach(function (table) {
    var wrap = table.closest(".table-wrap");
    if (wrap && table.tBodies[0] && table.tBodies[0].rows.length > 4) {
      addFilter(table, wrap);
    }
  });

  /* Open external sources in a safe new tab (defensive; links already carry rel). */
  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.hostname !== window.location.hostname) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    }
  });
})();
