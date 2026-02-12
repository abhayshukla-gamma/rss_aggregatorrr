from app.models.item import Item   # Item table
from app.core.database import sessionLocal  # DB session
from app.services.email_service import send_email  # email function


def send_daily_digest():

    db = sessionLocal()   # DB open

    # unread items nikaalo
    unread_items = db.query(Item).filter(Item.is_read == False).all()

    if not unread_items:
        print("No unread items")
        db.close()
        return

    # Email ka text banana
    body  = "Your Unread Articles:  \n\n"

    for item in unread_items:
        body += f"- {item.title}\n"

    # Email bhejo
    send_email(
        subject="Daily RSS Digest",
        body=body,
        to_email="abhay.shukla@gammaedge.io"
    )

    db.close()
