-- Tabla: Pagador (persona que abona el coste mensual)
CREATE TABLE IF NOT EXISTS pagador (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    cuenta_corriente VARCHAR(50) NOT NULL
);

-- Tabla: PersonaAutorizada (puede recoger al niño)
CREATE TABLE IF NOT EXISTS persona_autorizada (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion TEXT NOT NULL,
    telefono1 VARCHAR(20) NOT NULL,
    telefono2 VARCHAR(20),
    relacion VARCHAR(100) NOT NULL
);

-- Tabla: Niño
CREATE TABLE IF NOT EXISTS nino (
    matricula_id INTEGER PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_baja DATE,
    pagador_dni VARCHAR(20) NOT NULL REFERENCES pagador(dni)
);

-- Relación N:M Niño - PersonaAutorizada
CREATE TABLE IF NOT EXISTS nino_autorizado (
    nino_matricula INTEGER NOT NULL REFERENCES nino(matricula_id),
    autorizado_dni VARCHAR(20) NOT NULL REFERENCES persona_autorizada(dni),
    PRIMARY KEY (nino_matricula, autorizado_dni)
);

-- Tabla: Ingrediente
CREATE TABLE IF NOT EXISTS ingrediente (
    nombre VARCHAR(100) PRIMARY KEY
);

-- Tabla: Plato
CREATE TABLE IF NOT EXISTS plato (
    nombre VARCHAR(100) PRIMARY KEY
);

-- Tabla: Menú
CREATE TABLE IF NOT EXISTS menu (
    numero INTEGER PRIMARY KEY
);

-- Relación N:M Menú - Plato
CREATE TABLE IF NOT EXISTS menu_plato (
    menu_numero INTEGER NOT NULL REFERENCES menu(numero),
    plato_nombre VARCHAR(100) NOT NULL REFERENCES plato(nombre),
    PRIMARY KEY (menu_numero, plato_nombre)
);

-- Relación N:M Plato - Ingrediente
CREATE TABLE IF NOT EXISTS plato_ingrediente (
    plato_nombre VARCHAR(100) NOT NULL REFERENCES plato(nombre),
    ingrediente_nombre VARCHAR(100) NOT NULL REFERENCES ingrediente(nombre),
    PRIMARY KEY (plato_nombre, ingrediente_nombre)
);

-- Tabla: Alergia (niño alérgico a un ingrediente)
CREATE TABLE IF NOT EXISTS alergia (
    nino_matricula INTEGER NOT NULL REFERENCES nino(matricula_id),
    ingrediente_nombre VARCHAR(100) NOT NULL REFERENCES ingrediente(nombre),
    PRIMARY KEY (nino_matricula, ingrediente_nombre)
);

-- Tabla: Comida (registro diario de qué menú consumió cada niño)
CREATE TABLE IF NOT EXISTS comida (
    id SERIAL PRIMARY KEY,
    nino_matricula INTEGER NOT NULL REFERENCES nino(matricula_id),
    fecha DATE NOT NULL,
    menu_numero INTEGER NOT NULL REFERENCES menu(numero),
    UNIQUE (nino_matricula, fecha)
);

-- Tabla: Usuario (autenticación)
CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
