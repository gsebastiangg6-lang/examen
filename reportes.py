from datetime import datetime

import herramientas as mod_herramientas
import usuarios as mod_usuarios
import prestamos as mod_prestamos


FORMATO_FECHA = "%Y-%m-%d"
STOCK_MINIMO = 3


def stock_bajo():
    resultado = []
    for herramienta in mod_herramientas.listar_herramientas():
        if herramienta["cantidad_disponible"] < STOCK_MINIMO:
            resultado.append(herramienta)
    return resultado


def prestamos_activos():
    resultado = []
    for prestamo in mod_prestamos.listar_prestamos():
        if prestamo["estado"] == "activo":
            resultado.append(prestamo)
    return resultado


def prestamos_vencidos():
    hoy = datetime.now()
    resultado = []
    for prestamo in mod_prestamos.listar_prestamos():
        if prestamo["estado"] == "activo":
            fecha_limite = datetime.strptime(
                prestamo["fecha_devolucion_estimada"], FORMATO_FECHA
            )
            if fecha_limite < hoy:
                resultado.append(prestamo)
    return resultado


def historial_usuario(id_usuario):
    resultado = []
    for prestamo in mod_prestamos.listar_prestamos():
        if prestamo["id_usuario"] == id_usuario:
            resultado.append(prestamo)
    return resultado


def herramientas_mas_solicitadas():
    contador = {}
    for prestamo in mod_prestamos.listar_prestamos():
        clave = prestamo["id_herramienta"]
        if clave in contador:
            contador[clave] += 1
        else:
            contador[clave] = 1

    lista = []
    for id_herramienta, veces in contador.items():
        herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
        nombre = herramienta["nombre"] if herramienta else "Desconocida"
        lista.append({"nombre": nombre, "veces": veces})

    lista.sort(key=lambda item: item["veces"], reverse=True)
    return lista


def usuarios_mas_solicitantes():
    contador = {}
    for prestamo in mod_prestamos.listar_prestamos():
        clave = prestamo["id_usuario"]
        if clave in contador:
            contador[clave] += 1
        else:
            contador[clave] = 1

    lista = []
    for id_usuario, veces in contador.items():
        usuario = mod_usuarios.buscar_usuario(id_usuario)
        nombre = (
            usuario["nombres"] + " " + usuario["apellidos"]
            if usuario
            else "Desconocido"
        )
        lista.append({"nombre": nombre, "veces": veces})

    lista.sort(key=lambda item: item["veces"], reverse=True)
    return lista
