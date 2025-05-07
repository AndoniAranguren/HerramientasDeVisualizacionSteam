import pandas as pd
import os
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a csv file.

    Args:
        file_path (str): Path to the csv file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    # No index are defined in the csv file
    df = pd.read_csv(file_path, encoding='utf-8', index_col=None, header=0)
    return df

def reduce_data(data_rec):
    data = data_rec[["AppID","Name", "Genres"]]
    data["Genres"] = data["Genres"].str.split(",")
    data = data.explode("Genres")
    remove_chars = ['"', "'"]
    for col in ["Name"]:
        for char in remove_chars:
            data[col] = data[col].str.replace(char, "", regex=False)

    data = data.dropna()

    data.to_csv("./data/data_reduced.csv")
    return data

    # Save the JSON data to a file
    #with open("./../data/genre_data.json", "w", encoding="utf-8") as f:
    #    f.write(str(data_reduced).replace("'", '"'))
#
    #return data_json

def group_and_json(data, top_how_many):
    data_or = data
    data = data.rename(columns = {"Genres": "name"})
    data = data.groupby(['name']).count().sort_values(by=["Name"], ascending=False)
    data['Name'] = data['Name'] / 111453
    data = data.rename(columns = {"Name": "value"})
    total = data['value'].sum()
    data = data.head(top_how_many)
    others = 1 - total 
    data = data[["value"]]
    
    
   
    csv = data
    csv.to_csv("./data/genres.csv")




    data_C = data_or.loc[data_or['Genres'].isin(["Indie", "Singleplayer","Action", "Casual", "Adventure"])][["Name","Genres"]]

    #data_C = data_C.groupby(["Name"])["Genres"].unique().reset_index()
    print(data_C)
    lista = []
    total_C = data_C.count()
    
    a = ["Indie", "Singleplayer","Action", "Casual", "Adventure"]
    dfs = []
    for i in range(len(a)):
        dfs.append(data_C.loc[data_C["Genres"] == a[i]])
        print(i,dfs[i])
    
    lista = []
    for i in range(len(a)):
        genero = []
        for j in range(len(a)):
            if a[i] != a[j]:
                un = pd.merge(dfs[i], dfs[j], on= "Name", how='inner')
                genero.append(un["Name"].count()/dfs[i]["Name"].count())
        lista.append(genero)
    
    df = pd.DataFrame(lista)
    print(df)
    df.to_csv("./data/relations.csv")

    #with open("./data/genres.csv", "a") as myfile:
    #    myfile.write("others" + "," + str(others))
    

    #quedan unos " " que hay que borrar en la colleccion
    # Save the JSON data to a file
    #with open("data/genre_data.json", "w", encoding="utf-8") as f:
    #    f.write(str(json).replace("'", '"'))
#
    #return data_json

if __name__ == "__main__":
    # Example usage
    data = load_data("data/data_reduced.csv")

    #data = reduce_data(data)
    group_and_json(data, 15)
    print("Done")
