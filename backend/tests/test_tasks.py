def test_create_task(client):
    response = client.post("/tasks", json={"title": "Купить хлеб"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Купить хлеб"
    assert data["is_done"] is False

def test_get_missing_task_return_404(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404