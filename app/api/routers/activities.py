from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# Importamos lo que construimos
from app.core.security import get_current_user
from app.infrastructure.repositories import ProfileRepository, CategoryRepository
from app.application.services import RankService, ValidationManager

router = APIRouter(prefix="/activities", tags=["Activities"])

# Lo que esperamos recibir del Frontend (Next.js)
class ActivityCreateRequest(BaseModel):
    category_id: str
    photo_url: str

@router.post("/log")
def log_activity(
    request: ActivityCreateRequest,
    user_id: str = Depends(get_current_user) # 🔒 Esto exige el JWT y saca el ID
):
    try:
        # 1. Validar que la foto sea una URL de verdad
        ValidationManager.validate_evidence(request.photo_url)
        
        # 2. Buscar la categoría en la base de datos (Ej: "estudio")
        category = CategoryRepository.get_category(request.category_id)
        
        # 3. Buscar el perfil del usuario
        try:
            profile = ProfileRepository.get_profile(user_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Perfil no encontrado en la base de datos")

        # 4. Sumar los XP
        profile.add_xp(category.base_xp)
        
        # 5. Calcular si subió de rango
        new_rank = RankService.calculate_rank(profile.total_xp)
        profile.current_rank = new_rank
        
        # 6. Guardar los cambios en Supabase
        ProfileRepository.update_profile(profile)
        
        # (Aquí en el futuro guardaremos también el ActivityLog en su tabla)

        return {
            "message": "¡Actividad registrada con éxito!",
            "xp_earned": category.base_xp,
            "new_total_xp": profile.total_xp,
            "current_rank": profile.current_rank
        }

    except ValueError as e:
        # Si el ValidationManager detecta trampa, mandamos error al frontend
        raise HTTPException(status_code=400, detail=str(e))