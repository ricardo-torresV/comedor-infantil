import asyncio
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.database import db

AGENT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agent.md")


def load_agent_md() -> str:
    with open(AGENT_PATH, encoding="utf-8") as f:
        return f.read()


def save_agent_md(content: str):
    with open(AGENT_PATH, "w", encoding="utf-8") as f:
        f.write(content)


async def get_db_status() -> dict:
    await db.connect()
    tables = await db.get_tables()
    table_names = [t["table_name"] for t in tables]
    schemas = {}
    for t in table_names:
        schemas[t] = await db.get_table_schema(t)
    await db.disconnect()
    return {"tables": table_names, "schemas": schemas}


RULES = {
    "ninos": {
        "label": "Niños (Matrícula)",
        "rules": [
            "número de matrícula, nombre, fecha de nacimiento, fecha de ingreso",
            "fecha de baja (solo si aplica)",
            "CRUD completo en backend y frontend",
            "frontend: listado con scroll (10 filas), panel de detalle, registro de nuevo niño",
        ],
        "tables": ["nino"],
        "endpoints": ["POST /ninos/", "GET /ninos/", "GET /ninos/{id}", "GET /lista-ninos (UI)"],
        "implemented": True,
    },
    "autorizados": {
        "label": "Personas Autorizadas para Recoger",
        "rules": [
            "DNI, nombre, dirección, al menos un teléfono de contacto",
            "relación: vínculo con el niño (familiar/conocido)",
            "pueden ser también las personas que pagan",
            "asignación/desasignación desde el detalle del niño en UI",
            "creación inline desde el panel de detalle",
        ],
        "tables": ["persona_autorizada", "nino_autorizado"],
        "endpoints": ["POST /personas-autorizadas/", "GET /personas-autorizadas/", "GET /personas-autorizadas/{dni}", "POST /ninos/{id}/autorizados", "GET /ninos/{id}/autorizados", "DELETE /ninos/{id}/autorizados/{dni}"],
        "implemented": True,
    },
    "pagadores": {
        "label": "Personas que Abonan (Pagadores)",
        "rules": [
            "DNI, nombre, dirección, teléfono, número de cuenta corriente",
            "pueden estar autorizadas para recoger al niño",
            "creación inline desde el formulario de registro de niño",
        ],
        "tables": ["pagador"],
        "endpoints": ["POST /pagadores/", "GET /pagadores/", "GET /pagadores/{dni}"],
        "implemented": True,
    },
    "menus": {
        "label": "Menús, Platos e Ingredientes",
        "rules": [
            "Menú identificado por un número, compuesto por varios platos",
            "Plato caracterizado por su nombre",
            "Ingrediente caracterizado por su nombre",
            "CRUD completo con interfaz unificada SPA en /platos",
            "asignación/desasignación de ingredientes a platos y platos a menús",
        ],
        "tables": ["menu", "plato", "ingrediente", "menu_plato", "plato_ingrediente"],
        "endpoints": ["POST /menus/", "GET /menus/", "GET /menus/{numero}", "PUT /menus/{numero}", "DELETE /menus/{numero}", "POST /menus/{numero}/platos", "GET /menus/{numero}/platos", "DELETE /menus/{numero}/platos/{plato}", "POST /platos/", "GET /platos/", "GET /platos/{nombre}", "PUT /platos/{nombre}", "DELETE /platos/{nombre}", "POST /platos/{nombre}/ingredientes", "GET /platos/{nombre}/ingredientes", "DELETE /platos/{nombre}/ingredientes/{ingrediente}", "POST /ingredientes/", "GET /ingredientes/", "GET /ingredientes/{nombre}", "PUT /ingredientes/{nombre}", "DELETE /ingredientes/{nombre}", "GET /platos (UI)"],
        "implemented": True,
    },
    "alergias": {
        "label": "Alergias",
        "rules": [
            "niño alérgico a ciertos ingredientes",
            "no puede consumir platos con dichos ingredientes",
            "control obligatorio para evitar intoxicaciones",
            "gestión desde el panel de detalle del niño en UI",
        ],
        "tables": ["alergia"],
        "endpoints": ["POST /alergias/", "GET /alergias/{nino_id}", "DELETE /alergias/{nino_id}/{ingrediente}"],
        "implemented": True,
    },
    "coste": {
        "label": "Coste Mensual",
        "rules": [
            "coste fijo mensual + coste de comidas realizadas",
            "coste de comidas: número de días que el niño comió",
            "controlar número de días que cada niño come",
            "registrar qué menú consumió cada niño cada día",
        ],
        "tables": ["comida"],
        "endpoints": ["POST /comidas/", "GET /comidas/{nino_id}"],
        "implemented": True,
    },
    "auth": {
        "label": "Autenticación",
        "rules": [
            "acceso protegido con JWT",
            "usuario administrador único",
            "contraseñas hasheadas con bcrypt",
            "protección de rutas en frontend (redirección a /login si no hay token)",
        ],
        "tables": ["usuario"],
        "endpoints": ["POST /auth/login", "POST /auth/setup-admin", "GET /auth/me"],
        "implemented": True,
    },
}


def generate_report(db_status: dict) -> str:
    lines = []
    lines.append("# Reporte de Implementacion")
    lines.append(f"Generado: {date.today()}\n")
    lines.append("## Resumen")
    total = len(RULES)
    implemented = sum(1 for r in RULES.values() if r["implemented"])
    lines.append(f"- Reglas de negocio: {implemented}/{total} implementadas")
    lines.append(f"- Tablas en BD: {len(db_status['tables'])}")
    lines.append("")

    for key, rule in RULES.items():
        icon = "[OK]" if rule["implemented"] else "[--]"
        lines.append(f"### {icon} {rule['label']}")
        for r in rule["rules"]:
            status = "[OK]" if rule["implemented"] else "[--]"
            lines.append(f"  - {status} {r}")
        tb_ok = all(t in db_status["tables"] for t in rule["tables"])
        lines.append(f"  - {'[OK]' if tb_ok else '[XX]'} Tablas: {', '.join(rule['tables'])}")
        lines.append("")

    return "\n".join(lines)


def update_agent_md_with_status():
    md = load_agent_md()
    status_lines = [
        "",
        "## Estado de Implementacion",
        f"*Actualizado: {date.today()}*",
        "",
    ]
    for key, rule in RULES.items():
        icon = "[OK]" if rule["implemented"] else "[--]"
        status_lines.append(f"- {icon} **{rule['label']}**")

    if "## Estado de Implementacion" in md:
        md = re.sub(r"## Estado de Implementacion.*?(?=\n## |\Z)", "\n".join(status_lines), md, flags=re.DOTALL)
    else:
        md += "\n" + "\n".join(status_lines)

    save_agent_md(md)
    return md


async def main():
    print("=" * 55)
    print(" BUSINESS RULES AGENT - Seguimiento de Implementacion")
    print("=" * 55)

    print("\n[1] Conectando a la base de datos...")
    db_status = await get_db_status()
    print(f"    {len(db_status['tables'])} tablas encontradas: {', '.join(db_status['tables'])}")

    print("\n[2] Generando reporte de implementacion...")
    report = generate_report(db_status)
    print(report)

    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "reporte_implementacion.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n[3] Reporte guardado en: database/reporte_implementacion.md")

    print("\n[4] Actualizando agent.md con estado...")
    update_agent_md_with_status()
    print("    agent.md actualizado")

    print("\n" + "=" * 55)
    print(" AGENTE FINALIZADO")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())
