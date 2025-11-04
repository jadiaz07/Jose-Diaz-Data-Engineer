# 🗽 Análisis de la Dispersión del SAT en Escuelas de NYC

## 📝 Sobre Este Proyecto

Este es un análisis que realicé para mi portafolio usando **Pandas** y **Matplotlib**. Mi objetivo principal fue investigar la variabilidad en las puntuaciones del examen **SAT Total** entre los diferentes distritos (boroughs) de la Ciudad de Nueva York.

Busqué responder a una pregunta clave: **¿Qué distrito de NYC presenta la mayor heterogeneidad en el rendimiento del SAT (mayor desviación estándar)?**

## ⚙️ Lo Que Hice

1.  Calculé el **Total SAT** por escuela.
2.  Agrupé los datos por distrito y obtuve el **conteo de escuelas**, el **SAT promedio** y la **desviación estándar (std)**.
3.  Identifiqué el distrito con la desviación estándar más alta.
4.  Generé un **DataFrame final (`largest_std_dev`)** con una única fila, que resume las métricas clave de ese distrito, con valores redondeados a dos decimales.
5.  Creé una **visualización** para comparar las métricas de ese distrito específico.

## 📊 Resultado Clave

El distrito con la mayor dispersión en las puntuaciones del SAT fue **[NOMBRE DEL DISTRITO AQUÍ]**.

### Mi DataFrame `largest_std_dev`

| borough | num_schools | average_SAT | std_SAT |
| :--- | :--- | :--- | :--- |
| **[NOMBRE DEL DISTRITO AQUÍ]** | [VALOR] | [VALOR] | [VALOR] |

*(**Nota:** Asegúrate de llenar esta tabla con el resultado real de tu ejecución.)*

### Visualización

Aquí se puede ver la comparación de las métricas de este distrito en un gráfico de barras:

<img width="1262" height="941" alt="Resultado" src="https://github.com/user-attachments/assets/e5fa7024-dedf-49da-995c-418ea350ed47" />


## 🛠️ Tecnologías

* **Python**
* **Pandas** (Para el análisis y la manipulación de datos)
* **Matplotlib** (Para la visualización del resultado)

---
*¡Gracias por revisar mi análisis!*

Estas son algunas de las preguntas que estoy analzando: 

¿Qué escuelas de la ciudad de Nueva York tienen los mejores resultados en matemáticas?

¿Cuáles son las 10 escuelas con mejor rendimiento según las puntuaciones combinadas del SAT?

¿Qué distrito tiene la mayor desviación estándar en la puntuación combinada del SAT?
