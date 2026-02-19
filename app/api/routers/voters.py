from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import VoterCreate, VoterRead
from app.repositories import VoterRepository
from app.services import VotingService
from app.utils.errors import not_found

router = APIRouter(prefix="/voters", tags=["Voters"])
service = VotingService()
repo = VoterRepository()


@router.post("", response_model=VoterRead, status_code=status.HTTP_201_CREATED)
def create_voter(payload: VoterCreate, db: Session = Depends(get_db)):
    # begin() => commit/rollback automático
    with db.begin():
        return service.create_voter(db, name=payload.name, email=str(payload.email))


@router.get("", response_model=list[VoterRead])
def list_voters(db: Session = Depends(get_db)):
    return repo.list(db)


@router.get("/{voter_id}", response_model=VoterRead)
def get_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = repo.get(db, voter_id)
    if not voter:
        raise not_found("Voter", voter_id)
    return voter

@router.delete("/{voter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    voter = repo.get(db, voter_id)
    if not voter:
        raise not_found("Voter", voter_id)

    try:
        repo.delete(db, voter)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None
