from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

# from src.resources.record.model import HealthRecord, ProblemRecord


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    # hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    records: Mapped[List["HealthRecord"]] = \
        relationship(back_populates="owner")

    problems: Mapped[List["ProblemRecord"]] = \
        relationship(back_populates="owner")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email})"