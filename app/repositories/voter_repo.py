from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Voter


class VoterRepository:
    """Acceso a datos para Voter."""

    def email_exists(self, db: Session, email: str) -> bool:
        return (db.scalar(select(func.count()).select_from(Voter).where(Voter.email == email)) or 0) > 0

    def name_exists(self, db: Session, name: str) -> bool:
        return (db.scalar(select(func.count()).select_from(Voter).where(func.lower(Voter.name) == name.lower())) or 0) > 0

    def create(self, db: Session, name: str, email: str) -> Voter:
        voter = Voter(name=name, email=email)
        db.add(voter)
        db.flush()  # obtiene id sin commit
        return voter

    def get(self, db: Session, voter_id: int) -> Voter | None:
        return db.get(Voter, voter_id)

    def list(self, db: Session) -> list[Voter]:
        return list(db.scalars(select(Voter).order_by(Voter.id)).all())

    def delete(self, db: Session, voter: Voter) -> None:
        db.delete(voter)
