-- 1. Ventas diarias por moneda
SELECT 
    TRUNC(created_at) AS fecha,
    currency,
    SUM(amount) AS total_ventas,
    COUNT(order_id) AS cantidad_ordenes
FROM public.fact_sales
GROUP BY 1, 2
ORDER BY 1 DESC;

-- 2. Detección de posibles duplicados por order_id
-- (Si el pipeline es correcto, esta query no debería devolver nada)
SELECT 
    order_id, 
    COUNT(*) as repeticiones
FROM public.fact_sales
GROUP BY order_id
HAVING COUNT(*) > 1;
