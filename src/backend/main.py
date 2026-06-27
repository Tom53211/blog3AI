from loguru import logger

from firestore_store import store_feed
from scrape_blogs import load_sources, scrape_and_parse_blog


def main() -> None:
    sources = {source.id: source for source in load_sources()}

    # anthropic_feed = scrape_and_parse_blog(sources["anthropic"])
    # store_feed(sources["anthropic"], anthropic_feed)

    # openai_feed = scrape_and_parse_blog(sources["openai"])
    # store_feed(sources["openai"], openai_feed)

    deepmind_feed = scrape_and_parse_blog(sources["deepmind"])
    store_feed(sources["deepmind"], deepmind_feed)

    logger.info("Pipeline complete")


if __name__ == "__main__":
    main()
