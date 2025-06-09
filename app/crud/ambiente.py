from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from app.core.security import get_hashed_password
from app.schemas.users import UserCreate, UserUpdate
from app.schemas.ambiente import AmbienteCreate, AmbienteUpdate
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)
# almacena errores



def create_ambiente(db: Session, ambiente: AmbienteCreate) -> Optional[bool]:
    try:
        ambiente_data = ambiente.model_dump()

        query = text("""
            INSERT INTO ambiente_formacion (
                nombre_ambiente, num_max_aprendices, municipio,
                ubicacion, cod_centro,estado
            ) VALUES (
                :nombre_ambiente, :num_max_aprendices, :municipio,
                :ubicacion, :cod_centro, :estado
            )
        """)
        db.execute(query, ambiente_data)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear ambiente: {e}")
        raise Exception("Error de base de datos al crear el ambiente")



def get_ambiente_by_id(db: Session, id_ambiente: int):
    try:
        query = text("""SELECT id_ambiente,nombre_ambiente, num_max_aprendices, municipio,
                        ubicacion, cod_centro,estado
                     FROM ambiente_formacion 
                     WHERE id_ambiente = :id""")
        result = db.execute(query, {"id": id_ambiente}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener ambiente por id: {e}")
        raise Exception("Error de base de datos al obtener el ambiente")
    


def update_ambiente(db: Session, ambiente_id: int, ambiente_update: AmbienteUpdate) -> bool:
    try:
        fields = ambiente_update.model_dump(exclude_unset=True)
        if not fields:
            return False
        set_clause = ", ".join([f"{key} = :{key}" for key in fields])
        fields["ambiente_id"] = ambiente_id

        query = text(f"UPDATE ambiente_formacion SET {set_clause} WHERE id_ambiente = :ambiente_id")
        db.execute(query, fields)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar ambiente: {e}")
        raise Exception("Error de base de datos al actualizar el ambiente")
    


def modify_status_ambiente(db:Session,ambiente_id:int):
    try:
        query = text("""
                        UPDATE ambiente_formacion SET estado = IF(estado, FALSE, TRUE) WHERE id_ambiente = :id
                     """)
        result = db.execute(query,{"id":ambiente_id})
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al modificar el estado del ambiente: {e}")
        raise Exception("Error de base de datos al  modificar el estado del ambiente")
    


def get_ambiente_by_centro(db: Session, cod_centro: int):
    try:
        query = text("""
            SELECT id_ambiente,nombre_ambiente, num_max_aprendices, municipio,
                    ubicacion, cod_centro,estado
            FROM ambiente_formacion 
            WHERE cod_centro = :cod_centro
        """)
        result = db.execute(query, {"cod_centro": cod_centro}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener los ambientes por cod_centro: {e}")
        raise Exception("Error de base de datos al obtener los ambientes")
    


def get_ambiente_by_centro_and_ubicacion(db: Session, cod_centro: int, ubicacion: str):
    try:
        query = text("""
            SELECT id_ambiente, nombre_ambiente, num_max_aprendices, municipio,
                   ubicacion, cod_centro, estado
            FROM ambiente_formacion 
            WHERE cod_centro = :cod_centro AND ubicacion = :ubicacion
        """)
        result = db.execute(query, {"cod_centro": cod_centro,"ubicacion": ubicacion}).mappings().all()

        if not result:
            raise Exception("No se encuentran relaciones entre el código del centro y su ubicación.")
        
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener los ambientes por cod_centro: {e}")
        raise Exception("Error de base de datos al obtener los ambientes")
