from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import PersonaAutorizadaCreate, PersonaAutorizadaResponse
from app import crud

router = APIRouter(prefix="/personas-autorizadas", tags=["Personas Autorizadas"])


@router.post("/", response_model=PersonaAutorizadaResponse)
async def crear_persona(data: PersonaAutorizadaCreate, db: AsyncSession = Depends(get_session)):
    existente = await crud.get_persona_autorizada(db, data.dni)
    if existente:
        raise HTTPException(400, "Ya existe una persona con ese DNI")
    return await crud.create_persona_autorizada(db, data.model_dump())


@router.get("/", response_model=list[PersonaAutorizadaResponse])
async def listar_personas(db: AsyncSession = Depends(get_session)):
    return await crud.get_personas_autorizadas(db)


@router.get("/{dni}", response_model=PersonaAutorizadaResponse)
async def obtener_persona(dni: str, db: AsyncSession = Depends(get_session)):
    persona = await crud.get_persona_autorizada(db, dni)
    if not persona:
        raise HTTPException(404, "Persona no encontrada")
    return persona
