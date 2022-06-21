# Importare librarii necesare
from asyncore import read
from cgi import print_form
from importlib.resources import path
from logging import shutdown
from multiprocessing.connection import wait
from nturl2path import pathname2url
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import glob
import os
from numpy import equal
import pandas as pd
import json
import geojson
import csv
from pandas.io.json import json_normalize
import influxdb_client
import matplotlib
from statsmodels.tsa.api import Holt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# Realizarea conexiunii cu InfluxDB
token = "G6D1pD2v4wsQSCjgUEtJYZA_myiaQUdIJLS7D7LhJVhIJyta-G7ip7iUi2PlZ-yP_EtjC8gWyy00xyKbgKs0qA=="
org = "Licenta-UPT"
bucket = "Licenta_2022"
url = "http://localhost:8086"

# Instanta client
client = InfluxDBClient(url=url, token=token, org=org, debug=False)
# Instanta scriere
write_api = client.write_api(write_options=WriteOptions(batch_size=80_000, flush_interval=10_000, jitter_interval=2_000, retry_interval=5_000))

# Scrierea datelor in InfluxDB
def f_call():
    path = 'D:\Facultate\Licenta\Date\Date_1\call'
    files = glob.glob(path + "/*.csv")
    for filename in files:
        df = pd.read_csv(filename, index_col=None)
        # Pregatirea datelor
        fields = ['datetime', 'CellID', 'provinceName', 'cell2Province', 'Province2cell'] 
        datatags = ['provinceName']
        # Pastrarea coloanele de interes
        df = df[fields]
        # Geolocatie - coordonate geojson
        with open("D:\Facultate\Licenta\Date\Date_1\milano-grid.geojson", "r") as pathX:
            data = json.load(pathX)
            df1 = pd.DataFrame(data["features"])
            df1['cellId'] = df1['properties'].apply(lambda x: x['cellId'])
            df1['lat'] = df1['geometry'].apply(lambda x: x['coordinates'][0][0][1])
            df1['lon'] = df1['geometry'].apply(lambda x: x['coordinates'][0][0][0])
            df1 = df1.drop(['type', 'id', 'geometry', 'properties'], axis=1)
        df2 = pd.merge(df, df1, left_on= 'CellID', right_on= 'cellId') 
        df2 = df2.drop(['cellId'], axis=1)
        print(df2)
        #Indexare
        df2.set_index('datetime',inplace=True)
        #Scriere
        write_api.write(bucket, record=df2, data_frame_measurement_name='Activitatea telefoanelor', data_frame_tag_columns=datatags)

def f_sms():
    path = 'D:\Facultate\Licenta\Date\Date_1\sms'
    files = glob.glob(path + "/*.csv")
    #Inlocuire 'CountryCode' cu 'CountryName' in fisierele sms 
    for filename in files:
        df = pd.read_csv(filename, index_col=None)
        fields = ['datetime', 'CellID', 'countrycode', 'smsin', 'smsout', 'callin', 'callout', 'internet'] 
        df = df[fields]
        df1 = pd.read_csv('D:\Facultate\Licenta\Date\Date_1\CountryCode.csv')
        df2 = pd.merge(df, df1, on='countrycode')
        # print(df2)
        fields1 = ['datetime', 'CellID', 'CountryName', 'smsin', 'smsout', 'callin', 'callout', 'internet']
        datatags1 = ['CountryName']
        df2 = df2[fields1]
        # Geolocatie - coordonate geojson
        with open("D:\Facultate\Licenta\Date\Date_1\milano-grid.geojson", "r") as pathX:
            data = json.load(pathX)
            df3 = pd.DataFrame(data["features"])
            df3['cellId'] = df3['properties'].apply(lambda x: x['cellId'])
            df3['lat'] = df3['geometry'].apply(lambda x: x['coordinates'][0][0][1])
            df3['lon'] = df3['geometry'].apply(lambda x: x['coordinates'][0][0][0])
            df3 = df3.drop(['type', 'id', 'geometry', 'properties'], axis=1)
        df4 = pd.merge(df2, df3, left_on= 'CellID', right_on= 'cellId') 
        df4 = df4.drop(['cellId'], axis=1)
        print(df4)
        df4.set_index('datetime',inplace=True)
        write_api.write(bucket, record=df4, data_frame_measurement_name='Activitatea telefoanelor', data_frame_tag_columns=datatags1)

