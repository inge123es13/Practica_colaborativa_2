import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


class Conexion:

    @staticmethod
    def obtener_conexion():
        try:
            conexion = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT")
            )

            return conexion

        except Exception as error:
            print("Error al conectar con PostgreSQL:")
            print(error)

            return None