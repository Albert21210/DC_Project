/* ── API helper ── */
const API = {
  async _req(method, url, body) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body !== undefined) opts.body = JSON.stringify(body);
    const res = await fetch(url, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'Ошибка сервера');
    }
    return res.json();
  },
  get:    (url)        => API._req('GET',  url),
  post:   (url, body)  => API._req('POST', url, body),
  patch:  (url, body)  => API._req('PATCH',url, body),
};
