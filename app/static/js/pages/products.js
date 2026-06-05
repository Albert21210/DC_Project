/* ── Products page ── */
async function loadProducts() {
  spinner('products-table');
  try {
    const data = await API.get('/api/products/');
    const html = `
      <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th>#</th>
          <th onclick="sortProducts('ProductName')" style='cursor:pointer'>Наименование ↕</th>
          <th>Категория</th>
          <th onclick="sortProducts('Price')" style='cursor:pointer'>Цена ↕</th>
          <th onclick="sortProducts('StockQuantity')" style='cursor:pointer'>Остаток ↕</th>
          <th>Гарантия</th><th>Поставщик</th>
        </tr></thead>
        <tbody>
          ${data.map(p => `<tr>
            <td>${p.ProductID}</td>
            <td><strong>${p.ProductName}</strong></td>
            <td>${p.CategoryName || '—'}</td>
            <td>${rub(p.Price)}</td>
            <td>${stockBadge(p.StockQuantity)}</td>
            <td>${p.WarrantyMonths} мес.</td>
            <td>${p.SupplierName || '—'}</td>
          </tr>`).join('')}
        </tbody>
      </table></div>`;
    document.getElementById('products-table').innerHTML = html;
  } catch(e) { toast(e.message, 'error'); }
}

function stockBadge(qty) {
  if (qty === 0)  return `<span class="badge badge-danger">${qty} шт.</span>`;
  if (qty < 5)    return `<span class="badge badge-warning">${qty} шт.</span>`;
  if (qty < 10)   return `<span class="badge badge-info">${qty} шт.</span>`;
  return `<span class="badge badge-success">${qty} шт.</span>`;
}

async function submitRestock(e) {
  e.preventDefault();
  const pid = +document.getElementById('restock-pid').value;
  const qty = +document.getElementById('restock-qty').value;
  try {
    await API.post('/api/products/restock', { product_id: pid, quantity: qty });
    toast('Склад пополнен!');
    closeModal('modal-restock');
    loadProducts();
  } catch(err) { toast(err.message, 'error'); }
}

async function openRestockModal() {
  const prods = await API.get('/api/products/');
  const sel = document.getElementById('restock-pid');
  sel.innerHTML = prods.map(p =>
    `<option value="${p.ProductID}">${p.ProductName} (${p.StockQuantity} шт.)</option>`
  ).join('');
  openModal('modal-restock');
}


let searchTimer = null;
function searchProducts(q) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    if (!q.trim()) { loadProducts(); return; }
    spinner('products-table');
    try {
      const data = await API.get(`/api/products/search?q=${encodeURIComponent(q)}`);
      renderProductTable(data);
    } catch(e) { toast(e.message, 'error'); }
  }, 300);
}

function renderProductTable(data) {
  document.getElementById('products-table').innerHTML = `
    <div class="tbl-wrap"><table>
      <thead><tr><th>#</th><th>Наименование</th><th>Категория</th>
        <th>Цена</th><th>Остаток</th><th>Гарантия</th><th>Поставщик</th></tr></thead>
      <tbody>${data.map(p => `<tr>
        <td>${p.ProductID}</td>
        <td><strong>${p.ProductName}</strong></td>
        <td>${p.CategoryName || '—'}</td>
        <td>${rub(p.Price)}</td>
        <td>${stockBadge(p.StockQuantity)}</td>
        <td>${p.WarrantyMonths ? p.WarrantyMonths+' мес.' : '—'}</td>
        <td>${p.SupplierName || '—'}</td>
      </tr>`).join('')}</tbody>
    </table></div>`;
}


let _productsData = [];
let _sortCol = '', _sortDir = 1;

async function loadProducts() {
  spinner('products-table');
  try {
    _productsData = await API.get('/api/products/');
    renderProductTable(_productsData);
  } catch(e) { toast(e.message, 'error'); }
}

function sortProducts(col) {
  if (_sortCol === col) _sortDir *= -1;
  else { _sortCol = col; _sortDir = 1; }
  const sorted = [..._productsData].sort((a,b) =>
    a[col] > b[col] ? _sortDir : a[col] < b[col] ? -_sortDir : 0
  );
  renderProductTable(sorted);
}


async function initCategoryFilter() {
  try {
    const cats = await API.get('/api/categories/');
    const sel = document.getElementById('category-filter');
    if (!sel) return;
    cats.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c.CategoryID;
      opt.textContent = `${c.CategoryName} (${c.ProductCount})`;
      sel.appendChild(opt);
    });
  } catch(_) {}
}

async function filterByCategory(categoryId) {
  spinner('products-table');
  try {
    const url = categoryId
      ? `/api/products/by-category/${categoryId}`
      : '/api/products/';
    _productsData = await API.get(url);
    renderProductTable(_productsData);
  } catch(e) { toast(e.message, 'error'); }
}
