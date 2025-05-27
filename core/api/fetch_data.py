import requests
from core.config import Settings
from datetime import datetime, timedelta

settings = Settings()


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
    Генерация списка дат с 2023-01-01 по настоящее время
    :return: список дат
    """
    start_date = datetime.today().strftime("2023-01-01")
    start = datetime.strptime(start_date, "%Y-%m-%d")
    today = datetime.today()

    return [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((today - start).days + 1)
    ]


if __name__ == "__main__":
    client = APIClient()
    dates = generate_date_list()
    for date_str in dates:
        params = {"date": date_str}
        data = client.fetch_data("data", param=params)
        print(data)
