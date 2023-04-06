from pathlib import Path
from datetime import datetime
import sys, logging, platform,warnings
log_file = Path(__file__).resolve().parent / 'logs' /  ('log_PA_'+str(datetime.now().strftime('%Y%m%d')) +'.log')
logging.basicConfig(
    filename=log_file, 
    filemode='a+',
    format='[%(asctime)s](%(funcName)s)/%(lineno)d\t%(levelname)s: %(message)s',
    datefmt='%Y%m%d-%H:%M:%S',
    level=logging.INFO
)
try:
    from bs4 import BeautifulSoup
    import json,phonenumbers,sqlalchemy,re
    import pandas as pd
    from sqlalchemy import create_engine
    from urllib.parse import urlsplit
    from selenium import webdriver
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
    from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager
    from random import randint
    from time import sleep
    from pandas.core.common import SettingWithCopyWarning
    warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
    warnings.simplefilter(action='ignore', category=FutureWarning)
except Exception as e:
    logging.error("ERROR AL CARGAR MODULO: " + str(e))
    print("ERROR AL CARGAR MODULO: " + str(e))
    quit()

def pagina_vacia(engine,directorio,pagina,tipo,now):
    try:
        tempDF = pd.DataFrame([[directorio,pagina,tipo,now]],columns=['directorio','pagina','seccion','fecha'])
        tempDF.to_sql (name = 'bbdd_directorios_paginas_vacias_temp', con = engine , if_exists = 'append', index = False)
    except Exception as e:
        logging.error('\t\t\tPAGINA VACIA: ' + str(pagina) + ' - ' + str(tipo))
        print(e)

