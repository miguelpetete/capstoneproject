def test_login(client):
    response = client.get("/sign-in")
    assert response.status_code == 200


"""
def test_admin_create(client):
    response = client.get("/createoffer")
    assert response.status_code == 200


def test_admin_delete(client):
    response = client.get("/deleteoffer/1")
    assert response.status_code == 200
"""
