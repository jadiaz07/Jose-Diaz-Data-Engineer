# Vuelve a ejecutar esta celda 
import pandas as pd
import matplotlib.pyplot as plt 

# Leer los datos desde el archivo
schools = pd.read_csv("schools.csv")

# Previsualizar los datos (descomentar para ver)
# schools.head()

# ¿Qué escuelas son las mejores en matemáticas?
# Filtra las escuelas con un promedio de matemáticas >= 640 y las ordena descendentemente.
best_math_schools = schools[schools["average_math"] >= 640][["school_name", "average_math"]].sort_values("average_math", ascending=False)

# Calcular la puntuación total del SAT por escuela
schools["total_SAT"] = schools["average_math"] + schools["average_reading"] + schools["average_writing"]

# ¿Cuáles son las 10 mejores escuelas en rendimiento?
# Ordena por total_SAT descendentemente y toma las 10 primeras.
top_10_schools = schools.sort_values("total_SAT", ascending=False)[["school_name", "total_SAT"]].head(10)

# 1. Calcular las estadísticas por distrito (borough)
# Agrupar por 'borough' y calcular el conteo (num_schools), la media (average_SAT) y la desviación estándar (std_SAT).
borough_stats = schools.groupby("borough")["total_SAT"].agg(
    num_schools='count',
    average_SAT='mean',
    std_SAT='std'
)

# 2. Encontrar el distrito con la mayor desviación estándar ('std_SAT')
max_std_borough = borough_stats['std_SAT'].idxmax()

# 3. Crear el DataFrame final 'largest_std_dev'
largest_std_dev = (
    borough_stats
    .loc[[max_std_borough]]  
    .round(2)                
    .reset_index()          
)

# Mostrar el DataFrame resultante
print("DataFrame largest_std_dev:")
print(largest_std_dev)
print("-" * 50)

# 4. Generar el gráfico (Plot) para visualizar los resultados
# Se transpone el DataFrame para que las métricas (num_schools, average_SAT, std_SAT)
# se conviertan en barras en el eje X para una mejor comparación visual.
plot_data = largest_std_dev[['num_schools', 'average_SAT', 'std_SAT']].T
plot_data.columns = [largest_std_dev['borough'].iloc[0]] # Nombre de la columna = Nombre del distrito

plt.figure(figsize=(8, 5))
plot_data.plot(kind='bar', legend=False, rot=0, color='skyblue')

# Añadir etiquetas y título al gráfico
plt.title(f'Métricas SAT para {largest_std_dev["borough"].iloc[0]} (Distrito con Mayor Desv. Estándar)', fontsize=14)
plt.ylabel('Valor Redondeado', fontsize=12)
plt.xlabel('Métrica', fontsize=12)

# Añadir el valor de cada barra para hacerlo más informativo
for i, v in enumerate(plot_data.values.flatten()):
    # Muestra el texto del valor de la barra ligeramente por encima de la misma
    plt.text(i, v + 5, str(v), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.show()
