# # tests/test_items.py

# from app.models.feed import Feed
# from app.models.item import Item
# from app.core.database import get_db, sessionLocal
# from app.tests.conftest import TestingSessionLocal

# def test_mark_item_read(client):

#     # First create feed
#     feed_response = client.post(
#         "/feeds/create",
#         json={
#             "title": "Item Feed",
#             "url": "https://example2.com/rss"
#         }
#     )

#     feed_id = feed_response.json()["id"]

#     # Manually insert item
#     # from app.core.database import SessionLocal
#     db = TestingSessionLocal()

#     item = Item(
#         feed_id=feed_id,
#         title="Test Item",
#         link="https://example.com/item",
#         is_read=False
#     )

#     db.add(item)
#     db.commit()
#     db.refresh(item)

#     db.close()

#     # Mark as read
#     response = client.patch(f"/feeds/{item.id}/read")

#     assert response.status_code == 200
#     assert response.json()["message"] == "item marked as read"


# def test_get_unread_items(client):

#     response = client.get("/feeds/1/unread")

#     assert response.status_code in [200, 404]
