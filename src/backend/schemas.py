from pydantic import BaseModel, Field


class BlogPost(BaseModel):
    title: str = Field(description="The title of the blog post")
    url: str = Field(description="The absolute URL link to the blog post")
    published_date: str | None = Field(
        default=None,
        description=(
            "Publication date normalized to 'YYYY-MM-DD' (year, month, and day). "
            "If only month and year are shown, set day to '01'. "
            "Null if no date is shown for the post."
        ),
    )


class BlogFeed(BaseModel):
    posts: list[BlogPost]


class BlogSource(BaseModel):
    id: str
    name: str
    url: str
    prompt: str | None = None
    enabled: bool = True
    rss_feed: str | None = None


class SourcesConfig(BaseModel):
    sources: list[BlogSource]
