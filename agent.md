# Comedor Infantil - Sistema de Control de Gastos

## Reglas de Negocio

### 1. Niños (Matrícula)
- **Datos**: número de matrícula, nombre, fecha de nacimiento, fecha de ingreso
- **Baja**: fecha de baja (solo si aplica)

### 2. Personas Autorizadas para Recoger
- **Datos**: DNI, nombre, dirección, al menos un teléfono de contacto
- **Relación**: debe quedar constancia del vínculo con el niño (familiar/conocido)
- Pueden ser también las personas que pagan

### 3. Personas que Abonan (Pagadores)
- **Datos**: DNI, nombre, dirección, teléfono, número de cuenta corriente (para cargo)
- Pueden estar autorizadas para recoger al niño

### 4. Menús, Platos e Ingredientes
- **Menú**: identificado por un número, compuesto por varios platos
- **Plato**: caracterizado por su nombre
- **Ingrediente**: caracterizado por su nombre

### 5. Alergias
- Un niño puede ser alérgico a ciertos ingredientes
- No puede consumir platos que contengan dichos ingredientes
- Control obligatorio para evitar intoxicaciones

### 6. Coste Mensual
- **Cálculo**: coste fijo mensual + coste de comidas realizadas
- **Coste de comidas**: número de días que el niño comió en la guardería
- Se debe controlar el número de días que cada niño come
- Se debe registrar qué menú consumió cada niño cada día

## Stack Tecnológico
- **Base de datos**: PostgreSQL 18
- **Backend**: Python 3.13 + FastAPI
- **ORM**: SQLAlchemy 2.0 (async) + asyncpg
- **Autenticación**: JWT + bcrypt
- **Frontend**: HTML + CSS (colores cálidos)
- **MCP**: Model Context Protocol para conexión con BD

## Estado de Implementacion
*Actualizado: 2026-06-03*

- [OK] **Niños (Matrícula)**
- [OK] **Personas Autorizadas para Recoger**
- [OK] **Personas que Abonan (Pagadores)**
- [OK] **Menús, Platos e Ingredientes**
- [OK] **Alergias**
- [OK] **Coste Mensual**
- [OK] **Autenticación**