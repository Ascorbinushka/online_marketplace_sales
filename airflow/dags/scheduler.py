from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.decorators import task


with DAG(
        dag_id="online_marketplace_sales_dag",
        schedule="0 7 * * *",
        start_date=datetime(2025, 1, 1),
        catchup=False,
        tags=["simulative"],
) as dag:
    @task
    def get_data_sales():
        from core.api.fetch_data import APIClient

        # Получаем текущую дату и время
        now = datetime.now()

        # Вычитаем один день из текущей даты
        yesterday = now - timedelta(days=1)

        # Форматируем дату в строку в формате "YYYY-MM-DD"
        date_str = yesterday.strftime("%Y-%m-%d")
        client = APIClient()
        params = {"date": date_str}
        return client.fetch_data("data", param=params)



    @task
    def load_data_to_pg(ti):
        from core.database.database_operations import Purchases
        from core.config import DatabaseConnection

        db_connection = DatabaseConnection.get_instance(host='airflow')
        purchases = Purchases(db_connection)

        data = ti.xcom_pull(task_ids="get_data_sales")
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


    data = get_data_sales()
    load = load_data_to_pg()
    data >> load
