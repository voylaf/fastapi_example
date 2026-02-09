def test_login(auth_token, client):
    assert "access_token" in auth_token
    assert auth_token["token_type"] == "bearer"


def test_false_password(auth_token, client):
    _ = auth_token
    form_data = {"username": "aa@g.com", "password": "groijnnenbi46"}
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 401


def test_create_item_requires_auth(client):
    payload = {"name": "Mouse", "price": 50.0, "tax": 5.0}
    response = client.post("/items", json=payload)
    assert response.status_code == 401


def test_create_item_success(client, auth_headers):
    payload = {"name": "Mouse", "description": "Wireless", "price": 50.0, "tax": 5.0}
    response = client.post("/items", json=payload, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mouse"
    assert "id" in data


def test_create_item_without_description(client, auth_headers):
    payload = {"name": "Mouse2", "price": 50.0, "tax": 5.0}
    response = client.post("/items", json=payload, headers=auth_headers)

    assert response.status_code == 200


def test_create_item_without_price_fails(client, auth_headers):
    payload = {"name": "NoPrice", "tax": 5.0}
    response = client.post("/items", json=payload, headers=auth_headers)

    assert response.status_code == 422


def test_create_item_without_tax(client, auth_headers):
    payload = {"name": "NoTax", "price": 50.0}
    response = client.post("/items", json=payload, headers=auth_headers)

    assert response.status_code == 200


def test_list_items_returns_created_items(client, auth_headers):
    payloads = [
        {"name": "Mouse", "price": 50.0},
        {"name": "Keyboard", "price": 100.0},
    ]

    for p in payloads:
        client.post("/items", json=p, headers=auth_headers)

    response = client.get("/items")
    items = response.json()

    assert len(items) == 2
    assert {i["name"] for i in items} == {"Mouse", "Keyboard"}
