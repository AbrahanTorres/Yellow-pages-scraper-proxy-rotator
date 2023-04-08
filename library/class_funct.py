ExcelFile_row = 1 

ExcelFile_headers = ['directorio','pagina','nombre','direccion','zipcode','ciudad',
    'provincia','especialidad','categoria','correo','texto_telefono','telefono_1',
    'telefono_2','telefono_3','horario','web','link']


class Linea:
    def __init__(self, directorio=None, pagina=None, nombre=None, direccion=None, zipcode=None, ciudad=None, provincia=None, especialidad=None, categoria=None, correo=None, texto_telefono=None, telefono_1=None, telefono_2=None, telefono_3=None,web=None,link=None):
        self.directorio = directorio
        self.pagina = pagina
        self.nombre = nombre
        self.direccion = direccion
        self.zipcode = zipcode
        self.ciudad = ciudad
        self.provincia = provincia
        self.especialidad = especialidad
        self.categoria = categoria
        self.correo = correo
        self.texto_telefono = texto_telefono
        self.telefono_1 = telefono_1
        self.telefono_2 = telefono_2
        self.telefono_3 = telefono_3
        self.web = web
        self.link = link


def Validacion_Telefono(telefono):
    import phonenumbers
    from phonenumbers import geocoder
    from phonenumbers import carrier
    texto_telefono = telefono
    telefono = telefono.replace('/',' ')
    telefono = telefono.replace('mob',' ').replace("mob",' ')
    telefono = telefono.replace('mov',' ').replace("mov",' ')
    telefono = telefono.replace('y',' ').replace("y",' ')
    telefono = telefono.replace('-',' ').replace('_',' ').replace('.',' ')
    n = 1
    telefono_1 = 'vacio'
    telefono_2 = 'vacio'
    telefono_3 = 'vacio'
    telefono_1_geo = 'vacio'
    telefono_2_geo = 'vacio'
    telefono_3_geo = 'vacio'
    telefono_1_carr = 'vacio'
    telefono_2_carr = 'vacio'
    telefono_3_carr = 'vacio'
    for match in phonenumbers.PhoneNumberMatcher(telefono, "ES"):
        x = phonenumbers.parse(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164), "ES")
        if telefono_1 == 'vacio' and n == 1:
            telefono_1 = str(x.national_number)
            telefono_1_geo = geocoder.description_for_number(x, "ES")
            telefono_1_carr = carrier.name_for_number(x, "ES")
        elif telefono_2 == 'vacio' and n == 2:
            telefono_2 = str(x.national_number)
            telefono_2_geo = geocoder.description_for_number(x, "ES")
            telefono_2_carr = carrier.name_for_number(x, "ES")
        elif telefono_3 == 'vacio' and n == 3:
            telefono_3 = str(x.national_number)
            telefono_3_geo = geocoder.description_for_number(x, "ES")
            telefono_1_carr = carrier.name_for_number(x, "ES")
        n += 1
    diccionario_numeros = {"texto_telefono": texto_telefono, 
        "telefono_1": telefono_1,
        "telefono_1_geo": telefono_1_geo,
        "telefono_1_carr": telefono_1_carr,
        "telefono_2": telefono_2,
        "telefono_2_geo": telefono_2_geo,
        "telefono_2_carr": telefono_2_carr,
        "telefono_3": telefono_3,
        "telefono_3_geo": telefono_3_geo,
        "telefono_3_carr": telefono_3_carr
    }
    return(diccionario_numeros)


def ExcelFile_Write(excel_workbook, linea, reset_row=False):
    global ExcelFile_row, ExcelFile_headers
    if reset_row == False:
        if ExcelFile_row == 1:
            try:
                for i in range(0,len(ExcelFile_headers)):
                    e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                    e.value=ExcelFile_headers[i]
                ExcelFile_row += 1
                for i in range(0,len(ExcelFile_headers)):
                    e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                    e.value=getattr(linea, ExcelFile_headers[i])
                ExcelFile_row += 1
            except Exception as e:
                print('**Error al escribir el registro ******* LINEA ext 091 *******')
                print(e)
        else:
            try:
                for i in range(0,len(ExcelFile_headers)):
                    e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                    e.value=getattr(linea, ExcelFile_headers[i])
                ExcelFile_row += 1
            except Exception as e:
                print('**Error al escribir el registro ******* LINEA ext 100 *******')
                print(e)
    elif reset_row == True and linea == False:
        ExcelFile_row = 1
        try:
            for i in range(0,len(ExcelFile_headers)):
                e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                e.value=ExcelFile_headers[i]
            ExcelFile_row += 1
        except Exception as e:
            print('**Error al escribir el registro ******* LINEA ext 110 *******')
            print(e)
    elif reset_row == True:
        ExcelFile_row = 1
        try:
            for i in range(0,len(ExcelFile_headers)):
                e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                e.value=ExcelFile_headers[i]
            ExcelFile_row += 1
            for i in range(0,len(ExcelFile_headers)):
                e=excel_workbook.cell(row=ExcelFile_row,column=1+i)
                e.value=getattr(linea, ExcelFile_headers[i])
            ExcelFile_row += 1
        except Exception as e:
            print('**Error al escribir el registro ******* LINEA ext 124 *******')
            print(e)


def ExcelFile_Nombre(path,origendatos,fechahora,pagina, opcional=None):
    if opcional:
        nombre = path+origendatos+'_'+opcional+'_'+fechahora+'_'+str(pagina)+'.xlsx'
    else:
        nombre = path+origendatos+'_'+fechahora+'_'+str(pagina)+'.xlsx'
    return(nombre)

def texto_valido(text):
    text = text.replace('á','a').replace('à','a').replace('À','A').replace('Á','A')
    text = text.replace('é','e').replace('è','e').replace('È','E').replace('É','E')
    text = text.replace('í','i').replace('í','a').replace('Ì','I').replace('Í','I')
    text = text.replace('ó','o').replace('ò','o').replace('Ò','O').replace('Ó','O')
    text = text.replace('ú','u').replace('ù','u').replace('Ù','U').replace('Ú','U')
    text = text.replace('/ ','').replace('- ',' ')
    return str(text)