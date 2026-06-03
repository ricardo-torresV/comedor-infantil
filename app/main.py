import os
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
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


@app.get("/nuevo-nino", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def nuevo_nino_page():
    return _html("nuevo_nino.html")


app.include_router(nino.router, dependencies=[Depends(get_current_user)])
app.include_router(menu.router, dependencies=[Depends(get_current_user)])
app.include_router(plato.router, dependencies=[Depends(get_current_user)])
app.include_router(ingrediente.router, dependencies=[Depends(get_current_user)])
app.include_router(alergia.router, dependencies=[Depends(get_current_user)])
app.include_router(comida.router, dependencies=[Depends(get_current_user)])


TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def _html(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, encoding="utf-8") as f:
        return f.read()


@app.get("/")
async def root():
    return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    return _html("login.html")


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page():
    return _html("dashboard.html")


@app.get("/ninos", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def ninos_page():
    return _html("ninos.html")


@app.get("/platos", response_class=HTMLResponse)
async def platos_page():
    return _html("platos.html")


@app.get("/tarifas", response_class=HTMLResponse)
async def tarifas_page():
    return _html("tarifas.html")
