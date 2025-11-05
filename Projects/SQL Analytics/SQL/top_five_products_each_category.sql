WITH ProductSalesSummary AS (
    -- CTE 1: Calcula las métricas totales por producto (Ventas, Ganancias)
    SELECT
        p.category,
        p.product_name,
        ROUND(SUM(CAST(o.sales AS NUMERIC)), 2) AS product_total_sales,
        ROUND(SUM(CAST(o.profit AS NUMERIC)), 2) AS product_total_profit
    FROM
        orders AS o
    INNER JOIN 
        products AS p
        ON o.product_id = p.product_id
    GROUP BY
        p.category,
        p.product_name
),
RankedProducts AS (
    -- CTE 2: Calcula el rango (product_rank) usando los resultados del CTE 1
    -- Esta CTE es necesaria para evitar el error de ventana
    SELECT
        *,
        -- Aplica el ranking sobre las ventas totales dentro de cada categoría
        RANK() OVER (
            PARTITION BY category 
            ORDER BY product_total_sales DESC
        ) AS product_rank
    FROM
        ProductSalesSummary
)

-- Consulta Final: Filtra el Top 5
SELECT
    category,
    product_name,
    product_total_sales,
    product_total_profit,
    product_rank
FROM
    RankedProducts 
WHERE
    product_rank <= 5  
ORDER BY
    category ASC,
    product_total_sales DESC;
