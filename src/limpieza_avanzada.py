
"""limpieza_avanzada.py
Limpieza avanzada y generación de dataset_final.csv
"""
import pandas as pd
import numpy as np

CAT_FILL="Unknown"

def limpiar_texto(s):
    return s.astype(str).str.strip()

def convertir_numericas(df, cols):
    for c in cols:
        if c in df.columns:
            df[c]=pd.to_numeric(df[c], errors="coerce")
    return df

def reemplazar_nulos_categoricos(df, cols):
    existentes=[c for c in cols if c in df.columns]
    df[existentes]=(df[existentes]
        .replace(r"^\s*$", np.nan, regex=True)
        .fillna(CAT_FILL))
    return df

def eliminar_outliers_iqr(df, cols):
    for c in cols:
        if c in df.columns:
            q1=df[c].quantile(.25)
            q3=df[c].quantile(.75)
            iqr=q3-q1
            li=q1-1.5*iqr
            ls=q3+1.5*iqr
            df=df[(df[c].isna())|((df[c]>=li)&(df[c]<=ls))]
    return df

metadata=pd.read_csv("../data/raw/movies_metadata.csv", low_memory=False)
tmdb=pd.read_csv("../data/raw/tmdb_movie_dataset_v11.csv", low_memory=False)

metadata.drop_duplicates(inplace=True)
tmdb.drop_duplicates(inplace=True)

metadata["imdb_id"]=limpiar_texto(metadata["imdb_id"])
tmdb["imdb_id"]=limpiar_texto(tmdb["imdb_id"])

metadata=metadata[metadata["imdb_id"].notna()]
metadata=metadata[~metadata["imdb_id"].isin(["","nan","None"])]

tmdb=tmdb[tmdb["imdb_id"].notna()]
tmdb=tmdb[~tmdb["imdb_id"].isin(["","nan","None"])]

dataset_final=pd.merge(metadata,tmdb,on="imdb_id",how="inner")

categoricas=[
"original_language","original_title","overview","status","tagline",
"title","video","genres","production_companies",
"production_countries","spoken_languages"
]
dataset_final=reemplazar_nulos_categoricos(dataset_final,categoricas)

numericas=["budget","revenue","runtime","popularity","vote_average","vote_count"]
dataset_final=convertir_numericas(dataset_final,numericas)

for c in ["budget","revenue","runtime","popularity","vote_average","vote_count"]:
    if c in dataset_final.columns:
        dataset_final.loc[dataset_final[c]<0,c]=np.nan

if "release_date" in dataset_final.columns:
    dataset_final["release_date"]=pd.to_datetime(dataset_final["release_date"],errors="coerce")
    dataset_final["release_year"]=dataset_final["release_date"].dt.year
    dataset_final["release_month"]=dataset_final["release_date"].dt.month
    dataset_final["release_decade"]=(dataset_final["release_year"]//10)*10

if {"budget","revenue"}.issubset(dataset_final.columns):
    dataset_final["profit"]=dataset_final["revenue"]-dataset_final["budget"]
    dataset_final["roi"]=np.where(dataset_final["budget"]>0,
                                  dataset_final["profit"]/dataset_final["budget"],
                                  np.nan)

dataset_final=eliminar_outliers_iqr(dataset_final,["runtime","vote_average"])

dataset_final.reset_index(drop=True,inplace=True)

print(dataset_final.info())
print(dataset_final.isnull().sum())

dataset_final.to_csv("../data/output/dataset_final.csv",index=False)
print("dataset_final.csv generado")
