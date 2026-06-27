import os
from datetime import UTC, datetime
from urllib.parse import quote

import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from loguru import logger

from schemas import BlogFeed, BlogSource

_app: firebase_admin.App | None = None


def _get_db() -> firestore.Client:
    global _app
    if _app is None:
        _app = firebase_admin.initialize_app(
            options={"projectId": os.environ["GOOGLE_CLOUD_PROJECT"]}
        )
    return firestore.client()


def store_feed(source: BlogSource, feed: BlogFeed) -> None:
    db = _get_db()
    col = db.collection("blogs")
    scraped_at = datetime.now(UTC)

    # The doc ID is the post URL, and existing posts never change, so only the
    # posts we haven't stored before need writing. One query for the source's
    # existing IDs is far cheaper than re-writing every post on every run.
    query = col.where(filter=FieldFilter("source_id", "==", source.id)).select([])
    existing = {doc.id for doc in query.stream()}
    new_posts = [p for p in feed.posts if quote(p.url, safe="") not in existing]

    if not new_posts:
        logger.info("No new posts for {} ({} already stored)", source.name, len(existing))
        return

    batch = db.batch()
    pending = 0
    stored = 0
    for post in new_posts:
        batch.set(col.document(quote(post.url, safe="")), {
            "title": post.title,
            "url": post.url,
            "published_date": post.published_date,
            "source_id": source.id,
            "source_name": source.name,
            "scraped_at": scraped_at,
        })
        pending += 1
        if pending == 500:  # Firestore caps a batch at 500 writes
            batch.commit()
            stored += pending
            batch, pending = db.batch(), 0

    if pending:
        batch.commit()
        stored += pending

    logger.info("Stored {}/{} new posts for {}", stored, len(new_posts), source.name)
