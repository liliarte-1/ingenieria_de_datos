import os
import logging
import requests
#import zipfiles 


download_urls = {
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
"https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
}

base_dir = r"D:\USJ_2025_2026\Ingenieria de Datos\Git\ingenieria_de_datos\Ejercicio1"
download_dir = os.path.join(base_dir, "downloads")
os.makedirs(download_dir, exist_ok=True)




#for url in download_urls:
    #filename=os.path.basename(url)
    #file_path=os.path.join(base_dir,"filename")        
    #response=

    #os.remove(filename)

