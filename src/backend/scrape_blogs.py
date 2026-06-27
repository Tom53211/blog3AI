import html
import json
import os
from datetime import UTC, datetime
from pathlib import Path

import feedparser
import yaml
from firecrawl import Firecrawl
from google import genai
from google.genai import types
from loguru import logger

from schemas import BlogFeed, BlogPost, BlogSource, SourcesConfig

BACKEND_DIR = Path(__file__).parent
SOURCES_PATH = BACKEND_DIR / "config" / "sources.yaml"

firecrawl_client = Firecrawl()
ai_client = genai.Client()


def load_sources() -> list[BlogSource]:
    with SOURCES_PATH.open() as f:
        data = yaml.safe_load(f)
    config = SourcesConfig.model_validate(data)
    return [source for source in config.sources if source.enabled]


def load_prompt(prompt_path: str) -> str:
    return (BACKEND_DIR / prompt_path).read_text().strip()


def parse_feed_from_rss(source: BlogSource) -> BlogFeed:
    logger.info("Fetching {} RSS feed ({})...", source.name, source.rss_feed)
    feed = feedparser.parse(source.rss_feed)
    posts = []
    for entry in feed.entries:
        published_date = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            dt = datetime(*entry.published_parsed[:6])
            published_date = dt.strftime("%Y-%m-%d")
        posts.append(BlogPost(title=html.unescape(entry.title), url=entry.link, published_date=published_date))
    logger.info("Got {} posts from {} RSS", len(posts), source.name)
    return BlogFeed(posts=posts)


def scrape_and_parse_blog(source: BlogSource) -> BlogFeed:
    if source.rss_feed:
        return parse_feed_from_rss(source)

    logger.info("Scraping {} ({}) with Firecrawl...", source.name, source.url)

    scrape_result = firecrawl_client.scrape(source.url, formats=["markdown"])
    markdown_content = scrape_result.markdown or ""

    logger.info("Parsing {} content with Gemini...", source.name)

    prompt_template = load_prompt(source.prompt)
    today = datetime.now(UTC).date()
    contents = (
        f"{prompt_template}\n\n"
        f"Today's date is {today:%Y-%m-%d}.\n\n"
        f"{markdown_content}"
    )
    response = ai_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BlogFeed,
            temperature=0.1,
        ),
    )

    if response.parsed is None:
        raise ValueError(f"Failed to parse response: {response.text}")

    return response.parsed


if __name__ == "__main__":
    sources = {source.id: source for source in load_sources()}

    # anthropic_feed = scrape_and_parse_blog(sources["anthropic"])
    # logger.info(
    #     "Results for anthropic:\n{}",
    #     json.dumps(anthropic_feed.model_dump(), indent=2),
    # )

    # openai_feed = scrape_and_parse_blog(sources["openai"])
    # logger.info(
    #     "Results for openai:\n{}",
    #     json.dumps(openai_feed.model_dump(), indent=2, ensure_ascii=False),
    # )

    deepmind_feed = scrape_and_parse_blog(sources["deepmind"])
    logger.info(
        "Results for deepmind:\n{}",
        json.dumps(deepmind_feed.model_dump(), indent=2, ensure_ascii=False),
    )
