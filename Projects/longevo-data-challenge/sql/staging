CREATE SCHEMA IF NOT EXISTS staging;

DROP TABLE IF EXISTS staging.stg_sales;

CREATE TABLE staging.stg_sales (
    order_id    VARCHAR(50),
    user_id     VARCHAR(50),
    amount      DECIMAL(18, 2),
    currency    VARCHAR(10),
    status      VARCHAR(20),
    created_at  TIMESTAMP,
    updated_at  TIMESTAMP
) 
BACKUP NO; -- Optimizamos espacio ya que es data transitoria
