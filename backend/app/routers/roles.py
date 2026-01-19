from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
import backend.app.models as models
import backend.app.schemas as schemas

router = APIRouter(
	prefix="/roles",
	tags=["roles"]
)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# -----Endpoints para roles-----

# Obtener todos los roles
@router.get("/", response_model=list[schemas.RolOut])
def get_roles(db: Session = Depends(get_db)):
	return db.query(models.Rol).all()

# Obtener un rol por ID
@router.get("/{rol_id}", response_model=schemas.RolOut)
def get_rol(rol_id: int, db: Session = Depends(get_db)):
	rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
	if not rol:
		raise HTTPException(status_code=404, detail="Rol no encontrado")
	return rol

# Crear un rol
@router.post("/", response_model=schemas.RolOut)
def create_rol(rol: schemas.RolCreate, db: Session = Depends(get_db)):
	db_rol = models.Rol(**rol.dict())
	db.add(db_rol)
	db.commit()
	db.refresh(db_rol)
	return db_rol

# Actualizar un rol
@router.put("/{rol_id}", response_model=schemas.RolOut)
def update_rol(rol_id: int, rol: schemas.RolCreate, db: Session = Depends(get_db)):
	db_rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
	if not db_rol:
		raise HTTPException(status_code=404, detail="Rol no encontrado")
	for key, value in rol.dict().items():
		setattr(db_rol, key, value)
	db.commit()
	db.refresh(db_rol)
	return db_rol

# Eliminar un rol
@router.delete("/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
	rol = db.query(models.Rol).filter(models.Rol.id == rol_id).first()
	if not rol:
		raise HTTPException(status_code=404, detail="Rol no encontrado")
	db.delete(rol)
	db.commit()
	return {"ok": True, "msg": "Rol eliminado"}
