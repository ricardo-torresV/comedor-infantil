from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import PlatoCreate, PlatoResponse, PlatoUpdate, PlatoIngredienteCreate
from app import crud

router = APIRouter(prefix="/platos", tags=["Platos"])


@router.post("/", response_model=PlatoResponse)
async def crear_plato(data: PlatoCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_plato(db, data.model_dump())


@router.get("/", response_model=list[PlatoResponse])
async def listar_platos(db: AsyncSession = Depends(get_session)):
    return await crud.get_platos(db)


@router.get("/{nombre}", response_model=PlatoResponse)
async def obtener_plato(nombre: str, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_plato(db, nombre)
    if not obj:
        raise HTTPException(404, "Plato no encontrado")
    return obj


@router.put("/{nombre}", response_model=PlatoResponse)
async def actualizar_plato(nombre: str, data: PlatoUpdate, db: AsyncSession = Depends(get_session)):
    obj = await crud.update_plato(db, nombre, data.model_dump())
    if not obj:
        raise HTTPException(404, "Plato no encontrado")
    return obj


@router.delete("/{nombre}")
async def eliminar_plato(nombre: str, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_plato(db, nombre)
    if not ok:
        raise HTTPException(404, "Plato no encontrado")
    return {"mensaje": "Plato eliminado correctamente"}


@router.get("/{nombre}/ingredientes", response_model=list[str])
async def listar_ingredientes_plato(nombre: str, db: AsyncSession = Depends(get_session)):
    plato = await crud.get_plato(db, nombre)
    if not plato:
        raise HTTPException(404, "Plato no encontrado")
    ingredientes = await crud.get_ingredientes_por_plato(db, nombre)
    return [i.nombre for i in ingredientes]


@router.post("/{nombre}/ingredientes", response_model=dict)
async def asignar_ingrediente(
    nombre: str, data: PlatoIngredienteCreate, db: AsyncSession = Depends(get_session)
):
    await crud.create_plato_ingrediente(db, nombre, data.ingrediente_nombre)
    return {"mensaje": "Ingrediente asignado al plato correctamente"}


@router.delete("/{nombre}/ingredientes/{ingrediente_nombre}")
async def eliminar_ingrediente_plato(nombre: str, ingrediente_nombre: str, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_plato_ingrediente(db, nombre, ingrediente_nombre)
    if not ok:
        raise HTTPException(404, "Relación plato-ingrediente no encontrada")
    return {"mensaje": "Ingrediente eliminado del plato correctamente"}
