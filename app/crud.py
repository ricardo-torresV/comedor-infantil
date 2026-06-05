from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database import models as m


async def create_pagador(db: AsyncSession, data: dict) -> m.Pagador:
    obj = m.Pagador(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_pagador(db: AsyncSession, dni: str) -> m.Pagador | None:
    result = await db.execute(select(m.Pagador).where(m.Pagador.dni == dni))
    return result.scalar_one_or_none()


async def get_pagadores(db: AsyncSession) -> list[m.Pagador]:
    result = await db.execute(select(m.Pagador).order_by(m.Pagador.nombre))
    return list(result.scalars().all())


async def create_persona_autorizada(db: AsyncSession, data: dict) -> m.PersonaAutorizada:
    obj = m.PersonaAutorizada(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_persona_autorizada(db: AsyncSession, dni: str) -> m.PersonaAutorizada | None:
    result = await db.execute(select(m.PersonaAutorizada).where(m.PersonaAutorizada.dni == dni))
    return result.scalar_one_or_none()


async def get_personas_autorizadas(db: AsyncSession) -> list[m.PersonaAutorizada]:
    result = await db.execute(select(m.PersonaAutorizada).order_by(m.PersonaAutorizada.nombre))
    return list(result.scalars().all())


async def create_nino(db: AsyncSession, data: dict) -> m.Nino:
    obj = m.Nino(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_nino(db: AsyncSession, matricula_id: int) -> m.Nino | None:
    result = await db.execute(select(m.Nino).where(m.Nino.matricula_id == matricula_id))
    return result.scalar_one_or_none()


async def get_ninos(db: AsyncSession) -> list[m.Nino]:
    result = await db.execute(select(m.Nino).order_by(m.Nino.nombre))
    return list(result.scalars().all())


async def create_nino_autorizado(db: AsyncSession, nino_matricula: int, dni: str) -> m.NinoAutorizado:
    obj = m.NinoAutorizado(nino_matricula=nino_matricula, autorizado_dni=dni)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def create_ingrediente(db: AsyncSession, data: dict) -> m.Ingrediente:
    obj = m.Ingrediente(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_ingredientes(db: AsyncSession) -> list[m.Ingrediente]:
    result = await db.execute(select(m.Ingrediente).order_by(m.Ingrediente.nombre))
    return list(result.scalars().all())


async def create_plato(db: AsyncSession, data: dict) -> m.Plato:
    obj = m.Plato(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_platos(db: AsyncSession) -> list[m.Plato]:
    result = await db.execute(select(m.Plato).order_by(m.Plato.nombre))
    return list(result.scalars().all())


async def create_menu(db: AsyncSession, data: dict) -> m.Menu:
    obj = m.Menu(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_menus(db: AsyncSession) -> list[m.Menu]:
    result = await db.execute(select(m.Menu).order_by(m.Menu.numero))
    return list(result.scalars().all())


async def create_menu_plato(db: AsyncSession, menu_numero: int, plato_nombre: str) -> m.MenuPlato:
    obj = m.MenuPlato(menu_numero=menu_numero, plato_nombre=plato_nombre)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def create_plato_ingrediente(db: AsyncSession, plato_nombre: str, ingrediente_nombre: str) -> m.PlatoIngrediente:
    obj = m.PlatoIngrediente(plato_nombre=plato_nombre, ingrediente_nombre=ingrediente_nombre)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def update_ingrediente(db: AsyncSession, nombre_actual: str, data: dict) -> m.Ingrediente | None:
    obj = await get_ingrediente(db, nombre_actual)
    if not obj:
        return None
    for key, val in data.items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_ingrediente(db: AsyncSession, nombre: str) -> bool:
    obj = await get_ingrediente(db, nombre)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_ingrediente(db: AsyncSession, nombre: str) -> m.Ingrediente | None:
    result = await db.execute(select(m.Ingrediente).where(m.Ingrediente.nombre == nombre))
    return result.scalar_one_or_none()


async def get_plato(db: AsyncSession, nombre: str) -> m.Plato | None:
    result = await db.execute(select(m.Plato).where(m.Plato.nombre == nombre))
    return result.scalar_one_or_none()


async def update_plato(db: AsyncSession, nombre_actual: str, data: dict) -> m.Plato | None:
    obj = await get_plato(db, nombre_actual)
    if not obj:
        return None
    for key, val in data.items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_plato(db: AsyncSession, nombre: str) -> bool:
    obj = await get_plato(db, nombre)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_ingredientes_por_plato(db: AsyncSession, plato_nombre: str) -> list[m.Ingrediente]:
    result = await db.execute(
        select(m.Ingrediente)
        .join(m.PlatoIngrediente, m.PlatoIngrediente.ingrediente_nombre == m.Ingrediente.nombre)
        .where(m.PlatoIngrediente.plato_nombre == plato_nombre)
        .order_by(m.Ingrediente.nombre)
    )
    return list(result.scalars().all())


async def delete_plato_ingrediente(db: AsyncSession, plato_nombre: str, ingrediente_nombre: str) -> bool:
    result = await db.execute(
        select(m.PlatoIngrediente).where(
            m.PlatoIngrediente.plato_nombre == plato_nombre,
            m.PlatoIngrediente.ingrediente_nombre == ingrediente_nombre,
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_menu(db: AsyncSession, numero: int) -> m.Menu | None:
    result = await db.execute(select(m.Menu).where(m.Menu.numero == numero))
    return result.scalar_one_or_none()


async def update_menu(db: AsyncSession, numero_actual: int, data: dict) -> m.Menu | None:
    obj = await get_menu(db, numero_actual)
    if not obj:
        return None
    for key, val in data.items():
        setattr(obj, key, val)
    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_menu(db: AsyncSession, numero: int) -> bool:
    obj = await get_menu(db, numero)
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_platos_por_menu(db: AsyncSession, menu_numero: int) -> list[m.Plato]:
    result = await db.execute(
        select(m.Plato)
        .join(m.MenuPlato, m.MenuPlato.plato_nombre == m.Plato.nombre)
        .where(m.MenuPlato.menu_numero == menu_numero)
        .order_by(m.Plato.nombre)
    )
    return list(result.scalars().all())


async def delete_menu_plato(db: AsyncSession, menu_numero: int, plato_nombre: str) -> bool:
    result = await db.execute(
        select(m.MenuPlato).where(
            m.MenuPlato.menu_numero == menu_numero,
            m.MenuPlato.plato_nombre == plato_nombre,
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def get_autorizados_por_nino(db: AsyncSession, matricula_id: int) -> list[m.PersonaAutorizada]:
    result = await db.execute(
        select(m.PersonaAutorizada)
        .join(m.NinoAutorizado, m.NinoAutorizado.autorizado_dni == m.PersonaAutorizada.dni)
        .where(m.NinoAutorizado.nino_matricula == matricula_id)
        .order_by(m.PersonaAutorizada.nombre)
    )
    return list(result.scalars().all())


async def delete_nino_autorizado(db: AsyncSession, matricula_id: int, dni: str) -> bool:
    result = await db.execute(
        select(m.NinoAutorizado).where(
            m.NinoAutorizado.nino_matricula == matricula_id,
            m.NinoAutorizado.autorizado_dni == dni,
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def create_alergia(db: AsyncSession, nino_matricula: int, ingrediente_nombre: str) -> m.Alergia:
    obj = m.Alergia(nino_matricula=nino_matricula, ingrediente_nombre=ingrediente_nombre)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_alergias_nino(db: AsyncSession, nino_matricula: int) -> list[m.Alergia]:
    result = await db.execute(
        select(m.Alergia).where(m.Alergia.nino_matricula == nino_matricula)
    )
    return list(result.scalars().all())


async def delete_alergia(db: AsyncSession, nino_matricula: int, ingrediente_nombre: str) -> bool:
    result = await db.execute(
        select(m.Alergia).where(
            m.Alergia.nino_matricula == nino_matricula,
            m.Alergia.ingrediente_nombre == ingrediente_nombre,
        )
    )
    obj = result.scalar_one_or_none()
    if not obj:
        return False
    await db.delete(obj)
    await db.commit()
    return True


async def create_comida(db: AsyncSession, data: dict) -> m.Comida:
    obj = m.Comida(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_comidas_nino(db: AsyncSession, nino_matricula: int) -> list[m.Comida]:
    result = await db.execute(
        select(m.Comida).where(m.Comida.nino_matricula == nino_matricula).order_by(m.Comida.fecha)
    )
    return list(result.scalars().all())
