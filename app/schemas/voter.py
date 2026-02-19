from pydantic import BaseModel, EmailStr, Field


class VoterCreate(BaseModel):
    """Payload para crear votante."""
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr


class VoterRead(BaseModel):
    """Respuesta de votante."""
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    class Config:
        from_attributes = True
