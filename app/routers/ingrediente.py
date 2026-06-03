from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import IngredienteCreate, IngredienteResponse
from app import crud

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post("/", response_model=IngredienteResponse)
async def crear_ingrediente(data: IngredienteCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_ingrediente(db, data.model_dump())


@router.get("/", response_model=list[IngredienteResponse])
async def listar_ingredientes(db: AsyncSession = Depends(get_session)):
    return await crud.get_ingredientes(db)