#Query
def query_1():
    query_api = client.query_api()
    query = 'from(bucket: "Licenta")\
    |> range(start: 2013-11-01, stop: 2013-11-02)\
    |> filter(fn: (r) => r._measurement == "Date_9")\
    |> filter(fn: (r) => r._field == "internet")\
    |> filter(fn: (r) => r.CountryName == "Italy" )\
    |> limit(n:20)\
    |> keep(columns:["_time", "_value"])' 

    final_df = client.query_api().query_data_frame(org=org, query=query)
    final_df["_time"] = pd.to_datetime(final_df["_time"].astype(str))
    final_df = final_df.drop(columns=["result", "table"])
    final_df = final_df.set_index("_time")
    final_df.plot()

def prognozare():
    # Interogarea datelor
    query = 'from(bucket: "Licenta") \
    |> range(start: 2013-11-01, stop: 2013-11-02) \
    |> filter(fn: (r) => r._measurement == "Date_9") \
    |> filter(fn: (r) => r.CountryName == "Italy") \
    |> filter(fn: (r) => r._field == "internet")'
    # Query dataframe
    df = client.query_api().query_data_frame(org=org, query=query)
    #Pregatirea datelor
    df_holt = df.set_index("_time") # setare index
    df2 = df_holt.iloc[:,4] # pastrarea indexului si valorilor

    df3 = Holt(df2,damped_trend=True,initialization_method="estimated").fit(optimized=True)
    df4 = df3.forecast(10).rename("Prognozarea in timp")
    # Caracteristicile vizualizarii
    plt.figure(figsize=(10, 8))
    plt.plot(df_holt["_value"], marker='o', color='black')
    plt.plot(df3.fittedvalues, color='green')
    line1, = plt.plot(df4, marker='o', color='red')
    plt.legend([line1], [df4.name])

def locatie():
    path = 'D:\Facultate\Licenta\Date\Test\sms'
    files = glob.glob(path + "/*.csv")
    for filename in files:
        df = pd.read_csv(filename, index_col=None)
        fields = ['CellID','internet'] 
        df = df[fields]
        df4 = df.groupby('CellID')["internet"].sum() 

        with open("D:\Facultate\Licenta\Date\Test\milano-grid.geojson", "r") as pathX:
            data = json.load(pathX)
            df3 = pd.DataFrame(data["features"])
            df3['cellId'] = df3['properties'].apply(lambda x: x['cellId'])
            df3['lat'] = df3['geometry'].apply(lambda x: x['coordinates'][0][0][1])
            df3['lon'] = df3['geometry'].apply(lambda x: x['coordinates'][0][0][0])
            df3 = df3.drop(['type', 'id', 'geometry', 'properties'], axis=1)
        df2 = pd.merge(df4, df3, left_on= 'CellID', right_on= 'cellId')

    fig = px.scatter_mapbox(df2, lat="lat", lon="lon", hover_data=["cellId"], 
                                color = 'internet', zoom=12, height=500, 
                                mapbox_style = "carto-positron") 
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# #Stergerea masuratorilor din influxDB
# start = "1970-01-01T00:00:00Z"
# stop = "2022-01-01T00:00:00Z"
# delete_api = client.delete_api()
# delete_api.delete(start, stop, '_measurement = "Date_9"', bucket=bucket, org=org) 

# Executie fisier
if __name__ == "__main__":
    # f_call()
    # f_sms()
    # query_1()
    prognozare()
    # locatie()