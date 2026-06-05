/* ── Suppliers page ── */
async function loadSuppliers() {
  spinner('suppliers-table');
  try {
    const data = await API.get('/api/suppliers/');
    document.getElementById('suppliers-table').innerHTML = `
      <div class="tbl-wrap"><table>
        <thead><tr>
          <th>#</th><th>Наименование</th><th>Телефон</th><th>Email</th>
        </tr></thead>
        <tbody>${data.map(s => `<tr>
          <td>${s.SupplierID}</td>
          <td><strong>${s.SupplierName}</strong></td>
          <td>${s.ContactPhone || '—'}</td>
          <td>${s.Email || '—'}</td>
        </tr>`).join('')}</tbody>
      </table></div>`;
  } catch(e) { toast(e.message, 'error'); }
}
