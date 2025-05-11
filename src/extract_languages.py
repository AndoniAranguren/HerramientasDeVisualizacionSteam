import pandas as pd
import re

# 1. Cargar el dataset
df = pd.read_csv("./../data/games.csv", low_memory=False)

# 2. Normalizar el campo 'supported_languages'
def clean_lang(raw):
    if pd.isna(raw):
        return []
    # Poner en minuscula
    raw = str(raw).lower()
    # Quitar [ ] , " y '
    raw = raw.replace("[", "").replace("]", "").replace('"', "").replace("'", "")
    # Replace \r\\n
    raw = raw.replace("\\r\\n", "")
    # Replace (text only) and (full audio)
    raw = re.sub(r"\(text only\)", "", raw)
    raw = re.sub(r"b/b", "", raw)
    raw = re.sub(r"\r\n\r\n", "", raw)
    raw = re.sub(r"/b", "", raw)

    raw = re.sub(r"&amp", "", raw)
    raw = re.sub(r"lt", "", raw)
    raw = re.sub(r"strong&amp", "", raw)
    raw = re.sub(r"gt", "", raw)

    raw = re.sub(r";", "", raw)

    # Separar por comas
    langs = [lang.strip() for lang in raw.split(",")]
    return langs

df["lang_list"] = df["Supported languages"].apply(clean_lang)

# Crear una lista de cada año desde el valor mínimo a 1 de enero y hasta este año
# 3.1. Obtener el año mínimo y máximo
df["Release date"] = pd.to_datetime(df["Release date"], errors='coerce')
min_year = df["Release date"].min()
max_year = df["Release date"].max()

# 3.2. Crear una lista de años desde el mínimo hasta el máximo
years = pd.date_range(start=min_year, end=max_year+1, freq="Y").year.tolist()

# Drop rows with NaT in Release date
df = df.dropna(subset=["Release date"])

# For every year count the amount of times each language appears if it in that year of any of the previous ones
# 3.3. Crear un diccionario para almacenar por cada año, por cada lenguaje el número de veces que aparece
lang_count_by_year = {year: {} for year in years}
for index, row in df.iterrows():
    try:
        release_year = pd.to_datetime(row["Release date"]).year
        for lang in row["lang_list"]:
            if lang != "":
            # Si el lenguaje no está en el diccionario, inicializarlo
                if lang not in lang_count_by_year[release_year]:
                    lang_count_by_year[release_year][lang] = 0
                # Incrementar el contador del lenguaje para ese año
                for year in years:
                    if year >= release_year:
                        if lang not in lang_count_by_year[year]:
                            lang_count_by_year[year][lang] = 1
                        else:
                            lang_count_by_year[year][lang] += 1
    except:
        print(f"Error processing year: {row['lang_list']} {row['Release date']}")
        continue

# Create an array of dictionaries with date: 2000-01-01 name: "language" category: "latin or anglo or other" value: 1
lang_data = []
for year, langs in lang_count_by_year.items():
    for lang, count in langs.items():
        if lang != "":
            lang_data.append({
                "date": f"{year}-01-01",
                "name": lang,
                "category": "latin"
                    if lang in ["italian", "french", "spanish", "spanish - latin america", "spanish - spain",
                                                    "portuguese", "portuguese - brazil", "romanian"]
                    else "anglo" if lang in ["german", "english", "dutch"]
                    else "slavic" if lang in ["russian", "bulgarian", "ukrainian"]
                    else "nordic" if lang in ["swedish", "norwegian", "danish", "finnish"]
                    else "japanese" if lang in ["japanese"]
                    else "korean" if lang in ["korean"]
                    else "arabic" if lang in ["arabic"]
                    else "turkish" if lang in ["turkish"]
                    else "greek" if lang in ["greek"]
                    else "czech" if lang in ["czech"]
                    else "hungarian" if lang in ["hungarian"]
                    else "chinese" if lang in ["traditional chinese", "simplified chinese"] else "other",
                "value": count
            })

# Save lang_data as a csv file
pd.DataFrame(lang_data).to_csv("./../data/languages_by_year.csv", index=False)