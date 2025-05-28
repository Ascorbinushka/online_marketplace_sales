import requests
from core.config import Settings, DatabaseConnection
from datetime import datetime, timedelta
from core.database.database_operations import Purchases
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
settings = Settings()
db_connection = DatabaseConnection.get_instance()


class APIClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL

    def fetch_data(self, endpoint, param=None) -> list:
        """
        Получение информации о продажах крупного онлайн-маркетплейса
        """
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.get(url, params=param)
            if response.status_code == 200:
                return response.json()
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")


def generate_date_list() -> list:
    """
    Генерация списка дат с 2023-01-01 по вчерашнюю дату
    :return: список дат
    """
    start_date = datetime.today().strftime("2023-01-01")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    today = datetime.today()

    return [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((today - start).days)
    ]


def filling_historical_data():
    purchases = Purchases(db_connection)
    client = APIClient()
    dates = generate_date_list()
    for date_str in dates:
        params = {"date": date_str}
        data = client.fetch_data("data", param=params)
        for record in data:
            gender_id = purchases.get_gender_id(gender=record["gender"])
            purchases.insert_stock(
                client_id=record["client_id"],
                gender_id=gender_id,
                purchase_datetime=record["purchase_datetime"],
                purchase_time_as_seconds_from_midnight=record[
                    "purchase_time_as_seconds_from_midnight"
                ],
                product_id=record["product_id"],
                quantity=record["quantity"],
                price_per_item=record["price_per_item"],
                discount_per_item=record["discount_per_item"],
                total_price=record["total_price"],
            )


if __name__ == "__main__":
    filling_historical_data()
