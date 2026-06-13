import logging

from contextlib import AsyncExitStack

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from langchain.embeddings import init_embeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from .settings import Settings

settings = Settings()

DATABASE_URL = settings.database_url.get_secret_value()
DEFAULT_EMBEDDING_MODEL = settings.embedding_model

logger = logging.getLogger(__name__)


class LangGraphPersistenceClient:
    def __init__(self):
        self.stack: AsyncExitStack | None = None
        self.store: AsyncPostgresStore | None = None
        self.checkpointer: AsyncPostgresSaver | None = None

    async def start(self) -> None:
        self.stack = AsyncExitStack()

        # checkpointer
        try:
            logger.info(f"Initializing LangGraph checkpointer")
            self.checkpointer = await self.stack.enter_async_context(
                AsyncPostgresSaver.from_conn_string(DATABASE_URL)
            )
        except Exception as e:
            logger.error(f"Error initializing checkpointer: {e}")
            raise

        # store
        try:
            logger.info(f"Initializing LangGraph store")
            self.store = await self.stack.enter_async_context(
                AsyncPostgresStore.from_conn_string(
                    DATABASE_URL,
                    index={
                        "embed": init_embeddings(DEFAULT_EMBEDDING_MODEL),
                        "dims": 1536,
                        "fields": ["$"],
                    },
                )
            )
        except Exception as e:
            logger.error(f"Error initializing store: {e}")
            raise

        # first setup for checkpointer and store
        await self.checkpointer.setup()
        await self.store.setup()

    async def stop(self) -> None:
        logger.info(f"Stopping langgraph store client")

        if self.stack:
            await self.stack.aclose()

        self.stack = None
        self.checkpointer = None
        self.store = None

    def get_instance(self) -> tuple[AsyncPostgresSaver, AsyncPostgresStore]:
        if not self.checkpointer or not self.store:
            raise RuntimeError("LangGraph resources not started")

        return self.checkpointer, self.store


# singleton instance
langgraph_persistence_client = LangGraphPersistenceClient()
