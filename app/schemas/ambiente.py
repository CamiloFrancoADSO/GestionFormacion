from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class AmbienteBase(BaseModel):
    nombre_ambiente: str = Field(min_length=3, max_length=40)
    num_max_aprendices: int = Field(ge=6, le=45)
    municipio: str = Field(min_length=6, max_length=40)
    ubicacion: str = Field(min_length=7, max_length=80)
    cod_centro: int
    estado: bool

class AmbienteCreate(AmbienteBase):
    pass

class AmbienteUpdate(BaseModel):
    nombre_ambiente: Optional[str] = Field(default=None, min_length=3, max_length=40)
    num_max_aprendices: Optional[int] = Field(default=None, ge=6, le=45)
    municipio: Optional[str] = Field(default=None, min_length=6, max_length=40)
    ubicacion: Optional[str] = Field(default=None,min_length=7,max_length=80)
    estado: Optional[bool] = None

class AmbienteOut(AmbienteBase):
    id_ambiente: int



