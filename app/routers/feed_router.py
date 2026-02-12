from fastapi import APIRouter ,Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.feed_schema import FeedCreate  # class import for validation from table's pydantic class 
from app.models.feed import Feed   # ja class ka router usko import 
from app.services.rss_service import fetch_feed
from app.services.item_service import save_feed_items
from app.models.item import Item
from sqlalchemy import func
router = APIRouter(prefix="/feeds",tags=["feeds"])

@router.post("/create")
def create_feed(feed : FeedCreate, db: Session=Depends(get_db)):
    existing = db.query(Feed).filter(Feed.url == str(feed.url)).first()

    if existing:
        raise HTTPException(status_code=400,detail="feild already exists")
    
    new_feed = Feed(
    title=feed.title,
    url=str(feed.url)
    )       

    db.add(new_feed)
    db.commit()
    db.refresh(new_feed)

    return new_feed

@router.get("/")
def list_feeds(db: Session  = Depends(get_db)):
    return db.query(Feed).all()

# @router.get("/{feed_id}/items")
# def get_feed_items(feed_id :int,limit :int =10, db:Session=Depends(get_db)):
#     feed =db.query(Feed).filter(Feed.id==(feed_id)).first()
#     if not feed:
#         raise HTTPException(status_code=404, detail="file not found ")

#     items = db.query(Item).filter(Item.feed_id == feed.id).all()


#     return {
#         "feed_title" : feed.title,
#         "total_item": len(items),
#         "items": items[:limit]
#     }

@router.post("/{feed_id}/")
def fetch_and_save_items(feed_id : int, db :Session=Depends(get_db)):
    # print(type(feed_id),feed_id)
    feed = db.query(Feed).filter(Feed.id == (feed_id)).first()
    # print(feed.id,feed.url)
    if not feed:
        raise HTTPException(status_code=404,detail="file  not founf")
    #feed_id : int,feed_url : str, db : Session)
    items = save_feed_items(feed.id, feed.url, db)
    print(items)
    return {
        "feed_id": feed.id,
        "saved_items": len(items)
    }

@router.get("/{feed_id}/items/db")
def get_items_from_db(feed_id: int, db: Session = Depends(get_db)):

    items = db.query(Item).filter(Item.feed_id == feed_id).all()

    return {
        "feed_id": feed_id,
        "total_items": len(items),
        "items": items
    }

@router.patch("/{item_id}/read")
def mark_item_read(item_id : int,db :Session=Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()

    if not item :
        raise HTTPException(status_code=404,detail="file not found")
    

    item.is_read = True

  
    db.commit()
    db.refresh(item)
    return {
        "message" : "item marked as read",
        "item_id" : item.id
    }

@router.get("/{feed_id}/unread")
def get_unread_items(feed_id : int, db : Session=Depends (get_db)) :

    feed = db.query(Feed).filter(Feed.id == feed_id).first()

    if not feed :
        raise HTTPException(status_code=404,detail="article not found")

    unread_items = db.query(Item).filter(Item.feed_id== feed_id,Item.is_read==False).all()


    return {
        "feed_title": feed.title,
        "unread_count": len(unread_items),
        "items": unread_items
    }

@router.get("/search")
def search_items(q: str, db: Session = Depends(get_db)):

    results = db.query(Item).filter(
        func.to_tsvector('english', Item.title).match(q)
    ).all()

    return {
        "query": q,
        "count": len(results),
        "results": results
    }