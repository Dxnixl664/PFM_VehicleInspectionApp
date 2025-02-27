from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.base import engine
from database import models as db

from api.endpoints import reports, users, auth

db.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vehicle Inspection API",
    description="API para la gestión de reportes de inspección de vehículos",
    version="1.0.0",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (en producción, especificar dominios)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

# Incluir routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Vehicle Inspection API running. Go to /docs for the API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)