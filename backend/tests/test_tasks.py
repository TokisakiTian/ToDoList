from datetime import date, timedelta


def test_create_task(client):
    response = client.post("/tasks", json={"title": "Купить хлеб"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Купить хлеб"
    assert data["is_done"] is False

def test_get_missing_task_return_404(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_complete_one_time_task(client):
    created = client.post("/tasks", json={"title": "test"})
    task_id = created.json()["id"]

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200, response.json
    assert response.json()["is_done"] is True

    assert client.get(f"/tasks/{task_id}").json()["is_done"] is True

def test_complete_daily_task(client):
    created = client.post("/tasks", json={"title": "test", "is_daily": True})
    task_id = created.json()["id"]
    assert created.json()["is_done"] is False

    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200, response.json
    assert response.json()["is_done"] is True

    reread = client.get(f"/tasks/{task_id}")
    assert reread.json()["is_done"] is True

def test_delete_task(client):
    created = client.post("/tasks", json={"title": "test"})
    task_id = created.json()["id"]
    other = client.post("/tasks", json={"title": "other"}).json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    assert client.get(f"/tasks/{task_id}").status_code == 404
    assert client.get(f"/tasks/{other}").status_code == 200
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_validation_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_overdue_filter(client):
    today = date.today()
    yesterday = (today - timedelta(days=1)).isoformat()
    tomorrow = (today + timedelta(days=1)).isoformat()

    client.post("/tasks", json={"title": "old", "due_date": yesterday})
    client.post("/tasks", json={"title": "future", "due_date": tomorrow})
    client.post("/tasks", json={"title": "today", "due_date": today.isoformat()})
    client.post("/tasks", json={"title": "no_due"})
    client.post("/tasks", json={"title": "old_done", "due_date": yesterday, "is_done": True})

    response = client.get("/tasks?overdue=true")
    titles = {t["title"] for t in response.json()}
    assert titles == {"old"}

