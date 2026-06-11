from sqlalchemy import Text, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class SqlAlchemyBaseModel(DeclarativeBase):
    pass


class User(SqlAlchemyBaseModel):
    __tablename__ = "users"

    id: Mapped[Uuid] = mapped_column(
        Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )

    telegram_id: Mapped[int] = mapped_column(Text, nullable=False, unique=True)
    username: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})"
