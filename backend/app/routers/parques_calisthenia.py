from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
import backend.app.models as models
import backend.app.schemas as schemas

router = APIRouter(
	prefix="/parques_calisthenia",
	tags=["parques_calisthenia"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para parques de calistenia-----

# Obtener todos los parques
@router.get("/", response_model=list[schemas.ParqueCalistheniaOut])
def get_parques(db: Session = Depends(get_db)):
	return db.query(models.ParqueCalisthenia).all()

# Obtener un parque por ID
@router.get("/{parque_id}", response_model=schemas.ParqueCalistheniaOut)
def get_parque(parque_id: int, db: Session = Depends(get_db)):
	parque = db.query(models.ParqueCalisthenia).filter(models.ParqueCalisthenia.id == parque_id).first()
	if not parque:
		raise HTTPException(status_code=404, detail="Parque no encontrado")
	return parque

# Crear un parque
@router.post("/", response_model=schemas.ParqueCalistheniaOut)
def create_parque(parque: schemas.ParqueCalistheniaCreate, db: Session = Depends(get_db)):
	db_parque = models.ParqueCalisthenia(**parque.dict())
	db.add(db_parque)
	db.commit()
	db.refresh(db_parque)
	return db_parque

# Actualizar un parque
@router.put("/{parque_id}", response_model=schemas.ParqueCalistheniaOut)
def update_parque(parque_id: int, parque: schemas.ParqueCalistheniaCreate, db: Session = Depends(get_db)):
	db_parque = db.query(models.ParqueCalisthenia).filter(models.ParqueCalisthenia.id == parque_id).first()
	if not db_parque:
		raise HTTPException(status_code=404, detail="Parque no encontrado")
	for key, value in parque.dict().items():
		setattr(db_parque, key, value)
	db.commit()
	db.refresh(db_parque)
	return db_parque

# Eliminar un parque
@router.delete("/{parque_id}")
def delete_parque(parque_id: int, db: Session = Depends(get_db)):
	parque = db.query(models.ParqueCalisthenia).filter(models.ParqueCalisthenia.id == parque_id).first()
	if not parque:
		raise HTTPException(status_code=404, detail="Parque no encontrado")
	db.delete(parque)
	db.commit()
	return {"ok": True, "msg": "Parque eliminado"}
