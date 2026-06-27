import warnings

from loguru import logger

warnings.filterwarnings("ignore", category=UserWarning, module="firecrawl")

from firestore_store import store_feed
from scrape_blogs import load_sources, scrape_and_parse_blog


def main() -> None:
    for source in load_sources():
        feed = scrape_and_parse_blog(source)
        store_feed(source, feed)

    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()
