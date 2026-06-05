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
| v0.7.0 | 2026-06-05 | CRUD completo ingredientes/platos/menús con UI unificada SPA en /platos + panel de detalle de niños con gestión de autorizados y alergias + 18 niños de prueba |

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

## Frontend — Rutas

| Ruta | Descripción |
|------|-------------|
| `/login` | Login con JWT |
| `/dashboard` | Dashboard principal con 3 secciones |
| `/nuevo-nino` | Formulario de registro de niño (con creación inline de pagador) |
| `/lista-ninos` | Listado de niños con scroll (10 filas), panel de detalle con información general, personas autorizadas (creación inline + consulta) y alergias |
| `/platos` | SPA unificada: CRUD ingredientes, platos, menús + asignación/desasignación |

## Estructura del Proyecto

```
Comedor_Infantil/
├── agents/                    # Agentes autónomos
│   ├── test_db_agent.py       # Test de conexión y operaciones BD
│   ├── business_rules_agent.py# Seguimiento de reglas de negocio
│   └── git_push_agent.py      # Subida automática a GitHub
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

## Endpoints API

### Niños
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/ninos/` | Crear niño |
| GET | `/ninos/` | Listar todos |
| GET | `/ninos/{id}` | Obtener por matrícula |
| GET | `/ninos/{id}/autorizados` | Personas autorizadas del niño |
| POST | `/ninos/{id}/autorizados` | Asignar persona autorizada |
| DELETE | `/ninos/{id}/autorizados/{dni}` | Desasignar persona autorizada |

### Personas Autorizadas
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/personas-autorizadas/` | Crear |
| GET | `/personas-autorizadas/` | Listar todas |
| GET | `/personas-autorizadas/{dni}` | Obtener por DNI |

### Pagadores
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/pagadores/` | Crear |
| GET | `/pagadores/` | Listar todos |
| GET | `/pagadores/{dni}` | Obtener por DNI |

### Ingredientes
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/ingredientes/` | Crear |
| GET | `/ingredientes/` | Listar todos |
| GET | `/ingredientes/{nombre}` | Obtener por nombre |
| PUT | `/ingredientes/{nombre}` | Actualizar |
| DELETE | `/ingredientes/{nombre}` | Eliminar |

### Platos
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/platos/` | Crear |
| GET | `/platos/` | Listar todos |
| GET | `/platos/{nombre}` | Obtener por nombre |
| PUT | `/platos/{nombre}` | Actualizar |
| DELETE | `/platos/{nombre}` | Eliminar |
| POST | `/platos/{nombre}/ingredientes` | Asignar ingrediente |
| GET | `/platos/{nombre}/ingredientes` | Ingredientes del plato |
| DELETE | `/platos/{nombre}/ingredientes/{ing}` | Desasignar ingrediente |

### Menús
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/menus/` | Crear |
| GET | `/menus/` | Listar todos |
| GET | `/menus/{numero}` | Obtener por número |
| PUT | `/menus/{numero}` | Actualizar |
| DELETE | `/menus/{numero}` | Eliminar |
| POST | `/menus/{numero}/platos` | Asignar plato |
| GET | `/menus/{numero}/platos` | Platos del menú |
| DELETE | `/menus/{numero}/platos/{plato}` | Desasignar plato |

### Alergias
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/alergias/` | Registrar alergia |
| GET | `/alergias/{nino_id}` | Alergias del niño |
| DELETE | `/alergias/{nino_id}/{ingrediente}` | Eliminar alergia |

### Comidas
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/comidas/` | Registrar comida |
| GET | `/comidas/{nino_id}` | Comidas del niño |

### Autenticación
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/auth/login` | Iniciar sesión |
| POST | `/auth/setup-admin` | Crear admin inicial |
| GET | `/auth/me` | Perfil del usuario |
