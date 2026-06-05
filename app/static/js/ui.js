/* ── UI helpers ── */

// Toast уведомления
function toast(msg, type = 'success') {
  const box = document.getElementById('toast-container');
  const el  = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.textContent = msg;
  box.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

// Открыть/закрыть модал
function openModal(id)  { document.getElementById(id).classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

// Отрисовать спиннер
function spinner(containerId) {
  document.getElementById(containerId).innerHTML = '<div class="spinner"></div>';
}

// Форматирование рублей
function rub(v) {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(v);
}

// Статус-бейдж заказа
function statusBadge(s) {
  const map = { 'Оформлен': 'info', 'Оплачен': 'warning', 'Выдан': 'success', 'Отменён': 'danger' };
  return `<span class="badge badge-${map[s] || 'info'}">${s}</span>`;
}

// Навигация
function navigate(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.sidebar__item').forEach(i => i.classList.remove('active'));
  document.getElementById('page-' + pageId)?.classList.add('active');
  document.querySelector(`[data-page="${pageId}"]`)?.classList.add('active');
}
