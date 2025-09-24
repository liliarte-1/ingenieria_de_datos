import os
import logging
import requests
import pandas as pd
import zipfile
import io


download_urls = {
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
}

#creamos la carpeta dowloads en la url (cambiar URL para seleccionar donde queremos guardarlo), si no existe ya
base_dir = r"D:\USJ_2025_2026\Ingenieria de Datos\Git\ingenieria_de_datos\Ejercicio1"
download_dir = os.path.join(base_dir, "downloads")
os.makedirs(download_dir, exist_ok=True)



#al parecer, la propia libreria detecta que zips se han descargado ya, pero seria conveniente 
# crear algun control de flujo para que solo se descarse si no esta ya descargado.

#de esta forma no hay que borrar los zips de la carpeta (PREGUNTAR SI SE PUEDE DE ESTA FORMA)
#con esto se extraeria el nombre pero no hace falta
#filename=os.path.basename(url)
#print(filename)

for url in download_urls:
    try:
        response = requests.get(url)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        zip_file.extractall(download_dir)
    
    #filtro para los zips
    except zipfile.BadZipFile:
        print(f"{url} no es un ZIP valido")

dataframes = []
    
#para cada csv dentro de la carpeta (lista una direccion) downloads
for csv in os.listdir(download_dir):
    #asegurarse de que acaba en csv, pero no es relevante aqui
    if csv.lower().endswith(".csv"):

    #el path de cada uno tendra que ser la carpeta donde esta guardado + /el nombre del archivo
    #el nombre es el objeto de iteración del primer bucle
        path = os.path.join(download_dir, csv)
        print(path)
        df = pd.read_csv(path)
        dataframes.append(df)

print(dataframes[0].head())

    
    #file_path=os.path.join(base_dir,"filename")        
    #response=

    #os.remove(filename)

