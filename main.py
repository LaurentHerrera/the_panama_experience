import folium
import ast
import base64
from pathlib import Path
import pandas as pd
import random

def main():
    mapObj = folium.Map(location=[8.4272562,-80.1337719], zoom_start=8)
    panama_provinces_geojson = "https://s3.amazonaws.com/tabulario/Data/Instituto+Tommy+Guardia/limites-geograficos-de-panama/provincias-panama.geojson" # This part is to divide Panama into provinces and comarcas (at the date we have ten provinces and four comarcas with province status)
    borderStyle = { # Here I define my border style
        'color': 'black',
        'weight': 3,
        'fillOpacity': 0,
        'dashArray': '5, 5'
    }
    
    folium.GeoJson(panama_provinces_geojson, style_function=lambda x: borderStyle).add_to(mapObj) # I add my argument to the GeoJson function and I put the Panama's coordinate and border style

    # I declare where is my .csv file (iow my dataset) and the images
    panama_dataset = Path.cwd() / "fun_facts_panama.csv"
    images = Path.cwd() / "static"

    df = pd.read_csv(filepath_or_buffer=panama_dataset, sep=";", index_col=False)

    # I call the function we made
    add_info(df, images, mapObj)

    # THIS IS THE END, JUST REMEMBER TO OPEN THE "Panama.html" WHICH IS THE RESULT OF THIS SCRIPT
    mapObj.save("Panama.html")

def add_info(df, images, mapObj):
    # I iterate over my dataset
    for i, val in df.iterrows():
        # My column index of the dataset now is the number of the image file that will represent my info later
        image_index = val['Index']
        # with list and .glob I find the file with my Index number, e.g. if my image_index = 1 then my image would look like this "1.jpg "
        image_panama = list(images.glob(f"{image_index}.*"))
        
        # I decode my image in order to be read inside my html
        with open(image_panama[0], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

        # here I declare the information of the rows as my variables in order to recall it later as a string
        mission = val['Mission']
        description = val['Perspective text']
        location = ast.literal_eval(val['Location'])

        # this is when you click on the leaf
        popup_fun_fact = f"""
        <div style="text-align: center;">
            <strong>{image_index}. {mission}</strong><br><br>
            <div style="text-align: justify;">{description}</div> <br>
            <img src="data:image/jpeg;base64,{encoded_string}" style="max-width: 200px;">
        </div>
        """
        # the different types of leaf color, to have a diversity of colors
        images_files = ["leaf-orange.png", "leaf-green.png", "leaf-red.png"]
        icon_image = str(images / random.choice(images_files))
        shadow_image = str(images / "leaf-shadow.png")

        icon = folium.CustomIcon(
            icon_image,
            icon_size=(38, 95),
            icon_anchor=(22, 94),
            shadow_image=shadow_image,
            shadow_size=(50, 64),
            shadow_anchor=(4, 62),
            popup_anchor=(-3, -76),
        )

        # here we add a new leaf to the map
        folium.Marker(location=location, icon=icon, popup=popup_fun_fact, tooltip=f"<center>{mission}</center>").add_to(mapObj)

if __name__ == "__main__":
    main()