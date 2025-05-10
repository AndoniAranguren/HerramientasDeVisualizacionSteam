import pandas as pd
import re
from collections import Counter
import json

# 1. Cargar el dataset
df = pd.read_csv("games_may2024_full.csv", low_memory=False)      # ajusta el nombre si es distinto

# 2. Normalizar el campo 'supported_languages'
#   • Eliminamos etiquetas HTML, paréntesis y guiones
#   • Separamos por ; , /  o salto de línea
#   • Pasamos a minúsculas y quitamos espacios extras
def clean_lang(raw):
    if pd.isna(raw):
        return []
    # Quitar HTML (p.ej. <br>, <strong>…) y paréntesis tipo "(+Audio)"
    raw = re.sub(r"<[^>]+>", " ", str(raw))
    raw = re.sub(r"\([^)]*\)", " ", raw)
    # Sustituir separadores por coma estándar
    raw = re.sub(r"[;/|•]", ",", raw)
    # Dividir, limpiar espacios y bajar a minúsculas
    langs = [l.strip().lower() for l in raw.split(",") if l.strip()]
    return langs

df["lang_list"] = df["supported_languages"].apply(clean_lang)

# 3. Construir el conteo global
all_langs = [lang for sub in df["lang_list"] for lang in sub]
counter = Counter(all_langs)

# 4.a Exportar a JSON para Observable (array de objetos)
wordcloud_data = [{"text": k, "value": v} for k, v in counter.items()]
with open("languages_wordcloud.json", "w", encoding="utf8") as f:
    json.dump(wordcloud_data, f, ensure_ascii=False, indent=2)

# 4.b Exportar a CSV simple por si quieres inspeccionarlo
pd.DataFrame(wordcloud_data).to_csv("languages_wordcloud.csv", index=False)