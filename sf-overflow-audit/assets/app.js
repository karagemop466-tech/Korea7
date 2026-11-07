(function () {
  "use strict";
  document.querySelectorAll("[data-filter-table]").forEach(function (toolbar) {
    var tableId = toolbar.getAttribute("data-filter-table");
    var table = document.getElementById(tableId);
    if (!table || !table.tBodies.length) return;
    var rows = Array.prototype.slice.call(table.tBodies[0].rows);
    var search = toolbar.querySelector(".search-input");
    var select = toolbar.querySelector(".filter-select");
    var counter = toolbar.querySelector(".row-count");

    function update() {
      var q = search ? search.value.trim().toLowerCase() : "";
      var st = select ? select.value.trim().toLowerCase() : "";
      var visible = 0;
      rows.forEach(function (row) {
        var text = row.textContent.toLowerCase();
        var rowStatus = (row.getAttribute("data-status") || "").toLowerCase();
        var matchQ = !q || text.indexOf(q) !== -1;
        var matchS = !st || rowStatus.indexOf(st) !== -1;
        var show = matchQ && matchS;
        row.style.display = show ? "" : "none";
        if (show) visible += 1;
      });
      if (counter) {
        counter.textContent = "Showing " + visible + " of " + rows.length + " rows";
      }
    }

    if (search) search.addEventListener("input", update);
    if (select) select.addEventListener("change", update);
    update();
  });
})();
