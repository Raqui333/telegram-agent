from tavily import TavilyClient
from langchain.tools import tool

from src.features.shared.logging import logger

from ..config import Settings

settings = Settings()
TAVILY_API_KEY = settings.tavily_api_key.get_secret_value()

client = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """
    Search the web for information

    If the search depends on the current date or time,
    use get_current_datetime first.
    """

    logger.info(f'Tool called: name="web_search" query="{query}"')

    try:
        response = client.search(
            query,
            max_results=5,
            topic="general",
        )
    except Exception as e:
        logger.error(f"Error searching the web: {e}")
        return "Desculpe, eu não consegui buscar informações na web. 😔"

    return response
