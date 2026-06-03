from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import ComidaCreate, ComidaResponse
from app import crud

router = APIRouter(prefix="/comidas", tags=["Comidas"])


@router.post("/", response_model=ComidaResponse)
async def registrar_comida(data: ComidaCreate, db: AsyncSession = Depends(get_session)):
    nino = await crud.get_nino(db, data.nino_matricula)
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    return await crud.create_comida(db, data.model_dump())


@router.get("/{nino_matricula}", response_model=list[ComidaResponse])
async def listar_comidas_nino(nino_matricula: int, db: AsyncSession = Depends(get_session)):
    return await crud.get_comidas_nino(db, nino_matricula)
