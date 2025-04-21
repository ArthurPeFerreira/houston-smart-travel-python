import psycopg2

# Dados de conexão com o banco
conn = psycopg2.connect(
    host="hst-db.ctq0w4i4kk5c.us-east-1.rds.amazonaws.com",        # ou IP do servidor
    database="hst_db",    # nome do banco
    user="hst_db",      # nome do usuário
    password="DGzeu1Ce7l43oWGGEeRx"   # senha do usuário
)

# Cria um cursor
database_cursor = conn.cursor()