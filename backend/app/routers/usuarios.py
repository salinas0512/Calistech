from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
from .. import schemas
from .. import auth

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----Endpoints para usuarios-----

# Registro público de usuario (sin autenticación)
@router.post("/registro", response_model=schemas.UsuarioOut)
def register_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    usuario_dict = usuario.dict()
    contrasena = usuario_dict.get("contrasena")
    if not isinstance(contrasena, str) or not contrasena or len(contrasena) > 72:
        raise HTTPException(status_code=400, detail="La contraseña debe ser un string de 5 a 72 caracteres.")
    usuario_dict["contrasena"] = auth.get_password_hash(contrasena[:72])
    db_usuario = models.Usuario(**usuario_dict)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Obtener todos los usuarios
@router.get("/", response_model=list[schemas.UsuarioOut])
def get_usuarios(db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.require_admin)):
    return db.query(models.Usuario).all()

# Obtener un usuario por ID
@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.get_current_user)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    # Solo el propio usuario o admin puede ver el perfil
    if current_user.id != usuario_id and (not current_user.rol or current_user.rol.nombre != "administrador"):
        raise HTTPException(status_code=403, detail="Acceso denegado")
    return usuario

# Crear un usuario

@router.post("/", response_model=schemas.UsuarioOut)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.require_admin)):
    usuario_dict = usuario.dict()
    contrasena = usuario_dict.get("contrasena")
    if not isinstance(contrasena, str) or not contrasena or len(contrasena) > 72:
        raise HTTPException(status_code=400, detail="La contraseña debe ser un string de 5 a 72 caracteres.")
    usuario_dict["contrasena"] = auth.get_password_hash(contrasena[:72])
    db_usuario = models.Usuario(**usuario_dict)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Eliminar un usuario
@router.delete("/{usuario_id}")
def delete_usuario(usuario_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.require_admin)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return {"ok": True, "msg": "Usuario eliminado"}

# Actualizar un usuario
@router.put("/{usuario_id}", response_model=schemas.UsuarioOut)
def update_usuario(usuario_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(auth.require_admin)):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in usuario.dict().items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario