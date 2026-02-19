from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import CandidateCreate, CandidateRead
from app.repositories import CandidateRepository
from app.services import VotingService
from app.utils.errors import not_found

router = APIRouter(prefix="/candidates", tags=["Candidates"])
service = VotingService()
repo = CandidateRepository()


@router.post("", response_model=CandidateRead, status_code=status.HTTP_201_CREATED)
def create_candidate(payload: CandidateCreate, db: Session = Depends(get_db)):
    with db.begin():
        return service.create_candidate(db, name=payload.name, party=payload.party)


@router.get("", response_model=list[CandidateRead])
def list_candidates(db: Session = Depends(get_db)):
    return repo.list(db)


@router.get("/{candidate_id}", response_model=CandidateRead)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = repo.get(db, candidate_id)
    if not candidate:
        raise not_found("Candidate", candidate_id)
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = repo.get(db, candidate_id)
    if not candidate:
        raise not_found("Candidate", candidate_id)

    try:
        repo.delete(db, candidate)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None
