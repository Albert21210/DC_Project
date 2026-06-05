/* ── Customers page ── */
async function loadCustomers() {
  spinner('customers-table');
  try {
    const data = await API.get('/api/customers/');
    document.getElementById('customers-table').innerHTML = `
      <div class="tbl-wrap"><table>
        <thead><tr><th>#</th><th>Фамилия</th><th>Имя</th><th>Телефон</th><th>Email</th></tr></thead>
        <tbody>${data.map(c => `<tr>
          <td>${c.CustomerID}</td><td>${c.LastName}</td><td>${c.FirstName}</td>
          <td>${c.Phone || '—'}</td><td>${c.Email || '—'}</td>
        </tr>`).join('')}</tbody>
      </table></div>`;
  } catch(e) { toast(e.message, 'error'); }
}

async function submitNewCustomer(e) {
  e.preventDefault();
  const f = e.target;
  try {
    const res = await API.post('/api/customers/', {
      last_name: f.last_name.value, first_name: f.first_name.value,
      phone: f.phone.value, email: f.email.value,
    });
    toast(`Клиент добавлен (ID ${res.customer_id})`);
    closeModal('modal-new-customer');
    f.reset();
    loadCustomers();
  } catch(err) { toast(err.message, 'error'); }
}
