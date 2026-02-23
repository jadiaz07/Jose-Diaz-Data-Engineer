CREATE TABLE public.fact_sales (
    order_id    VARCHAR(50) NOT NULL,
    user_id     VARCHAR(50) NOT NULL,
    amount      DECIMAL(18, 2),
    currency    VARCHAR(10),
    status      VARCHAR(20),
    created_at  TIMESTAMP NOT NULL,
    updated_at  TIMESTAMP,
    
    PRIMARY KEY (order_id) -- Redshift no la hace cumplir, pero ayuda al optimizador
)
DISTSTYLE KEY
DISTKEY (user_id) -- Clave de Distribución
COMPOUND SORTKEY (created_at); -- Clave de Ordenamiento
