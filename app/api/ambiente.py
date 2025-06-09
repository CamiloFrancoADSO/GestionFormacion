from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.ambiente import AmbienteCreate, AmbienteUpdate, AmbienteOut
from app.crud import ambiente as crud_ambiente
from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.users import UserOut  

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_ambiente(
    ambiente: AmbienteCreate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        crud_ambiente.create_ambiente(db, ambiente)
        return {"message": "Ambiente creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-by-centro", response_model=List[AmbienteOut])
def get_ambiente_by_centro(
    cod_centro: int,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    try:
        ambiente = crud_ambiente.get_ambiente_by_centro(db, cod_centro)
        if not ambiente:
            raise HTTPException(status_code=404, detail="No se encontraron ambientes")
        return ambiente
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{ambiente_id}")
def update_ambiente(
    ambiente_id: int,
    ambiente: AmbienteUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.id_rol != 1:
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    try:
        success = crud_ambiente.update_ambiente(db, ambiente_id, ambiente)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el ambiente")
        return {"message": "Ambiente actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
