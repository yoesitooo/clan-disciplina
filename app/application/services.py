from app.domain.models import Rank

# Definición de rangos
RANKS = [
    Rank(name="Iron", min_xp=0, max_xp=199),
    Rank(name="Bronze", min_xp=200, max_xp=399),
    Rank(name="Silver", min_xp=400, max_xp=599),
    Rank(name="Gold", min_xp=600, max_xp=799),
    Rank(name="Platinum", min_xp=800, max_xp=999),
    Rank(name="Diamond", min_xp=1000, max_xp=1199),
    Rank(name="Master", min_xp=1200, max_xp=1399),
    Rank(name="GrandMaster", min_xp=1400, max_xp=1599),
    Rank(name="Challenger", min_xp=1600, max_xp=None)
]

class RankService:
    @staticmethod
    def calculate_rank(total_xp: int) -> str:
        for rank in RANKS:
            if rank.max_xp is None:
                return rank.name
            if rank.min_xp <= total_xp <= rank.max_xp:
                return rank.name
        return "Iron"

class ValidationManager:
    @staticmethod
    def validate_evidence(photo_url: str):
        if not photo_url or not photo_url.startswith("http"):
            raise ValueError("Se requiere una URL de foto válida.")