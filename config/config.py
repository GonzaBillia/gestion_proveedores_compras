import os
from dotenv import load_dotenv

# Carga las variables de entorno del archivo .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

P_DB_HOST = os.getenv("P_DB_HOST")
P_DB_PORT = os.getenv("P_DB_PORT")
P_DB_USER = os.getenv("P_DB_USER")
P_DB_PASSWORD = os.getenv("P_DB_PASSWORD")
P_DB_DATABASE = os.getenv("P_DB_DATABASE")