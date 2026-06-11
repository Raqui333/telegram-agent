import logging

from rich.logging import RichHandler


def configure_terminal_logging(level: str = "INFO") -> logging.Logger:
    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, markup=True, show_path=False)],
    )

    # Prevent HTTPX and HTTPCORE from logging too much
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    return logging.getLogger("system_logger")


logger = configure_terminal_logging()
