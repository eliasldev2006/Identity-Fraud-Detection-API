from pydantic import BaseModel, EmailStr, Field

class CadastroRequest(BaseModel):
    nome: str = Field(..., min_length=3)
    email: EmailStr
    cpf: str = Field(..., min_length=11, max_length=14)
    idade: int = Field(..., ge=18, le=120)