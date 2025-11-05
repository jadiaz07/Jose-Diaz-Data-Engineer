WITH UnitPriceReference AS (
    -- CTE: Calcula el Precio Unitario de Referencia (UPR) específico.
    -- Se asegura que la división interna sea NUMERIC antes de calcular el promedio.
    SELECT
        product_id,
        discount,
        market,
        region,
        -- UPR = AVG( Sales / (Quantity * (1 - Discount)) )
        ROUND(
            AVG(CAST(sales AS NUMERIC) / (CAST(quantity AS NUMERIC) * (1 - discount)))::NUMERIC
        , 4) AS reference_unit_price -- Redondeo del promedio a 4 decimales
    FROM
        orders
    WHERE
        quantity IS NOT NULL -- Solo usamos pedidos con cantidad conocida
        AND quantity > 0     
        AND discount < 1     
    GROUP BY
        product_id,
        discount,
        market,
        region
)

-- Consulta Final: Aplica la imputación.
SELECT
    t1.product_id,
    t1.discount,
    t1.market,
    t1.region,
    t1.sales,
    t1.quantity, 
    
    -- Lógica de Imputación y Cálculo: Se usa CAST para garantizar el tipo NUMERIC
    ROUND(
        -- La estructura CASE WHEN debe manejar todos los casos
        CASE
            -- 1. Si la cantidad NO es nula, usamos el valor original.
            WHEN t1.quantity IS NOT NULL THEN CAST(t1.quantity AS NUMERIC)
            
            -- 2. Si la cantidad ES nula, calculamos el valor estimado:
            WHEN t2.reference_unit_price IS NOT NULL AND t1.discount < 1 THEN
                CAST(t1.sales AS NUMERIC) / (t2.reference_unit_price * (1 - t1.discount))
            
            -- 3. Si no se puede imputar, el valor es NULL.
            ELSE NULL 
        END
    ::NUMERIC, 0) AS calculated_quantity -- Redondeado a cero decimales, con input NUMERIC
FROM
    orders t1
LEFT JOIN
    UnitPriceReference t2
    -- Unir por todas las claves de referencia de precio
    ON t1.product_id = t2.product_id
    AND t1.discount = t2.discount
    AND t1.market = t2.market
    AND t1.region = t2.region
ORDER BY
    calculated_quantity DESC NULLS LAST;
