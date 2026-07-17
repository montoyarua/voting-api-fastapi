from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Candidate(Base):
    """
    Candidate (Candidato)
    - votes: contador que incrementamos al emitir voto (cache)
    """
    __tablename__ = "candidate"
    __table_args__ = (
        UniqueConstraint("name", "party", name="uq_candidate_name_party"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    party: Mapped[str | None] = mapped_column(String(150), nullable=True)
    votes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    votes_rel = relationship(
        "Vote",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
