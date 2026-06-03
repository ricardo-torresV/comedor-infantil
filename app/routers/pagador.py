from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import PagadorCreate, PagadorResponse
from app import crud

router = APIRouter(prefix="/pagadores", tags=["Pagadores"])


@router.post("/", response_model=PagadorResponse)
async def crear_pagador(data: PagadorCreate, db: AsyncSession = Depends(get_session)):
    existente = await crud.get_pagador(db, data.dni)
    if existente:
        raise HTTPException(400, "Ya existe un pagador con ese DNI")
    return await crud.create_pagador(db, data.model_dump())


@router.get("/", response_model=list[PagadorResponse])
async def listar_pagadores(db: AsyncSession = Depends(get_session)):
    return await crud.get_pagadores(db)


@router.get("/{dni}", response_model=PagadorResponse)
async def obtener_pagador(dni: str, db: AsyncSession = Depends(get_session)):
    pagador = await crud.get_pagador(db, dni)
    if not pagador:
        raise HTTPException(404, "Pagador no encontrado")
    return pagador
