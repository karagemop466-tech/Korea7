document.addEventListener('DOMContentLoaded', () => {
  // Copy buttons: <button data-copy-target="#id">Copy</button>
  document.querySelectorAll('[data-copy-target]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const target = document.querySelector(btn.getAttribute('data-copy-target'));
      if (!target) return;
      const text = target.textContent.trim();
      try {
        await navigator.clipboard.writeText(text);
        const old = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(() => { btn.textContent = old; }, 1500);
      } catch (err) {
        window.prompt('Copy this text:', text);
      }
    });
  });
  // Print buttons
  document.querySelectorAll('[data-print]').forEach((btn) => {
    btn.addEventListener('click', () => window.print());
  });
  // Back-to-top
  const top = document.createElement('a');
  top.href = '#main';
  top.className = 'btn btn-ghost btn-sm no-print';
  top.style.cssText = 'position:fixed;right:18px;bottom:18px;z-index:60;box-shadow:0 10px 30px rgba(0,0,0,.35)';
  top.textContent = '↑ Top';
  document.body.appendChild(top);
});
