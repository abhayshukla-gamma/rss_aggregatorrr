def test_create_feed(client):
    response = client.post(
        "/feeds/create", json={"title": "Test Feed", "url": "https://example.com/rss"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test Feed"
    assert data["url"] == "https://example.com/rss"


def test_list_feeds(client):
    # Create a feed first (so test is independent)
    client.post(
        "/feeds/create",
        json={"title": "Another Feed", "url": "https://example2.com/rss"},
    )

    response = client.get("/feeds/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
