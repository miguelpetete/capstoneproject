def test_home(client):
    response = client.get("/home")
    assert response.status_code == 200