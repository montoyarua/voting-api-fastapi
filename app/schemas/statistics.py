from pydantic import BaseModel


class CandidateStats(BaseModel):
    candidate_id: int
    name: str
    party: str | None
    votes: int
    percentage: float


class VoteStatistics(BaseModel):
    total_votes: int
    total_voters_voted: int
    by_candidate: list[CandidateStats]
