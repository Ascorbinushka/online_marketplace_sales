from core.database.database_operations import Purchases
from core.config import DatabaseConnection
from core.api.fetch_data import APIClient
from datetime import datetime, timedelta


def get_data_sales():
    # Получаем текущую дату и время
    now = datetime.now()

    # Вычитаем один день из текущей даты
    yesterday = now - timedelta(days=1)

    # Форматируем дату в строку в формате "YYYY-MM-DD"
    date_str = yesterday.strftime("%Y-%m-%d")
    client = APIClient()
    params = {"date": date_str}
    return client.fetch_data("data", param=params)


def load_data_to_pg(data):
    db_connection = DatabaseConnection.get_instance(host="airflow")
    purchases = Purchases(db_connection)

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


def main():
    data = get_data_sales()
    # load_data_to_pg(data)
    print(data)


if __name__ == "__main__":
    main()
