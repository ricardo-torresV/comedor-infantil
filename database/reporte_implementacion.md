# Reporte de Implementacion
Generado: 2026-06-05

## Resumen
- Reglas de negocio: 7/7 implementadas
- Tablas en BD: 12

### [OK] Niños (Matrícula)
  - [OK] número de matrícula, nombre, fecha de nacimiento, fecha de ingreso
  - [OK] fecha de baja (solo si aplica)
  - [OK] CRUD completo en backend y frontend
  - [OK] frontend: listado con scroll (10 filas), panel de detalle, registro de nuevo niño
  - [OK] Tablas: nino

### [OK] Personas Autorizadas para Recoger
  - [OK] DNI, nombre, dirección, al menos un teléfono de contacto
  - [OK] relación: vínculo con el niño (familiar/conocido)
  - [OK] pueden ser también las personas que pagan
  - [OK] asignación/desasignación desde el detalle del niño en UI
  - [OK] creación inline desde el panel de detalle
  - [OK] Tablas: persona_autorizada, nino_autorizado

### [OK] Personas que Abonan (Pagadores)
  - [OK] DNI, nombre, dirección, teléfono, número de cuenta corriente
  - [OK] pueden estar autorizadas para recoger al niño
  - [OK] creación inline desde el formulario de registro de niño
  - [OK] Tablas: pagador

### [OK] Menús, Platos e Ingredientes
  - [OK] Menú identificado por un número, compuesto por varios platos
  - [OK] Plato caracterizado por su nombre
  - [OK] Ingrediente caracterizado por su nombre
  - [OK] CRUD completo con interfaz unificada SPA en /platos
  - [OK] asignación/desasignación de ingredientes a platos y platos a menús
  - [OK] Tablas: menu, plato, ingrediente, menu_plato, plato_ingrediente

### [OK] Alergias
  - [OK] niño alérgico a ciertos ingredientes
  - [OK] no puede consumir platos con dichos ingredientes
  - [OK] control obligatorio para evitar intoxicaciones
  - [OK] gestión desde el panel de detalle del niño en UI
  - [OK] Tablas: alergia

### [OK] Coste Mensual
  - [OK] coste fijo mensual + coste de comidas realizadas
  - [OK] coste de comidas: número de días que el niño comió
  - [OK] controlar número de días que cada niño come
  - [OK] registrar qué menú consumió cada niño cada día
  - [OK] Tablas: comida

### [OK] Autenticación
  - [OK] acceso protegido con JWT
  - [OK] usuario administrador único
  - [OK] contraseñas hasheadas con bcrypt
  - [OK] protección de rutas en frontend (redirección a /login si no hay token)
  - [OK] Tablas: usuario
