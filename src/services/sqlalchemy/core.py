from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class SQLAlchemyClient:
    def __init__(self, database_url: str):
        if not database_url:
            raise ValueError("DATABASE_URL was not provided")

        self._engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=5,
            pool_timeout=30,
            pool_recycle=1800,
        )

        self._SessionLocal = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
        )

    @contextmanager
    def session(self):
        session: Session = self._SessionLocal()
        # this is a context manager, so we can use it with the with statement
        # all commands are executed within a transaction, so we can rollback if an error occurs
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
