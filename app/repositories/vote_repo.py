from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Vote, Voter


class VoteRepository:
    """Acceso a datos para Vote."""

    def create(self, db: Session, voter_id: int, candidate_id: int) -> Vote:
        vote = Vote(voter_id=voter_id, candidate_id=candidate_id)
        db.add(vote)
        db.flush()
        return vote

    def list(self, db: Session) -> list[Vote]:
        return list(db.scalars(select(Vote).order_by(Vote.id)).all())

    def total_votes(self, db: Session) -> int:
        return int(db.scalar(select(func.count(Vote.id))) or 0)

    def total_voters_voted(self, db: Session) -> int:
        return int(db.scalar(select(func.count(Voter.id)).where(Voter.has_voted.is_(True))) or 0)

    def has_vote_for_voter(self, db: Session, voter_id: int) -> bool:
        return (db.scalar(select(func.count(Vote.id)).where(Vote.voter_id == voter_id)) or 0) > 0
