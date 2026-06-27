from google import genai
from loguru import logger

llm_client = genai.Client()

response = llm_client.models.generate_content(
    model="gemini-3.5-flash", contents="Explain how AI works in a few words"
)
logger.info("{}", response.text)
