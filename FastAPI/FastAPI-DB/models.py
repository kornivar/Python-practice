import os

from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from connection import Base

class Mercenary(Base):
    __tablename__ = "mercenaries"

    __table_args__ = (
        CheckConstraint("level >= 1", name="check_mercenary_level"),
        CheckConstraint(
            "reputation >= 0",
            name="check_mercenary_reputation",
        ),
        CheckConstraint("balance >= 0", name="check_mercenary_balance"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    nickname: Mapped[str] = mapped_column(
        String(50), unique=True, index=True
    )

    level: Mapped[int] = mapped_column(Integer)

    reputation: Mapped[int] = mapped_column(Integer, default=0)

    balance: Mapped[float] = mapped_column(Float, default=0)


class Contract(Base):
    __tablename__ = "contracts"

    __table_args__ = (
        CheckConstraint(
            "difficulty BETWEEN 1 AND 10",
            name="check_contract_difficulty",
        ),
        CheckConstraint(
            "reward > 0",
            name="check_contract_reward",
        ),
        CheckConstraint(
            "status IN ('OPEN', 'IN_PROGRESS', 'COMPLETED', 'FAILED')",
            name="check_contract_status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(120), index=True)

    description: Mapped[str] = mapped_column(String(500))

    difficulty: Mapped[int] = mapped_column(Integer)

    reward: Mapped[float] = mapped_column(Float)

    district: Mapped[str] = mapped_column(String(100), index=True)

    status: Mapped[str] = mapped_column(
        String(20), default="OPEN", server_default="OPEN"
    )

    mercenary_id: Mapped[int | None] = mapped_column(
        ForeignKey("mercenaries.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )