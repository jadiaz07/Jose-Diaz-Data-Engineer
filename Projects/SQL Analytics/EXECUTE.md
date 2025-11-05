# 🚀 Guía de Ejecución

Este documento provee las instrucciones necesarias para ejecutar las consultas SQL de este proyecto en un entorno PostgreSQL.

## 🛠️ Requisitos del Entorno

* **SGBD:** PostgreSQL (Necesario para funciones como `RANK()` y `CAST(AS NUMERIC)`).
* **Cliente SQL:** Un cliente para conectar a la base de datos (ej. pgAdmin, DBeaver, o `psql`).

## ⚙️ Pasos de Ejecución

1.  **Conexión:** Conéctate a tu base de datos PostgreSQL.
2.  **Preparación de Datos:** Asegúrate de que las tablas `orders` y `products` existan en el esquema de tu base de datos con los datos necesarios.
3.  **Ejecución de Consultas:** Ejecuta secuencialmente el contenido de los dos archivos SQL principales ubicados en el directorio `sql/`:

    * **Análisis Top 5:** Ejecuta `sql/top_five_products_each_category.sql`.
    * **Imputación:** Ejecuta `sql/impute_missing_values.sql`.

Cada archivo es una consulta completa que devolverá la tabla de resultados solicitada.
