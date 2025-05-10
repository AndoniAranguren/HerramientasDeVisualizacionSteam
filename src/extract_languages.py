import pandas as pd
import re
from collections import Counter
import json

# 1. Cargar el dataset
df = pd.read_csv("games_may2024_full.csv", low_memory=False)

# 2. Normalizar el campo 'supported_languages'
def clean_lang(raw):
    if pd.isna(raw):
        return []
    # 2.1 Quitar HTML (<br>, <strong>…) y paréntesis tipo "(+Audio)"
    raw = re.sub(r"<[^>]+>", " ", str(raw))
    raw = re.sub(r"\([^)]*\)", " ", raw)
    # 2.2 Unificar separadores en coma
    raw = re.sub(r"[;/|•]", ",", raw)
    # 2.3 Eliminar comillas simples y dobles
    raw = raw.replace("'", "").replace('"', "")
    # 2.4 Separar en tokens y procesar cada idioma
    langs = []
    for part in raw.split(","):
        part = part.strip().lower()
        if not part:
            continue
        # 2.4.1 Tomar solo la primera palabra (antes de espacios o guiones)
        first = re.split(r"[\s\-]+", part)[0]
        # 2.4.2 Quitar todo lo que no sea letra (incluye acentos)
        letters_only = "".join(ch for ch in first if ch.isalpha())
        if letters_only:
            langs.append(letters_only)
    return langs

df["lang_list"] = df["supported_languages"].apply(clean_lang)

# 3. Lista completa (mantiene repeticiones en orden original)
all_langs = [lang for sub in df["lang_list"] for lang in sub]

# 4.a Exportar a JSON para Observable (conteos únicos)
counter = Counter(all_langs)
wordcloud_data = [{"text": k, "size": v} for k, v in counter.items()]
with open("languages_wordcloud.json", "w", encoding="utf8") as f:
    json.dump(wordcloud_data, f, ensure_ascii=False, indent=2)

# 4.b Exportar a CSV simple
pd.DataFrame(wordcloud_data).to_csv("languages_wordcloud.csv", index=False)

# 5. Exportar TXT con cada idioma (repetido) separado por espacio
with open("languages_all.txt", "w", encoding="utf8") as f_txt:
    f_txt.write(" ".join(all_langs))
s_wordcloud.csv", index=False)