import pandas as pd
import requests
from typing import Set
import sqlite3
import json


#Carga los datos demográficos

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    datos_demograficos = pd.DataFrame()
    url = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=America/New_York&use_labels_for_header=true"
    datos_demograficos = pd.read_csv(url, sep=';')
    return datos_demograficos

#Parsea los datos de calidad del aire 

def ej_2_cargar_calidad_aire(ciudades: Set[str]) -> pd.DataFrame:
    Calidad_aire = pd.DataFrame(columns=["city"])
    for city in ciudades:
        api_url = 'https://api.api-ninjas.com/v1/airquality?city={}'.format(city)
        response = requests.get(api_url, headers={'X-Api-Key': "xlXXVUNmRBjmIpQqtqlDMQ==sDlzxl2lzG6v3btQ"})
        
        if response.status_code == 200:
            try:
                
                data = response.text
                new_row = pd.DataFrame([{"city": city, "quality_data": data }])
                Calidad_aire = pd.concat([Calidad_aire, new_row], ignore_index=True)
            except ValueError:
                
                print(f"Respuesta no es un JSON válido para la ciudad: {city}")
        else:
            
            print(f"Error {response.status_code} al obtener datos para la ciudad: {city}")
    
    return Calidad_aire

datos_demograficos = ej_1_cargar_datos_demograficos()

ciudades = set(datos_demograficos['City'].to_list())
ciudades_lista = list(ciudades)
primeras_diez_ciudades = ciudades_lista[:10]

calidad_aire_df = ej_2_cargar_calidad_aire(primeras_diez_ciudades)
print(calidad_aire_df.head())   

#Toma el elemento concentration de cada entrada por fila.


#Eliminar duplicados  y las columnas "Race", "Count", "Number of Veterans"

data_demograficos= datos_demograficos.drop(columns=["Race", "Count", "Number of Veterans"]).drop_duplicates().reset_index(drop=True)
print(data_demograficos.head())

calidad_aire_df.to_csv('calidad_aire.csv', index=False)
data_demograficos.to_csv('data_demograficos.csv', index=False)



