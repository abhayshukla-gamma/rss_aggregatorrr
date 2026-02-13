from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session 
from fastapi.templating import Jinja2Templates
from app.core.database import get_db
from app.models.feed import Feed
from app.models.item import Item

router = APIRouter(tags=["UI"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request : Request):
    return templates.TemplateResponse("home.html", {"request" : request})     # request means we are passingt the templates # home.html means which html file ,request:Request means jinja2 needs it 

@router.get("/ui/feeds")
def ui_feeds(request: Request, db: Session = Depends(get_db)):
    feeds = db.query(Feed).all()

    return templates.TemplateResponse(
        "feeds.html",
        {
            "request": request,
            "feeds": feeds
        }
    )

@router.get("/ui/feeds/{feed_id}/items")
def ui_feed_items(feed_id: int, request: Request, db: Session = Depends(get_db)):
    items = db.query(Item).filter(Item.feed_id == feed_id).all()

    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "items": items
        }
    )

