from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class VoterCreate(BaseModel):
    """Payload para crear votante."""
    name: str = Field(..., min_length=1, max_length=150)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("name must not be blank")
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class VoterRead(BaseModel):
    """Respuesta de votante."""
    id: int
    name: str
    email: EmailStr
    has_voted: bool

    model_config = ConfigDict(from_attributes=True)
