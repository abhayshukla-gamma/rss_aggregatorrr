import feedparser

def fetch_feed(url:str):
    feed = feedparser.parse(url)
    if feed.bozo:
        return []
    items = []

    for entry in feed.entries:
        items.append({
            "title" : entry.title,
            "link" : entry.link,
            "published" : entry.get("published", "")
        })
    return items    