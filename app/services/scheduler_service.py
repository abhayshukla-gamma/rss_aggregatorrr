# here we will write the code for automated fetching from the rss feeds
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import sessionLocal
from app.models.feed import Feed
from app.services.digest_service import send_daily_digest
from app.services.item_service import save_feed_items

scheduler = BackgroundScheduler()


def fetch_all_feeds():
    print("scheduler running ")
    db = sessionLocal()

    feeds = db.query(Feed).all()

    for feed in feeds:
        save_feed_items(feed.id, feed.url, db)

    db.close()


def start_scheduler():
    scheduler.add_job(fetch_all_feeds, "interval", hours=8)
    scheduler.add_job(send_daily_digest, "interval", hours=23)

    scheduler.start()
