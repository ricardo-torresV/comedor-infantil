from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import MenuCreate, MenuResponse, MenuUpdate, MenuPlatoCreate
from app import crud

router = APIRouter(prefix="/menus", tags=["Menús"])


@router.post("/", response_model=MenuResponse)
async def crear_menu(data: MenuCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_menu(db, data.model_dump())


@router.get("/", response_model=list[MenuResponse])
async def listar_menus(db: AsyncSession = Depends(get_session)):
    return await crud.get_menus(db)


@router.get("/{numero}", response_model=MenuResponse)
async def obtener_menu(numero: int, db: AsyncSession = Depends(get_session)):
    obj = await crud.get_menu(db, numero)
    if not obj:
        raise HTTPException(404, "Menú no encontrado")
    return obj


@router.put("/{numero}", response_model=MenuResponse)
async def actualizar_menu(numero: int, data: MenuUpdate, db: AsyncSession = Depends(get_session)):
    obj = await crud.update_menu(db, numero, data.model_dump())
    if not obj:
        raise HTTPException(404, "Menú no encontrado")
    return obj


@router.delete("/{numero}")
async def eliminar_menu(numero: int, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_menu(db, numero)
    if not ok:
        raise HTTPException(404, "Menú no encontrado")
    return {"mensaje": "Menú eliminado correctamente"}


@router.get("/{numero}/platos", response_model=list[str])
async def listar_platos_menu(numero: int, db: AsyncSession = Depends(get_session)):
    menu = await crud.get_menu(db, numero)
    if not menu:
        raise HTTPException(404, "Menú no encontrado")
    platos = await crud.get_platos_por_menu(db, numero)
    return [p.nombre for p in platos]


@router.post("/{numero}/platos", response_model=dict)
async def asignar_plato(
    numero: int, data: MenuPlatoCreate, db: AsyncSession = Depends(get_session)
):
    await crud.create_menu_plato(db, numero, data.plato_nombre)
    return {"mensaje": "Plato asignado al menú correctamente"}


@router.delete("/{numero}/platos/{plato_nombre}")
async def eliminar_plato_menu(numero: int, plato_nombre: str, db: AsyncSession = Depends(get_session)):
    ok = await crud.delete_menu_plato(db, numero, plato_nombre)
    if not ok:
        raise HTTPException(404, "Relación menú-plato no encontrada")
    return {"mensaje": "Plato eliminado del menú correctamente"}
