import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("¡Faltan credenciales de Supabase! Revisa tu archivo .env")

# Instancia de conexión global
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)