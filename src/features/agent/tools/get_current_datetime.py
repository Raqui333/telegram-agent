from datetime import datetime, timezone
from langchain.tools import tool

from src.features.shared.logging import logger


@tool
def get_current_datetime() -> str:
    """
    Get the current date and time in UTC.
    Only in UTC, does not support other timezones.

    Use this tool whenever the user asks about:
    - today
    - yesterday
    - tomorrow
    - current
    - latest
    - recent
    - this week
    - this month
    - this year
    """

    logger.info('Tool called: name="get_current_datetime"')

    return datetime.now(timezone.utc).isoformat()
