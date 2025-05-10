import pandas as pd
import re
from collections import Counter
import json

from src.prepare_data import load_data

data = load_data("./../data/games.csv")
data["Reviews"] = data["Positive"] + data["Negative"]
data = data[data["Reviews"] > 0]

# For each Publishers, get the number of recommendations accumulated for each game
publisher_rec_count = data.groupby(["Publishers"])["Reviews"].sum().reset_index()
publisher_rec_count = publisher_rec_count.rename(columns={"Reviews": "Total_Reviews"})

# Remove the " and ' characters from the Publishers, Developers and Name columns
columns = ["Name", "Publishers", "Developers"]
remove_chars = ['"', "'"]
for col in columns:
    for char in remove_chars:
        data[col] = data[col].str.replace(char, "", regex=False)

# Rank the top 50 publishers by the number of recommendations
top_publishers_names = publisher_rec_count.sort_values(by="Total_Reviews", ascending=False).head(10)[
    "Publishers"].unique().tolist()

# 1. Cargar el dataset desde json

df = pd.read_json("./../data/games.json").T     # ajusta el nombre si es distinto

# Get the games of the top publishers
top_publishers_games = data[data["Publishers"].isin(top_publishers_names)]

top_games_from_json = df[df.index.isin(top_publishers_games["AppID"].unique())]

descriptions = top_games_from_json["short_description"].values

# Eliminar stop words, números, caracteres especiales y convertir a minúsculas
def clean_description(raw):
    if pd.isna(raw):
        return ""
    # Quitar HTML (p.ej. <br>, <strong>…) y paréntesis tipo "(+Audio)"
    raw = re.sub(r"<[^>]+>", " ", str(raw))
    raw = re.sub(r"\([^)]*\)", " ", raw)
    # Sustituir separadores por coma estándar
    raw = re.sub(r"[;/|•]", ",", raw)
    # Dividir, limpiar espacios y bajar a minúsculas
    raw = re.sub(r"[^a-zA-Z0-9\s]", "", raw)
    return raw.strip().lower()
descriptions = [clean_description(desc) for desc in descriptions]

# Eliminar stop words
stop_words = set(["the", "and", "is", "to", "in", "of", "for", "a", "on", "that", "this", "it", "as", "with", "by"])
descriptions = [" ".join([word for word in desc.split() if word not in stop_words]) for desc in descriptions]

# Eliminar números
descriptions = [" ".join([word for word in desc.split() if not (word.isdigit() or word in ["i", "ii", "iii", "iv", "v"])]) for desc in descriptions]

# Export the description as a single txt file
with open("./../data/descriptions.txt", "w", encoding="utf-8") as f:
    for description in descriptions:
        f.write(description + "\n")