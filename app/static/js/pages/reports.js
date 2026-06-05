/* ── Reports page ── */
async function loadLowStock() {
  spinner('low-stock-table');
  try {
    const data = await API.get('/api/products/low-stock?threshold=10');
    document.getElementById('low-stock-table').innerHTML = data.length
      ? `<div class="tbl-wrap"><table>
          <thead><tr><th>Товар</th><th>Остаток</th><th>Цена</th></tr></thead>
          <tbody>${data.map(r => `<tr>
            <td>${r.ProductName}</td>
            <td>${stockBadge(r.StockQuantity)}</td>
            <td>${rub(r.Price)}</td>
          </tr>`).join('')}</tbody>
        </table></div>`
      : '<div class="empty-state">✅ Все товары в достаточном количестве</div>';
  } catch(e) { toast(e.message, 'error'); }
}

async function loadOrderSums() {
  spinner('order-sums-table');
  try {
    const data = await API.get('/api/analytics/order-sums');
    document.getElementById('order-sums-table').innerHTML = `
      <div class="tbl-wrap"><table>
        <thead><tr><th>#</th><th>Клиент</th><th>Дата</th><th>Статус</th><th>Сумма чека</th></tr></thead>
        <tbody>${data.map(r => `<tr>
          <td>${r.OrderID}</td><td>${r.Customer}</td>
          <td>${r.OrderDate}</td><td>${statusBadge(r.OrderStatus)}</td>
          <td><strong>${rub(r.Total)}</strong></td>
        </tr>`).join('')}</tbody>
      </table></div>`;
  } catch(e) { toast(e.message, 'error'); }
}

async function loadReports() {
  await Promise.all([loadLowStock(), loadOrderSums()]);
}
