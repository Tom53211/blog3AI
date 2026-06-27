from pydantic import BaseModel, Field


class BlogPost(BaseModel):
    title: str = Field(description="The title of the blog post")
    url: str = Field(description="The absolute URL link to the blog post")
    published_month: str | None = Field(
        default=None,
        description=(
            "Publication date normalized to 'YYYY-MM' (year and month only). "
            "Null if no date is shown for the post."
        ),
    )


class BlogFeed(BaseModel):
    posts: list[BlogPost]


class BlogSource(BaseModel):
    id: str
    name: str
    url: str
    prompt: str
    enabled: bool = True


class SourcesConfig(BaseModel):
    sources: list[BlogSource]
