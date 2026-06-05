/* ── App bootstrap ── */
document.addEventListener('DOMContentLoaded', () => {
  // Навигация по sidebar
  document.querySelectorAll('.sidebar__item').forEach(item => {
    item.addEventListener('click', () => {
      const page = item.dataset.page;
      navigate(page);
      const loaders = {
        products:  () => { loadProducts(); initCategoryFilter(); },
        orders:    loadOrders,
        analytics: loadAnalytics,
        customers: loadCustomers,
        employees: loadEmployees,
        reports:   loadReports,
        suppliers: loadSuppliers,
      };
      loaders[page]?.();
    });
  });

  // Закрытие модалов кликом на оверлей
  document.querySelectorAll('.modal-overlay').forEach(ov => {
    ov.addEventListener('click', e => {
      if (e.target === ov) ov.classList.remove('open');
    });
  });

  // Открыть дашборд по умолчанию
  navigate('analytics');
  loadAnalytics();
  updateSidebarStats();
});


async function updateSidebarStats() {
  try {
    const rev = await API.get('/api/analytics/monthly-revenue');
    const el = document.getElementById('sidebar-revenue');
    if (el) el.textContent = rub(rev.revenue);
  } catch(_) {}
}
