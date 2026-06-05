from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.schemas import AlergiaCreate
from app import crud

router = APIRouter(prefix="/alergias", tags=["Alergias"])


@router.post("/", response_model=dict)
async def crear_alergia(data: AlergiaCreate, db: AsyncSession = Depends(get_session)):
    nino = await crud.get_nino(db, data.nino_matricula)
    if not nino:
        raise HTTPException(404, "Niño no encontrado")
    await crud.create_alergia(db, data.nino_matricula, data.ingrediente_nombre)
    return {"mensaje": "Alergia registrada correctamente"}


@router.delete("/{nino_matricula}/{ingrediente_nombre}", response_model=dict)
async def eliminar_alergia(
    nino_matricula: int, ingrediente_nombre: str, db: AsyncSession = Depends(get_session)
):
    ok = await crud.delete_alergia(db, nino_matricula, ingrediente_nombre)
    if not ok:
        raise HTTPException(404, "La alergia no existe")
    return {"mensaje": "Alergia eliminada correctamente"}


@router.get("/{nino_matricula}", response_model=list[dict])
async def listar_alergias_nino(nino_matricula: int, db: AsyncSession = Depends(get_session)):
    alergias = await crud.get_alergias_nino(db, nino_matricula)
    return [{"ingrediente_nombre": a.ingrediente_nombre} for a in alergias]
