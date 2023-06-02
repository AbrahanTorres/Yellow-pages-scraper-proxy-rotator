#https://www.geeksforgeeks.org/web-scraping-without-getting-blocked/

import requests
from requests.adapters import HTTPAdapter
# use to parse html text
from lxml.html import fromstring 
from itertools import cycle
import traceback
from bs4 import BeautifulSoup
from time import sleep
import urllib3
import pandas as pd
import datetime

def to_get_proxies():
    # website to get free proxies
    url = 'https://free-proxy-list.net/' 
    #url = 'https://www.geonode.com/free-proxy-list/'

    response = requests.get(url)

    parser = fromstring(response.text)
    # using a set to avoid duplicate IP entries.
    proxies = set() 

    for i in parser.xpath('//tbody/tr')[:10]:

        # to check if the corresponding IP is of type HTTPS
        if i.xpath('.//td[7][contains(text(),"yes")]'):

            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                            i.xpath('.//td[2]/text()')[0]])

            proxies.add(proxy)
            type(proxies)    
    return proxies


proxies = to_get_proxies()
#print(proxies)

# to rotate through the list of IPs
proxyPool = cycle(proxies) 

print(proxyPool)

# insert the url of the website you want to scrape.
#url = 'https://httpbin.org/ip'   #website que devuelve el ip en json.
urls = ['https://www.elmundo.es/','https://elpais.com/','https://www.cnbc.com/world/?region=world']

try:
    proxy = next(proxyPool)
except StopIteration:
    # si no hay más proxies disponibles, volver a iniciar el iterable
    proxyPool = iter(proxies)
    proxy = next(proxyPool)

df = pd.DataFrame(columns=['falla','proxy','url','respuesta', 'tiempo'])

for i in range(0,5): 
    for url in urls:
        # Aumentar el número de intentos al request
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=4)
        session.mount("https://", adapter)
        session.mount("http://", adapter)

        # Bucle while de busqueda de proxy funcional.
        proxies_rapidos = [] # lista auxiliar para almacenar los proxies que cumplen con el umbral de tiempo de respuesta
        attempts = 0
        max_attempts = 3
        falla = False  # valor inicial de falla
        while attempts < max_attempts:
            try:
                response = session.get(url, proxies={"http": proxy, "https": proxy})
                tiempo = response.elapsed.total_seconds()
                if tiempo > 4:  # si el tiempo de respuesta es mayor a 4 segundos
                    falla = True
                    print(f'ERROR PROXY: {proxy} Fallo: {falla} Tiempo: {tiempo}')
                    proxy = next(proxyPool)  # pasar al siguiente proxy
                    continue
                else:
                    # si el tiempo de respuesta es menor o igual a 4 segundos, agregar el proxy a la lista auxiliar
                    proxies_rapidos.append(proxy)
                break  # interrumpe el bucle si se obtiene una respuesta
            except (requests.exceptions.SSLError, 
                    requests.exceptions.ConnectionError, 
                    requests.exceptions.Timeout,
                    requests.exceptions.ProxyError,
                    requests.exceptions.ChunkedEncodingError):
                falla = True
                print(f'ERROR PROXY: {proxy} Fallo: {falla} Tiempo: {tiempo}')
                attempts += 1
                proxy = next(proxyPool) 
                sleep(1) 

        # si el proxy fue agregado a la lista auxiliar, agregarlo al pool de proxies
        if proxy in proxies_rapidos:
            proxyPool = cycle(proxies_rapidos)
        
        # Conexión establecida con el proxy funcional.
        print("Request #%d" % i)
        print(f"Website: {url} \nProxy: {proxy} \nStatus: {response.status_code} \nTiempo: {tiempo} ")

        # Scrape de la página del url
        soup = BeautifulSoup(response.text, 'lxml')

        # Agregando data al dataframe
        row = {"falla":falla, "proxy": proxy, "url": url, "respuesta": response.status_code, "tiempo": tiempo}
        df = df.append(row, ignore_index=True)    

df.to_csv("mydf3.csv", mode= "w+", index=False)


















#    try:
#        response = requests.get(url, proxies={"http": proxy, "https": proxy})
#        # print(response)
#        # print(response.json())
#        while response.status_code == 200:
#            print("Se ha establecido conexión")
#            soup = BeautifulSoup(response.text, 'lxml')
#            print(soup.title)
#            # print(soup.title.text)
#            # print(soup.title.parent)
#            # print(soup)
#        
#    #SI PRXY FALLA NUEVO PRXY E INTENTO DE NUEVO
#        else:
#            sleep(10) 
#            proxy = next(proxyPool)
#    except Exception as err:
#        print(f"Skipping.  Connection error: {err}")
    
