import folium
import pandas as pd


def create_map():
    map_loc = folium.Map(
        location=(49, 31),
        zoom_start=6,
        tiles='Stamen Terrain'  # maybe to change
    )

    locs = folium.FeatureGroup("123")  # not so conventional
    table = pd.read_csv("data/ua_regions.csv")
    coords = pd.read_csv("data/ua_regions_coords.csv")["Coords"].str[1:-1].str.split(",")

    for ind, row in enumerate(table.iterrows()):
        row = row[1]
        point = coords[ind - 1]

        # to check the correctness
        data = f"""{row["Регіон"]}

                   Cases: {row["Випадкiв"]}
                   Recovered: {row["Одужало"]}
                   Deaths: {row["Померло"]}"""
        locs.add_child(folium.Marker(location=point, popup=data))

    map_loc.add_child(locs)

    return map_loc._repr_html_()
