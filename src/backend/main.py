import os

from google import genai
from loguru import logger

PROJECT_ID = os.getenv("GOOGLE_PROJECT")

llm_client = genai.Client(
    vertexai=True,
    location="global",
    project=PROJECT_ID,
)

response = llm_client.models.generate_content(
    model="gemini-3.5-flash", contents="Explain how AI works in a few words"
)
logger.info("{}", response.text)
