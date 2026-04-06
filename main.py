from fastapi import FastAPI
from app.api.routers import activities

app = FastAPI(
    title="Clan Disciplina API",
    description="Backend para plataforma gamificada de hábitos",
    version="1.0.0"
)

# Conectamos las rutas de actividades
app.include_router(activities.router)

@app.get("/")
def root_health_check():
    return {"status": "ok", "message": "Motor del Clan Disciplina en línea y conectado."}