# Importamos pandas y matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Leemos el CSV Netflix CSV 
netflix_df = pd.read_csv("netflix_data.csv")

# --- 1. Filtrado de la Década de 1990 (1990-1999) y tipo 'Movie' ---
# Se utiliza un solo filtro combinado para mayor claridad y eficiencia.
movies_1990s = netflix_df[
    (netflix_df["type"] == "Movie") &
    (netflix_df["release_year"] >= 1990) &
    (netflix_df["release_year"] <= 1999)
].copy() # Se usa .copy() para evitar SettingWithCopyWarning

# --- 2. Encontrar la Duración Más Frecuente (Moda) ---
# La duración más frecuente es la moda (mode()). Tomamos el primer valor [0] y lo convertimos a entero.
duration = int(movies_1990s["duration"].mode()[0])

print(f"La duración más frecuente de las películas en la década de 1990 es (duration): {duration} minutos.")

# --- 3. Contar las Películas de Acción Cortas ---
# Definición de corto: duración < 90 minutos.
short_action_movies = movies_1990s[
    (movies_1990s["genre"] == "Action") &
    (movies_1990s["duration"] < 90)
]

# Contamos el número de filas del DataFrame filtrado.
short_movie_count = len(short_action_movies)

print(f"El número de películas de acción cortas (< 90 min) es (short_movie_count): {short_movie_count}")

# --- 4. Visualización (Histograma) ---
plt.figure(figsize=(10, 6))
plt.hist(movies_1990s["duration"], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribución de la Duración de Películas en la Década de 1990', fontsize=16)
plt.xlabel('Duración (minutos)', fontsize=12)
plt.ylabel('Número de Películas', fontsize=12)
plt.axvline(duration, color='red', linestyle='dashed', linewidth=2, label=f'Moda ({duration} min)') # Marca la duración más frecuente
plt.legend()
plt.grid(axis='y', alpha=0.75)
plt.show()
