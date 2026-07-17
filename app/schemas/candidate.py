from pydantic import BaseModel, ConfigDict, Field, field_validator


class CandidateCreate(BaseModel):
    """Payload para crear candidato."""
    name: str = Field(..., min_length=1, max_length=150)
    party: str | None = Field(default=None, max_length=150)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("name must not be blank")
        return value

    @field_validator("party")
    @classmethod
    def normalize_party(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = " ".join(value.split())
        return value or None


class CandidateRead(BaseModel):
    """Respuesta de candidato."""
    id: int
    name: str
    party: str | None
    votes: int

    model_config = ConfigDict(from_attributes=True)
