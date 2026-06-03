from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import MenuCreate, MenuResponse, MenuPlatoCreate
from app import crud

router = APIRouter(prefix="/menus", tags=["Menús"])


@router.post("/", response_model=MenuResponse)
async def crear_menu(data: MenuCreate, db: AsyncSession = Depends(get_session)):
    return await crud.create_menu(db, data.model_dump())


@router.get("/", response_model=list[MenuResponse])
async def listar_menus(db: AsyncSession = Depends(get_session)):
    return await crud.get_menus(db)


@router.post("/{numero}/platos", response_model=dict)
async def asignar_plato(
    numero: int, data: MenuPlatoCreate, db: AsyncSession = Depends(get_session)
):
    await crud.create_menu_plato(db, numero, data.plato_nombre)
    return {"mensaje": "Plato asignado al menú correctamente"}
