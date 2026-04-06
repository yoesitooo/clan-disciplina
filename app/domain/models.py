from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Category(BaseModel):
    id: str
    name: str  # Ej: Estudio, Gym, Comida Sana, Ahorro
    base_xp: int
    is_variable: bool = False

class Rank(BaseModel):
    name: str # Iron, Bronze, Silver...
    min_xp: int
    max_xp: Optional[int] = None

class UserProfile(BaseModel):
    user_id: str
    username: str
    avatar_url: Optional[str] = None
    total_xp: int = 0
    current_rank: str = "Iron"
    
    def add_xp(self, xp: int):
        self.total_xp += xp

class ActivityLog(BaseModel):
    id: str
    user_id: str
    category_id: str
    photo_url: str
    xp_awarded: int
    created_at: datetime = Field(default_factory=datetime.utcnow)