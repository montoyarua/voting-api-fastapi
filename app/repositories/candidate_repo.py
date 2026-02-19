from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Candidate


class CandidateRepository:
    """Acceso a datos para Candidate."""

    def name_exists(self, db: Session, name: str) -> bool:
        # Mantienes este si aún lo usas para otras reglas
        return (
            (db.scalar(
                select(func.count())
                .select_from(Candidate)
                .where(func.lower(func.trim(Candidate.name)) == name.strip().lower())
            ) or 0) > 0
        )

    def exists_by_name_party(self, db: Session, name: str, party: str | None) -> bool:
        """
        Valida duplicado exacto: mismo name + mismo party.
        - Compara case-insensitive
        - Ignora espacios al inicio/fin
        - Si party es None, se compara como '' (vacío)
        """
        name_norm = name.strip().lower()
        party_norm = (party or "").strip().lower()

        stmt = (
            select(func.count())
            .select_from(Candidate)
            .where(
                func.lower(func.trim(Candidate.name)) == name_norm,
                func.lower(func.trim(func.coalesce(Candidate.party, ""))) == party_norm,
            )
        )
        return (db.scalar(stmt) or 0) > 0

    def create(self, db: Session, name: str, party: str | None) -> Candidate:
        # Normalización opcional para consistencia
        candidate = Candidate(
            name=name.strip(),
            party=(party.strip() if party else None),
        )
        db.add(candidate)
        db.flush()
        return candidate

    def get(self, db: Session, candidate_id: int) -> Candidate | None:
        return db.get(Candidate, candidate_id)

    def list(self, db: Session) -> list[Candidate]:
        return list(db.scalars(select(Candidate).order_by(Candidate.id)).all())

    def delete(self, db: Session, candidate: Candidate) -> None:
        db.delete(candidate)
