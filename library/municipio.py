import json
from nested_lookup import nested_lookup
from difflib import SequenceMatcher
import pandas as pd

def municipio_nombre(texto):
    municipios = ''
    texto = texto.lower()
    texto = texto.replace('á','a').replace('à','a')
    texto = texto.replace('é','e').replace('è','e')
    texto = texto.replace('í','i').replace('ì','i')
    texto = texto.replace('ó','o').replace('ò','o')
    texto = texto.replace('ú','u').replace('ù','u').replace('ñ','n')
    texto = texto.replace('ç','c').replace(',',' ')
    texto = texto.replace('º',' ').replace(';','').replace('.',' ')
    texto = texto.replace('+','').replace('ª','').replace(':','')
    texto = texto.replace('(','').replace(')','').replace('<','').replace('>','').replace('  ','')
    cambio = ['el','la','l','els','los','las','es','sa','ses','les','a','o','as','camallera','monells','os']
    if '/' in texto:
        municipios = texto.split('/')
    else:
        municipios = texto
    if isinstance(municipios, list):
        temp_municipio = []
        for municipio in municipios:
            temp = municipio.split(' ', 1)
            if temp[0] in cambio:
                temp_municipio.append(" ".join(temp[1:]) + ', ' + temp[0])
            else:
                temp_municipio.append(" ".join(temp))
    else:
        temp_municipio = texto.split(' ', 1)
        if temp_municipio[0] in cambio:
            temp_municipio = " ".join(temp_municipio[1:]) + ', ' + temp_municipio[0]
        else:
            temp_municipio = " ".join(temp_municipio)
    return(temp_municipio)

def municipio_validar(municipios, results):
    df = pd.DataFrame(columns=['municipio','zipcode','ratio'])
    if isinstance(municipios, list): 
        for municipio in municipios:
            for key, value in results.items():
                #print(key + ', ' + municipio +': '+ str(SequenceMatcher(None, key.lower(), municipio).ratio()) + '  ' + str(value))
                ratio = SequenceMatcher(None, key.lower(), municipio).ratio()
                if ratio >= 0.8:
                    df.loc[len(df)] = {'municipio': municipio,'zipcode': str(value[0]),'ratio': ratio}
    else:
        municipio = municipios
        for key, value in results.items():
                #print(key + ', ' + municipio +': '+ str(SequenceMatcher(None, key.lower(), municipio).ratio()) + '  ' + str(value))
                ratio = SequenceMatcher(None, key.lower(), municipio).ratio()
                if ratio >= 0.8:
                    df.loc[len(df)] = {'municipio': municipio,'zipcode': str(value[0]),'ratio': ratio}
    if df.empty:
        zip_str = '0'
    else:
        if df.zipcode.nunique() == 1:
            zip_str = str(df.zipcode.unique()[0])
        else:
            results = df.iloc[df['ratio'].idxmax()]
            zip_str = str(results['zipcode'])
    return(zip_str)

def municipio_zipcode(municipio, json):
    municipios = municipio_nombre(municipio)
    results = {}
    if isinstance(municipios, list):
        for municipio in municipios:
            results.update(
                nested_lookup(
                    key = municipio,
                    document = json,
                    with_keys = True,
                    wild = True
                )
            )
    else:
        results.update(
            nested_lookup(
                key = municipios,
                document = json,
                with_keys = True,
                wild = True
            )
        )
    results_dict = municipio_validar(municipios, results)
    return(results_dict)