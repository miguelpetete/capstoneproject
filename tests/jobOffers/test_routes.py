def test_view_job(client):
    response = client.get("/offer/1")
    assert response.status_code == 200
