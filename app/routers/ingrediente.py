from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import IngredienteCreate, IngredienteResponse, IngredienteUpdate
from app import crud

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


@router.post("/", response_model=IngredienteResponse)
async def crear_ingrediente(data: IngredienteCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_ingrediente(db, data.model_dump())


@router.get("/", response_model=list[IngredienteResponse])
async def listar_ingredientes(db: AsyncSession = Depends(get_session)):
    return await crud.get_ingredientes(db)


@router.get("/{nombre}", response_model=IngredienteResponse)
async def obtener_ingrediente(nombre: str, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_ingrediente(db, nombre)
    if not obj:
        raise HTTPException(404, "Ingrediente no encontrado")
    return obj


@router.put("/{nombre}", response_model=IngredienteResponse)
async def actualizar_ingrediente(nombre: str, data: IngredienteUpdate, db: AsyncSession = Depends(get_session)):
    obj = await crud.update_ingrediente(db, nombre, data.model_dump())
    if not obj:
        raise HTTPException(404, "Ingrediente no encontrado")
    return obj


@router.delete("/{nombre}")
async def eliminar_ingrediente(nombre: str, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_ingrediente(db, nombre)
    if not ok:
        raise HTTPException(404, "Ingrediente no encontrado")
    return {"mensaje": "Ingrediente eliminado correctamente"}
