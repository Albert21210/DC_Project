"""HTTP-тесты /api/customers."""


def test_list_customers_200(client):
    r = client.get("/api/customers/")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_create_customer_ok(client):
    r = client.post("/api/customers/", json={
        "last_name": "Тестов", "first_name": "Тест",
        "phone": "+79990000000", "email": "test@test.ru"
    })
    assert r.status_code == 200
    assert "customer_id" in r.json()


def test_create_customer_appears_in_list(client):
    client.post("/api/customers/", json={"last_name": "Новый", "first_name": "Клиент"})
    names = [c["LastName"] for c in client.get("/api/customers/").json()]
    assert "Новый" in names
