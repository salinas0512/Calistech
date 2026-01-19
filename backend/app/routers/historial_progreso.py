from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from .. import schemas

router = APIRouter(
	prefix="/historial_progreso",
	tags=["historial_progreso"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para historial de progreso-----

# Obtener todos los historiales
@router.get("/", response_model=list[schemas.HistorialProgresoOut])
def get_historial(db: Session = Depends(get_db)):
	return db.query(models.HistorialProgreso).all()

# Obtener un historial por ID
@router.get("/{historial_id}", response_model=schemas.HistorialProgresoOut)
def get_historial_id(historial_id: int, db: Session = Depends(get_db)):
	historial = db.query(models.HistorialProgreso).filter(models.HistorialProgreso.id == historial_id).first()
	if not historial:
		raise HTTPException(status_code=404, detail="Historial no encontrado")
	return historial

# Crear un historial
@router.post("/", response_model=schemas.HistorialProgresoOut)
def create_historial(historial: schemas.HistorialProgresoCreate, db: Session = Depends(get_db)):
	db_historial = models.HistorialProgreso(**historial.dict())
	db.add(db_historial)
	db.commit()
	db.refresh(db_historial)
	return db_historial

# Actualizar un historial
@router.put("/{historial_id}", response_model=schemas.HistorialProgresoOut)
def update_historial(historial_id: int, historial: schemas.HistorialProgresoCreate, db: Session = Depends(get_db)):
	db_historial = db.query(models.HistorialProgreso).filter(models.HistorialProgreso.id == historial_id).first()
	if not db_historial:
		raise HTTPException(status_code=404, detail="Historial no encontrado")
	for key, value in historial.dict().items():
		setattr(db_historial, key, value)
	db.commit()
	db.refresh(db_historial)
	return db_historial

# Eliminar un historial
@router.delete("/{historial_id}")
def delete_historial(historial_id: int, db: Session = Depends(get_db)):
	historial = db.query(models.HistorialProgreso).filter(models.HistorialProgreso.id == historial_id).first()
	if not historial:
		raise HTTPException(status_code=404, detail="Historial no encontrado")
	db.delete(historial)
	db.commit()
	return {"ok": True, "msg": "Historial eliminado"}
