// Minimal row filter for tables. Each search box has data-target="<table id>".
// Hides rows whose text does not contain the search term. No network calls.
(function () {
  'use strict';
  document.querySelectorAll('input.filter[data-target]').forEach(function (box) {
    var table = document.getElementById(box.getAttribute('data-target'));
    if (!table) { return; }
    box.addEventListener('input', function () {
      var term = box.value.trim().toLowerCase();
      table.querySelectorAll('tbody tr').forEach(function (row) {
        var text = row.textContent.toLowerCase();
        row.style.display = (!term || text.indexOf(term) !== -1) ? '' : 'none';
      });
    });
  });
})();
