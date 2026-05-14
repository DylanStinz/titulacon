from pydantic import BaseModel, EmailStr, Field

class UsuarioSchema(BaseModel):

    nombre: str = Field(..., min_length=3, max_length=100)

    apellido_paterno: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    apellido_materno: str = Field(
        ...,
        min_length=3,
        max_length=100
    )

    correo: EmailStr

    usuario: str = Field(
        ...,
        min_length=3,
        max_length=50
    )

    contraseña: str = Field(
        ...,
        min_length=6
    )
