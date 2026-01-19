from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# Usuario
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    contrasena: str
    rol_id: Optional[int]

class UsuarioCreate(UsuarioBase):
    contrasena: str = Field(..., min_length=5, max_length=72)

class UsuarioOut(UsuarioBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# Ejercicio
class EjercicioBase(BaseModel):
    nombre: str
    repeticiones: Optional[int]

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioOut(EjercicioBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# HistorialProgreso
class HistorialProgresoBase(BaseModel):
    usuario_id: int
    rutina_id: int
    fecha: date
    estadisticas: Optional[str]

class HistorialProgresoCreate(HistorialProgresoBase):
    pass

class HistorialProgresoOut(HistorialProgresoBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# ParqueCalisthenia
class ParqueCalistheniaBase(BaseModel):
    nombre: str
    latitud: Optional[float]
    longitud: Optional[float]
    comuna: Optional[str]

class ParqueCalistheniaCreate(ParqueCalistheniaBase):
    pass

class ParqueCalistheniaOut(ParqueCalistheniaBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# Progreso
class ProgresoBase(BaseModel):
    usuario_id: int
    rutina_id: int
    duracion: Optional[int]
    esfuerzo: Optional[str]
    notas: Optional[str]
    fecha: date

class ProgresoCreate(ProgresoBase):
    pass

class ProgresoOut(ProgresoBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# Rol
class RolBase(BaseModel):
    nombre: str

class RolCreate(RolBase):
    pass

class RolOut(RolBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

# RutinaEjercicio
class RutinaEjercicioBase(BaseModel):
    rutina_id: int
    ejercicio_id: int
    reps: Optional[int]
    series: Optional[int]

class RutinaEjercicioCreate(RutinaEjercicioBase):
    pass

class RutinaEjercicioOut(RutinaEjercicioBase):
    id: int
    class Config:
        orm_mode = True

# Rutina
class RutinaBase(BaseModel):
    nombre: str
    nivel: Optional[str]
    duracion: Optional[int]
    usuario_id: Optional[int]

class RutinaCreate(RutinaBase):
    pass

class RutinaOut(RutinaBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True
