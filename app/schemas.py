from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class PagadorBase(BaseModel):
    dni: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=150)
    direccion: str
    telefono: str = Field(..., max_length=20)
    cuenta_corriente: str = Field(..., max_length=50)


class PagadorCreate(PagadorBase):
    pass


class PagadorResponse(PagadorBase):
    class Config:
        from_attributes = True


class PersonaAutorizadaBase(BaseModel):
    dni: str = Field(..., max_length=20)
    nombre: str = Field(..., max_length=150)
    direccion: str
    telefono1: str = Field(..., max_length=20)
    telefono2: Optional[str] = Field(None, max_length=20)
    relacion: str = Field(..., max_length=100)


class PersonaAutorizadaCreate(PersonaAutorizadaBase):
    pass


class PersonaAutorizadaResponse(PersonaAutorizadaBase):
    class Config:
        from_attributes = True


class NinoBase(BaseModel):
    matricula_id: int
    nombre: str = Field(..., max_length=150)
    fecha_nacimiento: date
    fecha_ingreso: date
    fecha_baja: Optional[date] = None
    pagador_dni: str = Field(..., max_length=20)


class NinoCreate(NinoBase):
    pass


class NinoResponse(NinoBase):
    class Config:
        from_attributes = True


class NinoAutorizadoCreate(BaseModel):
    nino_matricula: int
    autorizado_dni: str = Field(..., max_length=20)


class IngredienteBase(BaseModel):
    nombre: str = Field(..., max_length=100)


class IngredienteCreate(IngredienteBase):
    pass


class IngredienteResponse(IngredienteBase):
    class Config:
        from_attributes = True


class PlatoBase(BaseModel):
    nombre: str = Field(..., max_length=100)


class PlatoCreate(PlatoBase):
    pass


class PlatoResponse(PlatoBase):
    class Config:
        from_attributes = True


class MenuBase(BaseModel):
    numero: int


class MenuCreate(MenuBase):
    pass


class MenuResponse(MenuBase):
    class Config:
        from_attributes = True


class IngredienteUpdate(BaseModel):
    nombre: str = Field(..., max_length=100)


class PlatoUpdate(BaseModel):
    nombre: str = Field(..., max_length=100)


class MenuUpdate(BaseModel):
    numero: int


class MenuPlatoCreate(BaseModel):
    menu_numero: int
    plato_nombre: str = Field(..., max_length=100)


class PlatoIngredienteCreate(BaseModel):
    plato_nombre: str = Field(..., max_length=100)
    ingrediente_nombre: str = Field(..., max_length=100)


class AlergiaCreate(BaseModel):
    nino_matricula: int
    ingrediente_nombre: str = Field(..., max_length=100)


class ComidaCreate(BaseModel):
    nino_matricula: int
    fecha: date
    menu_numero: int


class ComidaResponse(BaseModel):
    id: int
    nino_matricula: int
    fecha: date
    menu_numero: int

    class Config:
        from_attributes = True
