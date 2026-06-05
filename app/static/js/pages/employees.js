/* ── Employees page ── */
async function loadEmployees() {
  spinner('employees-table');
  try {
    const data = await API.get('/api/employees/');
    document.getElementById('employees-table').innerHTML = `
      <div class="tbl-wrap"><table>
        <thead><tr><th>#</th><th>Фамилия</th><th>Имя</th><th>Должность</th><th>Принят</th></tr></thead>
        <tbody>${data.map(e => `<tr>
          <td>${e.EmployeeID}</td><td>${e.LastName}</td><td>${e.FirstName}</td>
          <td>${e.Position || '—'}</td><td>${e.HireDate || '—'}</td>
        </tr>`).join('')}</tbody>
      </table></div>`;
  } catch(e) { toast(e.message, 'error'); }
}
