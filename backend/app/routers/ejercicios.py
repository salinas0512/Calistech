from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
import backend.app.models as models
import backend.app.schemas as schemas

router = APIRouter(
	prefix="/ejercicios",
	tags=["ejercicios"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para ejercicios-----

# Obtener todos los ejercicios
@router.get("/", response_model=list[schemas.EjercicioOut])
def get_ejercicios(db: Session = Depends(get_db)):
	return db.query(models.Ejercicio).all()

# Obtener un ejercicio por ID
@router.get("/{ejercicio_id}", response_model=schemas.EjercicioOut)
def get_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
	ejercicio = db.query(models.Ejercicio).filter(models.Ejercicio.id == ejercicio_id).first()
	if not ejercicio:
		raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
	return ejercicio

# Crear un ejercicio
@router.post("/", response_model=schemas.EjercicioOut)
def create_ejercicio(ejercicio: schemas.EjercicioCreate, db: Session = Depends(get_db)):
	db_ejercicio = models.Ejercicio(**ejercicio.dict())
	db.add(db_ejercicio)
	db.commit()
	db.refresh(db_ejercicio)
	return db_ejercicio

# Actualizar un ejercicio
@router.put("/{ejercicio_id}", response_model=schemas.EjercicioOut)
def update_ejercicio(ejercicio_id: int, ejercicio: schemas.EjercicioCreate, db: Session = Depends(get_db)):
	db_ejercicio = db.query(models.Ejercicio).filter(models.Ejercicio.id == ejercicio_id).first()
	if not db_ejercicio:
		raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
	for key, value in ejercicio.dict().items():
		setattr(db_ejercicio, key, value)
	db.commit()
	db.refresh(db_ejercicio)
	return db_ejercicio

# Eliminar un ejercicio
@router.delete("/{ejercicio_id}")
def delete_ejercicio(ejercicio_id: int, db: Session = Depends(get_db)):
	ejercicio = db.query(models.Ejercicio).filter(models.Ejercicio.id == ejercicio_id).first()
	if not ejercicio:
		raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
	db.delete(ejercicio)
	db.commit()
	return {"ok": True, "msg": "Ejercicio eliminado"}
