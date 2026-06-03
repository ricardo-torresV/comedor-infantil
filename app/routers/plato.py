from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import PlatoCreate, PlatoResponse, PlatoIngredienteCreate
from app import crud

router = APIRouter(prefix="/platos", tags=["Platos"])


@router.post("/", response_model=PlatoResponse)
async def crear_plato(data: PlatoCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_plato(db, data.model_dump())


@router.get("/", response_model=list[PlatoResponse])
async def listar_platos(db: AsyncSession = Depends(get_session)):
    return await crud.get_platos(db)


@router.post("/{nombre}/ingredientes", response_model=dict)
async def asignar_ingrediente(
    nombre: str, data: PlatoIngredienteCreate, db: AsyncSession = Depends(get_session)
):
    await crud.create_plato_ingrediente(db, nombre, data.ingrediente_nombre)
    return {"mensaje": "Ingrediente asignado al plato correctamente"}
