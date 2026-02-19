from pydantic import BaseModel, Field


class CandidateCreate(BaseModel):
    """Payload para crear candidato."""
    name: str = Field(..., min_length=1, max_length=150)
    party: str | None = Field(default=None, max_length=150)


class CandidateRead(BaseModel):
    """Respuesta de candidato."""
    id: int
    name: str
    party: str | None
    votes: int

    class Config:
        from_attributes = True
