from app.infrastructure.supabase_client import supabase
from app.domain.models import UserProfile, Category

class ProfileRepository:
    """Se encarga de hablar con la tabla 'profiles'"""
    
    @staticmethod
    def get_profile(user_id: str) -> UserProfile:
        response = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
        if not response.data:
            raise ValueError("Perfil no encontrado")
            
        data = response.data[0]
        return UserProfile(**data) # Convierte el diccionario a nuestro modelo Python

    @staticmethod
    def update_profile(profile: UserProfile):
        # Actualizamos la base de datos con los nuevos XP y Rango
        supabase.table("profiles").update({
            "total_xp": profile.total_xp,
            "current_rank": profile.current_rank
        }).eq("user_id", profile.user_id).execute()


class CategoryRepository:
    """Se encarga de leer la tabla 'categories'"""
    
    @staticmethod
    def get_category(category_id: str) -> Category:
        response = supabase.table("categories").select("*").eq("id", category_id).execute()
        if not response.data:
            raise ValueError(f"La categoría {category_id} no existe")
            
        data = response.data[0]
        return Category(**data)