# Consumo de API publica
import requests
import pandas as pd
from pandas import json_normalize

# Se carga la data, utilizando pandas para cargarla en un dataframe.
url = 'https://open.canada.ca/data/api/action/package_show?id=98f1a129-f628-4ce4-b24d-6f16bf24dd64'
data_api = requests.get(url)
data_api = data_api.json()

# Se realiza filtrado de la respuesta de la api para obtener solo el contenido necesario
df2 = json_normalize(data_api['result'])

# Se realiza filtro para obtener los registros con language igual a 'en'
list_filtro = []
for x in df2.resources:
  for var in x:
    list_filtro.append(x[var['language'] == 'en'])
# Se crea un dataframe con la data filtrada por language
filtro_language = pd.DataFrame(list_filtro)

# Se escogen las columnas name y url
filtro_language = filtro_language[['name', 'url']]

# Se exporta el dataframe creado en formato csv 
filtro_language.to_csv('extraccion_datos_api.csv',sep='|', decimal=',')