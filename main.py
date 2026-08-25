import herramientas as mod_herramientas
import usuarios as mod_usuarios
import prestamos as mod_prestamos
import reportes as mod_reportes
import estilos as ui


def pedir_numero_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            ui.error("Debes ingresar un numero entero.")


def pedir_telefono(mensaje):
    while True:
        telefono = input(mensaje).strip()
        if telefono.isdigit() and len(telefono) == 10:
            return telefono
        ui.error("El telefono debe tener exactamente 10 digitos numericos.")


def pedir_texto_obligatorio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        ui.error("Este campo no puede quedar vacio.")


def pedir_numero_positivo(mensaje):
    while True:
        numero = pedir_numero_entero(mensaje)
        if numero > 0:
            return numero
        ui.error("El numero debe ser mayor que cero.")


def nombre_herramienta(id_herramienta):
    herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
    return herramienta["nombre"] if herramienta else "Desconocida"


def nombre_usuario(id_usuario):
    usuario = mod_usuarios.buscar_usuario(id_usuario)
    if usuario:
        return usuario["nombres"] + " " + usuario["apellidos"]
    return "Desconocido"


def prestamos_activos_de_herramienta(id_herramienta):
    return [p for p in mod_prestamos.listar_prestamos()
            if p["id_herramienta"] == id_herramienta and p["estado"] == "activo"]


def emoji_estado(estado):
    iconos = {
        "pendiente": "\u23f3",
        "activo": "\U0001f4e4",
        "devuelto": "\u2705",
        "rechazado": "\u274c",
        "activa": "\U0001f7e2",
        "en reparacion": "\U0001f527",
        "fuera de servicio": "\U0001f534",
    }
    return iconos.get(estado, "\u2022")


def mostrar_tabla_herramientas(solo_disponibles=False):
    herramientas = mod_herramientas.listar_herramientas()
    if solo_disponibles:
        herramientas = [h for h in herramientas
                        if h["estado"] == "activa" and h["cantidad_disponible"] > 0]
    if not herramientas:
        ui.aviso("No hay herramientas para mostrar.")
        return
    ui.linea()
    print("  ID   HERRAMIENTA          STOCK   ESTADO")
    ui.linea()
    for h in herramientas:
        print("  " + str(h["id"]).ljust(4) + " " + h["nombre"][:20].ljust(20) + " "
              + str(h["cantidad_disponible"]).center(5) + "   "
              + emoji_estado(h["estado"]) + " " + h["estado"])
    ui.linea()


def mostrar_tabla_vecinos():
    usuarios = mod_usuarios.listar_usuarios()
    if not usuarios:
        ui.aviso("No hay vecinos registrados.")
        return
    ui.linea()
    print("  ID   NOMBRE COMPLETO           TELEFONO")
    ui.linea()
    for u in usuarios:
        nombre = (u["nombres"] + " " + u["apellidos"])[:24]
        print("  " + str(u["id"]).ljust(4) + " " + nombre.ljust(25) + " " + u["telefono"])
    ui.linea()


def menu_administrador():
    ui.seccion("\U0001f6e0  MENU ADMINISTRADOR")
    print("  -- Herramientas --")
    ui.opcion(1, "\U0001f528", "Registrar Herramienta")
    ui.opcion(2, "\U0001f4cb", "Listar Herramientas")
    ui.opcion(3, "\U0001f50e", "Buscar Herramienta")
    ui.opcion(4, "\u270f\ufe0f", "Actualizar Herramienta")
    ui.opcion(5, "\U0001f6ab", "Inactivar Herramienta")
    print("  -- Vecinos --")
    ui.opcion(6, "\U0001f464", "Registrar Vecino")
    ui.opcion(7, "\U0001f465", "Listar Vecinos")
    ui.opcion(8, "\U0001f50e", "Buscar Vecino")
    ui.opcion(9, "\u270f\ufe0f", "Actualizar Vecino")
    ui.opcion(10, "\U0001f5d1\ufe0f", "Eliminar Vecino")
    print("  -- Prestamos y reportes --")
    ui.opcion(11, "\u2696\ufe0f", "Aprobar / Rechazar Solicitud")
    ui.opcion(12, "\U0001f504", "Registrar Devolucion")
    ui.opcion(13, "\U0001f4ca", "Ver Reportes")
    ui.opcion(14, "\U0001f4dc", "Historial de un Vecino")
    ui.opcion(15, "\U0001f519", "Volver")


