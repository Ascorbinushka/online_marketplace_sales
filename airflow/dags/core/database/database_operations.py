import psycopg2


class Purchases:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def insert_stock(
        self,
        client_id: int,
        gender_id: int,
        purchase_datetime: str,
        purchase_time_as_seconds_from_midnight: int,
        product_id: int,
        quantity: int,
        price_per_item: float,
        discount_per_item: float,
        total_price: float,
    ) -> None:
        """Вставка данных о продажах крупного онлайн-маркетплейса"""
        query = """INSERT INTO purchases (
                client_id, gender_id, purchase_datetime,
                purchase_time_as_seconds_from_midnight,
                product_id, quantity, price_per_item,
                discount_per_item, total_price
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) ON CONFLICT (client_id, product_id, purchase_datetime) DO NOTHING;"""
        try:
            with self.db_connection.get_connection().cursor() as cursor:
                cursor.execute(
                    query,
                    (
                        client_id,
                        gender_id,
                        purchase_datetime,
                        purchase_time_as_seconds_from_midnight,
                        product_id,
                        quantity,
                        price_per_item,
                        discount_per_item,
                        total_price,
                    ),
                )
                row_count = cursor.rowcount
            self.db_connection.get_connection().commit()
            if row_count > 0:
                print(
                    f"Продажи загружены в базу. Дата: {purchase_datetime}, клиент id: {client_id}"
                )
            else:
                print(
                    f"Запись для клиент id: {client_id} на дату: {purchase_datetime} уже существует"
                    f" и не была добавлена (ON CONFLICT)."
                )
        except psycopg2.Error as e:
            self.db_connection.get_connection().rollback()
            print(f"Ошибка {e}")

    def get_gender_id(self, gender: str) -> int:
        """Получает gender_id"""
        query = "SELECT gender_id FROM genders WHERE gender = %s"
        try:
            with self.db_connection.get_connection().cursor() as cursor:
                cursor.execute(query, (gender,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Ошибка при получении gender_id: {e}")
