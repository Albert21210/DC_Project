"""HTTP-тесты /api/suppliers."""


def test_list_suppliers_200(client):
    r = client.get("/api/suppliers/")
    assert r.status_code == 200


def test_list_suppliers_count(client):
    assert len(client.get("/api/suppliers/").json()) == 2


def test_supplier_has_fields(client):
    item = client.get("/api/suppliers/").json()[0]
    for f in ("SupplierID", "SupplierName"):
        assert f in item
