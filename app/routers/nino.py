from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import NinoCreate, NinoResponse, NinoAutorizadoCreate
from app import crud

router = APIRouter(prefix="/ninos", tags=["Niños"])


@router.post("/", response_model=NinoResponse)
async def crear_nino(data: NinoCreate, db: AsyncSession = Depends(get_session)):
    existente = await crud.get_nino(db, data.matricula_id)
    if existente:
        raise HTTPException(400, "Ya existe un niño con esa matrícula")
    pagador = await crud.get_pagador(db, data.pagador_dni)
    if not pagador:
        raise HTTPException(400, "El pagador indicado no existe")
    return await crud.create_nino(db, data.model_dump())


@router.get("/", response_model=list[NinoResponse])
async def listar_ninos(db: AsyncSession = Depends(get_session)):
    return await crud.get_ninos(db)


@router.get("/{matricula_id}", response_model=NinoResponse)
async def obtener_nino(matricula_id: int, db: AsyncSession = Depends(get_session)):
    nino = await crud.get_nino(db, matricula_id)
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    return nino


@router.post("/{matricula_id}/autorizados", response_model=dict)
async def agregar_autorizado(
    matricula_id: int, data: NinoAutorizadoCreate, db: AsyncSession = Depends(get_session)
):
    nino = await crud.get_nino(db, matricula_id)
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    persona = await crud.get_persona_autorizada(db, data.autorizado_dni)
    if not persona:
        raise HTTPException(400, "La persona autorizada no existe")
    await crud.create_nino_autorizado(db, matricula_id, data.autorizado_dni)
    return {"mensaje": "Persona autorizada asignada correctamente"}
