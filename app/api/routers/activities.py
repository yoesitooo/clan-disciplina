from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/activities", tags=["Activities"])

# Esquema de entrada para el request
class ActivityCreateRequest(BaseModel):
    category_id: str
    photo_url: str

@router.post("/", response_model=dict)
def create_activity(
    request: ActivityCreateRequest,
    user_id: str = Depends(get_current_user),
    # Las dependencias inyectan los servicios instanciados
    activity_service: ActivityService = Depends(get_activity_service) 
):
    try:
        # Obtener la categoría del repositorio de categorías (simulado aquí)
        category = category_repo.get(request.category_id) 
        
        # Delegar TODO el trabajo al servicio de aplicación
        activity = activity_service.log_activity(
            user_id=user_id, 
            category=category, 
            photo_url=request.photo_url
        )
        return {"status": "success", "activity": activity.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))