from fastapi import FastAPI
# Esta es la ruta "a prueba de balas"
from app.api.routers.activities import router as activities_router

app = FastAPI(
    title="Clan Disciplina API",
    description="Backend para plataforma gamificada de hábitos",
    version="1.0.0"
)

# Conectamos las rutas
app.include_router(activities_router)

@app.get("/")
def root_health_check():
    return {"status": "ok", "message": "Motor del Clan Disciplina en línea y conectado."}