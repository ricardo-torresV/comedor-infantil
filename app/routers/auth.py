from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from database.models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticación"])


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario).where(Usuario.username == data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    token = create_access_token(user.username)
    return TokenResponse(access_token=token)


@router.post("/setup-admin", response_model=dict)
async def setup_admin(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Usuario).limit(1))
    if result.scalar_one_or_none():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Ya existe un usuario administrador")
    admin_user = Usuario(
        username="admin",
        password_hash=hash_password("admin123"),
    )
    db.add(admin_user)
    await db.commit()
    return {"mensaje": "Usuario administrador creado. Usuario: admin / Contraseña: admin123"}


@router.get("/me", response_model=dict)
async def me(user: Usuario = Depends(get_current_user)):
    return {"id": user.id, "username": user.username}
