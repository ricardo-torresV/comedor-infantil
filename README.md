# Comedor Infantil

Sistema de control de gastos para guardería. Gestión de niños, pagadores, menús, comidas y alergias.

## Stack Tecnológico

- **Backend**: Python 3.13 + FastAPI
- **Base de datos**: PostgreSQL 18
- **Autenticación**: JWT + bcrypt
- **ORM**: SQLAlchemy 2.0 (async) + asyncpg
- **Frontend**: HTML + CSS (colores cálidos)
- **MCP**: Model Context Protocol para PostgreSQL

## Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| v0.1.0 | 2026-06-03 | Initial commit: MCP server + PostgreSQL connection |
| v0.2.0 | 2026-06-03 | DB schema: 11 tablas (niños, pagadores, autorizados, menús, platos, ingredientes, alergias, comidas) |
| v0.3.0 | 2026-06-03 | FastAPI CRUD API para todas las tablas |
| v0.4.0 | 2026-06-03 | Autenticación JWT + bcrypt + usuario admin |
| v0.5.0 | 2026-06-03 | Interfaz gráfica de login y dashboard con colores cálidos |
| v0.6.0 | 2026-06-03 | Dashboard con 3 secciones (niños, platos, tarifas) + formulario registro de niños |

## Instalación

```powershell
# Clonar
git clone <repo-url>
cd Comedor_Infantil

# Entorno virtual
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Configurar BD en .env
# DATABASE_URL=postgresql+asyncpg://postgres:@localhost:5432/comedor_infantil

# Ejecutar schema
Get-Content database\schema.sql | psql -U postgres -h localhost -d comedor_infantil

# Crear admin
curl -X POST http://localhost:8000/auth/setup-admin

# Iniciar servidor
.venv\Scripts\uvicorn app.main:app --reload
```

## Ejecutar Tests

```powershell
.venv\Scripts\python agents\test_db_agent.py
.venv\Scripts\python agents\business_rules_agent.py
```

## Estructura del Proyecto

```
Comedor_Infantil/
├── agents/                    # Agentes autónomos
│   ├── test_db_agent.py       # Test de conexión y operaciones BD
│   └── business_rules_agent.py# Seguimiento de reglas de negocio
├── app/                       # API FastAPI
│   ├── main.py
│   ├── auth.py                # JWT + bcrypt
│   ├── database.py            # SQLAlchemy async
│   ├── schemas.py             # Pydantic models
│   ├── crud.py                # CRUD operations
│   ├── routers/               # Endpoints por entidad
│   └── templates/             # HTML templates
├── database/                  # Modelos y schemas SQL
│   ├── schema.sql
│   ├── models.py
│   └── reporte_implementacion.md
├── mcp_server/                # MCP server para PostgreSQL
├── agent.md                   # Reglas de negocio
└── requirements.txt
```
