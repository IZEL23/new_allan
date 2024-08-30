# %%
import hug
import geopandas as gpd
import pandas as pd
import numpy as np
import json

def process_geojson(file_path='./UBS_BRASIL.geojson'):
    
    print("Desafio do Allan Izel")
        
    try:
        gdf_ubs_brasil = gpd.read_file(file_path)
        print("File loaded")
    except FileNotFoundError:
        open(file_path, 'w').close()
        print("File not found")
        return [], False

    print(gdf_ubs_brasil.head())
    
    gdf_ubs_brasil.plot()
    
    is_all_points = all(gdf_ubs_brasil.geometry.geom_type == 'Point')
    
    # Cria uma lista de tuplas com coordenadas (latitude, longitude)
    coordinates = [(geom.y, geom.x) for geom in gdf_ubs_brasil.geometry]
    
    return coordinates, is_all_points


# %%
# Função principal para ser usada com o Hug
@hug.cli()
def main(filepath: hug.types.text, output_csv: hug.types.text = 'coordenadas.csv'):
    coordinates, is_all_points = process_geojson(filepath)
    
    # Cria um DataFrame com as coordenadas
    df = pd.DataFrame(coordinates, columns=['Latitude', 'Longitude'])
    
    # Salva o DataFrame em um arquivo CSV
    df.to_csv(output_csv, index=False)
    print(f'Coordenadas exportadas para {output_csv}')
    
    resultado = {
        "Coordinates": coordinates,
        "All geometries are Points": is_all_points
    }
    
    print(json.dumps(resultado, indent=4))
    return resultado

if __name__ == "__main__":
    main.interface.cli()