def menu_usuario():
    ui.seccion("\U0001f3e0  MENU VECINO")
    ui.opcion(1, "\U0001f50e", "Consultar Herramientas")
    ui.opcion(2, "\U0001f4e5", "Solicitar Prestamo")
    ui.opcion(3, "\U0001f4dc", "Ver Mi Historial")
    ui.opcion(4, "\U0001f519", "Volver")


def opciones_administrador():
    while True:
        menu_administrador()
        opcion = input("\n  Selecciona una opcion: ").strip()

        # ---------- HERRAMIENTAS ----------
        if opcion == "1":
            ui.subtitulo("Registrar nueva herramienta")
            nombre = pedir_texto_obligatorio("  Nombre: ")
            categoria = pedir_texto_obligatorio("  Categoria: ")
            cantidad = pedir_numero_positivo("  Cantidad: ")
            valor = pedir_numero_positivo("  Valor estimado: ")
            nueva = mod_herramientas.crear_herramienta(nombre, categoria, cantidad, valor)
            ui.exito("Herramienta registrada con ID " + str(nueva["id"]) + " - " + nueva["nombre"])

        elif opcion == "2":
            ui.subtitulo("Catalogo de herramientas")
            mostrar_tabla_herramientas()

        elif opcion == "3":
            ui.subtitulo("Buscar herramienta")
            id_herramienta = pedir_numero_entero("  Id de la herramienta: ")
            herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
            if herramienta:
                ui.linea()
                print("  ID:", herramienta["id"])
                print("  Nombre:", herramienta["nombre"])
                print("  Categoria:", herramienta["categoria"])
                print("  Disponible:", herramienta["cantidad_disponible"])
                print("  Estado:", emoji_estado(herramienta["estado"]), herramienta["estado"])
                print("  Valor estimado:", herramienta["valor_estimado"])
                ui.linea()
            else:
                ui.error("No se encontro ninguna herramienta con ese id.")

        elif opcion == "4":
            ui.subtitulo("Actualizar herramienta")
            mostrar_tabla_herramientas()
            id_herramienta = pedir_numero_entero("\n  Id de la herramienta a actualizar: ")
            if mod_herramientas.buscar_herramienta(id_herramienta) is None:
                ui.error("Esa herramienta no existe. Revisa el id en la lista de arriba.")
            else:
                print("\n  Que dato deseas actualizar?")
                ui.opcion(1, "\U0001f524", "Nombre")
                ui.opcion(2, "\U0001f3f7\ufe0f", "Categoria")
                ui.opcion(3, "\U0001f4b2", "Valor estimado")
                ui.opcion(4, "\U0001f504", "Estado")
                campo_opcion = input("\n  Opcion: ").strip()
                campo = None
                nuevo_valor = None
                if campo_opcion == "1":
                    nuevo_valor = pedir_texto_obligatorio("  Nuevo nombre: ")
                    campo = "nombre"
                elif campo_opcion == "2":
                    nuevo_valor = pedir_texto_obligatorio("  Nueva categoria: ")
                    campo = "categoria"
                elif campo_opcion == "3":
                    nuevo_valor = pedir_numero_positivo("  Nuevo valor estimado: ")
                    campo = "valor_estimado"
                elif campo_opcion == "4":
                    print("  1. Activa")
                    print("  2. En reparacion")
                    print("  3. Fuera de servicio")
                    estado_opcion = input("  Opcion: ").strip()
                    estados = {"1": "activa", "2": "en reparacion", "3": "fuera de servicio"}
                    if estado_opcion in estados:
                        nuevo_valor = estados[estado_opcion]
                        campo = "estado"
                    else:
                        ui.error("Opcion invalida.")
                else:
                    ui.error("Opcion invalida.")

                if campo:
                    if mod_herramientas.actualizar_herramienta(id_herramienta, campo, nuevo_valor):
                        ui.exito("Herramienta actualizada correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")

        elif opcion == "5":
            ui.subtitulo("Inactivar herramienta")
            mostrar_tabla_herramientas()
            id_herramienta = pedir_numero_entero("\n  Id de la herramienta a inactivar: ")
            if mod_herramientas.inactivar_herramienta(id_herramienta):
                ui.exito("Herramienta marcada como 'fuera de servicio'.")
            else:
                ui.error("No se pudo inactivar. Verifica el id.")

        # ---------- VECINOS ----------
        elif opcion == "6":
            ui.subtitulo("Registrar nuevo vecino")
            nombres = pedir_texto_obligatorio("  Nombres: ")
            apellidos = pedir_texto_obligatorio("  Apellidos: ")
            telefono = pedir_telefono("  Telefono (10 digitos): ")
            direccion = pedir_texto_obligatorio("  Direccion: ")
            print("\n  Tipo de usuario:")
            ui.opcion(1, "\U0001f3e0", "Residente")
            ui.opcion(2, "\U0001f9d1\u200d\U0001f4bc", "Administrador")
            tipo_opcion = input("\n  Opcion: ").strip()
            tipo = "administrador" if tipo_opcion == "2" else "residente"
            nuevo = mod_usuarios.crear_usuario(nombres, apellidos, telefono, direccion, tipo)
            ui.exito("Vecino registrado con ID " + str(nuevo["id"]) + " - "
                     + nuevo["nombres"] + " " + nuevo["apellidos"] + " (" + tipo + ")")

        elif opcion == "7":
            ui.subtitulo("Directorio de vecinos")
            mostrar_tabla_vecinos()

        elif opcion == "8":
            ui.subtitulo("Buscar vecino")
            id_usuario = pedir_numero_entero("  Id del vecino: ")
            usuario = mod_usuarios.buscar_usuario(id_usuario)
            if usuario:
                ui.linea()
                print("  ID:", usuario["id"])
                print("  Nombre:", usuario["nombres"], usuario["apellidos"])
                print("  Telefono:", usuario["telefono"])
                print("  Direccion:", usuario["direccion"])
                print("  Tipo:", usuario["tipo_usuario"])
                ui.linea()
            else:
                ui.error("No se encontro ningun vecino con ese id.")

        elif opcion == "9":
            ui.subtitulo("Actualizar datos de un vecino")
            mostrar_tabla_vecinos()
            id_usuario = pedir_numero_entero("\n  Id del vecino a actualizar: ")
            if mod_usuarios.buscar_usuario(id_usuario) is None:
                ui.error("Ese vecino no existe. Revisa el id en la lista de arriba.")
            else:
                print("\n  Que dato deseas actualizar?")
                ui.opcion(1, "\U0001f4de", "Telefono")
                ui.opcion(2, "\U0001f3e0", "Direccion")
                ui.opcion(3, "\U0001f524", "Nombres")
                ui.opcion(4, "\U0001f524", "Apellidos")
                ui.opcion(5, "\U0001f4bc", "Tipo de usuario")
                campo_opcion = input("\n  Opcion: ").strip()
                if campo_opcion == "1":
                    nuevo_valor = pedir_telefono("  Nuevo telefono (10 digitos): ")
                    if mod_usuarios.actualizar_usuario(id_usuario, "telefono", nuevo_valor):
                        ui.exito("Telefono actualizado correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                elif campo_opcion == "2":
                    nuevo_valor = pedir_texto_obligatorio("  Nueva direccion: ")
                    if mod_usuarios.actualizar_usuario(id_usuario, "direccion", nuevo_valor):
                        ui.exito("Direccion actualizada correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                elif campo_opcion == "3":
                    nuevo_valor = pedir_texto_obligatorio("  Nuevos nombres: ")
                    if mod_usuarios.actualizar_usuario(id_usuario, "nombres", nuevo_valor):
                        ui.exito("Nombres actualizados correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                elif campo_opcion == "4":
                    nuevo_valor = pedir_texto_obligatorio("  Nuevos apellidos: ")
                    if mod_usuarios.actualizar_usuario(id_usuario, "apellidos", nuevo_valor):
                        ui.exito("Apellidos actualizados correctamente.")
                    else:
                        ui.error("No se pudo actualizar.")
                elif campo_opcion == "5":
                    print("  1. Residente")
                    print("  2. Administrador")
                    tipo_opcion = input("  Opcion: ").strip()
                    nuevo_tipo = "administrador" if tipo_opcion == "2" else "residente"
                    if mod_usuarios.actualizar_usuario(id_usuario, "tipo_usuario", nuevo_tipo):
                        ui.exito("Tipo de usuario actualizado a '" + nuevo_tipo + "'.")
                    else:
                        ui.error("No se pudo actualizar.")
                else:
                    ui.error("Opcion invalida.")

        elif opcion == "10":
            ui.subtitulo("Eliminar vecino")
            mostrar_tabla_vecinos()
            id_usuario = pedir_numero_entero("\n  Id del vecino a eliminar: ")
            if mod_usuarios.buscar_usuario(id_usuario) is None:
                ui.error("Ese vecino no existe. Revisa el id en la lista de arriba.")
            else:
                ui.aviso("Si este vecino tiene prestamos registrados, su nombre aparecera")
                ui.aviso("como 'Desconocido' en el historial despues de eliminarlo.")
                confirmar = input("  Seguro que deseas eliminarlo? (S/N): ").strip().upper()
                if confirmar == "S":
                    if mod_usuarios.eliminar_usuario(id_usuario):
                        ui.exito("Vecino eliminado correctamente.")
                    else:
                        ui.error("No se pudo eliminar.")
                else:
                    ui.info("Operacion cancelada.")

        # ---------- PRESTAMOS Y REPORTES ----------
        elif opcion == "11":
            ui.subtitulo("Solicitudes pendientes")
            pendientes = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "pendiente"]
            if not pendientes:
                ui.aviso("No hay solicitudes pendientes.")
            else:
                ui.linea()
                for p in pendientes:
                    print("  \u23f3 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                          + " solicita " + str(p["cantidad"]) + " x " + nombre_herramienta(p["id_herramienta"]))
                ui.linea()
                id_prestamo = pedir_numero_entero("\n  Id del prestamo a procesar: ")
                decision = input("  Aprobar o Rechazar? (A/R): ").strip().upper()
                if decision == "A":
                    if mod_prestamos.aprobar_prestamo(id_prestamo):
                        ui.exito("Prestamo aprobado. Stock actualizado.")
                    else:
                        ui.error("No se pudo aprobar (sin stock suficiente o id invalido). Revisa el log.")
                elif decision == "R":
                    motivo = input("  Motivo del rechazo (opcional): ").strip()
                    if mod_prestamos.rechazar_prestamo(id_prestamo, motivo):
                        ui.exito("Prestamo rechazado.")
                    else:
                        ui.error("No se pudo rechazar. Verifica el id.")
                else:
                    ui.error("Opcion invalida. No se realizo ningun cambio.")

        elif opcion == "12":
            ui.subtitulo("Registrar devolucion")
            activos = [p for p in mod_prestamos.listar_prestamos() if p["estado"] == "activo"]
            if not activos:
                ui.aviso("No hay prestamos activos.")
            else:
                ui.linea()
                for p in activos:
                    print("  \U0001f4e4 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                          + " tiene " + str(p["cantidad"]) + " x " + nombre_herramienta(p["id_herramienta"]))
                ui.linea()
                id_prestamo = pedir_numero_entero("\n  Id del prestamo devuelto: ")
                if mod_prestamos.devolver_prestamo(id_prestamo):
                    ui.exito("Devolucion registrada. Stock restaurado.")
                else:
                    ui.error("No se pudo registrar la devolucion. Verifica el id.")

        elif opcion == "13":
            ui.subtitulo("\U0001f4c9 Herramientas con stock bajo")
            bajos = mod_reportes.stock_bajo()
            if not bajos:
                ui.info("Ninguna herramienta esta por debajo del minimo.")
            for h in bajos:
                ui.item("\u26a0\ufe0f  " + h["nombre"] + " - " + str(h["cantidad_disponible"]) + " unidad(es)")

            ui.subtitulo("\U0001f4e4 Prestamos activos")
            activos = mod_reportes.prestamos_activos()
            if not activos:
                ui.info("No hay prestamos activos.")
            for p in activos:
                ui.item("Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                        + " - " + nombre_herramienta(p["id_herramienta"])
                        + " - vence el " + p["fecha_devolucion_estimada"])

            ui.subtitulo("\u23f0 Prestamos vencidos")
            vencidos = mod_reportes.prestamos_vencidos()
            if not vencidos:
                ui.info("No hay prestamos vencidos.")
            for p in vencidos:
                ui.item("\U0001f6a8 Prestamo " + str(p["id"]) + " - " + nombre_usuario(p["id_usuario"])
                        + " - " + nombre_herramienta(p["id_herramienta"])
                        + " - vencio el " + p["fecha_devolucion_estimada"])

            ui.subtitulo("\U0001f3c6 Herramientas mas solicitadas")
            top_h = mod_reportes.herramientas_mas_solicitadas()
            if not top_h:
                ui.info("Aun no hay solicitudes registradas.")
            for item in top_h:
                ui.item(item["nombre"] + " - " + str(item["veces"]) + " vez(ces)")

            ui.subtitulo("\U0001f465 Vecinos que mas solicitan")
            top_u = mod_reportes.usuarios_mas_solicitantes()
            if not top_u:
                ui.info("Aun no hay solicitudes registradas.")
            for item in top_u:
                ui.item(item["nombre"] + " - " + str(item["veces"]) + " vez(ces)")

        elif opcion == "14":
            ui.subtitulo("Historial de prestamos de un vecino")
            mostrar_tabla_vecinos()
            id_usuario = pedir_numero_entero("\n  Id del vecino: ")
            if mod_usuarios.buscar_usuario(id_usuario) is None:
                ui.error("Ese vecino no existe. Revisa el id en la lista de arriba.")
            else:
                historial = mod_reportes.historial_usuario(id_usuario)
                if not historial:
                    ui.aviso("Ese vecino no tiene prestamos registrados.")
                else:
                    ui.linea()
                    for p in historial:
                        print("  " + emoji_estado(p["estado"]) + " Prestamo " + str(p["id"]) + " - "
                              + nombre_herramienta(p["id_herramienta"]) + " - "
                              + str(p["cantidad"]) + " unidad(es) - " + p["estado"])
                    ui.linea()

        elif opcion == "15":
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")


def opciones_usuario():
    ui.subtitulo("Identificate")
    mostrar_tabla_vecinos()
    id_usuario = pedir_numero_entero("\n  Ingresa tu id de vecino: ")
    if mod_usuarios.buscar_usuario(id_usuario) is None:
        ui.error("Ese vecino no existe. Pide al administrador que te registre.")
        return
    ui.exito("Hola, " + nombre_usuario(id_usuario) + " \U0001f44b")

    while True:
        menu_usuario()
        opcion = input("\n  Selecciona una opcion: ").strip()

        if opcion == "1":
            ui.subtitulo("Estado de las herramientas")
            herramientas = mod_herramientas.listar_herramientas()
            if not herramientas:
                ui.aviso("No hay herramientas registradas.")
            else:
                for h in herramientas:
                    print("\n  " + emoji_estado(h["estado"]) + " " + h["nombre"]
                          + " (" + h["categoria"] + ") - " + str(h["cantidad_disponible"])
                          + " disponible(s) - " + h["estado"])
                    if h["cantidad_disponible"] <= 0 or h["estado"] != "activa":
                        activos = prestamos_activos_de_herramienta(h["id"])
                        if activos:
                            for p in activos:
                                print("     -> En manos de " + nombre_usuario(p["id_usuario"])
                                      + ", disponible aprox. el " + p["fecha_devolucion_estimada"])
                        elif h["estado"] != "activa":
                            print("     -> No disponible (" + h["estado"] + ")")
                print()

        elif opcion == "2":
            ui.subtitulo("Solicitar un prestamo")
            mostrar_tabla_herramientas(solo_disponibles=True)
            id_herramienta = pedir_numero_entero("\n  Id de la herramienta: ")

            herramienta = mod_herramientas.buscar_herramienta(id_herramienta)
            if herramienta is None:
                ui.error("Esa herramienta no existe. Revisa el id en la lista de arriba.")
            elif herramienta["estado"] != "activa":
                ui.error("Esa herramienta no esta disponible (estado: "
                         + herramienta["estado"] + ").")
            else:
                cantidad = pedir_numero_positivo("  Cantidad: ")
                observaciones = input("  Observaciones: ").strip()

                if cantidad > herramienta["cantidad_disponible"]:
                    ui.aviso("Pediste " + str(cantidad) + " unidades, pero ahora mismo solo hay "
                             + str(herramienta["cantidad_disponible"]) + " disponibles.")
                    ui.aviso("La solicitud se enviara igual, pero es probable que sea rechazada.")

                solicitud = mod_prestamos.solicitar_prestamo(
                    id_usuario, id_herramienta, cantidad, observaciones)
                if solicitud:
                    ui.exito("Solicitud creada con ID " + str(solicitud["id"]) + " - "
                             + nombre_usuario(id_usuario) + " solicita " + str(cantidad)
                             + " x " + nombre_herramienta(id_herramienta))
                    ui.info("Espera la aprobacion del administrador.")
                else:
                    ui.error("No se pudo crear la solicitud.")

        elif opcion == "3":
            ui.subtitulo("Mi historial de prestamos")
            mios = mod_reportes.historial_usuario(id_usuario)
            if not mios:
                ui.aviso("Todavia no tienes prestamos registrados.")
            else:
                ui.linea()
                for p in mios:
                    print("  " + emoji_estado(p["estado"]) + " Prestamo " + str(p["id"]) + " - "
                          + nombre_herramienta(p["id_herramienta"]) + " - "
                          + str(p["cantidad"]) + " unidad(es) - " + p["estado"])
                ui.linea()

        elif opcion == "4":
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")


def main():
    ui.titulo("\U0001f527 SISTEMA DE PRESTAMO DE HERRAMIENTAS \U0001f528")
    ui.info("Junta comunal - prestamos entre vecinos")

    while True:
        ui.seccion("MENU PRINCIPAL")
        ui.opcion(1, "\U0001f9d1\u200d\U0001f4bc", "Entrar como Administrador")
        ui.opcion(2, "\U0001f3e0", "Entrar como Vecino")
        ui.opcion(3, "\U0001f6aa", "Salir")
        rol = input("\n  Selecciona una opcion: ").strip()

        if rol == "1":
            opciones_administrador()
        elif rol == "2":
            opciones_usuario()
        elif rol == "3":
            ui.despedida("\U0001f44b Hasta luego!")
            break
        else:
            ui.error("Opcion invalida. Intenta de nuevo.")

from reparaciones import (
    registrar_reparacion,
    mostrar_herramientas_en_reparacion,
    actualizar_estado_herramientas_finalizadas
)

def menu_principal():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Registrar reparación")
        print("2. Mostrar herramientas en reparación")
        print("3. Actualizar estado de herramientas finalizadas")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_reparacion()
        elif opcion == "2":
            mostrar_herramientas_en_reparacion()
        elif opcion == "3":
            actualizar_estado_herramientas_finalizadas()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()