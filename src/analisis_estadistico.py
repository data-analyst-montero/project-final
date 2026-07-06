
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def limpiar(df):
    return df.drop_duplicates()

metadata=pd.read_csv("../data/raw/movies_metadata.csv", low_memory=False)
tmdb=pd.read_csv("../data/raw/tmdb_movie_dataset_v11.csv", low_memory=False)

metadata=limpiar(metadata)
tmdb=limpiar(tmdb)

metadata["imdb_id"]=metadata["imdb_id"].astype(str).str.strip()
tmdb["imdb_id"]=tmdb["imdb_id"].astype(str).str.strip()

metadata=metadata[(metadata["imdb_id"]!="") & (metadata["imdb_id"]!="nan")]

dataset_final=pd.merge(metadata,tmdb,on="imdb_id",how="inner")

cat_cols=["original_language","original_title","overview","status","tagline","title","video","genres","production_companies","production_countries","spoken_languages"]
for c in cat_cols:
    if c in dataset_final.columns:
        dataset_final[c]=dataset_final[c].replace(r'^\s*$',np.nan,regex=True).fillna("Unknown")

num_cols=["budget","revenue","runtime","popularity","vote_average","vote_count"]
for c in num_cols:
    if c in dataset_final.columns:
        dataset_final[c]=pd.to_numeric(dataset_final[c],errors="coerce")

dataset_final.to_csv("../data/output/dataset_final.csv",index=False)

print(dataset_final.info())
print(dataset_final.describe(include="all").T)

print("\\nValores nulos")
print(dataset_final.isnull().sum())

print("\\nCorrelación")
corr=dataset_final[num_cols].corr()
print(corr)

plt.figure(figsize=(8,6))
sns.heatmap(corr,annot=True,cmap="coolwarm")
plt.tight_layout()
plt.savefig("correlacion.png")
plt.close()

for c in ["budget","revenue","runtime","popularity","vote_average"]:
    if c in dataset_final.columns:
        plt.figure(figsize=(6,4))
        dataset_final[c].dropna().hist(bins=30)
        plt.title(c)
        plt.tight_layout()
        plt.savefig(f"{c}_hist.png")
        plt.close()

if {"budget","revenue"}.issubset(dataset_final.columns):
    plt.figure(figsize=(6,4))
    plt.scatter(dataset_final["budget"],dataset_final["revenue"],s=8)
    plt.xlabel("Budget"); plt.ylabel("Revenue")
    plt.tight_layout()
    plt.savefig("budget_vs_revenue.png")
    plt.close()

for c in ["genres","original_language","production_companies","production_countries"]:
    if c in dataset_final.columns:
        print(dataset_final[c].value_counts().head(10))
