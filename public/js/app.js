// Enterprise Digital Banking UI Interactions & Data Binding
document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Handler
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      themeToggle.checked = true;
    }
    themeToggle.addEventListener('change', (e) => {
      const mode = e.target.checked ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', mode);
      localStorage.setItem('theme', mode);
    });
  }

  // Currency & Date Formatter
  window.formatCurrency = (num) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(num || 0);
  };

  // Toast / Banner notification
  window.showNotice = (msg, isError = false) => {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;display:flex;flex-direction:column;gap:10px;';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.style.cssText = `padding:12px 20px;border-radius:8px;font-weight:500;box-shadow:0 4px 12px rgba(0,0,0,0.15);color:#fff;background:${isError ? '#dc2626' : '#16a34a'};animation:fadeIn 0.3s ease;`;
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 4000);
  };
});
