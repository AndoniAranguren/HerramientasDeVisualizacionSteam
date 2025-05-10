import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load data from a csv file.

    Args:
        file_path (str): Path to the csv file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    # No index are defined in the csv file
    df = pd.read_csv(file_path, encoding='utf-8', header=0, index_col=False)
    return df

def get_hierarchy_publisher_developer_game_count(data, top_how_many = 10):

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
    top_publishers_names = publisher_rec_count.sort_values(by="Total_Reviews", ascending=False).head(top_how_many)["Publishers"].unique().tolist()

    publisher_json_list = []
    for publisher in top_publishers_names:
        data_publisher = data[data["Publishers"] == publisher]
        developers_list = data_publisher["Developers"].unique().tolist()
        developer_json_list = []
        for developer in developers_list:
            data_developer = data_publisher[data_publisher["Developers"] == developer]
            games_list = data_developer[data_developer["Developers"] == developer]["AppID"].unique().tolist()
            games_json_list = []
            for game in games_list:
                game_info = data_developer[data_developer["AppID"] == game].iloc[0]
                games_json_list.append({
                    "name": game_info["Name"],
                    "value": int(game_info["Reviews"]),
                })
            developer_json_list.append({
                "name": developer,
                "children": games_json_list
            })
        publisher_json_list.append({
            "name": publisher,
            "children": developer_json_list
        })
    data_json = {"name": "flare",
                "children": publisher_json_list}

    # Save the JSON data to a file
    with open("../charts/zoomable-sunburst/files/hierarchy_publisher_developer_game_count.json", "w", encoding="utf-8") as f:
        f.write(str(data_json).replace("'", '"'))

    return data_json

if __name__ == "__main__":
    # Example usage
    data = load_data("./../data/games.csv")
    data["Reviews"] = data["Positive"] + data["Negative"]
    data = data[data["Reviews"] > 0]

    get_hierarchy_publisher_developer_game_count(data, top_how_many=25)

    print("Done")
