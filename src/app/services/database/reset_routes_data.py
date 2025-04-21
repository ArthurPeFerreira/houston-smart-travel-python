from src.app.services.database.connection import database_cursor

def reset_routes_data():
    try:
        database_cursor.execute('TRUNCATE hst_schema."RoutesData" RESTART IDENTITY CASCADE')
        database_cursor.connection.commit()
        print("Tabela RoutesData resetada com sucesso.")
    except Exception as e:
        print(f"Erro ao resetar RoutesData: {e}")
