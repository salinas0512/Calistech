from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from .. import schemas

router = APIRouter(
	prefix="/rutina_ejercicios",
	tags=["rutina_ejercicios"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para rutina_ejercicios-----

# Obtener todos los rutina_ejercicios
@router.get("/", response_model=list[schemas.RutinaEjercicioOut])
def get_rutina_ejercicios(db: Session = Depends(get_db)):
	return db.query(models.RutinaEjercicio).all()

# Obtener un rutina_ejercicio por ID
@router.get("/{rutina_ejercicio_id}", response_model=schemas.RutinaEjercicioOut)
def get_rutina_ejercicio(rutina_ejercicio_id: int, db: Session = Depends(get_db)):
	rutina_ejercicio = db.query(models.RutinaEjercicio).filter(models.RutinaEjercicio.id == rutina_ejercicio_id).first()
	if not rutina_ejercicio:
		raise HTTPException(status_code=404, detail="RutinaEjercicio no encontrado")
	return rutina_ejercicio

# Crear un rutina_ejercicio
@router.post("/", response_model=schemas.RutinaEjercicioOut)
def create_rutina_ejercicio(rutina_ejercicio: schemas.RutinaEjercicioCreate, db: Session = Depends(get_db)):
	db_rutina_ejercicio = models.RutinaEjercicio(**rutina_ejercicio.dict())
	db.add(db_rutina_ejercicio)
	db.commit()
	db.refresh(db_rutina_ejercicio)
	return db_rutina_ejercicio

# Actualizar un rutina_ejercicio
@router.put("/{rutina_ejercicio_id}", response_model=schemas.RutinaEjercicioOut)
def update_rutina_ejercicio(rutina_ejercicio_id: int, rutina_ejercicio: schemas.RutinaEjercicioCreate, db: Session = Depends(get_db)):
	db_rutina_ejercicio = db.query(models.RutinaEjercicio).filter(models.RutinaEjercicio.id == rutina_ejercicio_id).first()
	if not db_rutina_ejercicio:
		raise HTTPException(status_code=404, detail="RutinaEjercicio no encontrado")
	for key, value in rutina_ejercicio.dict().items():
		setattr(db_rutina_ejercicio, key, value)
	db.commit()
	db.refresh(db_rutina_ejercicio)
	return db_rutina_ejercicio

# Eliminar un rutina_ejercicio
@router.delete("/{rutina_ejercicio_id}")
def delete_rutina_ejercicio(rutina_ejercicio_id: int, db: Session = Depends(get_db)):
	rutina_ejercicio = db.query(models.RutinaEjercicio).filter(models.RutinaEjercicio.id == rutina_ejercicio_id).first()
	if not rutina_ejercicio:
		raise HTTPException(status_code=404, detail="RutinaEjercicio no encontrado")
	db.delete(rutina_ejercicio)
	db.commit()
	return {"ok": True, "msg": "RutinaEjercicio eliminado"}
