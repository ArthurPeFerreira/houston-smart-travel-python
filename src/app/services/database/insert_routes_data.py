from psycopg2.extras import execute_values
from src.app.services.database.connection import database_cursor

def insert_routes_data(data):
    sql = 'INSERT INTO hst_schema."RoutesData" ("routeId", "cabinKey", date, direct, "originAirport", "destinationAirport", seats) VALUES %s'

    try:
        execute_values(database_cursor, sql, data)
        database_cursor.connection.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")