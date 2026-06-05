"""HTTP-тесты /api/categories."""


def test_list_categories_200(client):
    r = client.get("/api/categories/")
    assert r.status_code == 200


def test_list_categories_count(client):
    data = client.get("/api/categories/").json()
    assert len(data) == 4


def test_category_has_product_count(client):
    item = client.get("/api/categories/").json()[0]
    assert "ProductCount" in item
    assert item["ProductCount"] >= 0


def test_categories_sorted_by_name(client):
    names = [c["CategoryName"] for c in client.get("/api/categories/").json()]
    assert names == sorted(names)
