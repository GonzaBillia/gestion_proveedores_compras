from dotenv import load_dotenv
import os

import sys

def resource_path(relative_path):
    """Para que funcione tanto en el ejecutable como en dev."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

dotenv_path = resource_path('.env')
load_dotenv(dotenv_path=dotenv_path)

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