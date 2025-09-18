from app.interfaces.schemas import UserCreate


def test_create_and_list_items_without_authorization(client):
    payload = {"name": "Mouse", "description": "Wireless mouse", "price": 50.0, "tax": 5.0}

    # POST /items
    response = client.post("/items", json=payload)
    assert response.status_code == 401

    # GET /items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 0


def test_create_user(client):
    user = UserCreate(
        email="aa@g.com", password="lkjsaoiwhghb%iog535bajb", full_name="I'm the best user!"
    )
    # POST /auth/register
    response = client.post("/auth/register", json=user.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert "id" in data


def test_login(user_factory, client):
    email = "aa@g.com"
    password = "lkjsaoiwhghb%iog535bajb"
    full_name = "I'm the best user!"
    user = user_factory(email, password, full_name=full_name)
    form_data = {"username": user["email"], "password": password}
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

    # false password
    form_data = {"username": user["email"], "password": "groijnnenbi46"}
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 401


def test_create_and_list_items(user_factory, client):
    email = "aa@g.com"
    password = "lkjsaoiwhghb%iog535bajb"
    full_name = "I'm the best user!"
    user = user_factory(email, password, full_name=full_name)
    form_data = {"username": user["email"], "password": password}
    response = client.post("/auth/login", data=form_data)
    token_data = response.json()
    access_token = token_data["access_token"]

    payload = {"name": "Mouse", "description": "Wireless mouse", "price": 50.0, "tax": 5.0}
    # POST /items
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/items", json=payload)
    assert response.status_code == 401, "post item without any token should fail"

    response = client.post("/items", json=payload, headers=headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Mouse"
    assert "id" in data

    # GET /items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Mouse"

    # item without description
    payload = {"name": "Mouse2", "price": 50.0, "tax": 5.0}
    # POST /items
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/items", json=payload, headers=headers)
    assert response.status_code == 200, "An item without description should be added"
    data = response.json()
    assert data["name"] == "Mouse2"
    assert "id" in data

    # GET /items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2, "An item without description can be read"
    assert items[1]["name"] == "Mouse2"

    # item without description
    payload = {"name": "MouseWithoutPrice", "tax": 5.0}
    # POST /items
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/items", json=payload, headers=headers)
    assert response.status_code == 422, "An item which doesn't have a price, should not be added"

    # item without description
    payload = {"name": "MouseWithoutTax", "price": 50.0}
    # POST /items
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/items", json=payload, headers=headers)
    assert response.status_code == 200, "An item without tax should be added"
    data = response.json()
    assert data["name"] == "MouseWithoutTax"
    assert "id" in data

    # GET /items
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 3, "An item without tax can be read"
    assert items[2]["name"] == "MouseWithoutTax"
