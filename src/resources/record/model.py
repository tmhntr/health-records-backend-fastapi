from __future__ import annotations

from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from src.database import Base

# from src.resources.user.model import User



class HealthRecord(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True)
    record_type: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    date: Mapped[str] = mapped_column()

    owner_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="records")

    problem_id: Mapped[Optional[int]] = \
        mapped_column(ForeignKey("problem_records.id"))
        
    problem: Mapped[Optional["ProblemRecord"]] = \
        relationship(back_populates="records")

    # time
    start_date: Mapped[Optional[str]] = mapped_column()
    end_date: Mapped[Optional[str]] = mapped_column()

    # referral
    referral_to: Mapped[Optional[str]] = mapped_column()

    # medication
    instructions: Mapped[Optional[str]] = mapped_column()
    dose: Mapped[Optional[str]] = mapped_column()
    dose_unit: Mapped[Optional[str]] = mapped_column()

    # lab
    value: Mapped[Optional[str]] = mapped_column()
    value_unit: Mapped[Optional[str]] = mapped_column()

    def __repr__(self):
        return f"HealthRecord(id={self.id}, record_type={self.record_type})"


class ProblemRecord(Base):
    __tablename__ = "problem_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    record_type: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    records: Mapped[List["HealthRecord"]] \
        = relationship(back_populates="problem")

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="problems")
