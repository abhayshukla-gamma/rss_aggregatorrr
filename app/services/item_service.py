from sqlalchemy.orm import Session
from app.models.item import Item 
from app.services.rss_service import fetch_feed
from psycopg2 import errors

# def save_feed_items(feed_id : int,feed_url : str, db : Session) :

#     rss_items = fetch_feed(feed_url)
#     result = []

#     for item in rss_items :
#         old_item = db.query(Item).filter(Item.link == item["link"]).first() # first means limit 1

#         if old_item :
#          continue

#         new_item = Item(
#             feed_id = feed_id,
#             title=item["title"],
#             link=item["link"],
#             published=item.get("published")

#         )
#         # print(new_item) 
#         try:
#             db.add(new_item)
#             db.flush()
#         except errors.UniqueViolation:
#            print("already present")
#            continue
#         except Exception as e:
#            print(e)
#         result.append(new_item)


#     db.commit()
#     return result\

from sqlalchemy.exc import IntegrityError

def save_feed_items(feed_id: int, feed_url: str, db: Session):
    rss_items = fetch_feed(feed_url)
    result = []

    for item in rss_items:
                                                       
        with db.begin_nested():
           try:
                new_item = Item(
                    feed_id=feed_id,
                    title=item["title"],
                     link=item["link"],
                    published=item.get("published")
                )
                db.add(new_item)
                                                        
                db.flush()
                result.append(new_item)
           except IntegrityError:
                                                         
                print(f"Skipping duplicate URL: {item['link']}")
                continue 

                                                                              
    db.commit()
    return result   