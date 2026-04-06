class AntiSpamManager:
    def __init__(self, activity_repository):
        self.repo = activity_repository

    def check_limit(self, user_id: str, category_id: str) -> bool:
        # Lógica: Máximo 2 actividades de la misma categoría por día
        daily_logs = self.repo.count_today_logs(user_id, category_id)
        if daily_logs >= 2:
            raise ValueError("Límite diario alcanzado para esta categoría.")
        return True

class ValidationManager:
    @staticmethod
    def validate_evidence(photo_url: str):
        if not photo_url or not photo_url.startswith("https://"):
            raise ValueError("Se requiere evidencia fotográfica válida.")