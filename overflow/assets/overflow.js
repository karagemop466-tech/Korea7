/* Minimal table filter for the bathtub overflow project pages. */
(function () {
  function applyFilter(input) {
    var targetSel = input.getAttribute("data-table");
    var table = document.querySelector(targetSel);
    if (!table) return;
    var q = input.value.trim().toLowerCase();
    var rows = table.querySelectorAll("tbody tr");
    rows.forEach(function (row) {
      var show = !q || row.textContent.toLowerCase().indexOf(q) !== -1;
      row.style.display = show ? "" : "none";
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var inputs = document.querySelectorAll("input[data-table]");
    inputs.forEach(function (input) {
      input.addEventListener("input", function () { applyFilter(input); });
    });
  });
})();
