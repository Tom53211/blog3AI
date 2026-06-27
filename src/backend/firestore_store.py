from datetime import UTC, datetime
from urllib.parse import quote

import firebase_admin
from firebase_admin import firestore
from loguru import logger

from schemas import BlogFeed, BlogSource

_app: firebase_admin.App | None = None


def _get_db() -> firestore.Client:
    global _app
    if _app is None:
        _app = firebase_admin.initialize_app()
    return firestore.client()


def store_feed(source: BlogSource, feed: BlogFeed) -> None:
    db = _get_db()
    col = db.collection("blogs")
    scraped_at = datetime.now(UTC)

    stored = 0
    for post in feed.posts:
        doc_id = quote(post.url, safe="")
        try:
            col.document(doc_id).set({
                "title": post.title,
                "url": post.url,
                "published_month": post.published_month,
                "source_id": source.id,
                "source_name": source.name,
                "scraped_at": scraped_at,
            })
            stored += 1
        except Exception:
            logger.exception("Failed to store post: {}", post.url)

    logger.info("Stored {}/{} posts for {}", stored, len(feed.posts), source.name)
