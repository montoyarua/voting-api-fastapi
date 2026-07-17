from pydantic import BaseModel, ConfigDict, Field


class VoteCreate(BaseModel):
    """Payload para emitir voto."""
    voter_id: int = Field(..., ge=1)
    candidate_id: int = Field(..., ge=1)


class VoteRead(BaseModel):
    """Respuesta de voto."""
    id: int
    voter_id: int
    candidate_id: int

    model_config = ConfigDict(from_attributes=True)
