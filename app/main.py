from fastapi import FastAPI, Depends
from app.auth import get_current_user
from app.routers import (
    auth,
    pagador,
    persona_autorizada,
    nino,
    menu,
    plato,
    ingrediente,
    alergia,
    comida,
)

app = FastAPI(
    title="Comedor Infantil API",
    description="API para gestionar niños, pagadores, menús y comidas de una guardería",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(pagador.router, dependencies=[Depends(get_current_user)])
app.include_router(persona_autorizada.router, dependencies=[Depends(get_current_user)])
app.include_router(nino.router, dependencies=[Depends(get_current_user)])
app.include_router(menu.router, dependencies=[Depends(get_current_user)])
app.include_router(plato.router, dependencies=[Depends(get_current_user)])
app.include_router(ingrediente.router, dependencies=[Depends(get_current_user)])
app.include_router(alergia.router, dependencies=[Depends(get_current_user)])
app.include_router(comida.router, dependencies=[Depends(get_current_user)])


@app.get("/")
async def root():
    return {"mensaje": "Comedor Infantil API - v0.1.0"}
