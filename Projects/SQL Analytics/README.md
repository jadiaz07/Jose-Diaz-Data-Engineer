# 📈 SQL Analytics: Top Products & Data Imputation (PostgreSQL)

## 📝 Sobre Este Proyecto

Este repositorio contiene soluciones de **SQL (PostgreSQL)** centradas en el análisis de datos de ventas y la manipulación de valores faltantes. El objetivo es demostrar el dominio de:

1.  **Funciones de Ventana (`RANK()`):** Para clasificar y seleccionar los elementos principales dentro de grupos.
2.  **Expresiones Comunes de Tabla (CTEs / `WITH AS`):** Para modularizar y simplificar consultas complejas.
3.  **Lógica de Imputación Condicional (`CASE WHEN`):** Para estimar valores faltantes basados en cálculos de referencia.

## ⚙️ Análisis Realizados

### 1. 🏆 Top 5 Productos por Categoría (Consulta en `sql/top_five_products_each_category.sql`)

Esta consulta identifica los **cinco productos principales** de cada categoría basándose en sus **mayores ventas totales**.

* **Técnicas Clave:** Uso de **dos CTEs** para calcular el resumen de ventas/ganancias y luego aplicar la función de ventana `RANK()` antes de filtrar el resultado (`<= 5`).
* **Resultado:** Una tabla ordenada que muestra el `product_rank` dentro de cada `category`.

### 2. 🔢 Imputación de Cantidad Faltante (Consulta en `sql/impute_missing_values.sql`)

Esta consulta imputa (`calculated_quantity`) los valores faltantes en la columna `quantity` utilizando un cálculo de precio unitario de referencia (UPR).

## 🛠️ Estructura y Tecnologías

* **SGBD:** PostgreSQL (El código usa funciones como `CAST(AS NUMERIC)` específicas para PostgreSQL).
  
* **Archivos:**
* Las consultas se encuentran en el directorio SQL/.
* Los archivos CSV se encuentran en el directorio Data/.
## 🚀 Cómo Ejecutar

➡️ Para instrucciones detalladas sobre la ejecución, consulta el archivo EXECUTE.md.

¡Gracias por revisar este proyecto de SQL avanzado!
