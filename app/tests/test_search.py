# tests/test_search.py

def test_search_items(client):

    response = client.get("/feeds/search?q=Test")

    assert response.status_code == 200

    data = response.json()

    assert "query" in data
    assert "count" in data
    assert "results" in data
