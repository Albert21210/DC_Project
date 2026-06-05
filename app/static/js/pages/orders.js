/* ── Orders page ── */
let cart = {};

async function loadOrders() {
  spinner('orders-table');
  try {
    const data = await API.get('/api/orders/');
    renderOrdersTable(data);
  } catch(e) { 
    toast(e.message, 'error'); 
  }
}

function renderOrdersTable(data) {
  document.getElementById('orders-table').innerHTML = `
      <div class="tbl-wrap"><table>
        <thead><tr><th>#</th><th>Клиент</th><th>Менеджер</th>
          <th>Дата</th><th>Статус</th><th>Сумма</th><th></th></tr></thead>
        <tbody>${data.map(o => `<tr>
          <td style='cursor:pointer;color:var(--clr-primary);font-weight:600;text-decoration:underline' onclick='showOrderDetail(${o.OrderID})'>${o.OrderID}</td>
          <td>${o.Customer}</td>
          <td>${o.Employee || '—'}</td>
          <td>${o.OrderDate}</td>
          <td>${statusBadge(o.OrderStatus)}</td>
          <td>${rub(o.Total)}</td>
          <td>${o.OrderStatus === 'Оформлен'
            ? `<button class="btn btn-success btn-sm" onclick="payOrder(${o.OrderID})">💳 Оплатить</button>`
            : ''}</td>
        </tr>`).join('')}</tbody>
      </table></div>`;
}

async function payOrder(id) {
  if (!confirm(`Провести оплату заказа №${id}?`)) return;
  try {
    await API.post(`/api/orders/${id}/pay`);
    toast(`Заказ №${id} оплачен!`);
    loadOrders();
  } catch(e) { toast(e.message, 'error'); }
}

async function openNewOrderModal() {
  cart = {};
  renderCart();
  const [customers, employees, products] = await Promise.all([
    API.get('/api/customers/'),
    API.get('/api/employees/'),
    API.get('/api/products/available'),
  ]);
  const sel = (id, items, val) => {
    document.getElementById(id).innerHTML =
      items.map(i => `<option value="${i[val]}">${i.LastName} ${i.FirstName}</option>`).join('');
  };
  sel('order-customer', customers, 'CustomerID');
  sel('order-employee', employees, 'EmployeeID');
  const pSel = document.getElementById('order-product');
  pSel.innerHTML = products.map(p =>
    `<option value="${p.ProductID}" data-price="${p.Price}" data-stock="${p.StockQuantity}">${p.ProductName} — ${rub(p.Price)} (${p.StockQuantity} шт.)</option>`
  ).join('');
  openModal('modal-new-order');
}

function addToCart() {
  const sel   = document.getElementById('order-product');
  const opt   = sel.selectedOptions[0];
  const pid   = +sel.value;
  const qty   = +document.getElementById('order-qty').value;
  const price = +opt.dataset.price;
  const stock = +opt.dataset.stock;
  const name  = opt.text.split('—')[0].trim();
  if (!pid || qty < 1) return toast('Укажите товар и количество', 'error');
  const inCart = (cart[pid]?.qty || 0);
  if (inCart + qty > stock) return toast(`Доступно только ${stock} шт.`, 'error');
  cart[pid] = { qty: (cart[pid]?.qty || 0) + qty, price, name };
  renderCart();
}

function removeFromCart(pid) { delete cart[pid]; renderCart(); }

function renderCart() {
  const keys = Object.keys(cart);
  const total = keys.reduce((s, k) => s + cart[k].qty * cart[k].price, 0);
  document.getElementById('cart-body').innerHTML = keys.length
    ? keys.map(k => `<tr>
        <td>${cart[k].name}</td>
        <td>${cart[k].qty}</td>
        <td>${rub(cart[k].price)}</td>
        <td>${rub(cart[k].qty * cart[k].price)}</td>
        <td><button class="btn btn-danger btn-sm" onclick="removeFromCart(${k})">✕</button></td>
      </tr>`).join('')
    : '<tr><td colspan="5" class="empty-state">Корзина пуста</td></tr>';
  document.getElementById('cart-total').textContent = rub(total);
}

async function submitNewOrder() {
  if (!Object.keys(cart).length) return toast('Корзина пуста', 'error');
  const cid = +document.getElementById('order-customer').value;
  const eid = +document.getElementById('order-employee').value;
  try {
    const res = await API.post('/api/orders/', { customer_id: cid, employee_id: eid, cart });
    toast(`Заказ №${res.order_id} оформлен!`);
    closeModal('modal-new-order');
    loadOrders();
  } catch(e) { toast(e.message, 'error'); }
}

async function showOrderDetail(orderId) {
  try {
    const data = await API.get(`/api/orders/${orderId}`);
    const o = data.order;
    const lines = data.details;
    const total = lines.reduce((s, l) => s + l.Quantity * l.UnitPrice, 0);
    document.getElementById('order-detail-content').innerHTML = `
      <p><strong>Заказ №${o.OrderID}</strong> — ${statusBadge(o.OrderStatus)}</p>
      <p style="margin:6px 0;color:var(--clr-muted)">Клиент: ${o.Customer} | Дата: ${o.OrderDate}</p>
      <table style="width:100%;margin-top:12px;font-size:.85rem">
        <thead><tr><th>Товар</th><th>Кол-во</th><th>Цена</th><th>Сумма</th></tr></thead>
        <tbody>
          ${lines.map(l => `<tr>
            <td>${l.ProductName}</td>
            <td>${l.Quantity}</td>
            <td>${rub(l.UnitPrice)}</td>
            <td>${rub(l.Quantity * l.UnitPrice)}</td>
          </tr>`).join('')}
        </tbody>
      </table>
      <div style="text-align:right;font-weight:700;margin-top:10px">Итого: ${rub(total)}</div>
      ${o.OrderStatus === 'Оформлен' ? `
        <div style="display:flex;gap:8px;margin-top:14px">
          <button class="btn btn-success" style="flex:1"
            onclick="payOrder(${o.OrderID});closeModal('modal-order-detail')">
            💳 Подтвердить оплату</button>
          <button class="btn btn-danger" style="flex:1"
            onclick="cancelOrder(${o.OrderID})">
            ❌ Отменить заказ</button>
        </div>` : ''}`;
    openModal('modal-order-detail');
  } catch(e) { toast(e.message, 'error'); }
}

async function filterOrders(btn, status) {
  document.querySelectorAll('.order-filter').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  spinner('orders-table');
  try {
    const url = status ? `/api/orders/?status=${encodeURIComponent(status)}` : '/api/orders/';
    const data = await API.get(url);
    renderOrdersTable(data);
  } catch(e) { toast(e.message, 'error'); }
}

async function cancelOrder(orderId) {
  if (!confirm(`Отменить заказ №${orderId}?`)) return;
  try {
    await API.post(`/api/orders/${orderId}/cancel`);
    toast(`Заказ №${orderId} отменён`);
    closeModal('modal-order-detail');
    loadOrders();
    updateSidebarStats();
  } catch(e) { toast(e.message, 'error'); }
}