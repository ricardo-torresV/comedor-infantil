from fastapi import FastAPI
from app.routers import (
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

app.include_router(pagador.router)
app.include_router(persona_autorizada.router)
app.include_router(nino.router)
app.include_router(menu.router)
app.include_router(plato.router)
app.include_router(ingrediente.router)
app.include_router(alergia.router)
app.include_router(comida.router)


@app.get("/")
async def root():
    return {"mensaje": "Comedor Infantil API - v0.1.0"}