def main(envar,driver):
    logging.info('---INICIO---')
    try:
        engine = create_engine('postgresql+pg9000://' + envar['ddbb_user'] + ':' + envar['ddbb_pass'] + '@pentaho:xxxxx/' + envar['ddbb_name'])
        logging.info('\tCONEXION BASE DATOS CREADA')
    except Exception as e:
        print('\tCONEXION NO ESTABLECIDA: ' +str(e))
        logging.error('\tCONEXION NO ESTABLECIDA: ' +str(e))
        quit()
    now = datetime.strptime('2022-12-01', '%Y-%m-%d')
    now = now.date()
    consulta = '''SELECT DISTINCT pagina, seccion FROM bbdd_directorios_temp WHERE directorio = 'paginasAmarillas' and fecha = '2022-12-01'
                UNION ALL
                SELECT DISTINCT pagina, seccion FROM bbdd_directorios_paginas_vacias_temp WHERE directorio = 'paginasAmarillas' and fecha = '2022-12-01'
                ORDER BY seccion, pagina;'''
    try:
        consultaDF = pd.read_sql_query(consulta, engine)
        print(consultaDF)
    except Exception as e:
        logging.error('\tDATA CARGADA: ' +str(e))
        quit()
    try:
        driver.set_window_position(5, 5)
        driver.set_window_size(1100, 1400)
        driver.set_page_load_timeout(30)
        driver.get('https://www.paginasamarillas.es/')
        logging.info('\tINICIO NAVEGADOR CORRECTO')
    except Exception as ex:
        logging.warning("INICIO NAVEGADOR: " + str(ex))   
    try:
        sleep(5)
        driver.find_element("xpath",'//*[@id="onetrust-accept-btn-handler"]').click()
        logging.info('\tEXPANSION COOKIES ACEPTADAS')
    except Exception as ex:
        logging.error("COOKIES: " + str(ex))
        quit()

    sleep(3)
    lista_cat = ['a/profesionales','a/belleza-y-estetica','a/coches','a/construccion','a/deportes','a/despachos','a/empresas-de-transportes','a/enseñanza','a/hogar','h/hotel',
        'a/informatica','a/jardineria','a/muebles','a/ocio','a/pisos','a/artes-graficas','r/restaurantes','a/centro-de-salud','a/seguridad','a/seguros',
        'a/servicios-a-empresas','a/viajes','a/banca']
    #cargados = []
    #cargados = ['banca', 'belleza-y-estetica','coches','construccion','deportes','despachos','empresas-de-transportes','enseñanza','hogar','hotel','informatica','jardineria',
    #    'muebles','ocio','pisos','profesionales','artes-graficas','restaurantes','centro-de-salud','seguridad','seguros','servicios-a-empresas']
    for cat in lista_cat:
        tipo = cat.split("/")[1]
        cargadas = consultaDF[consultaDF['seccion'] == tipo]  # la columna sección en el dataframe será igual al tipo de categoría
        cargadas = list(cargadas['pagina'])
        logging.info('\tINICIO CATEGORIA "' + tipo + '"')
        #for i in range(0,4):
        for pagina in range(0,10000):
            if pagina in cargadas:
                logging.info('\t\t\tPAGINA "' + str(pagina) + '" CARGADA')
                continue
            df = pd.DataFrame(columns=['directorio','link','pagina','categoria','subcategoria','especialidad','nombre','texto_telefono','telefono_1','correo','direccion',
                'ciudad','provincia','zipcode','web','fecha','seccion','pa_free','lat','long'])
            print(cat + ' - ' + str(pagina))
            sleep(randint(2,5))
            if pagina == 0:
                html = 'https://www.paginasamarillas.es/' + cat
            else:
                html = 'https://www.paginasamarillas.es/' + cat + '/' + str(pagina)
            try:
                driver.get(html)
                logging.debug('\t\t\tdriver.get "' + str(html) + '"')
            except Exception as ex:
                #print("Exception has been thrown. " + str(ex))
                logging.debug('\t\t\tdriver.get "' + str(html) + '"')
                sleep(10)
                try:
                    driver.get(html)
                    logging.debug('\t\t\tdriver.get "' + str(html) + '"')
                except Exception as ex:
                    logging.warning('\t\t\tdriver.get: Exception has been thrown. ' + str(ex))
            contents = driver.page_source
            soup = BeautifulSoup(driver.page_source, features="html.parser")
            #soup = BeautifulSoup(contents, features="lxml")
            temp = soup.find_all('div',class_='span-24')
            if len(temp) > 0 and temp[0].contents[0].next == ' Lo sentimos pero no hemos encontrado lo que estabas buscando. ':
                break
            temp = soup.find_all('div',class_='cabecera')
            pages = []
            for html in temp:
                pages.append(html.contents[0].contents[0].contents[0].contents[1].attrs['href'])   # POR QUÉ 4 CONTENTS?
                #print(html.contents[0].contents[0].contents[0].contents[1].attrs['href'])
            for html in pages:
                print('  ->  ' + str(html))
                sleep(randint(2,5))
                #html = 'https://www.paginasamarillas.es/f/sitges/fincas-maricel_008548703_000000001.html'
                try:
                    driver.get(html)
                    logging.debug('\t\t\tdriver.get "' + str(html) + '"')
                except TimeoutException as ex:
                    #print("Exception has been thrown. " + str(ex))
                    logging.debug('\t\t\tdriver.get "' + str(html) + '"')
                    sleep(10)
                    try:
                        driver.get(html)
                        logging.debug('\t\t\tdriver.get "' + str(html) + '"')
                    except TimeoutException as ex:
                        logging.warning('\t\t\tdriver.get: Exception has been thrown. ' + str(ex))
                soup = BeautifulSoup(driver.page_source, features="html.parser")
                #soup = BeautifulSoup(contents, features="lxml")
                error = soup.body.findAll(text="Lo sentimos, no hemos podido encontrar la página que buscas.") # POR QUÉ BODY FINDALL ES ERROR?
                if len(error) > 0:
                    sleep(600)
                    try:
                        driver.get(html)
                        logging.debug('\t\tdriver.get "' + str(html) + '"')
                    except TimeoutException as ex:
                        #print("Exception has been thrown. " + str(ex))
                        logging.debug('\t\tdriver.get "' + str(html) + '"')
                        sleep(10)
                        try:
                            driver.get(html)
                            logging.debug('\t\tdriver.get "' + str(html) + '"')
                        except TimeoutException as ex:
                            logging.warning('\t\tdriver.get: Exception has been thrown. ' + str(ex))
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                soup = BeautifulSoup(driver.page_source, features="html.parser")
                error = soup.body.findAll(text="Lo sentimos, no hemos podido encontrar la página que buscas.")
                if len(error) > 0:
                    continue
                temp = soup.find_all('div',class_='contenedor')
                try:
                    business = json.loads(temp[0].attrs['data-business'])  # POR QUÉ temp[0]?
                except Exception as ex:
                    logging.warning('\t\t\tjson.loads: Exception has been thrown. ' + str(ex))
                    continue
                address = soup.find_all('span',class_='address')
                if len(address) != 0:
                    if isinstance(address[0].contents[0], str):
                        direccion = business['info']['businessAddress']
                        codpostal=''
                    else:
                        for element in address[0].contents:
                            if element.has_attr('itemprop') and element.attrs['itemprop'] == 'streetAddress': #POR QUÉ DOS VECES VERIFICAR SI TIENE ATRIBUTOS ITEMPROP EL ELEMENTO?
                                direccion = element.contents[0]
                            elif element.has_attr('itemprop') and element.attrs['itemprop'] == 'postalCode':
                                codpostal = element.contents[0]
                            else:
                                continue
                else:
                    direccion = business['info']['businessAddress']
                    codpostal=''
                texto_telefono = business['info']['phone'] if "phone" in business['info'] else None
                try:
                    telefono = phonenumbers.format_number(phonenumbers.parse(texto_telefono, 'ES'), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                    telefono = telefono.replace(' ','')
                except Exception:
                    telefono = None
                if "location" in business:
                    lat = float(business['location']['latitude']) if "latitude" in business['location'] else None
                    long = float(business['location']['longitude']) if "longitude" in business['location'] else None
                else:
                    lat = None
                    long = None
                df = df.append({
                    'directorio':'paginasAmarillas',
                    'link': html if html is None else html.rstrip(),
                    'pagina': pagina,
                    'categoria': tipo,
                    'subcategoria': business['info']['activity'] if "activity" in business['info'] else None,
                    'especialidad': business['info']['activity'] if "activity" in business['info'] else None,
                    'nombre': business['info']['name'].rstrip() if "name" in business['info'] else None, 
                    'texto_telefono': texto_telefono,
                    'telefono_1': telefono,
                    'correo': business['customerMail'] if "customerMail" in business else None,
                    'direccion': direccion.rstrip(), 
                    'ciudad': business['location']['locality'].rstrip() if 'location' in business and "locality" in business['location'] else None, 
                    'provincia' : business['location']['province'] if 'location' in business and "province" in business['location'] else None, 
                    'zipcode': str(codpostal),
                    'web': business['mapInfo']['adWebEstablecimiento'] if "adWebEstablecimiento" in business['mapInfo'] else None,
                    'fecha': now,
                    'seccion': tipo,
                    'pa_free': business['mapInfo']['isFreeAd'] if "isFreeAd" in business['mapInfo'] else None,
                    'lat': lat,
                    'long':long 
                }, ignore_index = True)
            #df = pd.json_normalize(business)
            if len(df) == 0:
                pagina_vacia(engine,'paginasAmarillas',pagina,tipo,now)
                continue
            try:
                df.to_sql (name = 'bbdd_directorios_temp', con = engine , if_exists = 'append', index = False)
                logging.info('\t\t\tCARGA PAGINA ' + str(pagina) + ' COMPLETA')
            except Exception as ex:
                logging.error('\t\t\tCARGA CARGA PAGINA ' + str(pagina) + ' ERROR: ' + str(ex))
                continue
            logging.info('\t\tFIN PAGINA "' + str(pagina) + '"')
        #filePath = Path(__file__).resolve().parent / 'files' / 'test'
        #nombre_archivo = 'PA_'+cat.split("/")[1]+'_'+str(i)+'_' + datetime.now().strftime("%Y%m%d_%H%M") + '.csv'
        #nombre_archivo = 'PA_'+cat.split("/")[1]+'_' + datetime.now().strftime("%Y%m%d_%H%M") + '.csv'
        #df.to_csv(filePath / nombre_archivo, index=False, sep=';', decimal=',')
    logging.info('--- FIN ---')


if __name__ == '__main__':
    json_path = Path(__file__).resolve().parent / 'library' / 'environment_variables.json'
    with open(str(json_path)) as json_file:
        envar = json.load(json_file)
    dir_base = Path(__file__).resolve().parent
    #driver_path = dir_base / 'assets' / 'chromedriver104.exe'
    driver_path = dir_base / 'assets' / 'gecko'
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    #options.add_argument('--headless')
    #driver = webdriver.Chrome(str(driver_path), chrome_options=options)
    #driver = webdriver.Firefox(str(driver_path))
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    main(envar, driver)



