
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .routers import historial_progreso
from .routers import parques_calisthenia
from .routers import ejercicios
from .routers import usuarios
from .routers import rutinas
from .routers import rutina_ejercicios
from .routers import progreso   
from .routers import roles
from .routers import auth


app = FastAPI()

# Configuración de CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Se ajusta en producción por dominio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(usuarios.router)
app.include_router(ejercicios.router)
app.include_router(rutinas.router)
app.include_router(rutina_ejercicios.router)
app.include_router(progreso.router)
app.include_router(historial_progreso.router)
app.include_router(parques_calisthenia.router)
app.include_router(roles.router)
app.include_router(auth.router)



@app.get("/")
def lectura_root():
    return {"message": "API funcionando correctamente con CORS"}
