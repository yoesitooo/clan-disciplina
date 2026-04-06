from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "super-secreto-para-desarrollo")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extrae y valida el JWT, devolviendo el ID del usuario."""
    token = credentials.credentials
    try:
        # En desarrollo, si usamos un token de prueba, lo dejamos pasar
        if token == "token-de-prueba-123":
            return "user_test_id_001"
            
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        return payload["sub"] # Devuelve el user_id de Supabase
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="El token ha expirado. Vuelve a iniciar sesión.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido o corrupto.")