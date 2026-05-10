from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey,
    text,
)
from sqlalchemy.orm import Mapped, relationship, mapped_column
import enum


from models.base import Base


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    gender = Column(Enum(GenderEnum), default=GenderEnum.unknown)
    bio = Column(String(500), nullable=True)
    phone = Column(String(20), unique=True, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    # # Relationships
    # tokens = relationship(
    #     "UserToken", back_populates="user", cascade="all, delete-orphan"
    # )
    # favorites = relationship(
    #     "Favorite", back_populates="user", cascade="all, delete-orphan"
    # )
    # histories = relationship(
    #     "History", back_populates="user", cascade="all, delete-orphan"
    # )
    # ai_chats = relationship(
    #     "AIChat", back_populates="user", cascade="all, delete-orphan"
    # )


class UserToken(Base):
    __tablename__ = "user_token"

    __table_args__ = (
        Index("TOKEN_UNIQUE", "token"),
        Index("fk_user_token_user_idx", "user_id"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="令牌ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id), nullable=False, comment="用户ID"
    )

    token: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, comment="令牌值"
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="过期时间"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="创建时间", default=datetime.now
    )
