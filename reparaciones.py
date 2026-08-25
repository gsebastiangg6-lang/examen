from reparaciones import registrar_reparacion, actualizar_estado_herramientas_finalizadas
import json
import os
from datetime import datetime

PATH_INVENTARIO = "inventario.json"
PATH_REPARACIONES = "reports/reparaciones.json" 

def cargar_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(path, datos):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def registrar_reparacion():
    inventario = cargar_json(PATH_INVENTARIO)

    id_herramienta = input("Ingrese el ID de la herramienta a reparar: ").strip()

    # 1. Validar que la herramienta exista
    herramienta = next((h for h in inventario if str(h.get("id")) == id_herramienta), None)
    if not herramienta:
            print(f"Error: La herramienta con ID '{id_herramienta}' no existe en el inventario.")
            return

    # 2. Manejar si la herramienta ya está en reparación
    if herramienta.get("estado") == "en reparación":
         print(f"Error: La herramienta '{herramienta['nombre']}' ya está en reparación.")
         return

    # 3. Solicitar datos de reparación
    fecha_inicio = input("Ingrese la fecha de inicio de la reparación (YYYY-MM-DD): ").strip()
    fecha_estimada = input("Ingrese la fecha estimada de finalización de la reparación (YYYY-MM-DD): ").strip() 
    observaciones = input("Ingrese observaciones sobre la reparación: ").strip()    

    # 4. Actualizar estado en el inventario
    herramienta["estado"] = "en reparación"
    guardar_json(PATH_INVENTARIO, inventario)

    # 5. Guardar registro en /reports/reparaciones.json
    registro = {
         "id_herramienta": herramienta["id"],
         "nombre" : herramienta["nombre"],
         "fecha_inicio": fecha_inicio,
         "fecha_estimada_finalizacion": fecha_estimada,
         "observaciones": observaciones
    }

    reparaciones = cargar_json(PATH_REPARACIONES)
    reparaciones.append(registro)
    guardar_json(PATH_REPARACIONES, reparaciones)   

    print("\n¡Herramienta registrada para reparación exitosamente!\n")
    mostrar_herramientas_en_reparacion()    

def mostrar_herramientas_en_reparacion():
    reparaciones = cargar_json(PATH_REPARACIONES)
    print("--- Herramientas en Reparación ---")
    if not reparaciones:
        print("No hay herramientas en reparación.")
        return  

    for item in reparaciones:
         print(f"- [{item['id_herramienta']}] {item['nombre']} | Inicio: {item['fecha_inicio']} | Estimada: {item['fecha_estimada_finalizacion']} | Observaciones: {item['observaciones']}")

def actualizar_estado_herramientas_reparadas():
     """Verificar si ya paso la fecha de finalizacion y cambiar el estado a 'Activa'"""
     inventario = cargar_json(PATH_INVENTARIO)
     reparaciones = cargar_json(PATH_REPARACIONES)
     hoy = datetime.now().strftime("%Y-%m-%d")

     Reparaciones_activas = []

     for reparacion in reparaciones:
          if reparacion["fecha_estimada_finalizacion"] <= hoy:
               # Reactivar herramienta en inventario
               for h in inventario:
                    if str(h["id"]) == str(reparacion["id_herramienta"]):
                         h["estado"] = "activa"
                         print(f"Herramienta '{h['nombre']}' reactivada en inventario.")
          else: 
                Reparaciones_activas.append(reparacion)

     guardar_json(PATH_INVENTARIO, inventario)
     guardar_json(PATH_REPARACIONES, Reparaciones_activas)

                        
          

