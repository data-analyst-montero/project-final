# 1.🎬 Análisis Exploratorio de Datos de Películas (TMDB + IMDb)

## 2.📖 Descripción del proyecto

Este proyecto consiste en la realización de un **Análisis Exploratorio de Datos ** sobre una recopilación de información cinematográfica procedente de dos conjuntos de datos relacionados mediante el identificador **IMDb (`imdb_id`)**.

El objetivo principal es integrar ambos conjuntos de datos, realizar un proceso de limpieza y transformación de la información, y obtener un conjunto de datos final que permita analizar las características más relevantes de las películas, identificando patrones, relaciones y tendencias mediante técnicas estadísticas y visualizaciones.

El proyecto se ha desarrollado utilizando **Python** y la biblioteca **Pandas** para el tratamiento de los datos, complementando el análisis con diferentes librerías de visualización para facilitar la interpretación de los resultados.

### 🎯 Objetivos

Los principales objetivos del proyecto son:

- Integrar dos conjuntos de datos mediante la clave `imdb_id`.
- Detectar y corregir problemas de calidad de los datos.
- Tratar valores nulos, duplicados y registros inconsistentes.
- Transformar las variables al tipo de dato adecuado.
- Obtener un conjunto de datos limpio (`dataset_final`) listo para el análisis.
- Realizar un análisis estadístico descriptivo de las variables.
- Identificar relaciones entre variables como presupuesto, ingresos, popularidad y valoración de los usuarios.
- Elaborar visualizaciones que permitan extraer conclusiones relevantes.
- Generar un dashboard que facilite la interpretación de la información.

### 📝 Contexto del análisis

La industria cinematográfica genera una enorme cantidad de información relacionada con la producción, distribución y recepción de las películas.

Analizar estos datos permite responder preguntas como:

- ¿Existe relación entre el presupuesto y la recaudación?
- ¿Qué géneros generan mayores ingresos?
- ¿Qué idiomas predominan en la industria?
- ¿Qué productoras producen un mayor número de películas?
- ¿Influye la popularidad en la valoración de los usuarios?
- ¿Qué países participan con mayor frecuencia en la producción cinematográfica?

Responder estas preguntas facilita comprender mejor el comportamiento de la industria y descubrir patrones ocultos dentro de los datos.

### ❓ Problema que se resuelve

Los datos originales presentan diversos problemas habituales en conjuntos de datos reales:

- Valores nulos.
- Registros duplicados.
- Diferentes tipos de datos.
- Información incompleta.
- Variables categóricas con valores vacíos.
- Datos procedentes de diferentes fuentes.

El proyecto resuelve estos problemas mediante un proceso de limpieza, integración y transformación de los datos, obteniendo un único dataset preparado para realizar análisis estadísticos y visualizaciones de calidad.

### 📂 Conjuntos de datos

El proyecto utiliza dos datasets:

### movies_metadata.csv

Contiene información general de las películas:

- imdb_id
- original_language
- original_title
- overview
- popularity
- release_date
- revenue
- runtime
- status
- video
- vote_average
- vote_count

### tmdb_movie_dataset_v11.csv

Contiene información adicional relacionada con la producción:

- imdb_id
- budget
- genres
- production_companies
- production_countries
- spoken_languages

Ambos datasets se integran mediante la clave común **imdb_id**

# 3. 📁 Estructura del proyecto

```
Proyecto/
│
├── data/
│   ├──── raw
│   │     ├── movies_metadata.csv
│   │     └── tmdb_movie_dataset_v11.csv
│   └──── output
│         └── dataset_final.csv
│
├── src/
│   ├── limpieza.py
│   ├── analisis_estadistico.py
│   └── dashboard.py
│
├── notebook/
│   └── 01-Analisis-preliminar.ipynb
│
│
├── results/
│   ├── graficos
│   └── Informe de resultados.doc/
│
└── README.md

```

## 4. 🛠 Instalación y requisitos

El proyecto se desarrolló utilizando:

- Python 3
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Visual Studio Code

### 🔄 Proceso realizado

El proyecto sigue las siguientes fases:

1. Carga de los datasets.
2. Exploración inicial.
3. Limpieza de datos.
4. Tratamiento de valores nulos.
5. Eliminación de duplicados.
6. Conversión de tipos de datos.
7. Integración mediante `imdb_id`.
8. Creación del `dataset_final`.
9. Análisis estadístico.
10. Visualización de los resultados.
11. Elaboración del dashboard.

## 🧹 Transformaciones realizadas

Durante el proceso de limpieza se realizaron, entre otras, las siguientes transformaciones:

- Eliminación de registros duplicados.
- Eliminación de registros sin `imdb_id`.
- Conversión de variables numéricas.
- Conversión de fechas.
- Sustitución de valores nulos en variables categóricas por **Unknown**.
- Tratamiento de valores inconsistentes.
- Creación de nuevas variables como:
  - Beneficio (`Profit`)
  - Retorno de inversión (`ROI`)
  - Año de estreno
  - Década de estreno

## 📊 Técnicas empleadas

Para llevar a cabo el análisis se utilizaron diferentes técnicas de análisis de datos:

### Limpieza de datos

- Tratamiento de valores nulos
- Eliminación de duplicados
- Conversión de tipos
- Validación de registros

### Transformación de datos

- Integración de datasets mediante `merge`
- Creación de nuevas variables
- Normalización de datos

## Análisis descriptivo

Se calcularon medidas estadísticas como:

- Media
- Mediana
- Moda
- Desviación estándar
- Varianza
- Percentiles
- Correlaciones

### Análisis exploratorio

Se estudiaron las relaciones entre variables como:

- Presupuesto vs ingresos
- Popularidad vs valoración
- Recaudación por género
- Producción por país
- Idiomas más frecuentes
- Productoras con mayor actividad

### Visualización

Se utilizaron gráficos como:

- Histogramas
- Diagramas de barras
- Boxplots
- Scatter plots
- Heatmaps
- Gráficos de correlación

# 5. 📈 Resultados esperados

El análisis permite obtener información útil sobre:

- Distribución de presupuestos e ingresos.
- Géneros más frecuentes.
- Productoras con mayor número de películas.
- Idiomas predominantes.
- Relación entre presupuesto y recaudación.
- Influencia de la popularidad en las valoraciones.
- Comportamiento temporal de la producción cinematográfica.

Puede encontrar los resultados y conclusiones en el informe localizado en results/Informe de resultados.doc

## 6. 🚀 Cómo ejecutar el proyecto

1. Clonar el repositorio.

```bash
git clone <repositorio>
```

2. Ejecutar el proceso de limpieza.

```bash
python limpieza.py

```

3. Ejecutar el análisis estadístico.

```bash
python analisis_estadistico.py
```

4. Generar el dashboard.

```bash
python dashboard.py
```

## 7. 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el proyecto, por favor abre un pull request o una issue.

## 8. 👩🏻‍💻 Autor

Giselle Montero González (https://github.com/data-analyst-montero)
