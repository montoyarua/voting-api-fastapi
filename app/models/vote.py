from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Vote(Base):
    """
    Vote (Voto)
    - UniqueConstraint(voter_id) garantiza 1 voto por votante a nivel BD.
    """
    __tablename__ = "vote"
    __table_args__ = (UniqueConstraint("voter_id", name="uq_votes_voter_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    voter_id: Mapped[int] = mapped_column(ForeignKey("voter.id", ondelete="CASCADE"), nullable=False, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id", ondelete="CASCADE"), nullable=False, index=True)

    voter = relationship("Voter", back_populates="vote")
    candidate = relationship("Candidate", back_populates="votes_rel")
