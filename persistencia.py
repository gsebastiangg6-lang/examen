import json 
import os 


CARPETA_DATOS = "datos"

def cargar(nombre_archivo):
    ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
    if not os.path.exists(ruta):
        return []
    try:
        with open(ruta, "r", encoding='utf-8') as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        print("El archivo está dañado. Se inicia con lista vacía.")
        return []
    except Exception as error:
        print("Error al leer el archivo:", error)
        return []

def guardar(nombre_archivo, datos):
    ruta = os.path.join(CARPETA_DATOS, nombre_archivo)
    with open(ruta, "w", encoding='utf-8') as archivo:
        json.dump(datos, archivo)

def siguiente_id(lista):
    if not lista:
        return 1
    return max(elemento["id"] for elemento in lista ) + 1 