import json
import os
from pathlib import Path

import yaml
from firecrawl import Firecrawl
from google import genai
from google.genai import types
from loguru import logger

from schemas import BlogFeed, BlogSource, SourcesConfig

BACKEND_DIR = Path(__file__).parent
SOURCES_PATH = BACKEND_DIR / "config" / "sources.yaml"

PROJECT_ID = os.getenv("GOOGLE_PROJECT")
REGION = os.getenv("GOOGLE_REGION")
logger.debug("PROJECT_ID: {}", PROJECT_ID)
logger.debug("REGION: {}", REGION)

firecrawl_client = Firecrawl()
ai_client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=REGION,
)


def load_sources() -> list[BlogSource]:
    with SOURCES_PATH.open() as f:
        data = yaml.safe_load(f)
    config = SourcesConfig.model_validate(data)
    return [source for source in config.sources if source.enabled]


def load_prompt(prompt_path: str) -> str:
    return (BACKEND_DIR / prompt_path).read_text().strip()


def scrape_and_parse_blog(source: BlogSource) -> BlogFeed:
    logger.info("Scraping {} ({}) with Firecrawl...", source.name, source.url)

    scrape_result = firecrawl_client.scrape(source.url, formats=["markdown"])
    markdown_content = scrape_result.markdown or ""

    logger.info("Parsing {} content with Gemini on Vertex AI...", source.name)

    prompt_template = load_prompt(source.prompt)
    response = ai_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"{prompt_template}\n\n{markdown_content}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BlogFeed,
            temperature=0.1,
        ),
    )

    if response.parsed is None:
        raise ValueError(f"Failed to parse response: {response.text}")

    return response.parsed


def scrape_all_sources() -> dict[str, BlogFeed]:
    results: dict[str, BlogFeed] = {}
    for source in load_sources():
        try:
            results[source.id] = scrape_and_parse_blog(source)
        except Exception:
            logger.exception("Failed to scrape {}", source.id)
    return results


if __name__ == "__main__":
    sources = {source.id: source for source in load_sources()}

    anthropic_feed = scrape_and_parse_blog(sources["anthropic"])
    logger.info(
        "Results for anthropic:\n{}",
        json.dumps(anthropic_feed.model_dump(), indent=2),
    )

    # openai_feed = scrape_and_parse_blog(sources["openai"])
    # logger.info(
    #     "Results for openai:\n{}",
    #     json.dumps(openai_feed.model_dump(), indent=2),
    # )

    # deepmind_feed = scrape_and_parse_blog(sources["deepmind"])
    # logger.info(
    #     "Results for deepmind:\n{}",
    #     json.dumps(deepmind_feed.model_dump(), indent=2),
    # )
