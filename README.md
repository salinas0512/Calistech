# CalisTech
LINK DE APLICACIÓN EN  HOSTING NETLIFY:
https://calistech.netlify.app

Plataforma web para la gestión de rutinas y ejercicios de calistenia.

## Estructura del Proyecto

- **backend/**: API REST construida con FastAPI y SQLAlchemy.
- **frontend/**: Aplicación web desarrollada con Vue 3.

## Instalación y Ejecución

### Backend
1. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar variables de entorno (.env) según el archivo `.env.example`.
4. Ejecutar el servidor:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

### Frontend
1. Instalar dependencias:
   ```bash
   cd frontend/calistech-frontend
   npm install
   ```
2. Ejecutar la aplicación:
   ```bash
   npm run dev
   ```

## Despliegue
- **Backend:** Recomendado en Render. Configura las variables de entorno en el panel de Render.
- **Frontend:** Recomendado en Netlify. Asegúrate de que las URLs de la API apunten al backend desplegado.

## Buenas Prácticas
- No subir archivos sensibles como `.env` ni carpetas como `.venv` o `__pycache__`.
- Usa el archivo `.env.example` para documentar las variables de entorno necesarias.
- Mantén actualizado el archivo `requirements.txt` y el `package.json`.

## Contacto
Para dudas o sugerencias, contacta al autor del repositorio.
