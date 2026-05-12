from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    apellido: str = Field(..., min_length=3, max_length=100)  
    email: EmailStr
    password: str = Field(..., min_length=8)


class TareaSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = None
    prioridad: str = "media" 
    clasificacion: str = "personal"