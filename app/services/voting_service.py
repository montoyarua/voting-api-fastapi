from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models import Candidate, Vote
from app.repositories import VoterRepository, CandidateRepository, VoteRepository
from app.utils.errors import not_found, conflict


class VotingService:
    """
    Servicio de negocio:
    - validaciones
    - transacciones
    - estadísticas
    """

    def __init__(self) -> None:
        self.voters = VoterRepository()
        self.candidates = CandidateRepository()
        self.votes = VoteRepository()

    # -------- VOTERS --------
    def create_voter(self, db: Session, name: str, email: str):
        if self.voters.email_exists(db, email):
            raise conflict("A voter with this email already exists")

        # Restricción aproximada (Candidate no tiene email en el enunciado)
        if self.candidates.name_exists(db, name):
            raise conflict("This person is already registered as a candidate (name conflict)")

        return self.voters.create(db, name=name, email=email)

    # ----- CANDIDATES -----
    def create_candidate(self, db: Session, name: str, party: str | None):
        # Regla del enunciado: un votante no puede ser candidato y viceversa
        # (como no hay email en Candidate, se valida por name)
        if self.voters.name_exists(db, name):
            raise conflict("This person is already registered as a voter (name conflict)")

        # ✅ Evita duplicados exactos en Candidate: mismo name + mismo party
        if self.candidates.exists_by_name_party(db, name, party):
            raise conflict("Candidate already registered with same name and party")

        return self.candidates.create(db, name=name, party=party)

    # -------- VOTES --------
    def cast_vote(self, db: Session, voter_id: int, candidate_id: int):
        voter = self.voters.get(db, voter_id)
        if not voter:
            raise not_found("Voter", voter_id)

        candidate = self.candidates.get(db, candidate_id)
        if not candidate:
            raise not_found("Candidate", candidate_id)

        if voter.has_voted:
            raise conflict("This voter has already voted")

        if self.votes.has_vote_for_voter(db, voter_id):
            raise conflict("This voter has already voted")

        try:
            vote = self.votes.create(db, voter_id=voter_id, candidate_id=candidate_id)
            voter.has_voted = True
            candidate.votes += 1
            return vote
        except IntegrityError:
            raise conflict("This voter has already voted")

    # ----- STATISTICS -----
    def statistics(self, db: Session):
        total_votes = self.votes.total_votes(db)
        total_voters_voted = self.votes.total_voters_voted(db)

        rows = db.execute(
            select(
                Candidate.id,
                Candidate.name,
                Candidate.party,
                func.count(Vote.id).label("vote_count"),
            )
            .select_from(Candidate)
            .join(Vote, Vote.candidate_id == Candidate.id, isouter=True)
            .group_by(Candidate.id)
            .order_by(Candidate.id)
        ).all()

        by_candidate = []
        for cid, name, party, vote_count in rows:
            vote_count = int(vote_count or 0)
            pct = (vote_count / total_votes * 100.0) if total_votes > 0 else 0.0
            by_candidate.append(
                {
                    "candidate_id": cid,
                    "name": name,
                    "party": party,
                    "votes": vote_count,
                    "percentage": round(pct, 2),
                }
            )

        return {
            "total_votes": total_votes,
            "total_voters_voted": total_voters_voted,
            "by_candidate": by_candidate,
        }
