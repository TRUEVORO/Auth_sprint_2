from datetime import datetime
from uuid import UUID

from pydantic import Field
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .mixin import UuidMixin, UuidOrmMixin


def create_partition(target, connection, **kw) -> None:  # noqa
    """Creating partition by user_sign_in."""

    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_smart" PARTITION OF "users_sign_in" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_mobile" PARTITION OF "users_sign_in" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "user_sign_in_web" PARTITION OF "users_sign_in" FOR VALUES IN ('web')"""
    )


class AuthHistoryOrm(UuidOrmMixin):
    """User's auth history table."""

    __tablename__ = 'auth_history'
    __table_args__ = (
        UniqueConstraint('id', 'user_device_type'),
        {
            'postgresql_partition_by': 'LIST (user_device_type)',
            'listeners': [('after_create', create_partition)],
        },
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    user_agent: Mapped[str] = mapped_column(nullable=False)
    user_device_type: Mapped[str] = mapped_column(nullable=False, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)


class AuthHistory(UuidMixin):
    """User's auth history model."""

    user_id: UUID
    user_agent: str
    user_device_type: str
    timestamp: datetime = Field(default=datetime.now())
