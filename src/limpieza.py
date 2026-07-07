import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración

#Entrada:
MOVIES_FILE = "movies_metadata.csv"
TMDB_FILE = "tmdb_movie_dataset_v11.csv"

#Salida:
OUTPUT_FILE = "dataset_final.csv"

# Cargar los datasets originales

movies = pd.read_csv(
    "../data/raw/movies_metadata.csv",
    low_memory=False
)

tmdb = pd.read_csv(
    "../data/raw/tmdb_movie_dataset_v11.csv",
    low_memory=False
)

print("\n2 datasets cargados")

print(f"movies_metadata: {movies.shape}")
print(f"tmdb_movie_dataset_v11: {tmdb.shape}")

# Selección de columnas necesarias

movies = movies[
    [       
        "imdb_id",
        "original_language",
        "original_title",
        "overview",
        "popularity",
        "adult",
        "release_date",
        "revenue",
        "runtime",
        "status",
        "tagline",
        "video",
        "vote_average",
        "vote_count",
        "homepage",
    ]
]

tmdb = tmdb[
    [
        "imdb_id",
        "budget",
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
    ]
]

# Limpiar imdb_id

movies["imdb_id"] = (
    movies["imdb_id"]
    .astype(str)
    .str.strip()
)

tmdb["imdb_id"] = (
    tmdb["imdb_id"]
    .astype(str)
    .str.strip()
)

# 1. Limpieza de claves de unión (imdb_id)

movies = movies[
    movies["imdb_id"].notna()
]

movies = movies[
    movies["imdb_id"] != ""
]

movies = movies[
    movies["imdb_id"] != "nan"
]

tmdb = tmdb[
    tmdb["imdb_id"].notna()
]

tmdb = tmdb[
    tmdb["imdb_id"] != ""
]

tmdb = tmdb[
    tmdb["imdb_id"] != "nan"
]

# Eliminar duplicados

movies = movies.drop_duplicates(
    subset="imdb_id"
)

tmdb = tmdb.drop_duplicates(
    subset="imdb_id"
)

print("\nDespués de eliminar duplicados")

print(f"movies_metadata: {movies.shape}")
print(f"tmdb_movie_dataset_v11: {tmdb.shape}")

# Info previa al merge

ids_movies = set(movies["imdb_id"])

ids_tmdb = set(tmdb["imdb_id"])

comunes = ids_movies.intersection(ids_tmdb)

print("\nIDs comunes")

print(len(comunes))

# Combinación de Datasets (Merge)

dataset_final = pd.merge(
    movies,
    tmdb,
    how="inner",
    on="imdb_id"
)

# Eliminar duplicados

dataset_final = dataset_final.drop_duplicates(
    subset="imdb_id"
)

# Ordenar

dataset_final = dataset_final.sort_values(
    by="release_date"
)

# Organizar columnas

dataset_final = dataset_final[
    [        
        "imdb_id",        
        "original_title",
        "original_language",
        "release_date",
        "runtime",
        "budget",
        "revenue",
        "popularity",
        "vote_average",
        "vote_count",
        "genres",
        "production_companies",
        "production_countries",
        "spoken_languages",
        "status",
        "overview",
        "tagline",
        "adult",
        "video",
        "homepage"
    ]
]

# Info final

# Conversión de Tipos de Datos y Tratamiento de Erreces
dataset_final['release_date'] = pd.to_datetime(dataset_final['release_date'], errors='coerce')
dataset_final['budget'] = pd.to_numeric(dataset_final['budget'], errors='coerce')
dataset_final['revenue'] = pd.to_numeric(dataset_final['revenue'], errors='coerce')
dataset_final['popularity'] = pd.to_numeric(dataset_final['popularity'], errors='coerce')
dataset_final['runtime'] = pd.to_numeric(dataset_final['runtime'], errors='coerce')

# Filtrado de Datos Inconsistentes (Optimización cinematográfica)
# Películas con presupuesto o recaudación cero suelen ser datos faltantes en TMDB.
# Para análisis financiero, filtramos temporalmente o creamos una bandera, aquí limpiamos negativos:
dataset_final = dataset_final[(dataset_final['budget'] >= 0) & (dataset_final['revenue'] >= 0)]

# Creación de Nuevas Columnas (Feature Engineering con Pandas)
dataset_final['release_year'] = dataset_final['release_date'].dt.year

# Calcular el Retorno de Inversión (ROI). Evitamos división por cero usando np.where
dataset_final['roi'] = np.where(dataset_final['budget'] > 0, dataset_final['revenue'] / dataset_final['budget'], 0)

# Columna de beneficio neto
dataset_final['profit'] = dataset_final['revenue'] - dataset_final['budget']

print("Dataset final")
print("-----------------------------------")
print(f"Filas: {dataset_final.shape[0]}")
print(f"Columnas: {dataset_final.shape[1]}")


#for columna in dataset_final.columns:
#    print(columna)

# Guardar el dataset final limpio

dataset_final.to_csv(
    "../data/output/dataset_final.csv",
    index=False,
    encoding="utf-8"
)

print("\nArchivo generado: dataset_final.csv en la ruta: data/output/")

print("\n--- Análisis Descriptivo ---")
# Estadísticos clave de las variables numéricas principales
variables_interes = ['budget', 'revenue', 'profit', 'runtime', 'vote_average', 'vote_count', 'roi']
print(dataset_final[variables_interes].describe())

# Correlaciones
print("\nMatriz de Correlación:")
correlacion = dataset_final[variables_interes].corr()
print(correlacion)

ruta = "../results/graficos"
if not os.path.exists(ruta):
    os.makedirs(ruta)

print("\n--- Visualización de Datos ---")

# Gráfico 1: Relación Presupuesto vs Recaudación (Scatter Plot)
plt.figure()
sns.scatterplot(data=dataset_final[(dataset_final['budget'] > 0) & (dataset_final['revenue'] > 0)], 
                x='budget', y='revenue', alpha=0.5, color='teal')
plt.title('Relación entre Presupuesto y Recaudación (Valores > 0)')
plt.xlabel('Presupuesto ($)')
plt.ylabel('Recaudación ($)')
plt.xscale('log')
plt.yscale('log')
plt.savefig('../results/graficos/presupuesto_vs_recaudacion.png')
plt.close()

# Gráfico 2: Distribución de Calificaciones (Histrograma)
plt.figure()
sns.histplot(dataset_final['vote_average'].dropna(), bins=20, kde=True, color='purple')
plt.title('Distribución del Promedio de Votos (TMDB)')
plt.xlabel('Calificación Promedio')
plt.ylabel('Frecuencia')
plt.savefig('../results/graficos/distribucion_votos.png')
plt.close()

# Gráfico 3: Evolución de las ganancias promedio a lo largo de los años
plt.figure()
df_yearly = dataset_final.groupby('release_year')['profit'].mean().reset_index()
# Filtrar años recientes con datos estables (ej. desde 1980 hasta 2026)
df_yearly = df_yearly[(df_yearly['release_year'] >= 1980) & (df_yearly['release_year'] <= 2026)]
sns.lineplot(data=df_yearly, x='release_year', y='profit', marker='o', color='red')
plt.title('Evolución del Beneficio Promedio por Año (1980 - 2026)')
plt.xlabel('Año de Estreno')
plt.ylabel('Beneficio Promedio ($)')
plt.savefig('../results/graficos/evolucion_beneficio.png')
plt.close()

print("Gráficos generados y guardados en el directorio /results/graficos/")