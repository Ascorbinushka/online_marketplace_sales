from pydantic_settings import BaseSettings
import psycopg2
import dotenv

dotenv.load_dotenv()


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DATABASE: str
    API_BASE_URL: str
    A_HOST: str


class DatabaseConnection:
    __instance = None

    @staticmethod
    def get_instance(host: str):
        if not DatabaseConnection.__instance:
            DatabaseConnection(host)
        return DatabaseConnection.__instance

    def __init__(self, host: str):
        if DatabaseConnection.__instance:
            raise Exception(
                "Класс является Singleton, используйте метод get_instance()"
            )
        else:
            if host == "airflow":
                self.connection = psycopg2.connect(
                    database=settings.PG_DATABASE,
                    user=settings.PG_USER,
                    password=settings.PG_PASSWORD,
                    host=settings.A_HOST,
                    port=settings.PG_PORT,
                )
            elif host == "localhost":
                self.connection = psycopg2.connect(
                    database=settings.PG_DATABASE,
                    user=settings.PG_USER,
                    password=settings.PG_PASSWORD,
                    host=settings.PG_HOST,
                    port=settings.PG_PORT,
                )
            DatabaseConnection.__instance = self

    def get_connection(self):
        return self.connection


try:
    settings = Settings()
except Exception as e:
    exit(f"error in module: {__name__}: {e}")

if __name__ == "__main__":
    db_connection = DatabaseConnection.get_instance(host='localhost')
    print(db_connection)
