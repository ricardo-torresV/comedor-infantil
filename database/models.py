from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Text, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Pagador(Base):
    __tablename__ = "pagador"
    dni = Column(String(20), primary_key=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text, nullable=False)
    telefono = Column(String(20), nullable=False)
    cuenta_corriente = Column(String(50), nullable=False)

    ninos = relationship("Nino", back_populates="pagador")


class PersonaAutorizada(Base):
    __tablename__ = "persona_autorizada"
    dni = Column(String(20), primary_key=True)
    nombre = Column(String(150), nullable=False)
    direccion = Column(Text, nullable=False)
    telefono1 = Column(String(20), nullable=False)
    telefono2 = Column(String(20))
    relacion = Column(String(100), nullable=False)

    ninos = relationship("Nino", secondary="nino_autorizado", back_populates="autorizados")


class Nino(Base):
    __tablename__ = "nino"
    matricula_id = Column(Integer, primary_key=True)
    nombre = Column(String(150), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    fecha_baja = Column(Date)
    pagador_dni = Column(String(20), ForeignKey("pagador.dni"), nullable=False)

    pagador = relationship("Pagador", back_populates="ninos")
    autorizados = relationship("PersonaAutorizada", secondary="nino_autorizado", back_populates="ninos")
    alergias = relationship("Ingrediente", secondary="alergia", back_populates="ninos_alergicos")
    comidas = relationship("Comida", back_populates="nino")


class NinoAutorizado(Base):
    __tablename__ = "nino_autorizado"
    nino_matricula = Column(Integer, ForeignKey("nino.matricula_id"), primary_key=True)
    autorizado_dni = Column(String(20), ForeignKey("persona_autorizada.dni"), primary_key=True)


class Ingrediente(Base):
    __tablename__ = "ingrediente"
    nombre = Column(String(100), primary_key=True)

    platos = relationship("Plato", secondary="plato_ingrediente", back_populates="ingredientes")
    ninos_alergicos = relationship("Nino", secondary="alergia", back_populates="alergias")


class Plato(Base):
    __tablename__ = "plato"
    nombre = Column(String(100), primary_key=True)

    ingredientes = relationship("Ingrediente", secondary="plato_ingrediente", back_populates="platos")
    menus = relationship("Menu", secondary="menu_plato", back_populates="platos")


class Menu(Base):
    __tablename__ = "menu"
    numero = Column(Integer, primary_key=True)

    platos = relationship("Plato", secondary="menu_plato", back_populates="menus")
    comidas = relationship("Comida", back_populates="menu")


class MenuPlato(Base):
    __tablename__ = "menu_plato"
    menu_numero = Column(Integer, ForeignKey("menu.numero"), primary_key=True)
    plato_nombre = Column(String(100), ForeignKey("plato.nombre"), primary_key=True)


class PlatoIngrediente(Base):
    __tablename__ = "plato_ingrediente"
    plato_nombre = Column(String(100), ForeignKey("plato.nombre"), primary_key=True)
    ingrediente_nombre = Column(String(100), ForeignKey("ingrediente.nombre"), primary_key=True)


class Alergia(Base):
    __tablename__ = "alergia"
    nino_matricula = Column(Integer, ForeignKey("nino.matricula_id"), primary_key=True)
    ingrediente_nombre = Column(String(100), ForeignKey("ingrediente.nombre"), primary_key=True)


class Comida(Base):
    __tablename__ = "comida"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nino_matricula = Column(Integer, ForeignKey("nino.matricula_id"), nullable=False)
    fecha = Column(Date, nullable=False)
    menu_numero = Column(Integer, ForeignKey("menu.numero"), nullable=False)

    __table_args__ = (UniqueConstraint("nino_matricula", "fecha"),)

    nino = relationship("Nino", back_populates="comidas")
    menu = relationship("Menu", back_populates="comidas")


class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
