from sqlalchemy import Column, Integer, String, DateTime, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Usuario(Base):
    __tablename__ = "usuarios"  
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    rol = relationship("Rol", back_populates="usuarios")

class Ejercicio(Base):
    __tablename__ = "ejercicios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    repeticiones = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class HistorialProgreso(Base):
    __tablename__ = "historial_progreso"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer)
    rutina_id = Column(Integer)
    fecha = Column(Date)
    estadisticas = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class ParqueCalisthenia(Base):
    __tablename__ = "parques_calisthenia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    latitud = Column(Float)
    longitud = Column(Float)
    comuna = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Progreso(Base):
    __tablename__ = "progreso"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer)
    rutina_id = Column(Integer)
    duracion = Column(Integer)
    esfuerzo = Column(String)
    notas = Column(Text)
    fecha = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    usuarios = relationship("Usuario", back_populates="rol")

class RutinaEjercicio(Base):
    __tablename__ = "rutina_ejercicios"
    id = Column(Integer, primary_key=True, index=True)
    rutina_id = Column(Integer)
    ejercicio_id = Column(Integer)
    reps = Column(Integer, nullable=True)
    series = Column(Integer, nullable=True)

class Rutina(Base):
    __tablename__ = "rutinas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nivel = Column(String)
    duracion = Column(Integer)
    usuario_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Prueba simple de consulta
if __name__ == "__main__":
    from database import SessionLocal
    session = SessionLocal()
    try:
        rutinas = session.query(Rutina).all()
        print("Rutinas encontradas:")
        for rutina in rutinas:
            print(f"ID: {rutina.id}, Nombre: {rutina.nombre}, Nivel: {rutina.nivel}, Duracion: {rutina.duracion}")
        if not rutinas:
            print("No hay rutinas en la base de datos.")
    except Exception as e:
        print(f"Error al consultar rutinas: {e}")
    finally:
        session.close()
