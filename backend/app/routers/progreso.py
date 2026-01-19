from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
import backend.app.models as models
import backend.app.schemas as schemas

router = APIRouter(
	prefix="/progreso",
	tags=["progreso"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para progreso-----

# Obtener todos los progresos
@router.get("/", response_model=list[schemas.ProgresoOut])
def get_progresos(db: Session = Depends(get_db)):
	return db.query(models.Progreso).all()

# Obtener un progreso por ID
@router.get("/{progreso_id}", response_model=schemas.ProgresoOut)
def get_progreso(progreso_id: int, db: Session = Depends(get_db)):
	progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
	if not progreso:
		raise HTTPException(status_code=404, detail="Progreso no encontrado")
	return progreso

# Crear un progreso
@router.post("/", response_model=schemas.ProgresoOut)
def create_progreso(progreso: schemas.ProgresoCreate, db: Session = Depends(get_db)):
	db_progreso = models.Progreso(**progreso.dict())
	db.add(db_progreso)
	db.commit()
	db.refresh(db_progreso)
	return db_progreso

# Actualizar un progreso
@router.put("/{progreso_id}", response_model=schemas.ProgresoOut)
def update_progreso(progreso_id: int, progreso: schemas.ProgresoCreate, db: Session = Depends(get_db)):
	db_progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
	if not db_progreso:
		raise HTTPException(status_code=404, detail="Progreso no encontrado")
	for key, value in progreso.dict().items():
		setattr(db_progreso, key, value)
	db.commit()
	db.refresh(db_progreso)
	return db_progreso

# Eliminar un progreso
@router.delete("/{progreso_id}")
def delete_progreso(progreso_id: int, db: Session = Depends(get_db)):
	progreso = db.query(models.Progreso).filter(models.Progreso.id == progreso_id).first()
	if not progreso:
		raise HTTPException(status_code=404, detail="Progreso no encontrado")
	db.delete(progreso)
	db.commit()
	return {"ok": True, "msg": "Progreso eliminado"}
