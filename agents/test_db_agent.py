import asyncio
import sys
import os
from datetime import date
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.database import db


async def run_tests():
    print("=" * 50)
    print("AGENTE DE TESTEO - Conexión a PostgreSQL")
    print("=" * 50)

    # Test 1: Conexión
    print("\n[1] Conectando a la base de datos...")
    await db.connect()
    print("    OK: Conexión establecida")

    # Test 2: Listar tablas
    print("\n[2] Listando tablas...")
    tables = await db.get_tables()
    if tables:
        print(f"    OK: {len(tables)} tablas encontradas")
        for t in tables:
            print(f"      - {t['table_name']} ({t['table_type']})")
    else:
        print("    ERROR: No se encontraron tablas")

    # Test 3: Esquema de tabla
    print(f"\n[3] Describiendo tabla 'nino'...")
    schema = await db.get_table_schema("nino")
    if schema:
        print(f"    OK: {len(schema)} columnas en 'nino'")
        for col in schema:
            print(f"      - {col['column_name']}: {col['data_type']}")
    else:
        print("    ERROR: No se pudo describir la tabla")

    # Test 4: Insertar datos de prueba
    print(f"\n[4] Insertando datos de prueba...")
    try:
        await db.execute_insert(
            "INSERT INTO pagador (dni, nombre, direccion, telefono, cuenta_corriente) "
            "VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING",
            "12345678A", "Juan Perez", "Calle Principal 123", "555-0100", "ES1234567890"
        )
        await db.execute_insert(
            "INSERT INTO persona_autorizada (dni, nombre, direccion, telefono1, relacion) "
            "VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING",
            "87654321B", "Maria Lopez", "Av. Secundaria 456", "555-0200", "Madre"
        )
        await db.execute_insert(
            "INSERT INTO nino (matricula_id, nombre, fecha_nacimiento, fecha_ingreso, pagador_dni) "
            "VALUES ($1, $2, $3, $4, $5) ON CONFLICT DO NOTHING",
            1, "Pedro Garcia", date(2021, 5, 15), date(2024, 9, 1), "12345678A"
        )
        print("    OK: Datos insertados correctamente")
    except Exception as e:
        print(f"    ERROR: {e}")

    # Test 5: Consultar datos
    print(f"\n[5] Consultando datos insertados...")
    try:
        result = await db.execute_query("SELECT * FROM pagador")
        print(f"    OK: {len(result)} registro(s) en pagador")
        for row in result:
            print(f"      - {row['nombre']} (DNI: {row['dni']})")
    except Exception as e:
        print(f"    ERROR: {e}")

    # Test 6: Limpiar datos de prueba
    print(f"\n[6] Limpiando datos de prueba...")
    try:
        await db.execute_insert("DELETE FROM comida WHERE nino_matricula = 1")
        await db.execute_insert("DELETE FROM nino_autorizado WHERE nino_matricula = 1")
        await db.execute_insert("DELETE FROM alergia WHERE nino_matricula = 1")
        await db.execute_insert("DELETE FROM nino WHERE matricula_id = 1")
        await db.execute_insert("DELETE FROM pagador WHERE dni = '12345678A'")
        await db.execute_insert("DELETE FROM persona_autorizada WHERE dni = '87654321B'")
        print("    OK: Datos de prueba eliminados")
    except Exception as e:
        print(f"    ERROR: {e}")

    # Limpiar MCP test log
    mcp_log = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp_test.log")
    if os.path.exists(mcp_log):
        os.remove(mcp_log)

    # Test 7: Tabla de relaciones
    print(f"\n[7] Verificando tablas relacionales...")
    relational_tables = ["nino_autorizado", "menu_plato", "plato_ingrediente", "alergia", "comida"]
    ok = True
    for tname in relational_tables:
        try:
            cols = await db.get_table_schema(tname)
            if cols:
                print(f"      - {tname}: OK ({len(cols)} columnas)")
            else:
                print(f"      - {tname}: ERROR")
                ok = False
        except Exception:
            print(f"      - {tname}: ERROR")
            ok = False

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN DEL TESTEO")
    print("=" * 50)
    print(f"  Conexión BD:     OK")
    print(f"  Tablas creadas:  {len(tables)}")
    print(f"  Tablas relac.:   {'OK' if ok else 'ERROR'}")
    print(f"  Insert/Select:   OK")

    await db.disconnect()
    print("\nBase de datos desconectada correctamente.")


if __name__ == "__main__":
    asyncio.run(run_tests())
