/* ── Analytics page ── */
async function loadAnalytics() {
  spinner('analytics-content');
  try {
    const [top, rev, emp, summ, catRev] = await Promise.all([
      API.get('/api/analytics/top-products?limit=5'),
      API.get('/api/analytics/monthly-revenue'),
      API.get('/api/analytics/employee-efficiency'),
      API.get('/api/analytics/summary'),
      API.get('/api/analytics/revenue-by-category'),
    ]);

    document.getElementById('analytics-content').innerHTML = `
      <!-- Stat cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-card__value">${rub(rev.revenue)}</div>
          <div class="stat-card__label">Выручка за 30 дней</div>
        </div>
        <div class="stat-card" style="border-color:var(--clr-success)">
          <div class="stat-card__value" style="color:var(--clr-success)">${rev.count}</div>
          <div class="stat-card__label">Оплаченных заказов</div>
        </div>
        <div class="stat-card" style="border-color:var(--clr-warning)">
          <div class="stat-card__value" style="color:var(--clr-warning)">${rub(rev.avg)}</div>
          <div class="stat-card__label">Средний чек</div>
        </div>
        <div class="stat-card" style="border-color:#805ad5">
          <div class="stat-card__value" style="color:#805ad5">${summ.products}</div>
          <div class="stat-card__label">Товаров в каталоге</div>
        </div>
        <div class="stat-card" style="border-color:#dd6b20">
          <div class="stat-card__value" style="color:#dd6b20">${summ.customers}</div>
          <div class="stat-card__label">Клиентов в базе</div>
        </div>
        <div class="stat-card" style="border-color:var(--clr-danger)">
          <div class="stat-card__value" style="color:var(--clr-danger)">${summ.low_stock}</div>
          <div class="stat-card__label">⚠️ Критич. остатки</div>
        </div>
      </div>

      <!-- Top products -->
      <div class="card" style="margin-bottom:20px">
        <div class="card__header"><span class="card__title">🔥 ТОП-5 продаваемых товаров</span></div>
        <div class="tbl-wrap"><table>
          <thead><tr><th>Место</th><th>Товар</th><th>Продано</th><th>Цена</th></tr></thead>
          <tbody>${top.map((r,i) => `<tr>
            <td><strong>${['🥇','🥈','🥉','4️⃣','5️⃣'][i] || i+1}</strong></td>
            <td>${r.ProductName}</td>
            <td>${r.TotalQty} шт.</td>
            <td>${rub(r.Price)}</td>
          </tr>`).join('')}</tbody>
        </table></div>
      </div>

      <!-- Employee efficiency -->
      <div class="card">
        <div class="card__header"><span class="card__title">🏆 Рейтинг сотрудников</span></div>
        <div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Сотрудник</th><th>Должность</th><th>Выручка</th></tr></thead>
          <tbody>${emp.map((r,i) => `<tr>
            <td>${i+1}</td>
            <td>${r.Name}</td>
            <td>${r.Position}</td>
            <td>${rub(r.Revenue)}</td>
          </tr>`).join('')}</tbody>
        </table></div>
      </div>

      <!-- Revenue by category -->
      <div class="card" style="margin-top:20px">
        <div class="card__header"><span class="card__title">📂 Выручка по категориям</span></div>
        <div class="tbl-wrap"><table>
          <thead><tr><th>Категория</th><th>Продано, шт.</th><th>Выручка</th></tr></thead>
          <tbody>${catRev.map(r => `<tr>
            <td>${r.CategoryName}</td>
            <td>${r.TotalQty} шт.</td>
            <td>${rub(r.Revenue)}</td>
          </tr>`).join('')}</tbody>
        </table></div>
      </div>`;
  } catch(e) { toast(e.message, 'error'); }
}
