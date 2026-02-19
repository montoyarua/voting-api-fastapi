from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Voter(Base):
    """
    Voter (Votante)
    - email único
    - has_voted se actualiza a True cuando emite voto
    """
    __tablename__ = "voter"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    has_voted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relación 1 a 1: 1 votante -> 1 voto (por restricción)
    vote = relationship(
        "Vote",
        back_populates="voter",
        uselist=False,
        cascade="all, delete-orphan",
    )
