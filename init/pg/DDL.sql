CREATE TABLE genders (
    gender_id SERIAL PRIMARY KEY,
    gender CHAR(1) UNIQUE NOT NULL
);

CREATE TABLE purchases (
    purchase_id SERIAL PRIMARY KEY,
    client_id INT,
    gender_id INT,
    purchase_datetime DATE,
    purchase_time_as_seconds_from_midnight INT,
    product_id INT,
    quantity INT,
    price_per_item NUMERIC(10, 2),
    discount_per_item NUMERIC(10, 2),
    total_price NUMERIC(15, 2),
    FOREIGN KEY (gender_id) REFERENCES genders(gender_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_purchases_client_product_purchase
ON purchases (client_id, product_id, purchase_datetime);

CREATE INDEX idx_purchases_client_id ON public.purchases USING btree (client_id);

CREATE INDEX idx_purchases_purchase_datetime ON public.purchases USING btree (purchase_datetime);

CREATE UNIQUE INDEX purchases_pkey ON public.purchases USING btree (purchase_id);

INSERT INTO genders (gender) VALUES ('F'), ('M');