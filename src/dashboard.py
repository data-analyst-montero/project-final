# Para ejecutar: streamlit run dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎬 Dashboard Operativo de Datos Cinematográficos")

df = pd.read_csv("../data/output/dataset_final.csv")

# Filtros en la barra lateral
year_range = st.sidebar.slider("Rango de Años", int(df['release_year'].min()), int(df['release_year'].max()), (2000, 2026))
min_votes = st.sidebar.number_input("Mínimo de Votos", min_value=0, value=100)

# Filtrado de datos dinámico
df_filtered = df[(df['release_year'].between(year_range[0], year_range[1])) & (df['vote_count'] >= min_votes)]

# Métricas Principales (KPIs)
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Películas Filtradas", len(df_filtered))
kpi2.metric("Recaudación Promedio", f"${df_filtered['revenue'].mean():,.2f}")
kpi3.metric("Calificación Media", round(df_filtered['vote_average'].mean(), 2))

# Gráficos Interactivos con Plotly
fig_scatter = px.scatter(df_filtered, x="budget", y="revenue", hover_name="original_title", title="Presupuesto vs Recaudación")
st.plotly_chart(fig_scatter, use_container_width=True)