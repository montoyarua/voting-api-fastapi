from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import VoteCreate, VoteRead, VoteStatistics
from app.repositories import VoteRepository
from app.services import VotingService

router = APIRouter(prefix="/votes", tags=["Votes"])
service = VotingService()
repo = VoteRepository()


@router.post("", response_model=VoteRead, status_code=status.HTTP_201_CREATED)
def cast_vote(payload: VoteCreate, db: Session = Depends(get_db)):
    with db.begin():
        return service.cast_vote(db, voter_id=payload.voter_id, candidate_id=payload.candidate_id)


@router.get("", response_model=list[VoteRead])
def list_votes(db: Session = Depends(get_db)):
    return repo.list(db)


@router.get("/statistics", response_model=VoteStatistics)
def statistics(db: Session = Depends(get_db)):
    return service.statistics(db)
