import json
from nested_lookup import nested_lookup
from difflib import SequenceMatcher
import pandas as pd

def provincia_texto(texto):
    texto = texto.lower()
    texto = texto.replace('á','a').replace('à','a')
    texto = texto.replace('é','e').replace('è','e')
    texto = texto.replace('í','i').replace('ì','i')
    texto = texto.replace('ó','o').replace('ò','o')
    texto = texto.replace('ú','u').replace('ù','u')
    return(texto)

def provincia_validar(nombre, json):
    df = pd.DataFrame(columns=['provincia','ratio'])
    nombre = provincia_texto(nombre)
    listado_provincias = list(nested_lookup(key = 'provincia', document = json, wild = True))
    for provincia in listado_provincias:
        ratio = SequenceMatcher(None, nombre, provincia.lower()).ratio()
        if ratio >= 0.75:
            df.loc[len(df)] = {'provincia': provincia, 'ratio': ratio}
            #print(nombre+' -> '+provincia+': '+str(ratio))
        elif len(provincia.split(' ')) > 1:
            temp = provincia.split(' ')[-1].lower()
            ratio = SequenceMatcher(None, nombre, temp).ratio()
            if ratio >= 0.75:
                df.loc[len(df)] = {'provincia': provincia, 'ratio': ratio}
    if df.empty:
        results = 'No Encontrado'
    else:
        results = df.iloc[df['ratio'].idxmax()]
        results =results['provincia']
    return(results)

def provincia_informacion(nombre, json):
    provincia = provincia_validar(nombre, json)
    json = json[0]['espana']
    item = next((item for item in json if item['provincia'] == provincia), None)
    return(item)