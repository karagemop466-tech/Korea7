/* Progressive enhancement for the static dashboard: accessible per-table filtering.
   All rows are present in HTML; no runtime data fetch is required. */
(function () {
  "use strict";

  function addFilter(table, wrap) {
    var body = table.tBodies[0];
    if (!body) return;
    var rows = Array.prototype.slice.call(body.rows);
    var section = table.closest(".section");
    var heading = section ? section.querySelector("h2") : null;
    var name = heading ? heading.textContent.trim() : "table";

    var row = document.createElement("div");
    row.className = "filter-row";
    var input = document.createElement("input");
    input.type = "search";
    input.setAttribute("aria-label", "Filter rows in " + name);
    input.placeholder = "Filter rows…";
    var count = document.createElement("span");
    count.className = "filter-count";
    count.setAttribute("role", "status");
    count.setAttribute("aria-live", "polite");
    row.appendChild(input);
    row.appendChild(count);
    wrap.parentNode.insertBefore(row, wrap);

    function update() {
      var q = input.value.trim().toLowerCase();
      var visible = 0;
      rows.forEach(function (tr) {
        var show = q === "" || tr.textContent.toLowerCase().indexOf(q) !== -1;
        tr.hidden = !show;
        if (show) visible += 1;
      });
      count.textContent = visible + " of " + rows.length + " rows";
    }
    input.addEventListener("input", update);
    update();
  }

  document.querySelectorAll("table.data-table").forEach(function (table) {
    var wrap = table.closest(".table-wrap");
    if (wrap && table.tBodies[0] && table.tBodies[0].rows.length > 4) {
      addFilter(table, wrap);
    }
  });

  document.querySelectorAll('a[href^="http"]').forEach(function (a) {
    if (a.hostname !== window.location.hostname) {
      a.setAttribute("target", "_blank");
      a.setAttribute("rel", "noopener noreferrer");
    }
  });
})();
