import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier

def telefono_validacion(telefono):
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