import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL")
DATABASE_USER =  os.getenv("DATABASE_USER")
DATABASE_PASSWORD =  os.getenv("DATABASE_PASSWORD")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")

# Dados de conexão com o banco
conn = psycopg2.connect(
    host=DATABASE_URL,        # ou IP do servidor
    database=DATABASE_SCHEMA,    # nome do banco
    user=DATABASE_USER,      # nome do usuário
    password=DATABASE_PASSWORD  # senha do usuário
)

# Cria um cursor
database_cursor = conn.cursor()