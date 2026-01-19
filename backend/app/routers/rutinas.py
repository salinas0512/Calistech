from fastapi import APIRouter, Depends, HTTPException
from  ..import auth
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from .. import schemas

router = APIRouter(
	prefix="/rutinas",
	tags=["rutinas"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para rutinas-----

# Obtener todas las rutinas
@router.get("/", response_model=list[schemas.RutinaOut])
def get_rutinas(db: Session = Depends(get_db)):
	return db.query(models.Rutina).all()

# Obtener solo las rutinas del usuario autenticado
@router.get("/personales", response_model=list[schemas.RutinaOut])
def get_rutinas_personales(
	db: Session = Depends(get_db),
	current_user: models.Usuario = Depends(auth.get_current_user)
):
	return db.query(models.Rutina).filter(models.Rutina.usuario_id == current_user.id).all()

# Obtener una rutina por ID
@router.get("/{rutina_id}", response_model=schemas.RutinaOut)
def get_rutina(rutina_id: int, db: Session = Depends(get_db)):
	rutina = db.query(models.Rutina).filter(models.Rutina.id == rutina_id).first()
	if not rutina:
		raise HTTPException(status_code=404, detail="Rutina no encontrada")
	return rutina

# Crear una rutina
@router.post("/", response_model=schemas.RutinaOut)
def create_rutina(rutina: schemas.RutinaCreate, db: Session = Depends(get_db)):
	db_rutina = models.Rutina(**rutina.dict())
	db.add(db_rutina)
	db.commit()
	db.refresh(db_rutina)
	return db_rutina

# Actualizar una rutina
@router.put("/{rutina_id}", response_model=schemas.RutinaOut)
def update_rutina(rutina_id: int, rutina: schemas.RutinaCreate, db: Session = Depends(get_db)):
	db_rutina = db.query(models.Rutina).filter(models.Rutina.id == rutina_id).first()
	if not db_rutina:
		raise HTTPException(status_code=404, detail="Rutina no encontrada")
	for key, value in rutina.dict().items():
		setattr(db_rutina, key, value)
	db.commit()
	db.refresh(db_rutina)
	return db_rutina

# Eliminar una rutina
@router.delete("/{rutina_id}")
def delete_rutina(rutina_id: int, db: Session = Depends(get_db)):
	rutina = db.query(models.Rutina).filter(models.Rutina.id == rutina_id).first()
	if not rutina:
		raise HTTPException(status_code=404, detail="Rutina no encontrada")
	db.delete(rutina)
	db.commit()
	return {"ok": True, "msg": "Rutina eliminada"}
