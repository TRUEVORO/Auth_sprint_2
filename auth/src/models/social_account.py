from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .mixin import UuidMixin, UuidOrmMixin


class SocialAccountOrm(UuidOrmMixin):
    """Social account table."""

    __tablename__ = 'social_account'

    user_id: Mapped[UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    social_id: Mapped[UUID] = mapped_column(unique=True, nullable=False)
    social_name: Mapped[str] = mapped_column(unique=True, nullable=False)

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'


class SocialAccount(UuidMixin):
    """Social account model."""

    user_id: UUID
    social_id: UUID
    social_name: str
